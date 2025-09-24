class RecursionEngine:
    def __init__(self, universe, energy, memory):
        self.universe = universe
        self.energy = energy
        self.memory = memory

    def run_cycle(self):
        galaxy, planet, moon = self.universe.get_random_path()
        pulse = self.energy.next_pulse()

        print(f"- Activated: {galaxy} → {planet} → {moon}")
        print(f"- Energy Used: {pulse}")

        self.memory.reinforce(moon, pulse)
