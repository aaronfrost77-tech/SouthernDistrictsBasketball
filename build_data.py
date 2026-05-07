import json

def generate():
    teams = {}
    
    # BOYS GROUP 1 [cite: 6]
    b1 = ["Southern Districts Spartans", "Northside Wizards", "Gold Coast Rollers", "RedCity Roar", "Brisbane Capitals Gold", "SWM Pirates Gold", "SC Phoenix Teal", "Ipswich Force 1", "North GC Seahawks 1", "Logan Thunder", "Gold Coast Waves", "SD Spartans Black"]
    for i, name in enumerate(b1):
        teams[f"{name} (Boys)"] = {"seed": i+1, "group": 1, "venue": "Morayfield/Northside [cite: 256]", "pathway": "Rank 1-4: Premier League; Rank 5-6: Phase 2 Group 1"}

    # BOYS GROUP 2 [cite: 6]
    b2 = ["Gold Coast Breakers", "Brisbane Capitals Silver", "Eastside Knights 1", "USC Rip City Black", "Toowoomba Mountaineers", "Greater Springfield Pioneers", "Moreton Bay Suns", "SWM Pirates Purple", "SWM Pirates Red", "North GC Seahawks 2", "SD Spartans White", "Ipswich Force 2", "SD Spartans Red", "Northside Wizards Sky"]
    for i, name in enumerate(b2):
        teams[f"{name} (Boys)"] = {"seed": i+13, "group": 2, "venue": "Varies (See PDF) [cite: 256]", "pathway": "Rank 1: Phase 2 G1; Rank 2-3: Phase 2 G2; Rank 4+: Phase 2 G3"}

    # BOYS GROUP 3 [cite: 6]
    b3 = ["Logan Thunder Gold", "SC Phoenix Orange", "Northside Wizards Navy", "Brisbane Capitals Bronze", "Northside Wizards Silver", "North GC Seahawks 3", "RedCity Pride", "SC Phoenix Black", "Gold Coast Tides", "Logan Thunder Blue", "RedCity Lions", "SC Phoenix Purple", "Gold Coast Combers", "North GC Seahawks 4", "Greater Springfield Pioneers 2", "Toowoomba Mountaineers Blue"]
    for i, name in enumerate(b3):
        teams[f"{name} (Boys)"] = {"seed": i+27, "group": 3, "venue": "Varies (See PDF) [cite: 256]", "pathway": "Consult Phase 2 Rules"}

    # GIRLS GROUP 1 [cite: 264]
    g1 = ["North GC Seahawks 1", "SC Phoenix Teal", "SD Spartans", "Brisbane Capitals Gold", "Ipswich Force 1", "Logan Thunder", "RedCity Roar", "Gold Coast Rollers", "SD Spartans Black", "SD Spartans White", "Northside Wizards", "SWM Pirates Gold"]
    for i, name in enumerate(g1):
        teams[f"{name} (Girls)"] = {"seed": i+1, "group": 1, "venue": "Cornubia Park [cite: 418]", "pathway": "Rank 1-4: Premier League; Rank 5-6: Phase 2 Group 1"}

    # GIRLS GROUP 2 [cite: 264]
    g2 = ["Moreton Bay Suns", "Ipswich Force 2", "SC Phoenix Orange", "RedCity Pride", "Brisbane Capitals Silver", "Gold Coast Waves", "Greater Springfield Pioneers", "Eastside Knights", "Northside Wizards Navy", "Brisbane Capitals Bronze", "SD Spartans Red", "Ipswich Force 3", "Logan Thunder Gold", "Toowoomba Mountaineers", "North GC Seahawks 2", "SWM Pirates Purple", "Gold Coast Breakers"]
    for i, name in enumerate(g2):
        teams[f"{name} (Girls)"] = {"seed": i+13, "group": 2, "venue": "Coomera/Northside [cite: 418]", "pathway": "Rank 1: Phase 2 G1; Rank 2-3: Phase 2 G2; Rank 4+: Phase 2 G3"}

    with open("data_map.py", "w") as f:
        f.write("TEAMS = " + json.dumps(teams, indent=4))
    print(f"DONE! Created data_map.py with {len(teams)} teams.")

generate()
