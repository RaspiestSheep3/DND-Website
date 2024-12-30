#!DO NOT TOUCH THIS
healthPoints = r"'Health Points'"

strCheck = r"'STR Check'"
dexCheck = r"'DEX Check'"
conCheck = r"'CON Check'"
intCheck = r"'INT Check'"
wisCheck = r"'WIS Check'"
chaCheck = r"'CHA Check'"

strSave = r"'STR Save'"
dexSave = r"'DEX Save'"
conSave = r"'CON Save'"
intSave = r"'INT Save'"
wisSave = r"'WIS Save'"
chaSave = r"'CHA Save'"

toHit = r"'To Hit'"

emptyString = ""

damageTypes = {
    "b" : r"'Damage (Bludgeoning)'",
    "s" : r"'Damage (Slashing)'",
    "pe": r"'Damage (Piercing)'",
    "a" : r"'Damage (Acid)'",
    "c" : r"'Damage (Cold)'",
    "fi": r"'Damage (Fire)'",
    "fo": r"'Damage (Bludgeoning)'",
    "l" : r"'Damage (Lightning)'",
    "n" : r"'Damage (Necrotic)'",
    "ps": r"'Damage (Psychic)'",
    "r" : r"'Damage (Radiant)'",
    "t" : r"'Damage (Thunder)'",
}

name = "Zombie" #Monster Name e.g. Zombie
typeAlignment = "Medium Undead, Neutral Evil" #Monster Type and Alignment e.g. Medium Undead, Neutral Evil
AC = "" #AC e.g. 8
hitPoints = ["22",3,8,9] #Base HP, Roll e.g. ["22",3,8,9] = 3d8 + 9
speed = "" #Movespeed e.g. 20ft
stats = [13,6,16,3,6,5] #stats e.g. 13 6 16 3 6 5
saveMods = [0,0,0,0,2,0] #save modifiers e.g. 0 0 0 0 2 0
savingThrows = "" #saving throw text e.g. WIS +0, write None if none
damageVulnerabilities = "" #Vulnerabilities, write None if none
damageResistances = "" #Resistances, write None if none
damageImmunities = "" #Immunities, write None if none
conditionImmunities = "" #Condition immunities, write None if none
senses = "" #Senses, write None if none
languages = "" #Languages, write None if none
cr = "" #CR
profBonus = "" #Prof bonus
traits = [["Undead Fortitude", "If damage reduces the zombie to 0 hp, it must make a Con. saving throw with a DC of 5 + the damage taken, unless the damage is radiant or from a critical hit. On a success, the zombie drops to 1hp instead."]] #Trait list, e.g. [["Undead Fortitude", "If damage reduces the zombie to 0 hp, it must make a Con. saving throw with a DC of 5 + the damage taken, unless the damage is radiant or from a critical hit. On a success, the zombie drops to 1hp instead."]]
#NOTE : YOU HAVE TO MANUALLY INPUT THE ROLL FUNCTION FOR TRAITS DO NOT SCREW THIS UP IF YOU CANNOT TELL ME AND ILL DO IT

actions = [["Slam",fr'<i>Melee Weapon Attack: </i> <b onclick="RollItem( 3,{toHit})" style="cursor: pointer;"> +3 </b> to hit, reach 5ft, one target. <i>Hit: </i> <b onclick="RollItem( 1,{damageTypes["b"]}, 6)" style="cursor: pointer;">4(1d6 + 1)</b> bludgeoning damage.']] 
#Action list e.g. [["Slam","<i>Melee Weapon Attack: </i> <b onclick="RollItem( 3,'To Hit')" style="cursor: pointer;"> +3 </b> to hit, reach 5ft, one target. <i>Hit: </i> <b onclick="RollItem( 1,'Damage (bludgeoning)', 6)" style="cursor: pointer;">4(1d6 + 1)</b> bludgeoning damage."]]
#NOTE : YOU HAVE TO MANUALLY INPUT THE ROLL FUNCTION FOR ACTIONS DO NOT SCREW THIS UP IF YOU CANNOT TELL ME AND ILL DO IT


