import streamlit as st
from groq import Groq
import json

# 1. Setup the Page
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

# Display chat history on the screen
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# React to user input
if prompt := st.chat_input("Ask about a team..."):
    # Add user message to session state
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # The Logic Brain for the AI
    context = f"""
    You are the Official U12 Grading Assistant. 
    DATA: {json.dumps(tournament_data)}
    
    STRICT OPERATING RULES:
    1. CONTEXT: You must look at the conversation history provided. If the user says "we", "us", or "our team", they are referring to the team mentioned in the most recent messages.
    2. DATA ONLY: Use these exact rules for outcomes:
       - GROUP 1 (Seeds 1-12): Rank 1, 2, 3, or 4 = Qualify for PREMIER LEAGUE (PL). Rank 5 or 6 = Move to Phase 2, Group 1.
       - GROUP 2 (Seeds 13-29): Rank 1 = Move to Phase 2, Group 1. Rank 2 or 3 = Move to Phase 2, Group 2.
    3. NO HALLUCINATIONS: Do not invent scores, potential, or rankings. 
    4. NO SCHEDULES: If asked for times, tell them to check the BasketballConnect app or the HQ desk.
    5. TEAMS: "Southern Districts Trojans Black / Spartans White" is ONE single team.

    RESPONSE STYLE:
    - Be helpful and direct. 
    - Apply the rule specifically to the team being discussed.
    """

    # Generate response using Groq with HISTORY
    try:
        # Build the message payload with History
        messages_to_send = [{"role": "system", "content": context}]
        
        # Include the last 4 messages for memory (2 exchanges)
        for msg in st.session_state.messages[-4:]:
            messages_to_send.append(msg)
            
        chat_completion = client.chat.completions.create(
            messages=messages_to_send,
            model="llama-3.1-8b-instant",
        )
        
        response_text = chat_completion.choices[0].message.content
        
        # Add assistant response to session state and display
        with st.chat_message("assistant"):
            st.markdown(response_text)
        st.session_state.messages.append({"role": "assistant", "content": response_text})
        
    except Exception as e:
        st.error(f"AI Error: {e}")
    
