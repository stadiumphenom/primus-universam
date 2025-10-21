// File: pages/api/cycle.ts

import { NextApiRequest, NextApiResponse } from "next";
import { promises as fs } from "fs";
import path from "path";

const STATE_PATH = path.join(process.cwd(), "data", "state.json");

function runLogicCycle(state: any): any {
  const logEntry = {
    cycle: (state.cycle_count ?? 0) + 1,
    orbit: "Galactic Core",
    planet: "Trust",
    moon: "Reflection",
    cost: Math.floor(Math.random() * 10) + 1,
    remaining_energy: Math.max(0, state.energy - (Math.floor(Math.random() * 10) + 1)),
  };

  const updatedTrustmap = { ...state.trustmap };
  const key = `entity-${logEntry.cycle}`;
  updatedTrustmap[key] = (updatedTrustmap[key] || 0) + 1;

  const updatedLattice = [...(state.regret_lattice || [])];
  if (Math.random() < 0.2) {
    updatedLattice.push([key, "Inaction"]);
  }

  return {
    updatedState: {
      energy: logEntry.remaining_energy,
      trustmap: updatedTrustmap,
      regret_lattice: updatedLattice,
      cycle_count: logEntry.cycle,
    },
    logEntry,
  };
}

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== "POST") {
    res.setHeader("Allow", ["POST"]);
    return res.status(405).end(`Method ${req.method} Not Allowed`);
  }

  const { count = 1 } = req.body;

  try {
    const raw = await fs.readFile(STATE_PATH, "utf-8");
    let state = JSON.parse(raw);
    const log = [];

    for (let i = 0; i < count; i++) {
      const { updatedState, logEntry } = runLogicCycle(state);
      state = updatedState;
      log.push(logEntry);
    }

    await fs.writeFile(STATE_PATH, JSON.stringify(state, null, 2), "utf-8");

    res.status(200).json({ ok: true, log });
  } catch (err) {
    console.error("Failed to process cycles:", err);
    res.status(500).json({ error: "Failed to process cycles", details: err });
  }
}
