import streamlit as st
import google.generativeai as genai
import json

# 1. Setup Page
st.set_page_config(page_title="U12 Grading Assistant", page_icon="🏀")
st.title("🏀 U12 Grading Bot")
st.info("I know the grading rules and team placements for the U12 Pre-Season.")

# 2. Load the JSON Brain
@st.cache_data
def load_data():
    try:
        with open('tournament_brain.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

tournament_data = load_data()

# 3. Setup AI (Gemini)
if "GEMINI_API_KEY" in st.secrets:
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        # This is the most stable naming convention for the new SDK
        model = genai.GenerativeModel(model_name='gemini-1.5-flash')
    except Exception as e:
        st.error(f"Connection Error: {e}")
        st.stop()
else:
    st.error("API Key missing. Please add GEMINI_API_KEY to Streamlit Secrets.")
    st.stop()

# 4. Chat logic
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Ask about a team..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # The "Secret Sauce" - System Instructions
    context = f"""
    You are an expert on the U12 Basketball Grading Competition.
    DATA: {json.dumps(tournament_data)}
    
    GRADING RULES:
    - GIRLS Group 1 (Seeds 1-12): Top 4 in each pool go to Premier League (PL). 5th/6th go to Phase 2 Group 1.
    - GIRLS Group 2 (Seeds 13-29): 1st in each pool moves to Phase 2 Group 1. 2nd/3rd move to Phase 2 Group 2.
    - BOYS Group 1 (Seeds 1-12): Top 4 in each pool go to PL. 5th/6th go to Phase 2 Group 1.
    
    INSTRUCTIONS:
    - If a parent asks 'What happens if we finish 2nd?', use the rules above to explain their path.
    - Always confirm the team name and their current Pool.
    - Be encouraging and concise. If you don't have a specific game result, tell them to check the HQ desk.
    """

    response = model.generate_content([context, prompt])
    
    with st.chat_message("assistant"):
        st.markdown(response.text)
    st.session_state.messages.append({"role": "assistant", "content": response.text})
