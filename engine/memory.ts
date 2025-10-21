// File: engine/memory.ts

export class MemorySystem {
  trustmap: Record<string, number> = {};
  regret_lattice: [string, string][] = [];

  trust(key: string, amount = 1) {
    if (!this.trustmap[key]) this.trustmap[key] = 0;
    this.trustmap[key] += amount;
  }

  regret(key: string, reason: string) {
    this.regret_lattice.push([key, reason]);
  }

  decay(factor = 0.95) {
    for (const key in this.trustmap) {
      this.trustmap[key] *= factor;
      if (this.trustmap[key] < 0.1) delete this.trustmap[key];
    }
  }
}