def CalculateStat(stat):
    stat -= 10
    output = str(stat // 2)
    if(int(output) > -1):
        output = "+" + output
    
    return output

def CalculateModifier(stat, modifier):
    stat -= 10
    output = (stat // 2)
    output += modifier
    output = str(output)
    if(int(output) > -1):
        output = "+" + output

    return output

print(int(CalculateStat(stats[1])) + saveMods[1])

fileHandle = open("DNDStatBlockWriterOutput.txt", "w")

fileHandle.write(f'<section class="MonsterDisplay">\n   <div class="MonsterGeneral">\n')
fileHandle.write(f'        <h1>{name}</h1>\n        <h2><i>{typeAlignment}<\i></h2>\n')
fileHandle.write(f'        <p><br><b>AC </b>{13}\n')
fileHandle.write(f'        <br><b>Hit Points </b> {hitPoints[0]} <b onclick="RollItem({hitPoints[3]},{healthPoints}, {hitPoints[2]}, {hitPoints[1]})" style="cursor: pointer;">({hitPoints[1]}d{hitPoints[2]} + {hitPoints[3]})</b>\n')
fileHandle.write(f'        <br><b>Speed </b> {speed}\n')
fileHandle.write(f'        </p>\n')
fileHandle.write(f'   </div>\n\n')
fileHandle.write(f'   <div class="MonsterStatTable">\n')
fileHandle.write(f'        <style>\n')
fileHandle.write(r'            table, th, td{' + "\n")
fileHandle.write(f'                border: 2px solid #cad670;\n')
fileHandle.write(f'                border-radius: 5px;\n')
fileHandle.write(r'            }' + "\n")
fileHandle.write(f'        </style>\n\n')
fileHandle.write(r'        <table style="width:550px">' + "\n")
fileHandle.write(f'            <tr>\n')
fileHandle.write(f'                <th>STR</th>\n')
fileHandle.write(f'                <th>DEX</th>\n')
fileHandle.write(f'                <th>CON</th>\n')
fileHandle.write(f'                <th>INT</th>\n')
fileHandle.write(f'                <th>WIS</th>\n')
fileHandle.write(f'                <th>CHA</th>\n')
fileHandle.write(f'            </tr>\n')
fileHandle.write(f'            <tr>\n')
fileHandle.write(rf'                <th onclick="RollItem({CalculateStat(stats[0])},{strCheck})" class="MonsterStatTableCell">{stats[0]} ({CalculateStat(stats[0])})</th>' + "\n")
fileHandle.write(rf'                <th onclick="RollItem({CalculateStat(stats[1])},{dexCheck})" class="MonsterStatTableCell">{stats[1]} ({CalculateStat(stats[1])})</th>'+ "\n")
fileHandle.write(rf'                <th onclick="RollItem({CalculateStat(stats[2])},{conCheck})" class="MonsterStatTableCell">{stats[2]} ({CalculateStat(stats[2])})</th>'+ "\n")
fileHandle.write(rf'                <th onclick="RollItem({CalculateStat(stats[3])},{intCheck})" class="MonsterStatTableCell">{stats[3]} ({CalculateStat(stats[3])})</th>'+ "\n")
fileHandle.write(rf'                <th onclick="RollItem({CalculateStat(stats[4])},{wisCheck})" class="MonsterStatTableCell">{stats[4]} ({CalculateStat(stats[4])})</th>'+ "\n")
fileHandle.write(rf'                <th onclick="RollItem({CalculateStat(stats[5])},{chaCheck})" class="MonsterStatTableCell">{stats[5]} ({CalculateStat(stats[5])})</th>'+ "\n")
fileHandle.write(f'            </tr>\n')
fileHandle.write(f'            <tr>\n')
fileHandle.write(rf'                <th onclick="RollItem({int(CalculateStat(stats[0])) + saveMods[0]},{strSave})" class="MonsterStatTableCell"> {CalculateModifier(stats[0], saveMods[0])}</th>'+ "\n")
fileHandle.write(rf'                <th onclick="RollItem({int(CalculateStat(stats[1])) + saveMods[1]},{dexSave})" class="MonsterStatTableCell"> {CalculateModifier(stats[1], saveMods[1])}</th>'+ "\n")
fileHandle.write(rf'                <th onclick="RollItem({int(CalculateStat(stats[2])) + saveMods[2]},{conSave})" class="MonsterStatTableCell"> {CalculateModifier(stats[2], saveMods[2])}</th>'+ "\n")
fileHandle.write(rf'                <th onclick="RollItem({int(CalculateStat(stats[3])) + saveMods[3]},{intSave})" class="MonsterStatTableCell"> {CalculateModifier(stats[3], saveMods[3])}</th>'+ "\n")
fileHandle.write(rf'                <th onclick="RollItem({int(CalculateStat(stats[4])) + saveMods[4]},{wisSave})" class="MonsterStatTableCell"> {CalculateModifier(stats[4], saveMods[4])}</th>'+ "\n")
fileHandle.write(rf'                <th onclick="RollItem({int(CalculateStat(stats[5])) + saveMods[5]},{chaSave})" class="MonsterStatTableCell"> {CalculateModifier(stats[5], saveMods[5])}</th>'+ "\n")
fileHandle.write(f'            </tr>\n')
fileHandle.write(f'        </table>\n')
fileHandle.write(f'    </div>\n\n')
fileHandle.write(f'    <div class="MonsterAbilities">\n')
fileHandle.write(f'        <p>\n')
fileHandle.write(f'            <b>Saving Throws</b> {savingThrows}\n')
fileHandle.write(f'            <b>Damage Vulnerabilities</b> {damageVulnerabilities}\n')
fileHandle.write(f'            <b>Damage Resistances</b> {damageResistances}\n')
fileHandle.write(f'            <b>Damage Immunities</b> {damageImmunities}\n')
fileHandle.write(f'            <b>Condition Immunities</b> {conditionImmunities}\n')
fileHandle.write(f'            <b>Senses</b> {senses}\n')
fileHandle.write(f'            <b>Languages</b> {languages}\n')
fileHandle.write(f'            <br><b>CR </b> {cr}           <b>Proficency Bonus</b> {profBonus}\n')
fileHandle.write(f'        </p>\n')
fileHandle.write(f'    </div>\n\n')
fileHandle.write(f'    <div class="MonsterTraits">\n')
fileHandle.write(f'        <p>\n')

for trait in traits:
    fileHandle.write(rf'        <b>{trait[0]}<\b> {trait[1]}' + "\n")

fileHandle.write(f'        </p>\n')
fileHandle.write(f'    </div>\n\n')
fileHandle.write(rf'    <div class="MonsterActions">' + "\n")
fileHandle.write(f'        <p>\n')
for action in actions:
    fileHandle.write(rf'        <b>{action[0]}<\b> {action[1]}' + "\n")
fileHandle.write(f'        </p>\n')
fileHandle.write(f'    </div>\n\n')
fileHandle.write(f'    <div class = "RolledOutput" id = "RollOutput" onclick="RollItemDisappear()">\n')
fileHandle.write(f'        <p>\n')
fileHandle.write(f'            <b>Generated Number : </b>\n')
fileHandle.write(f'        </p>\n')
fileHandle.write(f'    </div>\n\n')
fileHandle.write(f'</section>')

fileHandle.close()