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

st.title("\U0001F30C Primus-Universum")
st.write("A self-evolving cognitive universe. Run recursive pulse cycles below:")

# Input cycles
num_cycles = st.number_input("Number of pulse cycles", min_value=1, max_value=50, value=1)

if st.button("Run Cycles"):
    # Initialize systems
    universe = GalaxyUniverse(genesis)
    energy = EnergyPulse()
    memory = MemorySystem()
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

    # --- Show Cycle Log ---
    st.subheader("📜 Cycle Log")
    for entry in cycle_log:
        st.write(
            f"Cycle {entry.get('cycle', '?')}: "
            f"{entry.get('orbit', '?')} → {entry.get('planet', '?')} → {entry.get('moon', '?')} "
            f"(Cost {entry.get('cost', '?')}, Remaining {entry.get('remaining_energy', '?')})"
        )

    # --- Show Trustmap ---
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

    # --- Show Energy ---
    st.subheader("⚡ Energy Usage per Cycle")
    if energy_history:
        fig2, ax2 = plt.subplots()
        ax2.plot(range(1, len(energy_history) + 1), energy_history, marker="o")
        ax2.set_title("Energy Remaining After Each Cycle")
        ax2.set_xlabel("Cycle")
        ax2.set_ylabel("Energy Level")
        st.pyplot(fig2)

    # Raw debug
    with st.expander("🔍 Debug: Raw Trustmap History"):
        st.json(trustmap_history)
