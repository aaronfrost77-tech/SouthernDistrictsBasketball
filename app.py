import streamlit as st
from groq import Groq
import json

# 1. Page Configuration
st.set_page_config(page_title="U12 SQJBC Assistant", page_icon="🏀")
st.title("🏀 U12 Grading Bot")
st.info("2025-26 Phase 1 Grading Assistant")

# 2. Load the JSON Brain
@st.cache_data
def load_data():
    try:
        with open('tournament_brain.json', 'r') as f:
            data = json.load(f)
            # Ensure we are looking at the 'teams' sub-dictionary
            return data.get("teams", {})
    except FileNotFoundError:
        st.error("File 'tournament_brain.json' not found!")
        return {}
    except json.JSONDecodeError:
        st.error("Error reading JSON. Check for trailing commas or missing brackets!")
        return {}

teams_dict = load_data()

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

# 5. The Logic & AI Interaction
if prompt := st.chat_input("Ask about your team..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # --- START DEBUG & SEARCH LOGIC ---
    user_query = prompt.lower()
    found_team_data = None
    matched_key = None

    if not teams_dict:
        st.error("DEBUG: The team database is empty. Check your JSON file.")
    else:
        # Sort keys by length (longest first) to prevent partial matches
        sorted_team_keys = sorted(teams_dict.keys(), key=len, reverse=True)

        for team_key in sorted_team_keys:
            # Check if the team name (minus brackets) is in the prompt
            clean_name_key = team_key.split(" (")[0].lower()
            
            if clean_name_key in user_query:
                # Check for gender specific keywords to narrow it down
                user_wants_boys = "boy" in user_query
                user_wants_girls = "girl" in user_query
                is_boys_key = "(boys)" in team_key.lower()
                is_girls_key = "(girls)" in team_key.lower()

                if (user_wants_boys and is_boys_key) or (user_wants_girls and is_girls_key) or (not user_wants_boys and not user_wants_girls):
                    matched_key = team_key
                    found_team_data = teams_dict[team_key]
                    break

    # Construct Context based on Search Results
    if matched_key and found_team_data:
        st.success(f"DEBUG: Found match for '{matched_key}'")
        context = f"""
        You are the U12 SQJBC Assistant. Use 'You'.
        The user is with the team: {matched_key}
        STRICT DATA: {json.dumps(found_team_data, indent=2)}
        INSTRUCTIONS:
        1. Use ONLY the STRICT DATA provided.
        2. Give their Seed, Group, and Pathway from the DATA.
        3. Do NOT talk about QBL or guess if data is missing.
        """
    else:
        st.warning("DEBUG: No match found in JSON for that name.")
        context = "The user's team wasn't found. Ask them for their exact team name (e.g. Toowoomba Mountaineers Blue) and gender."
    # --- END DEBUG & SEARCH LOGIC ---

    try:
        messages_to_send = [{"role": "system", "content": context}]
        # Add history
        for msg in st.session_state.messages[-4:]:
            messages_to_send.append(msg)
