import helpers


def calculateModifiers(move, yourpoke, targetpoke, weather):
    modifier = 1
    modifier = modifier * weatherEffect(move, weather)
    modifier = modifier * stabWorks(move, yourpoke)
    modifier = modifier * typeEffective(move, targetpoke)
    return modifier


def weatherEffect(move, weather):
    if((weather == "Rain" and helpers.getType(move) == "Water") or (weather == "Sun" and helpers.getType(move) == "Fire")):
        return 1.5
    elif((weather == "Rain" and helpers.getType(move) == "Fire") or (weather == "Sun" and helpers.getType(move) == "Water")):
        return 0.5
    else:
        return 1


def stabWorks(move, yourpoke):
    if(helpers.getType(move) in helpers.getPokeTypes(yourpoke)):
        return 1.5
    else:
        return 1


def typeEffective(move, targetpoke):
    modifier = 1
    movetype = helpers.getType(move)
    print(movetype)
    poketypes = helpers.getPokeTypes(targetpoke)
    print(poketypes)
    for type in poketypes:
        ratio = modifier * helpers.getRatio(movetype, type)
    return ratio
