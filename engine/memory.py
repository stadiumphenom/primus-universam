class MemorySystem:
    def __init__(self):
        self.trustmap = {}
        self.regret_lattice = []

    def update_trust(self, key, value):
        self.trustmap[key] = self.trustmap.get(key, 0) + value
        print(f"- Trustmap Updated: {key} +{value}")

    def regret(self, key, reason):  # <-- renamed from log_regret
        self.regret_lattice.append((key, reason))
        print(f"- Regret Lattice: {key} → {reason}")
