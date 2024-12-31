import re
print("working")
import re

def extract_stat_block(text):
    # Clean up text: Remove all whitespaces, newlines, and join into a single line
    text = re.sub(r'\s+', ' ', text)

    monster_data = {}

    # Extracting Monster Name and Type (Assumes it's the first two words before 'Armor Class')
    name_type_pattern = re.compile(r'^(.*?)Armor Class')
    name_type_match = name_type_pattern.search(text)
    if name_type_match:
        name_type_string = name_type_match.group(1).strip()
        name_parts = name_type_string.split(" ", 1)  # Split into name and the rest
        monster_data["name"] = name_parts[0]  # The first word is the name
        monster_data["typeAlignment"] = name_parts[1] if len(name_parts) > 1 else "Unknown"  # Default value if no type
    else:
        monster_data["name"] = "Unknown"
        monster_data["typeAlignment"] = "Unknown"

    # Extracting Armor Class (AC)
    ac_pattern = re.compile(r'Armor Class (\d+)')
    ac_match = ac_pattern.search(text)
    if ac_match:
        monster_data["AC"] = ac_match.group(1).strip()
    else:
        monster_data["AC"] = "N/A"  # Default value if AC not found

    # Extracting Hit Points (e.g., 22 (3d8 + 9))
    hp_pattern = re.compile(r'Hit Points (\d+) \((\d+)d(\d+) \+ (\d+)\)')
    hp_match = hp_pattern.search(text)
    if hp_match:
        monster_data["hitPoints"] = [hp_match.group(1).strip(), int(hp_match.group(2)), int(hp_match.group(3)), int(hp_match.group(4))]
    else:
        monster_data["hitPoints"] = ["N/A", 0, 0, 0]  # Default value if Hit Points not found

    # Extracting Speed
    speed_pattern = re.compile(r'Speed (\d+\s?[a-zA-Z]+)')
    speed_match = speed_pattern.search(text)
    if speed_match:
        monster_data["speed"] = speed_match.group(1).strip()
    else:
        monster_data["speed"] = "30"  # Default value if Speed not found

    # Extracting Stats: STR, DEX, CON, INT, WIS, CHA
    stats_pattern = re.compile(r'STR (\d+)\s\(\+?([-+]?\d+)\)\sDEX (\d+)\s\(\+?([-+]?\d+)\)\sCON (\d+)\s\(\+?([-+]?\d+)\)\sINT (\d+)\s\(\+?([-+]?\d+)\)\sWIS (\d+)\s\(\+?([-+]?\d+)\)\sCHA (\d+)\s\(\+?([-+]?\d+)\)')
    stats_match = stats_pattern.search(text)
    if stats_match:
        monster_data["stats"] = [int(stats_match.group(i)) for i in range(1, 13, 2)]
        monster_data["modifiers"] = [int(stats_match.group(i)) for i in range(2, 14, 2)]
    else:
        monster_data["stats"] = [0, 0, 0, 0, 0, 0]  # Default stats if not found
        monster_data["modifiers"] = [0, 0, 0, 0, 0, 0]  # Default modifiers if not found

    # Extracting Saving Throws, Damage Immunities, Condition Immunities, and other data
    saving_throws_pattern = re.compile(r'Saving Throws ([A-Za-z]+) ([+-]?\d+)')
    saving_throws_match = saving_throws_pattern.search(text)
    if saving_throws_match:
        monster_data["savingThrows"] = f'{saving_throws_match.group(1)} {saving_throws_match.group(2)}'
    else:
        monster_data["savingThrows"] = "N/A"  # Default value if not found

    damage_immunities_pattern = re.compile(r'Damage Immunities ([A-Za-z]+)')
    damage_immunities_match = damage_immunities_pattern.search(text)
    if damage_immunities_match:
        monster_data["damageImmunities"] = damage_immunities_match.group(1)
    else:
        monster_data["damageImmunities"] = "N/A"  # Default value if not found

    condition_immunities_pattern = re.compile(r'Condition Immunities ([A-Za-z]+)')
    condition_immunities_match = condition_immunities_pattern.search(text)
    if condition_immunities_match:
        monster_data["conditionImmunities"] = condition_immunities_match.group(1)
    else:
        monster_data["conditionImmunities"] = "N/A"  # Default value if not found

    # Additional information (such as Traits, Actions, etc.)
    monster_data["traits"] = []
    monster_data["actions"] = []
    traits_pattern = re.compile(r'Traits ([A-Za-z\s.]+?)(?=Actions|$)')

    traits_match = traits_pattern.search(text)
    if traits_match:
        monster_data["traits"] = [trait.strip() for trait in traits_match.group(1).split('\n') if trait]
    else:
        monster_data["traits"] = ["N/A"]  # Default value if Traits not found
    actions_pattern = re.compile(r'Actions\s*(.*)', re.DOTALL)  # Match everything after "Actions"
    actions_match = actions_pattern.search(text)
    if actions_match:
        actions_text = actions_match.group(1).strip()

        # This function will convert a dice roll to the clickable format
        def make_dice_clickable(action_text):
            # Look for patterns like '1d6', '2d8', etc.
            def replace_dice(match):
                # Extract components from the matched text (e.g., '1d6')
                dice = match.group(1)  # '1d6'
                dice_amount, dice_sides = dice.split('d')  # Split into '1' and '6'
                
                # Look for the words after the dice roll (e.g., 'bludgeoning damage')
                damage_type_match = re.search(r'(\w+)\s+damage', action_text)
                damage_type = damage_type_match.group(1) if damage_type_match else 'damage'

                # Return the clickable HTML without introducing <br> tags
                return f'<b onclick="RollItem( {dice_amount}, \'Damage ({damage_type})\', {dice_sides})" style="cursor: pointer;">{dice}</b>'

            # Use the replace_dice function to convert all 'd' rolls
            action_text = re.sub(r'(\d+d\d+)', replace_dice, action_text)

            return action_text

        # Apply the function to make dice clickable
        monster_data["actions"] = make_dice_clickable(actions_text)
    else:
        monster_data["actions"] = "No actions found."
    
    languages_pattern = re.compile(r'Languages\s*(.*?)\s*(?=CR|$)')
    languages_match = languages_pattern.search(text)
    if languages_match:
        monster_data["languages"] = languages_match.group(1).strip()
    else:
        monster_data["languages"] = "None"

    # Extracting CR (Challenge Rating)
    cr_pattern = re.compile(r'CR\s*(\d+/\d+|\d+)')
    cr_match = cr_pattern.search(text)
    if cr_match:
        monster_data["CR"] = cr_match.group(1).strip()
    else:
        monster_data["CR"] = "Not available"

    # Extracting Proficiency Bonus
    proficiency_bonus_pattern = re.compile(r'Proficiency Bonus\s*(\+\d+)')
    proficiency_bonus_match = proficiency_bonus_pattern.search(text)
    if proficiency_bonus_match:
        monster_data["proficiency_bonus"] = proficiency_bonus_match.group(1).strip()
    else:
        monster_data["proficiency_bonus"] = "Not available"

    return monster_data

