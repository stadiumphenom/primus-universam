// File: pages/api/state.ts
import { NextApiRequest, NextApiResponse } from "next";
import { promises as fs } from "fs";
import path from "path";

const STATE_PATH = path.join(process.cwd(), "data", "state.json");

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  switch (req.method) {
    case "GET": {
      try {
        const raw = await fs.readFile(STATE_PATH, "utf-8");
        const parsed = JSON.parse(raw);
        res.status(200).json(parsed);
      } catch {
        res.status(200).json({ energy: 100, trustmap: {}, regret_lattice: [], cycle_count: 0 });
      }
      break;
    }
    case "POST": {
      try {
        const { energy, trustmap, regret_lattice, cycle_count } = req.body;
        const data = JSON.stringify({ energy, trustmap, regret_lattice, cycle_count }, null, 2);
        await fs.writeFile(STATE_PATH, data, "utf-8");
        res.status(200).json({ ok: true });
      } catch (err) {
        res.status(500).json({ error: "Failed to save state", details: err });
      }
      break;
    }
    case "DELETE": {
      try {
        await fs.unlink(STATE_PATH);
        res.status(200).json({ ok: true });
      } catch {
        res.status(200).json({ ok: false }); // file may not exist
      }
      break;
    }
    default:
      res.setHeader("Allow", ["GET", "POST", "DELETE"]);
      res.status(405).end(`Method ${req.method} Not Allowed`);
  }
}

export const config = {
  api: {
    bodyParser: true,
    externalResolver: true,
  },
};

