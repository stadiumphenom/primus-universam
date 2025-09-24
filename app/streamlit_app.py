import streamlit as st
import json
from engine.galaxy import GalaxyUniverse
from engine.energy import EnergyPulse
from engine.recursion import RecursionEngine
from engine.memory import MemorySystem

# Load Genesis Map
with open("data/genesis_map.json", "r", encoding="utf-8") as f:
    genesis = json.load(f)

st.title("🌌 Primus-Universum")
st.write("Run pulse cycles through the cognitive universe.")

if st.button("Run Pulse Cycle"):
    universe = GalaxyUniverse(genesis)
    energy = EnergyPulse()
    memory = MemorySystem()
    recursion = RecursionEngine(universe, energy, memory)
    recursion.run_cycle()
