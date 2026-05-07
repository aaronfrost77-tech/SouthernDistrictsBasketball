import streamlit as st
from openai import OpenAI # DeepSeek uses the OpenAI-compatible library
import json

# 1. THE DATA - Hardcoded to prevent all file-loading errors
TOURNAMENT_DATA = {
    "Boys": {
        "Group 1 (Seeds 1-12)": ["Southern Districts Spartans", "Northside Wizards", "Gold Coast Rollers", "RedCity Roar", "Brisbane Capitals Gold", "SWM Pirates Gold", "SC Phoenix Teal", "Ipswich Force 1", "North GC Seahawks 1", "Logan Thunder", "Gold Coast Waves", "SD Spartans Black"],
        "Group 2 (Seeds 13-26)": ["Gold Coast Breakers", "Brisbane Capitals Silver", "Eastside Knights 1", "USC Rip City Black", "Toowoomba Mountaineers", "Greater Springfield Pioneers", "Moreton Bay Suns", "SWM Pirates Purple", "SWM Pirates Red", "North GC Seahawks 2", "SD Spartans White", "Ipswich Force 2", "SD Spartans Red", "Northside Wizards Sky"],
        "Group 3 (Seeds 27-42)": ["Logan Thunder Gold", "SC Phoenix Orange", "Northside Wizards Navy", "Brisbane Capitals Bronze", "Northside Wizards Silver", "North GC Seahawks 3", "RedCity Pride", "SC Phoenix Black", "Gold Coast Tides", "Logan Thunder Blue", "RedCity Lions", "SC Phoenix Purple", "Gold Coast Combers", "North GC Seahawks 4", "Greater Springfield Pioneers 2", "Toowoomba Mountaineers Blue"]
    },
    "Girls": {
        "Group 1 (Seeds 1-12)": ["North GC Seahawks 1", "SC Phoenix Teal", "SD Spartans", "Brisbane Capitals Gold", "Ipswich Force 1", "Logan Thunder", "RedCity Roar", "Gold Coast Rollers", "SD Spartans Black", "SD Spartans White", "Northside Wizards", "SWM Pirates Gold"],
        "Group 2 (Seeds 13-29)": ["Moreton Bay Suns", "Ipswich Force 2", "SC Phoenix Orange", "RedCity Pride", "Brisbane Capitals Silver", "Gold Coast Waves", "Greater Springfield Pioneers", "Eastside Knights", "Northside Wizards Navy", "Brisbane Capitals Bronze", "SD Spartans Red", "Ipswich Force 3", "Logan Thunder Gold", "Toowoomba Mountaineers", "North GC Seahawks 2", "SWM Pirates Purple", "Gold Coast Breakers"]
    }
}

st.set_page_config(page_title="U12 SQJBC Assistant")
st.title("🏀 U12 Grading Assistant (DeepSeek)")

# 2. DeepSeek API Setup (OpenAI compatible)
# Get your key at platform.deepseek.com
client = OpenAI(api_key=st.secrets["DEEPSEEK_API_KEY"], base_url="https://api.deepseek.com")

if prompt := st.chat_input("I'm with the Toowoomba Mountaineers Blue..."):
    with st.chat_message("user"):
        st.markdown(prompt)

    system_msg = f"""
    You are the U12 SQJBC Assistant.
    DATA: {json.dumps(TOURNAMENT_DATA)}
    
    RULES & CONSTRAINTS:
    - User must specify Boys or Girls to ensure an exact match.
    - NO QBL MENTIONS. This is exclusively for U12 SQJBC Phase 1 Grading.
    
    STRICT DATA HANDLING:
    1. Find the user's exact team in the DATA using the team name and gender.
    2. Respond ONLY with the specific 'pathway' text provided in the JSON for that team.
    3. If the team is in Group 1: State "Top 4 -> Premier League" as per the DATA.
    4. If the team is in Group 3 (like Toowoomba Mountaineers Blue): State ONLY "Consult Phase 2 Rules". Do NOT invent "Top 4" or "Promotion" requirements for Group 3.
    5. If information is not in the DATA, do not guess. Tell the user to consult the official SQJBC handbook.
    """

    response = client.chat.completions.create(
        model="deepseek-chat", # Use "deepseek-reasoner" for even higher logic
        messages=[{"role": "system", "content": system_msg}, {"role": "user", "content": prompt}],
        stream=False
    )
    
    reply = response.choices[0].message.content
    with st.chat_message("assistant"):
        st.markdown(reply)
