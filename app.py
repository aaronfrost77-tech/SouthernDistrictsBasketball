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
    2. NICKNAME RESOLUTION: Use the 'nickname_map' in the DATA. 
    3. POOL LISTING: Only show teams that share the SAME 'gender', 'group', and 'pool' letter.

    PATHWAY RULES:
    - Group 1 (Seeds 1-12): Rank 1-4 = PREMIER LEAGUE. Rank 5-6 = Phase 2, Group 1.
    - Group 2: Rank 1 = Phase 2 Group 1; Rank 2-3 = Phase 2 Group 2.
    """

    try:
        # This is the line that likely glitched in your copy-paste
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
