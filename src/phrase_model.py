"""Tiny supervised phrase-table model learned from the synthetic train split."""
import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "synthetic"
MODEL = ROOT / "models" / "phrase-table.json"


def train():
    pairs = {}
    with (DATA / "train.csv").open(encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            pairs[row["informal_text"].lower()] = row["formal_text"]
    MODEL.parent.mkdir(parents=True, exist_ok=True)
    MODEL.write_text(json.dumps({"type": "synthetic_phrase_table", "pairs": pairs}, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(f"Learned {len(pairs)} sentence pairs; model size {MODEL.stat().st_size} bytes: {MODEL}")


def predict(text):
    data = json.loads(MODEL.read_text(encoding="utf-8"))
    exact = data["pairs"].get(text.lower())
    if exact is not None:
        return exact
    # Fallback to the rule baseline for inputs outside the learned examples.
    from src.converter import slang_to_formal
    return slang_to_formal(text)


if __name__ == "__main__":
    train()
