import streamlit as st
from openai import OpenAI
from data_map import TEAMS 

st.set_page_config(page_title="U12 SQJBC Assistant", page_icon="🏀")
st.title("🏀 U12 SQJBC Assistant")

client = OpenAI(api_key=st.secrets["DEEPSEEK_API_KEY"], base_url="https://api.deepseek.com")

def get_team_info(user_input):
    user_input = user_input.lower()
    matches = []
    for official_name, data in TEAMS.items():
        # Check if user input matches a significant part of the team name
        if user_input in official_name.lower() or any(word in official_name.lower() for word in user_input.split() if len(word) > 4):
            matches.append({"name": official_name, "data": data})
    return matches

if prompt := st.chat_input("Ask about your team (e.g. 'Spartans White')"):
    with st.chat_message("user"):
        st.markdown(prompt)

    found_matches = get_team_info(prompt)

    if found_matches:
        # We pass ALL found matches to the AI at once
        context_data = json.dumps(found_matches)
        system_msg = """
        You are the U12 SQJBC Assistant. 
        INSTRUCTIONS:
        1. If one team matches, show its Seed, Group, Venue, and Schedule.
        2. If multiple teams match (e.g., Boys and Girls), show BOTH schedules clearly labeled. 
        3. Use bold headers and bullet points for readability.
        4. Verbatim pathway: Use the 'pathway' field from the data.
        5. NEVER mention AAU, leagues, or standings not in the data.
        """
    else:
        context_data = "NONE"
        system_msg = "The team was not found. Ask for the exact name and remind them this is for U12 Phase 1 only."

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": system_msg},
            {"role": "user", "content": f"Context Data: {context_data}\n\nUser Question: {prompt}"}
        ]
    )
    
    with st.chat_message("assistant"):
        st.markdown(response.choices[0].message.content)
