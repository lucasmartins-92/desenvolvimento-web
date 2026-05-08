import sys
import re

if len(sys.argv) != 3:
    print("Usage: python update_roster.py <team_id> <roster_file>")
    sys.exit(1)

team_id = sys.argv[1]
roster_file = sys.argv[2]

file_path = r"c:\Users\lucas.ma\Documents\Desenvolvimento Web\Aula 10\worldcup.html"

with open(roster_file, "r", encoding="utf-8") as f:
    players_raw = f.read().strip()

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

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
    
    player_dict = {'pos': pos, 'name': name, 'num': num}
    players.append(player_dict)
    
    if num != 0 and num not in used_numbers:
        used_numbers.add(num)
    else:
        duplicates.append(player_dict)

# Assign free numbers to duplicates
free_numbers = [i for i in range(1, 28) if i not in used_numbers]
for p in duplicates:
    if free_numbers:
        p['num'] = free_numbers.pop(0)

tbody_html = "<tbody>\n"
for p in players:
    tbody_html += f'                            <tr>\n'
    tbody_html += f'                                <td><span class="pos-badge">{p["pos"]}</span></td>\n'
    tbody_html += f'                                <td>{p["name"]}</td>\n'
    tbody_html += f'                                <td><span class="jersey-number">{p["num"]}</span></td>\n'
    tbody_html += f'                            </tr>\n'
tbody_html += "                        </tbody>"

def replacer(match):
    return match.group(1) + tbody_html

pattern = rf'(<div class="selecao-block" id="{team_id}">.*?<table class="squad-table">.*?<thead>.*?</thead>\s*)<tbody>.*?</tbody>'
new_content, count = re.subn(pattern, replacer, content, flags=re.DOTALL)

if count == 0:
    print(f"Failed to find team {team_id}")
    sys.exit(1)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(new_content)

print(f"Replaced {count} occurrences for {team_id}.")
