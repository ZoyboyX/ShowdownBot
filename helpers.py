import re
import math


def calculateModifiers(move, yourpoke, targetpoke, weather):
    modifier = 1
    modifier = modifier * weatherEffect(move, weather)
    modifier = modifier * stabWorks(move, yourpoke)
    modifier = modifier * typeEffective(move, targetpoke["name"])
    modifier = modifier * itemMod(yourpoke["item"])
    return modifier


def itemMod(item):
    if item == "Life Orb":
        return 1.3
    return 1


def weatherEffect(move, weather):
    if((weather == "Rain" and getType(move) == "Water") or (weather == "Sun" and getType(move) == "Fire")):
        return 1.5
    elif((weather == "Rain" and getType(move) == "Fire") or (weather == "Sun" and getType(move) == "Water")):
        return 0.5
    else:
        return 1


def stabWorks(move, yourpoke):
    if(getType(move) in getPokeTypes(yourpoke["name"])):
        if(yourpoke["item"] == "Expert Belt"):
            return 1.5*1.2
        return 1.5
    else:
        return 1


def typeEffective(move, targetpoke):
    modifier = 1
    movetype = getType(move)
    poketypes = getPokeTypes(targetpoke)
    for type in poketypes:
        modifier = modifier * getRatio(movetype, type)
    return modifier


def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1


def getYourTeamInfo():
    team = []
    for k in range(0, 6):
        fname = "pokemon" + str(k+1)+"data.txt"
        file = open(fname, "r")
        length = file_len(fname)
        token = 0
        info = []
        while token < length:
            line = file.readline()
            token = token + 1
            if("<div id=\"tooltipwrapper\" role=\"tooltip\"" in line):
                nextline = file.readline()
                token = token + 1
                while token < length:
                    if "<" not in nextline:
                        info.append(nextline.strip())
                    nextline = file.readline()
                    token = token + 1
        # print(info)
        pokemon = {}
        stats = []
        moves = []
        for k in range(0, len(info)):
            data = info[k]
            if k == 0:
                pokemon['name'] = data
            elif k == 1 and data.startswith("("):
                pokemon["name"] = data.replace("(", "").replace(")", "")
            elif re.search(r"^L\d+", data):
                levellist = re.findall(r"\d+", data)
                levelnum = int(levellist[0])
                pokemon['level'] = levelnum
            elif re.search(r"\(\d+\/\d+\)", data):
                hplist = re.findall(r"\(\d+\/\d+\)", data)
                hpnum = hplist[0].split("/")
                hp = int(hpnum[0].replace("(", ""))
                stats.append(hp)
            elif info[k] == "Ability:":
                pokemon["ability"] = info[k+1].replace("/", "").strip()
            elif info[k] == "Item:":
                pokemon["item"] = info[k+1]
            elif info[k] == "Atk":
                for x in range(0, 5):
                    stats.append(int(info[k+(x*2)+1]))
            elif info[k].startswith("•"):
                moves.append(info[k].replace("•", "").strip())
        pokemon['stats'] = stats
        pokemon['moves'] = moves
        if 'level' not in pokemon:
            pokemon['level'] = 100
        team.append(pokemon)
    return team


def getbasestats(pokemon):
    fname = "pokedex.ts"
    file = open(fname, "r")
    length = file_len(fname)
    token = 0
    while token < length:
        line = file.readline()
        token = token + 1
        if(pokemon in line and "name:" in line):
            temp = re.findall(r'\".+\"', line)
            pokename = temp[0].replace("\"", "")
            if(pokename in line):
                nextline = file.readline()
                token = token + 1
                while "baseStats:" not in nextline:
                    nextline = file.readline()
                    token = token + 1
                temp = re.findall(r'\d+', nextline)
                res = list(map(int, temp))
                stats = res
                print(pokemon + ": "+"HP: " + str(stats[0]) + " ATK: " + str(stats[1]) + " DEF: " + str(stats[2]) +
                      " SPA: " + str(stats[3]) + " SPD: " + str(stats[4]) + " SPE: " + str(stats[5]))
                return res


