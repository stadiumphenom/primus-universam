import random

class GalaxyUniverse:
    """
    The Primus galaxy: holds orbits, planets, and moons.
    Genesis map structure:
    {
        "Science": {
            "Physics": ["Quantum", "Relativity"],
            "Biology": ["Genetics", "Neuroscience"]
        },
        "Technology": {
            "AI": ["LLMs", "NeuralNets"],
            "Energy": ["Solar", "Fusion"]
        }
    }
    """

    def __init__(self, genesis_map: dict):
        self.map = genesis_map

    def random_path(self):
        """
        Returns a random (orbit, planet, moon) tuple.
        """
        if not self.map:
            return ("Void", "None", "None")

        orbit = random.choice(list(self.map.keys()))
        planets = self.map[orbit]

        if not planets:
            return (orbit, "None", "None")

        planet = random.choice(list(planets.keys()))
        moons = planets[planet]

        if not moons:
            return (orbit, planet, "None")

        moon = random.choice(moons)
        return (orbit, planet, moon)
