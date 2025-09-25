import sys
import os
import json
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from engine.galaxy import GalaxyUniverse
from engine.energy import EnergyPulse
from engine.recursion import RecursionEngine
from engine.memory import MemorySystem

STATE_FILE = "data/state.json"

def load_state():
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            pass
    return {"energy": 100, "trustmap": {}, "regret_lattice": [], "cycle_count": 0}

def save_state(energy, trustmap, regret_lattice, cycle_count):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump({
            "energy": energy,
            "trustmap": trustmap,
            "regret_lattice": regret_lattice,
            "cycle_count": cycle_count
        }, f, indent=2)

def glyph_for_key(key):
    glyphs = "⟁⟴⋖⋗⋇⋉⋊⌖⧫⧬⨀⩚⩘⩇𐊧𐊪𐊬"
    return ''.join(glyphs[ord(c) % len(glyphs)] for c in key[:4])

def intent_color(value):
    if value >= 20:
        return "green"
    elif value >= 10:
        return "blue"
    elif value >= 3:
        return "orange"
    return "red"

st.title("🌌 Primus-Universum")
st.write("A self-evolving cognitive universe. Run recursive pulse cycles below:")

alien_mode = st.toggle("👽 Alien Mode", value=True)
num_cycles = st.number_input("Number of pulse cycles", min_value=1, max_value=50, value=1)
if st.button("Reset Universe"):
    if os.path.exists(STATE_FILE):
        os.remove(STATE_FILE)
    st.rerun()

state = load_state()
energy = EnergyPulse(starting_energy=state["energy"])
memory = MemorySystem()
memory.trustmap = state["trustmap"]
memory.regret_lattice = state["regret_lattice"]
cycle_offset = state["cycle_count"]

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
        trustmap_history.append(result["trustmap"])
        energy_history.append(result["remaining_energy"])
        cycle_log.append(result)

    save_state(energy.energy, memory.trustmap, memory.regret_lattice, recursion.cycle_count)

    st.success(f"✅ Completed {num_cycles} pulse cycle(s)")

    st.subheader("📜 Cycle Log")
    for entry in cycle_log:
        st.write(
            f"Cycle {entry['cycle']}: {entry['orbit']} → {entry['planet']} → {entry['moon']} "
            f"(Cost {entry['cost']}, Remaining {entry['remaining_energy']})"
        )

    st.subheader("🧠 Trustmap Evolution")
    if trustmap_history and isinstance(trustmap_history[-1], dict):
        final_map = trustmap_history[-1]
        if final_map:
            labels = list(final_map.keys())
            values = list(final_map.values())
            glyph_labels = [glyph_for_key(k) for k in labels]
            colors = [intent_color(v) for v in values]

            fig, ax = plt.subplots()
            ax.bar(glyph_labels if alien_mode else labels, values, color=colors)
            ax.set_title("⟴ Final Trustmap" if alien_mode else "Trustmap after final cycle")
            ax.set_ylabel("⋖ Trust ∴" if alien_mode else "Trust Value")
            plt.xticks(rotation=45, ha="right")
            st.pyplot(fig)

    st.subheader("⚡ Energy Usage per Cycle")
    if energy_history:
        fig2, ax2 = plt.subplots()
        ax2.plot(range(1, len(energy_history) + 1), energy_history, marker="o")
        ax2.set_title("Energy Remaining After Each Cycle")
        ax2.set_xlabel("Cycle")
        ax2.set_ylabel("Energy Level")
        st.pyplot(fig2)

    st.subheader("💔 Regret Lattice")
    if memory.regret_lattice:
        for regret in memory.regret_lattice:
            st.write(f"{glyph_for_key(regret[0]) if alien_mode else regret[0]} → {regret[1]}")
    else:
        st.info("No regrets yet. The universe is young.")

    with st.expander("🔍 Debug: Raw Trustmap"):
        st.json(memory.trustmap)
