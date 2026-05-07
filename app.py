import streamlit as st
from openai import OpenAI
from data_map import TEAMS # Import your list

client = OpenAI(api_key=st.secrets["DEEPSEEK_API_KEY"], base_url="https://api.deepseek.com")

def find_team(query):
    query = query.lower()
    for name, data in TEAMS.items():
        if name.lower().split(" (")[0] in query:
            return name, data
    return None, None

prompt = st.chat_input("Ask about your team...")
if prompt:
    team_name, team_data = find_team(prompt)
    
    if team_data:
        # We only send the SPECIFIC team data to the AI
        system_content = f"You are an assistant for {team_name}. Data: {team_data}"
    else:
        system_content = "Team not found. Ask for their team name and gender."

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "system", "content": system_content}, {"role": "user", "content": prompt}]
    )
    st.write(response.choices[0].message.content)
