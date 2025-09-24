import json
from engine.galaxy import GalaxyUniverse
from engine.energy import EnergyPulse
from engine.recursion import RecursionEngine
from engine.memory import MemorySystem

def main():
    # Load Genesis Map
    with open("data/genesis_map.json") as f:
        genesis = json.load(f)

    print("🌌 Primus Pulse Cycle")

    # Initialize systems
    universe = GalaxyUniverse(genesis)
    energy = EnergyPulse()
    memory = MemorySystem()
    recursion = RecursionEngine(universe, energy, memory)

    # Run one pulse cycle
    recursion.run_cycle()

if __name__ == "__main__":
    main()
