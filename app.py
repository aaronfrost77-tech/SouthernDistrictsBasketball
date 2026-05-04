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
    context = f"""
    You are an expert on the U12 Basketball Grading Competition.
    DATA: {json.dumps(tournament_data)}
    
    GRADING RULES:
    - GIRLS Group 1 (Seeds 1-12): Top 4 in each pool go to Premier League (PL). 5th/6th go to Phase 2 Group 1.
    - GIRLS Group 2 (Seeds 13-29): 1st in each pool moves to Phase 2 Group 1. 2nd/3rd move to Phase 2 Group 2.
    - BOYS Group 1 (Seeds 1-12): Top 4 in each pool go to PL. 5th/6th go to Phase 2 Group 1.
    
    INSTRUCTIONS:
    - Be friendly to parents.
    - If you don't know a specific score, tell them to check the HQ desk.
    - Always confirm the team's pool and seed from the data.
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
