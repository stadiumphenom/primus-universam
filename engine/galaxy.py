import random

class GalaxyUniverse:
    """
    Represents the Primus Universe structure — orbits, planets, and moons.
    Random paths are used to simulate recursive traversals during pulse cycles.
    """

    def __init__(self, map_data):
        self.map = map_data or {}

    def random_path(self):
        """
        Randomly selects an orbit → planet → moon path from the Genesis map.
        Includes fallback values if data is missing or incomplete.
        """
        planets = self.map.get("planets", {})
        if not planets:
            # fallback if planets are missing
            return "Void", "NoPlanet", "NoMoon"

        planet = random.choice(list(planets.keys()))
        orbits = self.map.get("orbits", {})
        moons = self.map.get("moons", {})

        orbit = orbits.get(planet, "UnknownOrbit")
        moon_list = moons.get(planet, ["NoMoon"])

        # Choose a moon safely
        moon = random.choice(moon_list) if moon_list else "NoMoon"

        return orbit, planet, moon
