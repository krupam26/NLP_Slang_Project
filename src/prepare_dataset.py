"""Generate a tiny, deterministic synthetic parallel corpus (no downloads)."""
import csv
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "data" / "synthetic"
SEED = 42

# Compact hand-authored patterns provide diverse contexts without storing a large corpus.
PAIRS = [
    ("hey {person}, what r u doing{punct}", "Hello {person}, what are you doing{punct}"),
    ("{person}, idk if this is gonna work{punct}", "{person}, I do not know if this is going to work{punct}"),
    ("tbh, i wanna help u with {thing}{punct}", "To be honest, I want to help you with {thing}{punct}"),
    ("btw, pls send it rn{punct}", "By the way, please send it right now{punct}"),
    ("cuz u gotta leave soon{punct}", "Because you have to leave soon{punct}"),
    ("imo, this is gr8{punct}", "In my opinion, this is great{punct}"),
    ("thx bro, that was awesome{punct}", "Thank you, friend, that was awesome{punct}"),
    ("omg, i cant believe it{punct}", "Oh my goodness, I cannot believe it{punct}"),
    ("brb, gonna grab my {thing}{punct}", "Be right back, I am going to get my {thing}{punct}"),
    ("ur idea is cool lol{punct}", "Your idea is cool{punct}"),
    ("pls let me know asap{punct}", "Please let me know as soon as possible{punct}"),
    ("idk where u are rn{punct}", "I do not know where you are right now{punct}"),
    ("we're gonna meet later{punct}", "We are going to meet later{punct}"),
    ("can u call me asap{punct}", "Can you call me as soon as possible{punct}"),
    ("that was so funny lmao{punct}", "That was very funny{punct}"),
    ("i gotta finish this asap{punct}", "I have to finish this as soon as possible{punct}"),
    ("wanna grab coffee later{punct}", "Would you like to get coffee later{punct}"),
    ("bc it was raining, we stayed home{punct}", "Because it was raining, we stayed home{punct}"),
    ("thx, i'll get back to u soon{punct}", "Thank you, I will get back to you soon{punct}"),
    ("yo, that sounds sus{punct}", "That sounds suspicious{punct}"),
]
PEOPLE = ["Alex", "Sam", "Jordan", "Taylor", "my friend"]
THINGS = ["project", "homework", "message", "laptop", "meeting"]
PUNCT = [".", "!", "?"]


def build_rows():
    rows = {}
    for template, target in PAIRS:
        for person in PEOPLE:
            for thing in THINGS:
                for punct in PUNCT:
                    values = {"person": person, "thing": thing, "punct": punct}
                    pair = {"informal_text": template.format(**values), "formal_text": target.format(**values)}
                    rows[pair["informal_text"].lower()] = pair
    # Stable shuffle prevents neighboring templates dominating each split.
    unique_rows = list(rows.values())
    random.Random(SEED).shuffle(unique_rows)
    return unique_rows


def main():
    rows = build_rows()
    n = len(rows)
    splits = {"train": rows[: int(n * .8)], "validation": rows[int(n * .8): int(n * .9)], "test": rows[int(n * .9):]}
    OUTPUT.mkdir(parents=True, exist_ok=True)
    for split, examples in splits.items():
        with (OUTPUT / f"{split}.csv").open("w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["informal_text", "formal_text"])
            writer.writeheader()
            writer.writerows(examples)
    print(f"Wrote {n} synthetic examples (train/validation/test: {len(splits['train'])}/{len(splits['validation'])}/{len(splits['test'])}) to {OUTPUT}")


if __name__ == "__main__":
    main()
