import streamlit as st
from groq import Groq
import json

# 1. Setup the Page (The Basketball Emoji & Welcome)
st.set_page_config(page_title="U12 Grading Assistant", page_icon="🏀")
st.title("🏀 U12 Grading Bot")
st.info("I know the grading rules and team placements for the U12 Pre-Season.")

# 2. Load the "Brain" (The JSON data)
@st.cache_data
def load_data():
    try:
        with open('tournament_brain.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# This line was missing or misplaced, causing your NameError:
tournament_data = load_data()

# 3. Setup AI (Groq)
if "GROQ_API_KEY" in st.secrets:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
else:
    st.error("Missing GROQ_API_KEY in Streamlit Secrets.")
    st.stop()

# 4. Chat Interface
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# React to user input
if prompt := st.chat_input("Ask about a team..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # The Logic Brain for the AI
    # This must be indented exactly 4 spaces from the left margin
    context = f"""
    You are an expert on the U12 Basketball Grading Competition.
    DATA: {json.dumps(tournament_data)}
    
    STRICT RULES:
    1. Only use the teams listed in the DATA 'teams' section.
    2. To find opponents, look at the 'pools' section. 
    3. IMPORTANT: You DO NOT have the schedule (times/dates). If asked for a schedule, say: "I don't have the specific court times yet. Please check the BasketballConnect app or the HQ Desk."
    4. IMPORTANT: You DO NOT have live scores. Do not invent wins or losses.
    5. Always mention the team's Seed and their Group (1 or 2).
    
    GRADING RULES (STRICT):
    - Teams in GROUP 1 (Seeds 1-12):
        * Rank 1-4 = PREMIER LEAGUE (PL).
        * Rank 5-6 = Phase 2, Group 1.
    
    - Teams in GROUP 2 (Seeds 13-29):
        * Rank 1 = Phase 2, Group 1.
        * Rank 2-3 = Phase 2, Group 2.
        * Others = Phase 2, Group 3 (or as directed by HQ).

    PERSONALITY:
    - If you know the user's team, apply the rule DIRECTLY to them.
    - Example: "Since Logan Thunder is in Group 1, finishing 1st means you qualify for the Premier League!"

    # Generate response using Groq
    # This 'try' must also be indented 4 spaces
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": context},
                {"role": "user", "content": prompt}
            ],
            model="llama-3.1-8b-instant",
        )
        
        response_text = chat_completion.choices[0].message.content
        
        with st.chat_message("assistant"):
            st.markdown(response_text)
        st.session_state.messages.append({"role": "assistant", "content": response_text})
        
    except Exception as e:
        st.error(f"AI Error: {e}")
