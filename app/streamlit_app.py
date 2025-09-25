import sys
import os
import json
import streamlit as st
import matplotlib.pyplot as plt

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from engine.galaxy import GalaxyUniverse
from engine.energy import EnergyPulse
from engine.recursion import RecursionEngine
from engine.memory import MemorySystem

STATE_FILE = "data/state.json"

def load_state():
    try:
        if os.path.exists(STATE_FILE):
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception as e:
        print("⚠️ load_state error:", e)
    return {"energy": 100, "trustmap": {}, "regret_lattice": [], "cycle_count": 0}

def save_state(energy, trustmap, regret_lattice, cycle_count):
    try:
        with open(STATE_FILE, "w", encoding="utf-8") as f:
            json.dump({
                "energy": energy,
                "trustmap": trustmap,
                "regret_lattice": regret_lattice,
                "cycle_count": cycle_count
            }, f, indent=2)
    except Exception as e:
        print("⚠️ save_state error:", e)

st.title("🌌 Primus-Universum")
st.write("A self-evolving cognitive universe. Run recursive pulse cycles below:")

num_cycles = st.number_input("Number of pulse cycles", min_value=1, max_value=50, value=1)
if st.button("Reset Universe"):
    if os.path.exists(STATE_FILE):
        os.remove(STATE_FILE)
    st.rerun()

state = load_state()
energy = EnergyPulse(starting_energy=state.get("energy", 100))
memory = MemorySystem()
memory.trustmap = state.get("trustmap", {})
memory.regret_lattice = state.get("regret_lattice", [])
cycle_offset = state.get("cycle_count", 0)

with open("data/genesis_map.json", "r", encoding="utf-8") as f:
    genesis = json.load(f)
universe = GalaxyUniverse(genesis)
recursion = RecursionEngine(universe, energy, memory, start_cycle=cycle_offset)

if st.button("Run Cycles"):
    trustmap_history = []
    energy_history = []
    cycle_log = []

    for _ in range(num_cycles):
        result = recursion.run_cycle()
        trustmap_history.append(result.get("trustmap", {}))
        energy_history.append(result.get("remaining_energy", 0))
        cycle_log.append(result)

    save_state(
        energy.energy,
        memory.trustmap,
        memory.regret_lattice,
        recursion.cycle_count
    )

    st.success(f"✅ Completed {num_cycles} pulse cycle(s)")

    st.subheader("📜 Cycle Log")
    for entry in cycle_log:
        st.write(f"Cycle {entry['cycle']}: {entry['orbit']} → {entry['planet']} → {entry['moon']} (Cost {entry['cost']}, Rem {entry['remaining_energy']})")

    st.subheader("🧠 Trustmap Evolution")
    if trustmap_history and isinstance(trustmap_history[-1], dict):
        last_map = trustmap_history[-1]
        if last_map:
            labels, values = zip(*last_map.items())
            fig, ax = plt.subplots()
            ax.bar(labels, values)
            ax.set_ylabel("Trust Value")
            plt.xticks(rotation=45, ha="right")
            st.pyplot(fig)

    st.subheader("⚡ Energy Usage per Cycle")
    if energy_history:
        fig2, ax2 = plt.subplots()
        ax2.plot(range(1, len(energy_history) + 1), energy_history, marker="o")
        ax2.set_xlabel("Cycle")
        ax2.set_ylabel("Energy")
        st.pyplot(fig2)

    st.subheader("💔 Regret Lattice")
    if memory.regret_lattice:
        for (n, r) in memory.regret_lattice:
            st.write(f"{n} → {r}")
    else:
        st.write("No regrets yet.")

    with st.expander("🔍 Debug: Trustmap"):
        st.json(memory.trustmap)
