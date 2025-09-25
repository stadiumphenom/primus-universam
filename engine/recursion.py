import random

class RecursionEngine:
    """
    The recursive driver that runs pulse cycles.
    It connects GalaxyUniverse, EnergyPulse, and MemorySystem.
    """

    def __init__(self, universe, energy, memory, start_cycle=0):
        self.universe = universe
        self.energy = energy
        self.memory = memory
        self.cycle_count = start_cycle

    def run_cycle(self):
        """
        Run a single recursive pulse cycle:
        - Selects a random orbit/planet/moon
        - Consumes energy via EnergyPulse
        - Updates trustmap in memory
        """
        self.cycle_count += 1

        # pick random orbit -> planet -> moon
        orbit, planet, moon = self.universe.random_path()

        # consume energy
        cost = self.energy.pulse()

        # update memory trustmap
        key = f"{orbit}:{planet}:{moon}"
        self.memory.update_trust(key, cost)

        # optionally add regret
        if cost >= 9:
            self.memory.regret(key, reason="High energy spike")

        # Debug
        print(f"🌌 Cycle {self.cycle_count}: {orbit} → {planet} → {moon}")
        print(f"⚡ Energy cost: {cost} | Remaining: {self.energy.energy}")
        print(f"🧠 Trust updated: {key} +{cost}")
        print("-" * 40)

        return {
            "cycle": self.cycle_count,
            "orbit": orbit,
            "planet": planet,
            "moon": moon,
            "cost": cost,
            "remaining_energy": self.energy.energy,
            "trustmap": dict(self.memory.trustmap)
        }
