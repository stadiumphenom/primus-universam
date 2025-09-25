import sys
import os
import json
import streamlit as st
import matplotlib.pyplot as plt
import networkx as nx

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
    return {
        "energy": 100,
        "trustmap": {},
        "regret_lattice": [],
        "cycle_count": 0
    }

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
st.write("A self‑evolving cognitive universe. Glyphic mode: alien symbology.")

alien_mode = st.checkbox("Alien Mode", value=True)
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

    save_state(energy.energy, memory.trustmap, memory.regret_lattice, recursion.cycle_count)

    st.success(f"✅ Completed {num_cycles} cycles")

    # --- Cycle Log ---
    st.subheader("📜 Cycle Log")
    for entry in cycle_log:
        st.write(
            f"Cycle {entry['cycle']}: {entry['orbit']} → {entry['planet']} → {entry['moon']} "
            f"(Cost {entry['cost']}, Rem {entry['remaining_energy']})"
        )

    # --- Trustmap Chart ---
    st.subheader("🧠 Trustmap Evolution")
    if trustmap_history and isinstance(trustmap_history[-1], dict):
        final_map = trustmap_history[-1]
        if final_map:
            labels = list(final_map.keys())
            values = [final_map[k] for k in labels]
            glyph_labels = [glyph_for_key(k) for k in labels]
            bar_labels = glyph_labels if alien_mode else labels
            colors = [intent_color(v) for v in values]

            fig, ax = plt.subplots()
            ax.bar(bar_labels, values, color=colors)
            ax.set_title("⟴ Final Trustmap" if alien_mode else "Trustmap after final cycle")
            ax.set_ylabel("⋖ Trust ∴" if alien_mode else "Trust Value")
            plt.xticks(rotation=45, ha="right")
            st.pyplot(fig)

    # --- Energy Chart ---
st.subheader("⚡ Energy Usage per Cycle")
if energy_history:
    fig2, ax2 = plt.subplots()

    x_vals = list(range(1, len(energy_history) + 1))
    y_vals = energy_history

    if alien_mode:
        # Plot basic line without markers
        ax2.plot(x_vals, y_vals, linestyle='-', color='cyan')

        # Add alien glyphs as annotations
        glyphs = ["⟁", "⟠", "⧫", "⟴", "⟁", "⧊", "⫷", "⊛", "⟁", "⋇"]  # looped as needed
        for i, (x, y) in enumerate(zip(x_vals, y_vals)):
            glyph = glyphs[i % len(glyphs)]
            ax2.text(x, y + 1, glyph, ha='center', fontsize=12, color='magenta')
        
        ax2.set_title("⟁ Energy Curve")
        ax2.set_xlabel("Ψ-Cycle")
        ax2.set_ylabel("≺ Trust ∷")
    else:
        # Normal readable mode
        ax2.plot(x_vals, y_vals, marker="o", linestyle='-', color='blue')
        ax2.set_title("Energy Remaining After Each Cycle")
        ax2.set_xlabel("Cycle")
        ax2.set_ylabel("Energy Level")

    st.pyplot(fig2)


    # --- Regret Lattice Display ---
    st.subheader("💔 Regret Lattice")
    if memory.regret_lattice:
        for (n, r) in memory.regret_lattice:
            label = glyph_for_key(n) if alien_mode else n
            st.write(f"{label} → {r}")
    else:
        st.info("No regrets yet.")

    # --- Universe Graph (network) ---
    st.subheader("🪐 Universe Map (orbits → planets → moons)")
    G = nx.DiGraph()
    # Build graph edges
    for planet, moons in universe.moons.items():
        orbit = universe.orbits.get(planet, "?")
        G.add_edge(orbit, planet)
        for moon in moons:
            G.add_edge(planet, moon)
    # Node labels: glyph or readable
    node_labels = {node: (glyph_for_key(node) if alien_mode else node) for node in G.nodes()}
    pos = nx.spring_layout(G, seed=42)
    fig3, ax3 = plt.subplots(figsize=(6, 6))
    nx.draw(G, pos, labels=node_labels, with_labels=True, node_size=800, node_color="lightblue", font_size=10, font_family="monospace")
    st.pyplot(fig3)

    # --- Debug expand ---
    with st.expander("🔍 Debug: Trustmap"):
        st.json(memory.trustmap)
