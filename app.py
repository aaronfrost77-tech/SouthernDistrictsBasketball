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
    context = f"""
    You are the Official U12 Grading Assistant. 
    DATA: {json.dumps(tournament_data)}
    
    STRICT OPERATING RULES:
    1. MEMORY: Always check previous messages. If the user says "we" or "our team", they are referring to the team previously discussed.
    2. DATA ONLY: Do not say "rules aren't clear." Use these exact rules:
       - GROUP 1 (Seeds 1-12): Rank 1, 2, 3, or 4 = Qualify for PREMIER LEAGUE (PL). Rank 5 or 6 = Move to Phase 2, Group 1.
       - GROUP 2 (Seeds 13-29): Rank 1 = Move to Phase 2, Group 1. Rank 2 or 3 = Move to Phase 2, Group 2.
    3. NO HALLUCINATIONS: Do not invent "potential," "standings," or "win/loss" records. 
    4. NO SCHEDULES: If asked for game times, tell them to check the BasketballConnect app or the HQ desk.
    5. TEAMS: "Southern Districts Trojans Black / Spartans White" is ONE single team.

    RESPONSE STYLE:
    - Be helpful but very direct. 
    - If you know the team, apply the rule to them specifically.
    - Example: "Logan Thunder is Seed 6 (Group 1). If you finish 1st, you qualify for the Premier League."
    """

    # Generate response using Groq
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
    
