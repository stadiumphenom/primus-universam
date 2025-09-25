import random

class GalaxyUniverse:
    """
    Represents the Primus Universe structure — orbits, planets, and moons.
    Supports trust-biased recursive traversal.
    """

    def __init__(self, map_data):
        self.map = map_data or {}
        self.orbits = self.map.get("orbits", {})
        self.planets = self.map.get("planets", {})
        self.moons = self.map.get("moons", {})

    def random_path(self, trustmap=None):
        """
        Selects an orbit → planet → moon path.
        If a trustmap is provided, selection is biased by trust values.
        """

        if not self.planets:
            return "Void", "NoPlanet", "NoMoon"

        trustmap = trustmap or {}

        # Build weighted candidates
        candidates = []
        for planet in self.planets:
            orbit = self.orbits.get(planet, "UnknownOrbit")
            moon_list = self.moons.get(planet, ["NoMoon"])

            for moon in moon_list:
                key = f"{orbit}:{planet}:{moon}"
                weight = trustmap.get(key, 1)  # default trust weight is 1
                candidates.append((orbit, planet, moon, weight))

        if not candidates:
            return "Void", "NoPlanet", "NoMoon"

        # Weighted random choice
        total = sum(w for _, _, _, w in candidates)
        pick = random.uniform(0, total)
        cumulative = 0

        for orbit, planet, moon, weight in candidates:
            cumulative += weight
            if pick <= cumulative:
                return orbit, planet, moon

        # Fallback
        return random.choice([(o, p, m) for o, p, m, _ in candidates])