def calculateHP(HP, level):
    return math.floor(((2*HP+31+math.floor(84/4.0))*level)/100.0)+level+10


def calculateStat(stat, level):
    return math.floor(((2*stat+31+math.floor(84/4))*level)/100.0)+5


def calculateDamage(attackerlevel, movepower, attackerattack, opponentdefense, modifier):
    print("attackerlevel", attackerlevel, "movepower", movepower, "attackerattack",
          attackerattack, "opponentdefense", opponentdefense, modifier, "modifier")
    attackerlevel = attackerlevel+0.0
    attackerattack = attackerattack + 0.0
    opponentdefense = opponentdefense + 0.0
    movepower = movepower + 0.0
    if(movepower == 0):
        return (0, 0)
    if(modifier == -1):
        # damage = int(int(int(2 * attackerlevel / 5.0 + 2) *
        #                  attackerattack * movepower / opponentdefense) / 50.0)
        damage = int(int((((2*attackerlevel)/5+2)*movepower *
                          (attackerattack/opponentdefense))/50.0)+2)
    else:
        # damage = int(int(int(2 * attackerlevel / 5.0 + 2) * attackerattack *
        #                  movepower / opponentdefense) / 50.0)*modifier
        damage = int(int((((2*attackerlevel)/5+2)*movepower *
                          (attackerattack/opponentdefense))/50.0)+2)*modifier
    min = int(damage*.85)
    max = int(damage * 1)
    return (min, max)


def testifstatsgood(pokemon, level):
    enemystats = getbasestats(pokemon)
    enemystats[0] = calculateHP(enemystats[0], level)
    for k in range(1, 6):
        enemystats[k] = calculateStat(enemystats[k], level)
    print(enemystats)


def getmovepower(movename):
    fname = "moves.ts"
    file = open(fname, "r")
    length = file_len(fname)
    token = 0
    while token < length:
        line = file.readline()
        token = token + 1
        if("basePower:" in line):
            temp = re.findall(r'\d+', line)
            res = list(map(int, temp))
            latestbasepower = res[0]
        if("name:" in line):
            moven = line.strip()
            moven = moven.replace("name:", "")
            moven = moven.replace('\"', "")
            moven = moven.replace(',', "")
            moven = moven.strip()
            if(movename == moven):
                return latestbasepower


def getPossibleMoves(enemy):
    enemyname = enemy["name"].lower()
    enemyname = enemyname.replace(" ", "").replace("-", "")
    fname = "formats-data.ts"
    file = open(fname, "r")
    length = file_len(fname)
    token = 0
    while token < length:
        line = file.readline()
        token = token + 1
        if(enemyname in line):
            line = line.strip().replace(" ", "").replace(":", "").replace("{", "")
            if(enemyname == line):
                while("randomBattleMoves:" not in line):
                    line = file.readline()
                    token = token + 1
                temp = re.findall(r'\".+\"', line)
                for move in temp:
                    move.replace("\"", "")
                print(temp)
                return temp


def yourTeamDamageOpponent(team, opponentstats):
    for k in range(0, len(team)):
        opponentdefense = opponentstats[2]
        opponentspecialdefense = opponentstats[4]
        print(team[k].get("name"))
        moves = team[k].get("moves")
        stats = team[k].get("stats")
        for x in range(0, len(team[k].get("moves"))):
            print(moves[x])
            movepower = getmovepower(moves[x])
            attackerlevel = team[k].get("level")
            if(moveCategory(moves[x]) == 'Physical'):
                attackerattack = stats[1]
                min, max = calculateDamage(attackerlevel, movepower,
                                           attackerattack, opponentdefense, -1)
            else:
                attackerspecialattack = stats[3]
                min, max = calculateDamage(attackerlevel, movepower,
                                           attackerspecialattack, opponentspecialdefense, -1)
            print(min, max)


