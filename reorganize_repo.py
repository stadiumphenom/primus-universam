"""
Primus-Universum Repo Reorganizer
---------------------------------
Run this script ONCE from the root of your repo (primus-universum/).
It will:
- Create missing folders (engine/, app/, tests/, docs/, visuals/, data/).
- Move files into correct places.
- Create __init__.py, requirements.txt, .gitignore, and doc placeholders if missing.
"""

import os
import shutil

# Define target structure
folders = ["engine", "app", "tests", "docs", "visuals", "data"]
engine_files = ["core.py", "galaxy.py", "energy.py", "recursion.py", "memory.py", "glyphs.py"]
data_files = ["genesis_map.json"]

def ensure_folder(path):
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"[+] Created folder: {path}")

def move_file(filename, target_folder):
    if os.path.exists(filename):
        dest = os.path.join(target_folder, os.path.basename(filename))
        shutil.move(filename, dest)
        print(f"[>] Moved {filename} -> {dest}")

def ensure_file(path, content=""):
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"[+] Created file: {path}")

def main():
    root = os.getcwd()
    print(f"Reorganizing repo at: {root}")

    # Ensure core folders exist
    for folder in folders:
        ensure_folder(folder)

    # Move engine files
    for f in engine_files:
        move_file(f, "engine")

    # Move data files
    for f in data_files:
        move_file(f, "data")

    # Create __init__.py in packages
    for pkg in ["engine", "app", "tests"]:
        ensure_file(os.path.join(pkg, "__init__.py"))

    # Create requirements.txt
    ensure_file("requirements.txt", "streamlit\nmatplotlib\n")

    # Create .gitignore
    ensure_file(".gitignore", "__pycache__/\n*.pyc\n.env\n")

    # Create docs placeholders
    ensure_file("docs/MANIFESTO.md", "# Primus-Universum Manifesto\n")
    ensure_file("docs/ARCHITECTURE.md", "# Architecture Notes\n")
    ensure_file("docs/ROADMAP.md", "# Roadmap\n")

    # Create app/streamlit_app.py placeholder
    ensure_file("app/streamlit_app.py",
        "import streamlit as st\n\nst.title('🌌 Primus-Universum')\nst.write('Pulse cycles coming soon...')\n"
    )

    # Create tests/test_engine.py placeholder
    ensure_file("tests/test_engine.py", "def test_dummy():\n    assert True\n")

    print("✅ Repo reorganization complete!")

if __name__ == "__main__":
    main()
