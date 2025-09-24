import sys
import os

# Add repo root to Python path so "engine" can be found
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import json
import matplotlib.pyplot as plt

from engine.galaxy import GalaxyUniverse
from engine.energy import EnergyPulse
from engine.recursion import RecursionEngine
from engine.memory import MemorySystem

# Load Genesis Map
with open("data/genesis_map.json", "r", encoding="utf-8") as f:
    genesis = json.load(f)

st.title("🌌 Primus-Universum")
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

    for i in range(num_cycles):
        recursion.run_cycle()
        trustmap_history.append(memory.trustmap.copy())
        energy_history.append(energy.energy)

    st.success(f"Completed {num_cycles} pulse cycle(s)!")

    # --- Show Trustmap evolution ---
    st.subheader("🧠 Trustmap Evolution")
    if trustmap_history:
        last_map = trustmap_history[-1]
        labels, values = zip(*last_map.items())

        fig, ax = plt.subplots()
        ax.bar(labels, values)
        ax.set_title("Trustmap after final cycle")
        ax.set_ylabel("Trust Value")
        plt.xticks(rotation=45, ha="right")

        st.pyplot(fig)

    # --- Show Energy over time ---
    st.subheader("⚡ Energy Usage per Cycle")
    fig2, ax2 = plt.subplots()
    ax2.plot(range(1, len(energy_history) + 1), energy_history, marker="o")
    ax2.set_title("Energy State After Each Cycle")
    ax2.set_xlabel("Cycle")
    ax2.set_ylabel("Remaining Energy")
    st.pyplot(fig2)

    # Show raw trustmap history for debugging
    with st.expander("Show raw trustmap history"):
        st.json(trustmap_history)
