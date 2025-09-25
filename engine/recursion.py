import random
import traceback

class RecursionEngine:
    def __init__(self, universe, energy, memory, start_cycle=0):
        self.universe = universe
        self.energy = energy
        self.memory = memory
        self.cycle_count = start_cycle

    def run_cycle(self):
        self.cycle_count += 1
        try:
            # Attempt path selection
            orbit, planet, moon = self.universe.random_path(trustmap=self.memory.trustmap)
        except Exception as e:
            print("⚠️ Error in random_path:", e)
            print(traceback.format_exc())
            # fallback to safe default
            orbit, planet, moon = ("Void", "NoPlanet", "NoMoon")

        # Energy pulse (safe)
        try:
            cost = self.energy.pulse()
        except Exception as e:
            print("⚠️ Error in energy.pulse:", e)
            print(traceback.format_exc())
            cost = 0

        # Memory update
        key = f"{orbit}:{planet}:{moon}"

        try:
            self.memory.update_trust(key, cost)
        except Exception as e:
            print("⚠️ Error in update_trust:", e)
            print(traceback.format_exc())

        # Regret logic (safe)
        try:
            if cost >= 9:
                # Use whichever method exists: log_regret or regret
                if hasattr(self.memory, "log_regret"):
                    self.memory.log_regret(key, "High energy spike")
                elif hasattr(self.memory, "regret"):
                    self.memory.regret(key, "High energy spike")
        except Exception as e:
            print("⚠️ Error in regret logging:", e)
            print(traceback.format_exc())

        # Debug
        print(f"Cycle {self.cycle_count}: {orbit} → {planet} → {moon}")
        print(f"Cost: {cost}, Remaining: {self.energy.energy}")

        # Build result
        return {
            "cycle": self.cycle_count,
            "orbit": orbit,
            "planet": planet,
            "moon": moon,
            "cost": cost,
            "remaining_energy": self.energy.energy,
            "trustmap": dict(self.memory.trustmap)
        }
