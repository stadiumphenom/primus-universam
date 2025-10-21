// File: engine/energy.ts

export class EnergyPulse {
  energy: number;

  constructor(starting_energy = 100) {
    this.energy = starting_energy;
  }

  consume(cost: number): boolean {
    if (cost <= this.energy) {
      this.energy -= cost;
      return true;
    }
    return false;
  }

  recharge(amount: number): void {
    this.energy += amount;
  }

  get remaining(): number {
    return this.energy;
  }
}
