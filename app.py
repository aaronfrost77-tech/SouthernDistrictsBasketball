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

    # --- START BULLETPROOF PRE-FILTER LOGIC ---
    user_query = prompt.lower()
    found_team_data = None
    teams_dict = tournament_data.get("teams", {})
    
    sorted_team_keys = sorted(teams_dict.keys(), key=len, reverse=True)

    matched_key = None
    for team_key in sorted_team_keys:
        clean_name_key = team_key.split(" (")[0].lower()
        
        if clean_name_key in user_query:
            user_wants_boys = "boy" in user_query
            user_wants_girls = "girl" in user_query
            is_boys_key = "(boys)" in team_key.lower()
            is_girls_key = "(girls)" in team_key.lower()
            
            if (user_wants_boys and is_boys_key) or (user_wants_girls and is_girls_key) or (not user_wants_boys and not user_wants_girls):
                matched_key = team_key
                found_team_data = teams_dict[team_key]
                break

    if not matched_key:
        for team_key in sorted_team_keys:
            name_parts = team_key.split(" (")[0].lower().split(" ")
            if any(part in user_query for part in name_parts if len(part) > 4):
                matched_key = team_key
                found_team_data = teams_dict[team_key]
                break

    if matched_key and found_team_data:
        context = f"""
        You are the U12 SQJBC Assistant. Use 'You'.
        The user is confirmed to be with: {matched_key}
        STRICT DATA: {json.dumps(found_team_data, indent=2)}
        INSTRUCTIONS:
        1. Use ONLY the STRICT DATA above.
        2. State the team's Seed, Group, and Pathway clearly.
        3. If schedule info is missing, say it is being updated.
        4. NEVER talk about QBL or general basketball knowledge.
        """
    else:
        context = "I couldn't find that team in the list. Ask the user for their team name and gender."
    # --- END BULLETPROOF PRE-FILTER LOGIC ---

    try:
        messages_to_send = [{"role": "system", "content": context}]
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
