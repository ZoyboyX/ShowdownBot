class Pokemon:
    def __init__(self, name, types, baseStats, randomBattleMoves, level):
        self.name = name
        self.types = types
        self.baseStats = baseStats
        self.randomBattleMoves = randomBattleMoves
        self.level = level


def compileAllPokemon():
    ArrayList pokemoninfo = list()
    f = open("pokedex.ts"):
    data = f.read()
