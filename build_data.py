import json

def generate():
    teams = {}
    
    # BOYS GROUP 1 (Morayfield)
    b1 = ["Southern Districts Spartans", "Northside Wizards", "Gold Coast Rollers", "RedCity Roar", "Brisbane Capitals Gold", "SWM Pirates Gold", "SC Phoenix Teal", "Ipswich Force 1", "North GC Seahawks 1", "Logan Thunder", "Gold Coast Waves", "SD Spartans Black"]
    for i, name in enumerate(b1):
        teams[f"{name} (Boys)"] = {
            "seed": i+1, "group": 1, "venue": "Morayfield Sports Centre", 
            "date": "Sunday 24th May",
            "times": "8:00am, 10:30am, 1:15pm",
            "pathway": "Rank 1-4: Premier League; Rank 5-6: Phase 2 Group 1"
        }

    # BOYS GROUP 2 (Various Venues)
    b2 = ["Gold Coast Breakers", "Brisbane Capitals Silver", "Eastside Knights 1", "USC Rip City Black", "Toowoomba Mountaineers", "Greater Springfield Pioneers", "Moreton Bay Suns", "SWM Pirates Purple", "SWM Pirates Red", "North GC Seahawks 2", "SD Spartans White", "Ipswich Force 2", "SD Spartans Red", "Northside Wizards Sky"]
    for i, name in enumerate(b2):
        teams[f"{name} (Boys)"] = {
            "seed": i+13, "group": 2, "venue": "Northside / Cornubia / South Pine (Check Pool)",
            "date": "Sunday 31st May",
            "times": "Morning sessions starting from 8:00am",
            "pathway": "Rank 1: Phase 2 G1; Rank 2-3: Phase 2 G2; Rank 4+: Phase 2 G3"
        }

    # BOYS GROUP 3 (Auchenflower/Sunshine Coast)
    b3 = ["Logan Thunder Gold", "SC Phoenix Orange", "Northside Wizards Navy", "Brisbane Capitals Bronze", "Northside Wizards Silver", "North GC Seahawks 3", "RedCity Pride", "SC Phoenix Black", "Gold Coast Tides", "Logan Thunder Blue", "RedCity Lions", "SC Phoenix Purple", "Gold Coast Combers", "North GC Seahawks 4", "Greater Springfield Pioneers 2", "Toowoomba Mountaineers Blue"]
    for i, name in enumerate(b3):
        teams[f"{name} (Boys)"] = {
            "seed": i+27, "group": 3, "venue": "Auchenflower / Morayfield / Sunshine Coast",
            "date": "24 May or 7 June",
            "times": "Check specific Pool for 8:00am or 9:15am starts",
            "pathway": "Consult Phase 2 Rules for Group 3"
        }

    # GIRLS GROUP 1 (Cornubia)
    g1 = ["North GC Seahawks 1", "SC Phoenix Teal", "SD Spartans", "Brisbane Capitals Gold", "Ipswich Force 1", "Logan Thunder", "RedCity Roar", "Gold Coast Rollers", "SD Spartans Black", "SD Spartans White", "Northside Wizards", "SWM Pirates Gold"]
    for i, name in enumerate(g1):
        teams[f"{name} (Girls)"] = {
            "seed": i+1, "group": 1, "venue": "Cornubia Park", 
            "date": "Sunday 24th May",
            "times": "9:15am, 11:45am, 2:15pm",
            "pathway": "Rank 1-4: Premier League; Rank 5-6: Phase 2 Group 1"
        }

    # GIRLS GROUP 2 (Coomera)
    g2 = ["Moreton Bay Suns", "Ipswich Force 2", "SC Phoenix Orange", "RedCity Pride", "Brisbane Capitals Silver", "Gold Coast Waves", "Greater Springfield Pioneers", "Eastside Knights", "Northside Wizards Navy", "Brisbane Capitals Bronze", "SD Spartans Red", "Ipswich Force 3", "Logan Thunder Gold", "Toowoomba Mountaineers", "North GC Seahawks 2", "SWM Pirates Purple", "Gold Coast Breakers"]
    for i, name in enumerate(g2):
        teams[f"{name} (Girls)"] = {
            "seed": i+13, "group": 2, "venue": "Coomera Indoor / Northside",
            "date": "Sunday 17th May or 31st May",
            "times": "8:00am, 10:30am, 1:15pm (Coomera Slots)",
            "pathway": "Rank 1: Phase 2 G1; Rank 2-3: Phase 2 G2; Rank 4+: Phase 2 G3"
        }

    with open("data_map.py", "w") as f:
        f.write("TEAMS = " + json.dumps(teams, indent=4))
    print(f"DONE! Library updated with {len(teams)} teams and full timing blocks.")

generate()
