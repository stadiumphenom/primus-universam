import sys
import os
import json
import math
import streamlit as st
import matplotlib.pyplot as plt

# Set up imports from engine
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from engine.galaxy import GalaxyUniverse
from engine.energy import EnergyPulse
from engine.recursion import RecursionEngine
from engine.memory import MemorySystem

STATE_FILE = "data/state.json"

# --- State Management ---
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

# --- Alien Mode Helpers ---
def glyph_for_key(key):
    glyphs = "⟁⟴⋖⋗⋇⋉⋊⌖⧫⧬⨀⩚⩘⩇𐊧𐊪𐊬"
    return ''.join(glyphs[ord(c) % len(glyphs)] for c in key[:4])

def intent_color(value):
    if value >= 20: return "green"
    if value >= 10: return "blue"
    if value >= 3: return "orange"
    return "red"

# --- Streamlit UI ---
st.title("🌌 Primus-Universum")
st.write("A self‑evolving cognitive universe. Glyphic mode enables alien symbology.")

alien_mode = st.checkbox("Alien Mode", value=True)
num_cycles = st.number_input("Number of pulse cycles", min_value=1, max_value=50, value=1)
if st.button("Reset Universe"):
    if os.path.exists(STATE_FILE):
        os.remove(STATE_FILE)
    st.rerun()

# --- Load Systems ---
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

# --- Execute Cycles ---
if st.button("Run Cycles"):
    trustmap_history, energy_history, cycle_log = [], [], []

    for _ in range(num_cycles):
        result = recursion.run_cycle()
        trustmap_history.append(result["trustmap"])
        energy_history.append(result["remaining_energy"])
        cycle_log.append(result)

    save_state(energy.energy, memory.trustmap, memory.regret_lattice, recursion.cycle_count)
    st.success(f"✅ Completed {num_cycles} cycle(s)")

    st.subheader("📜 Cycle Log")
    for entry in cycle_log:
        st.write(f"Cycle {entry['cycle']}: {entry['orbit']} → {entry['planet']} → {entry['moon']} (Cost {entry['cost']}, Rem {entry['remaining_energy']})")

    st.subheader("🧠 Trustmap Evolution")
    if trustmap_history:
        final_map = trustmap_history[-1]
        labels = list(final_map.keys())
        values = list(final_map.values())
        glyph_labels = [glyph_for_key(k) for k in labels]
        bar_labels = glyph_labels if alien_mode else labels
        colors = [intent_color(v) for v in values]

        fig, ax = plt.subplots()
        ax.bar(bar_labels, values, color=colors)
        ax.set_title("⟴ Final Trustmap" if alien_mode else "Trustmap after final cycle")
        ax.set_ylabel("⋖ Trust ∴" if alien_mode else "Trust Value")
        plt.xticks(rotation=45, ha="right")
        st.pyplot(fig)

    st.subheader("⚡ Energy Usage per Cycle")
    if energy_history:
        fig2, ax2 = plt.subplots()
        x_vals = list(range(1, len(energy_history)+1))
        y_vals = energy_history
        if alien_mode:
            ax2.plot(x_vals, y_vals, linestyle='-', color='cyan')
            glyphs = ["⟁", "⟠", "⧫", "⟴", "⋇", "⧊", "⫷", "⊛"]
            for i, (x, y) in enumerate(zip(x_vals, y_vals)):
                ax2.text(x, y + 1, glyphs[i % len(glyphs)], ha='center', fontsize=12, color='magenta')
            ax2.set_title("⟁ Energy Curve")
            ax2.set_xlabel("Ψ‑Cycle")
            ax2.set_ylabel("≺ Trust ∷")
        else:
            ax2.plot(x_vals, y_vals, marker="o", linestyle='-', color='blue')
            ax2.set_title("Energy Remaining After Each Cycle")
            ax2.set_xlabel("Cycle")
            ax2.set_ylabel("Energy Level")
        st.pyplot(fig2)

    st.subheader("💔 Regret Lattice")
    if memory.regret_lattice:
        for (key, reason) in memory.regret_lattice:
            label = glyph_for_key(key) if alien_mode else key
            st.write(f"{label} → {reason}")
    else:
        st.info("No regrets yet.")

    st.subheader("🪐 Universe Map (Orbits → Planets → Moons)")
    fig3, ax3 = plt.subplots(figsize=(8, 8))
    center = (0, 0)
    radii = {}
    orbit_names = list(set(universe.orbits.values()))
    num_orbits = len(orbit_names)

    for i, orbit in enumerate(orbit_names):
        radius = (i + 1) * 1.5
        radii[orbit] = radius
        num_planets = sum(1 for p, o in universe.orbits.items() if o == orbit)
        angle_step = 2 * math.pi / max(num_planets, 1)

        orbit_planets = [planet for planet, o in universe.orbits.items() if o == orbit]
    for j, planet in enumerate(orbit_planets):
            angle = j * angle_step
            px = center[0] + radius * math.cos(angle)
            py = center[1] + radius * math.sin(angle)
            planet_label = glyph_for_key(planet) if alien_mode else planet
            ax3.plot(px, py, 'o', color='gold')
            ax3.text(px, py, planet_label, fontsize=8, ha='center')

            moons = universe.planets.get(planet, [])
            moon_angle_step = 2 * math.pi / max(len(moons), 1)
            for k, moon in enumerate(moons):
                m_angle = angle + (k + 1) * moon_angle_step / 3
                mx = px + 0.3 * math.cos(m_angle)
                my = py + 0.3 * math.sin(m_angle)
                moon_label = glyph_for_key(moon) if alien_mode else moon
                ax3.plot(mx, my, 'o', color='gray', markersize=4)
                ax3.text(mx, my, moon_label, fontsize=6, ha='center')

        orbit_circle = plt.Circle(center, radius, color='white', fill=False, linestyle='dotted')
        ax3.add_patch(orbit_circle)

    ax3.set_aspect('equal')
    ax3.axis('off')
    st.pyplot(fig3)

    with st.expander("🔍 Debug: Raw Trustmap"):
        st.json(memory.trustmap)
