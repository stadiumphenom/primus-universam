import sys
import os
import json
import streamlit as st
import matplotlib.pyplot as plt

# Add repo root to path for engine imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from engine.galaxy import GalaxyUniverse
from engine.energy import EnergyPulse
from engine.recursion import RecursionEngine
from engine.memory import MemorySystem

# --- Constants ---
STATE_FILE = "data/state.json"

# --- Helper: Load state ---
def load_state():
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            pass
    return {
        "energy": 100,
        "trustmap": {},
        "regret_lattice": [],
        "cycle_count": 0
    }

# --- Helper: Save state ---
def save_state(energy, trustmap, regret_lattice, cycle_count):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump({
            "energy": energy,
            "trustmap": trustmap,
            "regret_lattice": regret_lattice,
            "cycle_count": cycle_count
        }, f, indent=2)

# --- UI ---
st.title("🌌 Primus-Universum")
st.write("A self-evolving cognitive universe. Run recursive pulse cycles below:")

# --- Controls ---
num_cycles = st.number_input("Number of pulse cycles", min_value=1, max_value=50, value=1)
if st.button("Reset Universe"):
    if os.path.exists(STATE_FILE):
        os.remove(STATE_FILE)
    st.experimental_rerun()

# --- Load state ---
state = load_state()
energy = EnergyPulse(starting_energy=state["energy"])
memory = MemorySystem()
memory.trustmap = state["trustmap"]
memory.regret_lattice = state["regret_lattice"]
cycle_offset = state["cycle_count"]

# --- Load genesis map ---
with open("data/genesis_map.json", "r", encoding="utf-8") as f:
    genesis = json.load(f)
universe = GalaxyUniverse(genesis)
recursion = RecursionEngine(universe, energy, memory, start_cycle=cycle_offset)

# --- Run Cycles ---
if st.button("Run Cycles"):
    trustmap_history = []
    energy_history = []
    cycle_log = []

    for _ in range(num_cycles):
        result = recursion.run_cycle()
        trustmap_history.append(result["trustmap"])
        energy_history.append(result["remaining_energy"])
        cycle_log.append(result)

    # Save updated state
    save_state(
        energy.energy,
        memory.trustmap,
        memory.regret_lattice,
        recursion.cycle_count
    )

    st.success(f"✅ Completed {num_cycles} pulse cycle(s)")

    # --- Cycle Log ---
    st.subheader("📜 Cycle Log")
    for entry in cycle_log:
        st.write(
            f"Cycle {entry['cycle']}: "
            f"{entry['orbit']} → {entry['planet']} → {entry['moon']} "
            f"(Cost {entry['cost']}, Remaining {entry['remaining_energy']})"
        )

    # --- Trustmap Chart ---
    st.subheader("🧠 Trustmap Evolution")
    if trustmap_history and isinstance(trustmap_history[-1], dict):
        final_map = trustmap_history[-1]
        if final_map:
            labels, values = zip(*final_map.items())
            fig, ax = plt.subplots()
            ax.bar(labels, values)
            ax.set_title("Trustmap after final cycle")
            ax.set_ylabel("Trust Value")
            plt.xticks(rotation=45, ha="right")
            st.pyplot(fig)

    # --- Energy Chart ---
    st.subheader("⚡ Energy Usage per Cycle")
    if energy_history:
        fig2, ax2 = plt.subplots()
        ax2.plot(range(1, len(energy_history) + 1), energy_history, marker="o")
        ax2.set_title("Energy Remaining After Each Cycle")
        ax2.set_xlabel("Cycle")
        ax2.set_ylabel("Energy Level")
        st.pyplot(fig2)

    # --- Regret Lattice ---
    st.subheader("💔 Regret Lattice")
    if memory.regret_lattice:
        for regret in memory.regret_lattice:
            st.write(f"{regret[0]} → {regret[1]}")
    else:
        st.info("No regrets yet. The universe is young.")

    # --- Debug ---
    with st.expander("🔍 Debug: Raw Trustmap"):
        st.json(memory.trustmap)
