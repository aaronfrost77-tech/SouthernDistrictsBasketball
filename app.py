import streamlit as st
from groq import Groq
import json

# ... (keep your existing page setup and data loading)

# 3. Setup AI (Groq)
if "GROQ_API_KEY" in st.secrets:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
else:
    st.error("Missing GROQ_API_KEY in Secrets.")
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

    # The Logic Brain
    context = f"DATA: {json.dumps(tournament_data)}. Rules: Group 1 Top 4 -> PL. Group 2 1st -> Phase 2 G1. Be helpful."

    # Generate response
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": context},
            {"role": "user", "content": prompt}
        ],
        model="llama-3.1-8b-instant", # This model is free and very fast
    )
    
    response_text = chat_completion.choices[0].message.content
    with st.chat_message("assistant"):
        st.markdown(response_text)
    st.session_state.messages.append({"role": "assistant", "content": response_text})
