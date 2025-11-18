import pickle
from pathlib import Path

PKL_PATH = Path("storage/syllabus.pkl")
PKL_PATH.parent.mkdir(parents=True, exist_ok=True)

def load_all_syllabi():
    if not PKL_PATH.exists():
        return []
    try:
        with open(PKL_PATH, "rb") as f:
            return pickle.load(f)
    except:
        return []

def save_syllabus(entry: dict):
    syllabi = load_all_syllabi()
    syllabi.append(entry)
    with open(PKL_PATH, "wb") as f:
        pickle.dump(syllabi, f)
