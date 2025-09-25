class MemorySystem:
    def __init__(self):
        self.trustmap = {}
        self.regret_lattice = []

    def update_trust(self, key, value):
        """Reinforce trust in a path/decision."""
        self.trustmap[key] = self.trustmap.get(key, 0) + value
        print(f"- Trustmap Updated: {key} +{value}")

    def log_regret(self, key, reason):
        """Log regret for a poor decision."""
        self.regret_lattice.append((key, reason))
        print(f"- Regret Lattice: {key} → {reason}")
