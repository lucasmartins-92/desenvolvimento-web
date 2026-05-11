import sys
import json
import re

if len(sys.argv) != 3:
    print("Usage: python update_roster.py <team_id> <roster_file>")
    sys.exit(1)

team_id = sys.argv[1]
roster_file = sys.argv[2]

file_path = "data.js"

with open(roster_file, "r", encoding="utf-8") as f:
    players_raw = f.read().strip()

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Extract JSON from data.js
# data.js looks like: const selecoesData = [...];
json_match = re.search(r'const selecoesData = (\[.*?\]);\s*$', content, re.DOTALL)
if not json_match:
    print("Could not find the JSON data inside data.js.")
    sys.exit(1)

json_str = json_match.group(1)
try:
    selecoes = json.loads(json_str)
except json.JSONDecodeError as e:
    print("Error decoding JSON from data.js:", e)
    sys.exit(1)

# Parse players and fix duplicate numbers
players = []
used_numbers = set()
duplicates = []

for line in players_raw.splitlines():
    parts = line.split()
    if len(parts) < 3: continue
    pos = parts[0]
    num_str = parts[-1]
    name = " ".join(parts[1:-1])
    try:
        num = int(num_str)
    except ValueError:
        num = 0
    
    player_dict = {'posicao': pos, 'nome': name, 'numero': num}
    players.append(player_dict)
    
    if num != 0 and num not in used_numbers:
        used_numbers.add(num)
    else:
        duplicates.append(player_dict)

# Assign free numbers to duplicates
free_numbers = [i for i in range(1, 28) if i not in used_numbers]
for p in duplicates:
    if free_numbers:
        p['numero'] = free_numbers.pop(0)

# Make sure all numbers are strings since HTML originally expected strings
for p in players:
    p['numero'] = str(p['numero'])

# Find the team and update its roster
found = False
for sel in selecoes:
    if sel["id"] == team_id:
        sel["jogadores"] = players
        found = True
        break

if not found:
    print(f"Failed to find team {team_id} in data.js")
    sys.exit(1)

# Save back to data.js
new_json_str = json.dumps(selecoes, indent=4, ensure_ascii=False)
new_content = "const selecoesData = " + new_json_str + ";\n"

with open(file_path, "w", encoding="utf-8") as f:
    f.write(new_content)

print(f"Successfully updated roster for {team_id} with {len(players)} players in data.js.")
