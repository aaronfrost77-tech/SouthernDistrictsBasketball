import streamlit as st
from groq import Groq
import json

# 1. Setup the Page
st.set_page_config(page_title="U12 Grading Assistant", page_icon="🏀")
st.title("🏀 U12 Grading Bot")
st.info("I'm here to help you navigate the U12 Grading pools and pathways!")

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

    # THE REFINED LOGIC BRAIN
    context = f"""
    You are the Official U12 Grading Assistant. Be direct and use second person ("You").
    DATA: {json.dumps(tournament_data)}
    
    GRADING RULES (STRICT):
    - IF a team is in GROUP 1 (Seeds 1-12):
        * Rank 1, 2, 3, or 4 = YOU QUALIFY FOR PREMIER LEAGUE (PL).
        * Rank 5 or 6 = You move to Phase 2, Group 1.
    - IF a team is in GROUP 2 (Seeds 13-29):
        * Rank 1 = You move to Phase 2, Group 1.
        * Rank 2 or 3 = You move to Phase 2, Group 2.
        * Rank 4+ = You move to Phase 2, Group 3.

    OPERATING RULES:
    1. OPPONENTS: Look at the "opponents" list for the team in the DATA. List them clearly.
    2. TEAM LOOKUP (Nicknames): 
       - "Spartans White" or "Trojans Black" = "Southern Districts Trojans Black / Spartans White"
       - "Spartans Black" or "Titans" = "Southern Districts Titans / Spartans Black"
       - "Spartans" = "Southern Districts Spartans"
    3. NO HALLUCINATIONS: Do not guess schedules or current wins/losses.
    4. NO SCHEDULES: Always direct users to the HQ desk for court times.
    5. MEMORY: Look at the previous message history. If the user says "we", "us", or "our team", they are talking about the team discussed in the message immediately prior.

    RESPONSE STYLE:
    - Keep it short and factual.
    - Example: "Your team (Logan Thunder) is Seed 6 in Group 1. If you finish 3rd in your pool, you qualify for the Premier League!"
    """

    try:
        # Build payload with history for memory
        messages_to_send = [{"role": "system", "content": context}]
        
        # Include last 6 messages to keep the team context alive
        for msg in st.session_state.messages[-6:]:
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
