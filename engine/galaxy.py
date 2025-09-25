import random

class GalaxyUniverse:
    def __init__(self, map_data):
        self.map = map_data or {}
        self.orbits = self.map.get("orbits", {})
        self.planets = self.map.get("planets", {})
        self.moons = self.map.get("moons", {})

    def random_path(self, trustmap=None):
        trustmap = trustmap or {}
        if not self.planets:
            return "Void", "NoPlanet", "NoMoon"

        candidates = []
        for planet, pdata in self.planets.items():
            try:
                orbit = self.orbits.get(planet, "UnknownOrbit")
                moon_list = self.moons.get(planet, [])
                if not moon_list:
                    moon_list = ["NoMoon"]
                for moon in moon_list:
                    key = f"{orbit}:{planet}:{moon}"
                    weight = trustmap.get(key, 1)
                    candidates.append((orbit, planet, moon, weight))
            except Exception as e:
                print("⚠️ Error constructing candidate:", planet, e)

        if not candidates:
            return "Void", "NoPlanet", "NoMoon"

        total = sum(w for (_, _, _, w) in candidates)
        if total <= 0:
            # fallback equally
            return random.choice([(o, p, m) for (o, p, m, _) in candidates])

        pick = random.uniform(0, total)
        cum = 0
        for (o, p, m, w) in candidates:
            cum += w
            if pick <= cum:
                return o, p, m

        # fallback
        return random.choice([(o, p, m) for (o, p, m, _) in candidates])
