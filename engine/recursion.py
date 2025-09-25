import traceback

class RecursionEngine:
    def __init__(self, universe, energy, memory, start_cycle=0):
        self.universe = universe
        self.energy = energy
        self.memory = memory
        self.cycle_count = start_cycle

    def run_cycle(self):
        self.cycle_count += 1

        # Select path
        try:
            orbit, planet, moon = self.universe.random_path(trustmap=self.memory.trustmap)
        except Exception as e:
            print("⚠️ random_path error:", e)
            print(traceback.format_exc())
            orbit, planet, moon = "Void", "NoPlanet", "NoMoon"

        # Pulse energy
        try:
            cost = self.energy.pulse()
        except Exception as e:
            print("⚠️ pulse error:", e)
            print(traceback.format_exc())
            cost = 0

        key = f"{orbit}:{planet}:{moon}"
        # Update trust
        try:
            self.memory.update_trust(key, cost)
        except Exception as e:
            print("⚠️ update_trust error:", e)
            print(traceback.format_exc())

        # Regret logic
        try:
            if cost >= 9 and hasattr(self.memory, "log_regret"):
                self.memory.log_regret(key, reason="High energy spike")
        except Exception as e:
            print("⚠️ regret logging error:", e)
            print(traceback.format_exc())

        print(f"Cycle {self.cycle_count}: {orbit}:{planet}:{moon} (cost {cost}, rem {self.energy.energy})")

        return {
            "cycle": self.cycle_count,
            "orbit": orbit,
            "planet": planet,
            "moon": moon,
            "cost": cost,
            "remaining_energy": self.energy.energy,
            "trustmap": dict(self.memory.trustmap)
        }
