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

# Load Genesis Map
with open("data/genesis_map.json", "r", encoding="utf-8") as f:
    genesis = json.load(f)

# File path for persistent state
state_path = "data/state.json"

# Load saved state if available
saved_state = {}
if os.path.exists(state_path):
    with open(state_path, "r", encoding="utf-8") as f:
        saved_state = json.load(f)

# Initialize systems
universe = GalaxyUniverse(genesis)
energy = EnergyPulse()
memory = MemorySystem()

# Restore saved values
energy.energy = saved_state.get("energy", 100)
memory.trustmap = saved_state.get("trustmap", {})
memory.regret_lattice = saved_state.get("regret_lattice", [])

# Streamlit UI
st.title("🌌 Primus-Universum")
st.write("A self-evolving cognitive universe. Run recursive pulse cycles below:")

col1, col2 = st.columns([3, 1])
with col1:
    num_cycles = st.number_input("Number of pulse cycles", min_value=1, max_value=50, value=1)
with col2:
    if st.button("🔄 Reset Universe"):
        energy.energy = 100
        memory.trustmap = {}
        memory.regret_lattice = []
        if os.path.exists(state_path):
            os.remove(state_path)
        st.warning("Universe state has been reset.")
        st.stop()

if st.button("Run Cycles"):
    recursion = RecursionEngine(universe, energy, memory)

    trustmap_history = []
    energy_history = []
    cycle_log = []

    for i in range(num_cycles):
        result = recursion.run_cycle()
        trustmap_history.append(result.get("trustmap", {}))
        energy_history.append(result.get("remaining_energy", 0))
        cycle_log.append(result)

    st.success(f"✅ Completed {num_cycles} pulse cycle(s)!")

    # Save new state
    with open(state_path, "w", encoding="utf-8") as f:
        json.dump({
            "energy": energy.energy,
            "trustmap": memory.trustmap,
            "regret_lattice": memory.regret_lattice
        }, f, indent=2)

    # --- Cycle Log ---
    st.subheader("📜 Cycle Log")
    for entry in cycle_log:
        st.write(
            f"Cycle {entry.get('cycle', '?')}: "
            f"{entry.get('orbit', '?')} → {entry.get('planet', '?')} → {entry.get('moon', '?')} "
            f"(Cost {entry.get('cost', '?')}, Remaining {entry.get('remaining_energy', '?')})"
        )

    # --- Trustmap ---
    st.subheader("🧠 Trustmap Evolution")
    if trustmap_history and isinstance(trustmap_history[-1], dict):
        last_map = trustmap_history[-1]
        if last_map:
            labels, values = zip(*last_map.items())

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
    st.subheader("🧩 Regret Lattice")
    if memory.regret_lattice:
        for node, reason in memory.regret_lattice:
            st.write(f"🔻 {node} → {reason}")
    else:
        st.write("No regrets recorded yet.")

    # --- Raw Debug ---
    with st.expander("🔍 Debug: Raw Trustmap History"):
        st.json(trustmap_history)
