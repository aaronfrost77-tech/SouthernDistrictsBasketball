import streamlit as st
from openai import OpenAI
from data_map import TEAMS 

st.set_page_config(page_title="U12 SQJBC Assistant", page_icon="🏀")
st.title("🏀 U12 SQJBC Assistant")

client = OpenAI(api_key=st.secrets["DEEPSEEK_API_KEY"], base_url="https://api.deepseek.com")

# IMPROVED SEARCH: Handles partial names like "Spartans" or "Toowoomba"
def get_team_info(user_input):
    user_input = user_input.lower()
    matches = []
    for official_name, data in TEAMS.items():
        # Match if the user's word is in the team name OR vice versa
        if user_input in official_name.lower() or any(word in official_name.lower() for word in user_input.split() if len(word) > 3):
            matches.append((official_name, data))
    return matches

if prompt := st.chat_input("Ask about your team (e.g. 'Spartans Black' or 'Toowoomba Blue')"):
    with st.chat_message("user"):
        st.markdown(prompt)

    found_matches = get_team_info(prompt)

    if len(found_matches) == 1:
        # Perfect match
        name, data = found_matches[0]
        system_msg = f"""
        You are the U12 SQJBC Assistant. 
        DATA: {name}: {data}
        INSTRUCTIONS:
        1. Summarize Seed, Group, Pool, and Venue.
        2. List games/times if available.
        3. Pathway: {data['pathway']}
        Stay concise. NO QBL. NO AAU.
        """
    elif len(found_matches) > 1:
        # Multiple matches (e.g., user just said 'Spartans')
        names = [m[0] for m in found_matches]
        system_msg = f"The user query matched multiple teams: {names}. Ask them to be more specific (e.g., mention 'Black', 'White', or 'Boys/Girls')."
    else:
        # No match found
        system_msg = "You are the U12 SQJBC Assistant. You don't know this team. Ask the user for their exact team name and whether they are Boys or Girls. Remind them you only have data for U12 Phase 1 Grading."

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "system", "content": system_msg}, {"role": "user", "content": prompt}]
    )
    
    with st.chat_message("assistant"):
        st.markdown(response.choices[0].message.content)
