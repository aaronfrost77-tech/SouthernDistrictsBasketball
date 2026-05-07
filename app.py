import streamlit as st
from groq import Groq
import json

# 1. Page Configuration
st.set_page_config(page_title="U12 SQJBC Assistant", page_icon="🏀")
st.title("🏀 U12 Grading Bot")

# 2. Simplified Load (The "If it ain't broke, don't fix it" version)
@st.cache_data
def load_data():
    try:
        with open('tournament_brain.json', 'r') as f:
            return json.load(f)
    except Exception as e:
        st.error(f"File loading error: {e}")
        return {}

full_database = load_data()

# 3. Groq AI Setup
if "GROQ_API_KEY" in st.secrets:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
else:
    st.error("Missing GROQ_API_KEY in Streamlit Secrets.")
    st.stop()

# 4. Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 5. Interaction Logic
if prompt := st.chat_input("Ask about your team..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Logic: Search the entire JSON for any mention of the team name
    user_query = prompt.lower()
    found_context = "No specific data found."
    
    # We look through the whole JSON object for a match
    # This is more robust than looking for a specific 'teams' key
    for key, value in full_database.items():
        # If the JSON is a flat list of teams
        if isinstance(value, dict) and any(word in key.lower() for word in user_query.split() if len(word) > 4):
            found_context = f"Team: {key}\nData: {json.dumps(value)}"
            break
        # If the JSON has a 'teams' wrapper
        if key == "teams":
            for t_name, t_data in value.items():
                if t_name.lower().split(" (")[0] in user_query:
                    found_context = f"Team: {t_name}\nData: {json.dumps(t_data)}"
                    break

    context = f"""
    You are the U12 SQJBC Assistant.
    CONTEXT DATA: {found_context}
    INSTRUCTIONS: Use the CONTEXT DATA to answer. If it's missing, ask for team name and gender.
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
