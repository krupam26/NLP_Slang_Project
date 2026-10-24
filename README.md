# Compact Slang ↔ Formal NLP Project

## Problem and objectives

Informal messages contain abbreviations, slang, and casual phrasing that can be hard to use in formal communication. This project detects likely slang and converts text in either direction. The goal is a transparent, offline-first educational prototype with a tiny synthetic dataset and no downloaded language model.

## Requirements and architecture

- Accept non-empty text and a direction (slang → formal or formal → slang).
- Detect a rough style label, preserve punctuation where possible, and show converted output.
- Provide a deterministic rule-based baseline and a small supervised phrase-table comparison.
- Keep source, synthetic CSV splits, and the optional JSON model local; no network or telemetry is needed.

Flow: Streamlit UI → style detector/converter → either reversible phrase dictionary or learned exact-pair table with rule fallback. Dataset tooling creates synthetic pairs → fixed-seed split → phrase table fit on train only → held-out evaluation.

## Dataset

The checked-in bootstrap corpus contains 18 hand-authored synthetic pairs across train/validation/test so the app and evaluation work immediately. `src/prepare_dataset.py` can regenerate and expand it to a few hundred unique templated pairs, writing an 80/10/10 split to `data/synthetic/{train,validation,test}.csv`. The generator is deterministic (seed 42), and each row has `informal_text,formal_text`. Examples are synthetic and intentionally narrow; they do not represent natural language diversity. Regenerate with:

```powershell
python -m src.prepare_dataset
```

## Baseline and compact ML experiment

The baseline uses a hand-maintained slang dictionary, whole-word substitutions, and a heuristic style detector (`src/converter.py`, `src/detector.py`). The ML experiment memorizes exact supervised sentence pairs from the train split in a compact JSON phrase table and falls back to the baseline for unseen input. This demonstrates a train/validation/test workflow without heavyweight frameworks, but is not a general-purpose neural translation model. Validation is reserved for tuning/extensions; test is held out for reporting.

```powershell
python -m src.prepare_dataset
python -m src.phrase_model
python -m src.evaluate
streamlit run app/streamlit_app.py
```

Evaluation reports held-out exact-match accuracy for both approaches. Inspect mismatches for dropped meaning, awkward expansions, and unseen slang; extend the hand-authored templates or dictionary, then regenerate the splits. A small test set makes metrics illustrative rather than statistically conclusive.

## Folder structure

```text
app/                 Streamlit UI
data/synthetic/      Generated train, validation, and test CSVs
models/               Optional tiny phrase-table JSON
src/                  Dataset, preprocessing, baseline, model, evaluation
tests/                Unit tests
```

## Storage policy

There are no large model downloads, online datasets, checkpoints, or Arrow caches in the intended workflow. Generated CSVs and the model are reproducible and may be deleted and regenerated. Keep virtual environments outside version control; install only Streamlit if needed.