# Sample text (for testing)
monster_text = """Zombie Medium Undead, Neutral Evil
Armor Class 8
Hit Points 22 (3d8 + 9)
Speed 20 ft.
STR 13 (+1) DEX 6 (-2) CON 16 (+3) INT 3 (-4) WIS 6 (-2) CHA 5 (-3)
Saving Throws WIS +0
Damage Immunities Poison
Condition Immunities Poisoned
Traits Undead Fortitude. If damage reduces the zombie to 0 hit points...
Actions Slam. Melee Weapon Attack: +3 to hit, reach 5 ft., one target. Hit: 4 (1d6 + 1) bludgeoning damage.
Languages Understands those it spoke in life but cannot speak.
CR 1/4 (50xp) Proficiency Bonus +2"""


# Extract data
monster_data = extract_stat_block(monster_text)

# Now generate HTML using the extracted data
html_output = f"""
<!DOCTYPE html>
<html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>DND Website</title>
        <link rel="stylesheet" href="DNDWebsite.css">
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Roboto+Mono:ital,wght@0,100..700;1,100..700&display=swap" rel="stylesheet">
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css">
    </head>
    <body>
        <section class="header">
            <nav></nav> 
            <h1>DND Website</h1><a href="DNDWebsite.html" class="ReturnBtn">Return Home</a>
        </section>

        <section class="MonsterDisplay">
            <div class="MonsterGeneral">
                <h1>{monster_data["name"]}</h1>
                <h2><i>{monster_data['typeAlignment']}</i></h2>
                <p><br><b>AC </b>{monster_data['AC']}
                <br><b>Hit Points </b> {monster_data['hitPoints'][0]} <b onclick="RollItem(9, 'Health Points',  8, 3)" style="cursor: pointer;">({monster_data['hitPoints'][1]}d{monster_data['hitPoints'][2]} + {monster_data['hitPoints'][3]})</b>
                <br><b>Speed </b> {monster_data['speed']}
                </p>
            </div>

            <div class="MonsterStatTable">
                <style>
                    table, th, td {{
                        border: 2px solid #cad670;
                        border-radius: 5px;
                    }}
                </style>
                <table style="width:550px">
                    <tr>
                        <th>STR</th>
                        <th>DEX</th>
                        <th>CON</th>
                        <th>INT</th>
                        <th>WIS</th>
                        <th>CHA</th>
                    </tr>
                    <tr>
                        <th onclick="RollItem({monster_data['stats'][0]}, 'STR Check')" class="MonsterStatTableCell">{monster_data['stats'][0]} ({monster_data['modifiers'][0]})</th>
                        <th onclick="RollItem({monster_data['stats'][1]}, 'DEX Check')" class="MonsterStatTableCell">{monster_data['stats'][1]} ({monster_data['modifiers'][1]})</th>
                        <th onclick="RollItem({monster_data['stats'][2]}, 'CON Check')" class="MonsterStatTableCell">{monster_data['stats'][2]} ({monster_data['modifiers'][2]})</th>
                        <th onclick="RollItem({monster_data['stats'][3]}, 'INT Check')" class="MonsterStatTableCell">{monster_data['stats'][3]} ({monster_data['modifiers'][3]})</th>
                        <th onclick="RollItem({monster_data['stats'][4]}, 'WIS Check')" class="MonsterStatTableCell">{monster_data['stats'][4]} ({monster_data['modifiers'][4]})</th>
                        <th onclick="RollItem({monster_data['stats'][5]}, 'CHA Check')" class="MonsterStatTableCell">{monster_data['stats'][5]} ({monster_data['modifiers'][5]})</th>
                    </tr>
                    <tr>
                        <th onclick="RollItem({monster_data['modifiers'][0]}, 'STR Save')" class="MonsterStatTableCell">{monster_data['modifiers'][0]}</th>
                        <th onclick="RollItem({monster_data['modifiers'][1]}, 'DEX Save')" class="MonsterStatTableCell">{monster_data['modifiers'][1]}</th>
                        <th onclick="RollItem({monster_data['modifiers'][2]}, 'CON Save')" class="MonsterStatTableCell">{monster_data['modifiers'][2]}</th>
                        <th onclick="RollItem({monster_data['modifiers'][3]}, 'INT Save')" class="MonsterStatTableCell">{monster_data['modifiers'][3]}</th>
                        <th onclick="RollItem({monster_data['modifiers'][4]}, 'WIS Save')" class="MonsterStatTableCell">{monster_data['modifiers'][4]}</th>
                        <th onclick="RollItem({monster_data['modifiers'][5]}, 'CHA Save')" class="MonsterStatTableCell">{monster_data['modifiers'][5]}</th>
                    </tr>
                </table>
            </div>

            <div class="MonsterAbilities">
                <p>
                    <b>Saving Throws</b> {monster_data['savingThrows']}
                    <br><b>Damage Immunities</b> {monster_data['damageImmunities']}
                    <br><b>Condition Immunities</b> {monster_data['conditionImmunities']}
                    <br><b>Senses</b> Darkvision 60ft, Passive Perception 8
                    <br><b>Languages</b> {monster_data['languages']}
                    <br><b>CR </b> {monster_data['CR']}           <b>Proficency Bonus</b> {monster_data['proficiency_bonus']}
                </p>
                </p>
            </div>

            <div class="MonsterTraits">
                <p>
                    <b>Traits</b>
                    <br>{'<br>'.join(monster_data['traits'])}
                </p>
            </div>

            <div class="MonsterActions">
                <p>
                    <b>Actions</b>
                    <br>{''.join(monster_data['actions'])}
                </p>
            </div>

            
            <div class = "RolledOutput" id = "RollOutput" onclick="RollItemDisappear()">
                <p>
                    <b>Generated Number : </b>
                </p>
            </div>

        </section>
        

    </body>

    <script>

        var rollHTML = document.getElementById("RollOutput")


        function RollItem(modifier, checkType, diceSides = 20, diceNum = 1){{
            rolledValue = 0;
            rolledValues = [];
            for(let i = 0; i < diceNum; i++)
            {{   
                newValue = Math.trunc(Math.random() * diceSides) + 1
                rolledValue += newValue;
                rolledValues.push(newValue)
                
            }}
              
            rollHTML.innerHTML = `${{checkType}}: ${{String(rolledValue + modifier)}} (${{String(rolledValues)}})`;

            rollHTML.style.right = "0";
            rollHTML.style.visibility = "visible";
        }}

        function RollItemDisappear(){{
            rollHTML.style.visibility = "hidden";
            rollHTML.innerHTML = "Bye";
        }}
        

    </script>

</html>
        </section>
    </body>
</html>
"""

# Save the generated HTML to a file
with open("m3onst4e1r.html", "w") as f:
    f.write(html_output)
