import streamlit as st
from groq import Groq
import json

# 1. Setup the Page
st.set_page_config(page_title="U12 Grading Assistant 2025/26", page_icon="🏀")
st.title("🏀 U12 Grading Bot")
st.info("Updated for the 2025-26 Phase 1 Grading (May/June 2026).")

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

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Ask about your team..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # THE HARDENED LOGIC BRAIN
    context = f"""
    You are the Official U12 SQJBC Grading Assistant. Use SECOND PERSON ("You").
    DATA: {json.dumps(tournament_data)}
    
    STRICT IDENTITY RULES:
    1. EXACT MATCHING: "Logan Thunder" is NOT the same as "Logan Thunder Gold" or "Logan Thunder Blue". 
    2. GENDER CHECK: Always check if the user is asking about Boys or Girls.
    3. CLARIFICATION: If a user says "Logan Thunder" and there are multiple variations, say: "Are you asking about the Championship team (Group 1), Logan Thunder Gold, or Logan Thunder Blue?"

    PATHWAY LOGIC (2025-26 Phase 1):
    - GROUP 1 (Seeds 1-12): Rank 1-4 = PREMIER LEAGUE. Rank 5-6 = Phase 2, Group 1.
    - GROUP 2 (Seeds 13-26): Rank 1 = Phase 2 Group 1. Rank 2-3 = Phase 2 Group 2. Rank 4+ = Phase 2 Group 3.
    - GROUP 3 (Seeds 27-42): Refer to Phase 2 transition rules in metadata.

    OPERATING RULES:
    1. For schedules, provide: Date, Time, Opponent, and Venue.
    2. Use the "nickname_map" in the DATA to resolve shorthand names (e.g., Spartans White).
    3. MEMORY: Use the last 4 messages to keep track of which team "you" refers to.
    """

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
