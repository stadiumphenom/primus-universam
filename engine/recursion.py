import random
import json
import os

class RecursionEngine:
    """
    The recursive driver that runs pulse cycles.
    It connects GalaxyUniverse, EnergyPulse, and MemorySystem.
    """

    def __init__(self, universe, energy, memory):
        self.universe = universe
        self.energy = energy
        self.memory = memory
        self.cycle_count = 0
        self.state_path = "data/state.json"

    def run_cycle(self):
        """
        Run a single recursive pulse cycle:
        - Selects a weighted orbit/planet/moon based on trustmap
        - Consumes energy
        - Updates trust or regret
        - Persists state
        """
        self.cycle_count += 1

        # Use trustmap to bias selection
        trustmap = self.memory.trustmap
        orbit, planet, moon = self.universe.random_path(trustmap)

        # Energy cost
        cost = self.energy.pulse()

        # Build unique key
        key = f"{orbit}:{planet}:{moon}"

        # Trust or regret based on cost
        if cost > 7:
            self.memory.regret(key, f"High cost: {cost}")
        else:
            self.memory.update_trust(key, cost)

        # Save updated state
        self.save_state()

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

    def save_state(self):
        state = {
            "trustmap": self.memory.trustmap,
            "regret_lattice": self.memory.regret_lattice,
            "energy": self.energy.energy
        }
        os.makedirs(os.path.dirname(self.state_path), exist_ok=True)
        with open(self.state_path, "w") as f:
            json.dump(state, f, indent=2)
