// File: engine/recursion.ts

import { GalaxyUniverse } from "./galaxy";
import { EnergyPulse } from "./energy";
import { MemorySystem } from "./memory";

export class RecursionEngine {
  universe: GalaxyUniverse;
  energy: EnergyPulse;
  memory: MemorySystem;
  cycle_count: number;

  constructor(
    universe: GalaxyUniverse,
    energy: EnergyPulse,
    memory: MemorySystem,
    start_cycle = 0
  ) {
    this.universe = universe;
    this.energy = energy;
    this.memory = memory;
    this.cycle_count = start_cycle;
  }

  run_cycle() {
    const orbit = this.universe.random_orbit();
    const planet = this.universe.random_planet(orbit);
    const moon = this.universe.random_moon(planet);
    const key = `${orbit}/${planet}/${moon}`;
    const cost = Math.floor(Math.random() * 10) + 1;

    if (this.energy.consume(cost)) {
      this.memory.trust(key);
    } else {
      this.memory.regret(key, "Insufficient energy");
    }

    this.memory.decay();
    this.cycle_count += 1;

    return {
      cycle: this.cycle_count,
      orbit,
      planet,
      moon,
      cost,
      remaining_energy: this.energy.remaining,
      trustmap: { ...this.memory.trustmap },
    };
  }
}
