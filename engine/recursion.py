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
        - Selects a biased orbit/planet/moon path
        - Consumes energy via EnergyPulse
        - Updates trustmap in memory
        - Logs regret if energy cost is high
        """
        self.cycle_count += 1

        # Pick path using trustmap bias
        orbit, planet, moon = self.universe.random_path(trustmap=self.memory.trustmap)

        # Consume energy
        cost = self.energy.pulse()

        # Generate key
        key = f"{orbit}:{planet}:{moon}"

        # Update trust
        self.memory.update_trust(key, cost)

        # Regret condition (example: cost is 9)
        if cost == 9:
            self.memory.log_regret(key, reason="High energy spike")

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
