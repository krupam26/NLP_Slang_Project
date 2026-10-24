"""Compare the rule baseline and learned phrase table on held-out examples."""
import csv
from src.converter import slang_to_formal
from src.phrase_model import predict
from pathlib import Path

TEST = Path(__file__).resolve().parents[1] / "data" / "synthetic" / "test.csv"

def main():
    rows = list(csv.DictReader(TEST.open(encoding="utf-8", newline="")))
    for name, fn in (("rule baseline", slang_to_formal), ("phrase model", predict)):
        exact = sum(fn(r["informal_text"]) == r["formal_text"] for r in rows)
        print(f"{name}: exact match {exact}/{len(rows)} ({100*exact/len(rows):.1f}%)")
    print("\nSample errors (phrase model):")
    shown = 0
    for row in rows:
        got = predict(row["informal_text"])
        if got != row["formal_text"]:
            print(f"IN : {row['informal_text']}\nREF: {row['formal_text']}\nOUT: {got}\n")
            shown += 1
            if shown >= 5:
                break

if __name__ == "__main__":
    main()
