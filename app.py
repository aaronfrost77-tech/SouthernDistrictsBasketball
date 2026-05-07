import streamlit as st
from groq import Groq
import json

# 1. Setup the Page
st.set_page_config(page_title="U12 SQJBC Assistant", page_icon="🏀")
st.title("🏀 U12 Grading Bot")
st.info("Updated for 2025-26 Phase 1 Grading. Use second person ('You') in responses.")

# 2. Load the "Brain"
@st.cache_data
def load_data():
    try:
        with open('tournament_brain.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

tournament_data = load_data()

# 3. Setup AI (Groq)
if "GROQ_API_KEY" in st.secrets:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
else:
    st.error("Missing GROQ_API_KEY in Streamlit Secrets.")
    st.stop()

# 4. Chat Interface Memory Setup
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display conversation
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# React to user input
if prompt := st.chat_input("Ask about your team..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # THE HARDENED GENDER-FIRST LOGIC BRAIN
    context = f"""
    You are the Official U12 SQJBC Grading Assistant. Be friendly and direct.
    DATA: {json.dumps(tournament_data)}
    
    CRITICAL IDENTITY RULES:
    1. GENDER LOCK: You MUST first determine if the user is asking about 'Boys' or 'Girls'. 
       - If they say "Spartans White", check both "SD Spartans White (Boys)" and "Southern Districts Spartans White (Girls)".
       - If unclear, ask: "Are you asking about the Boys or Girls team?"
    2. NICKNAME RESOLUTION: Use the 'nickname_map' in the DATA. 
       - "Spartans" (no color) is always Seed 1 for Boys or Seed 3 for Girls.
       - "Spartans Black" is Seed 12 for Boys or Seed 9 for Girls.
       - "Spartans White" is Seed 23 for Boys or Seed 10 for Girls.
    3. POOL LISTING: To list a pool, only show teams that share the SAME 'gender', 'group', and 'pool' letter as the target team.

    PATHWAY RULES:
    - Group 1 (Seeds 1-12): Rank 1-4 = PREMIER LEAGUE. Rank 5-6 = Phase 2, Group 1.
    - Group 2 (Seeds 13-26 Boys / 13-29 Girls): Rank 1 = Phase 2 Group 1; Rank 2-3 = Phase 2 Group 2.
    - Group 3 (Boys Seeds 27-42): Refer to Phase 2 transition rules.

    OPERATING RULES:
    - Provide specific Date, Time, Opponent, and Venue for schedules.
    - Use "You" and "Your team".
    - If a user says "we", refer to the team identified in the previous message.
    """

    try:
        # Build payload with restricted memory (last 4 messages) for speed and focus
        messages_to_
