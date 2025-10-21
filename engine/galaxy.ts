// File: engine/galaxy.ts

export class GalaxyUniverse {
  orbits: Record<string, string>;
  planets: Record<string, string[]>;

  constructor(genesis: { orbits: Record<string, string>; planets: Record<string, string[]> }) {
    this.orbits = genesis.orbits;
    this.planets = genesis.planets;
  }

  random_orbit(): string {
    const keys = Object.values(this.orbits);
    return keys[Math.floor(Math.random() * keys.length)];
  }

  random_planet(orbit: string): string {
    const matching = Object.entries(this.orbits)
      .filter(([_, o]) => o === orbit)
      .map(([p]) => p);
    return matching[Math.floor(Math.random() * matching.length)];
  }

  random_moon(planet: string): string {
    const moons = this.planets[planet] || [];
    if (moons.length === 0) return "none";
    return moons[Math.floor(Math.random() * moons.length)];
  }
}
