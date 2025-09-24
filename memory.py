class MemorySystem:
    def __init__(self):
        self.trustmap = {}
        self.regret_lattice = []

    def reinforce(self, node, value):
        self.trustmap[node] = self.trustmap.get(node, 0) + value
        print(f"- Trustmap Updated: {node} +{value}")

    def regret(self, node, reason):
        self.regret_lattice.append((node, reason))
        print(f"- Regret Lattice: {node} → {reason}")
