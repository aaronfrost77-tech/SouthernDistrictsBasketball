import streamlit as st
from openai import OpenAI
from data_map import TEAMS 

st.set_page_config(page_title="U12 SQJBC Assistant", page_icon="🏀")
st.title("🏀 U12 SQJBC Assistant")

client = OpenAI(api_key=st.secrets["DEEPSEEK_API_KEY"], base_url="https://api.deepseek.com")

def get_team_info(user_input):
    user_input = user_input.lower()
    matches = []
    # We look for a match in the keys of our dictionary
    for official_name in TEAMS.keys():
        # If the user's input (e.g. 'Spartans White') is in the official name
        if user_input in official_name.lower() or any(word in official_name.lower() for word in user_input.split() if len(word) > 4):
            matches.append((official_name, TEAMS[official_name]))
    return matches

if prompt := st.chat_input("Ask about your team (e.g. 'Spartans White')"):
    with st.chat_message("user"):
        st.markdown(prompt)

    found_matches = get_team_info(prompt)

    if len(found_matches) == 1:
        name, data = found_matches[0]
        # This is the "Grounding" content
        context_data = f"TEAM: {name}\nDATA: {data}"
        instructions = "Provide the Seed, Group, Pool, and Schedule from the DATA. Verbatim pathway only."
    elif len(found_matches) > 1:
        context_data = "NONE"
        matches_list = [m[0] for m in found_matches]
        instructions = f"I found multiple teams: {matches_list}. Ask the user which one they mean."
    else:
        context_data = "NONE"
        instructions = "The team was not found in the U12 SQJBC Phase 1 data. Ask for the specific name and gender. DO NOT make up standings or rankings."

    # Force the AI to stay in the box
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": f"You are the U12 SQJBC Assistant. {instructions}"},
            {"role": "user", "content": f"Context: {context_data}\nUser Question: {prompt}"}
        ]
    )
    
    with st.chat_message("assistant"):
        st.markdown(response.choices[0].message.content)
