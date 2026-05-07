import streamlit as st
from groq import Groq
import json

# 1. Page Configuration
st.set_page_config(page_title="U12 SQJBC Assistant", page_icon="🏀")
st.title("🏀 U12 Grading Bot")
st.info("2025-26 Phase 1 Grading Assistant")

# 2. Load the JSON Brain
@st.cache_data
def load_data():
    try:
        with open('tournament_brain.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

tournament_data = load_data()

# 3. Groq AI Setup
if "GROQ_API_KEY" in st.secrets:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
else:
    st.error("Missing GROQ_API_KEY in Streamlit Secrets.")
    st.stop()

# 4. Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 5. The Logic & AI Interaction
if prompt := st.chat_input("Ask about your team..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # --- START PRE-FILTER LOGIC ---
    # We find the team in Python so the AI doesn't have to guess
    user_query = prompt.lower()
    found_team_data = None
    teams_dict = tournament_data.get("teams", {})

    # We sort keys by length (longest first) so "Logan Thunder Gold" 
    # is found before "Logan Thunder"
    sorted_teams = sorted(teams_dict.keys(), key=len, reverse=True)

    for team_key in sorted_teams:
        # Check if the team name (minus the gender bracket) is in the prompt
        clean_name = team_key.split(" (")[0].lower()
        if clean_name in user_query:
            found_team_data = {team_key: teams_dict[team_key]}
            break

    # Construct the System Message
    if found_team_data:
        context = f"""
        You are the U12 SQJBC Assistant. Use 'You'.
        STRICT DATA FOR THIS USER: {json.dumps(found_team_data)}
        
        INSTRUCTIONS:
        1. Only answer using the STRICT DATA above.
        2. If the user asks for a schedule and it is in the DATA, list Date, Time, Venue, and Opponent.
        3. If the user asks for a pathway, explain their specific 'pathway' from the DATA.
        4. NEVER mention other teams or invent "alternate" status.
        """
    else:
        context = "The user hasn't specified a valid team name yet. Ask them which team and gender they are with."
    # --- END PRE-FILTER LOGIC ---

    try:
        messages_to_send = [{"role": "system", "content": context}]
        # Include a bit of history for context
        for msg in st.session_state.messages[-4:]:
            messages_to_send.append(msg)
            
        chat_completion = client.chat.completions.create(
            messages=messages_to_send,
            model="llama-3.1-8b-instant",
        )
        
        response_text = chat_completion.choices[0].message.content
        with st.chat_message("assistant"):
            st.markdown(response_text)
        st.session_state.messages.append({"role": "assistant", "content": response_text})
        
    except Exception as e:
        st.error(f"AI Error: {e}")
