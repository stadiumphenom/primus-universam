class MemorySystem:
    def __init__(self):
        self.trustmap = {}
        self.regret_lattice = []

    def update_trust(self, key, value):
        try:
            self.trustmap[key] = self.trustmap.get(key, 0) + value
            print(f"- Trustmap Updated: {key} +{value}")
        except Exception as e:
            print("⚠️ Error updating trust:", e)

    def log_regret(self, key, reason):
        try:
            self.regret_lattice.append((key, reason))
            print(f"- Regret Lattice: {key} → {reason}")
        except Exception as e:
            print("⚠️ Error logging regret:", e)
