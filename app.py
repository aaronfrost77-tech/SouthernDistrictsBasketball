import streamlit as st
from groq import Groq
import json

# 1. Setup the Page
st.set_page_config(page_title="U12 Grading Assistant", page_icon="🏀")
st.title("🏀 U12 Grading Bot")
st.info("I know the grading rules and team placements for the U12 Pre-Season.")

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

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# React to user input
if prompt := st.chat_input("Ask about a team..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # THE REFINED LOGIC BRAIN
    context = f"""
    You are the U12 Grading Assistant. 
    DATA: {json.dumps(tournament_data)}
    
    STRICT OPERATING RULES:
    1. CURRENT TEAM: The user is talking about the team mentioned in the message IMMEDIATELY above. Do not mention other teams (like Wizards) unless specifically asked.
    2. DATA ONLY:
       - GROUP 1 (Seeds 1-12): Rank 1-4 = PREMIER LEAGUE. Rank 5-6 = Phase 2, Group 1.
       - GROUP 2 (Seeds 13-29): Rank 1 = Phase 2, Group 1. Rank 2-3 = Phase 2, Group 2.
    3. NO HALLUCINATIONS: Do not guess potential or mention teams not in the user's current question.
    4. NO SCHEDULES: Direct users to HQ for court times.

    RESPONSE STYLE:
    - Keep it short. 
    - "Since [TEAM] is in Group [X], finishing [RANK] means [OUTCOME]."
    """

    try:
        # Build payload with history
        messages_to_send = [{"role": "system", "content": context}]
        
        # Include last 6 messages to ensure strong context
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
    