def moveCategory(move):
    fname = "moves.ts"
    file = open(fname, "r")
    length = file_len(fname)
    token = 0
    while token < length:
        line = file.readline()
        token = token + 1
        if("category:" in line):
            temp = re.findall(r'\".+\"', line)
            res = temp[0].replace("\"", "")
            category = res
        if(move in line and "name:" in line):
            moven = line.strip()
            moven = moven.replace("name:", "")
            moven = moven.replace('\"', "")
            moven = moven.replace(',', "")
            moven = moven.strip()
            if(move == moven):
                return category


def getType(move):
    fname = "moves.ts"
    file = open(fname, "r")
    length = file_len(fname)
    token = 0
    while token < length:
        line = file.readline()
        token = token + 1
        if(move in line):
            moven = line.strip()
            moven = moven.replace("name:", "")
            moven = moven.replace('\"', "")
            moven = moven.replace(',', "")
            moven = moven.strip()
            if(move == moven):
                while "type: \"" not in line:
                    line = file.readline()
                    token = token+1
                temp = re.findall(r'\".+\"', line)
                res = temp[0].replace("\"", "")
                type = res
                return type


def yourTeamDamageOpponentPercent(team, opponent, weather):
    opponentstats = opponent["stats"]
    for k in range(0, len(team)):
        print(team[k])
        opponentdefense = opponentstats[2]
        opponentHP = opponentstats[0]
        opponentspecialdefense = opponentstats[4]
        print(team[k].get("name"))
        moves = team[k].get("moves")
        stats = team[k].get("stats")
        for x in range(0, len(team[k].get("moves"))):
            print("\t" + moves[x])
            movepower = getmovepower(moves[x])
            attackerlevel = team[k].get("level")
            if(moveCategory(moves[x]) == 'Physical'):
                attackerattack = stats[1]
                modify = calculateModifiers(moves[x], team[k], opponent, weather)
                min, max = calculateDamage(attackerlevel, movepower,
                                           attackerattack, opponentdefense, modify)
            else:
                modify = calculateModifiers(moves[x], team[k], opponent, weather)
                attackerspecialattack = stats[3]
                min, max = calculateDamage(attackerlevel, movepower,
                                           attackerspecialattack, opponentspecialdefense, modify)
            print("\t\t", damageToPercent((min, max), opponentHP))


def damageToPercent(minimax, opponentHP):
    min, max = minimax
    opponentHP = opponentHP + 0.0
    min = min/opponentHP
    max = max/opponentHP
    return (min, max)


def getPokeTypes(pokemon):
    fname = "pokedex.ts"
    types = []
    file = open(fname, "r")
    length = file_len(fname)
    token = 0
    while token < length:
        line = file.readline()
        token = token + 1
        if(pokemon in line and "name:" in line):
            temp = re.findall(r'\".+\"', line)
            pokename = temp[0].replace("\"", "")
            if(pokename in line):
                nextline = file.readline()
                token = token + 1
                while "types:" not in nextline:
                    nextline = file.readline()
                    token = token + 1
                temp = re.findall(r'\"[^,]+\"', nextline)
                # print(temp)
                for z in range(0, len(temp)):
                    types.append(temp[z].replace("\"", ""))
                return types


def getRatio(attackingtype, defendingtype):
    fname = "typechart.ts"
    file = open(fname, "r")
    length = file_len(fname)
    token = 0
    while token < length:
        line = file.readline()
        token = token + 1
        if(defendingtype in line and re.search(r"\t[A-Z][a-z]+: {", line)):
            line = file.readline()
            token = token+2
            while attackingtype not in line:
                line = file.readline()
                token = token+1
            num = int(re.findall(r"\d", line)[0])
            if num == 0:
                return 1
            if num == 1:
                return 2
            if num == 2:
                return .5
            if num == 3:
                return 0


# enemy = {}
# enemy["name"] = "Rhyperior"
# # getPossibleMoves(enemy)
#
# ypokemon = {}
# ypokemon["name"] = "Whiscash"
# ypokemon["item"] = "Life Orb"
#
# print(calculateModifiers("Earthquake", ypokemon, enemy, "poop"))
