class GalaxyUniverse:
    def __init__(self, data):
        self.core = data.get("core", "Primus")
        self.galaxies = data.get("galaxies", {})

    def get_random_path(self):
        import random
        galaxy = random.choice(list(self.galaxies.keys()))
        planet = random.choice(list(self.galaxies[galaxy].keys()))
        moon = random.choice(self.galaxies[galaxy][planet])
        return galaxy, planet, moon
