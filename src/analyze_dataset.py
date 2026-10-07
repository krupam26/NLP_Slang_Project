from datasets import load_from_disk
from collections import Counter
import re


DATASET_PATH = "data/processed/informal_formal"


def word_count(text):
    return len(text.split())


def character_count(text):
    return len(text)


def main():
    print("Loading processed dataset...")

    dataset = load_from_disk(DATASET_PATH)

    print("\nDataset:")
    print(dataset)

    # --------------------------------------------------
    # Basic statistics
    # --------------------------------------------------

    print("\n========== DATASET SIZE ==========")

    for split in dataset:
        print(f"{split.capitalize():12}: {len(dataset[split])}")

    # --------------------------------------------------
    # Analyze training data
    # --------------------------------------------------

    train = dataset["train"]

    informal_lengths = [
        word_count(x)
        for x in train["informal_text"]
    ]

    formal_lengths = [
        word_count(x)
        for x in train["formal_text"]
    ]

    print("\n========== SENTENCE LENGTH ==========")

    print(
        f"Average informal sentence length: "
        f"{sum(informal_lengths) / len(informal_lengths):.2f} words"
    )

    print(
        f"Average formal sentence length:   "
        f"{sum(formal_lengths) / len(formal_lengths):.2f} words"
    )

    print(
        f"Shortest informal sentence: {min(informal_lengths)} words"
    )

    print(
        f"Longest informal sentence:  {max(informal_lengths)} words"
    )

    print(
        f"Shortest formal sentence:   {min(formal_lengths)} words"
    )

    print(
        f"Longest formal sentence:    {max(formal_lengths)} words"
    )

    # --------------------------------------------------
    # Vocabulary
    # --------------------------------------------------

    informal_words = []

    for sentence in train["informal_text"]:
        words = re.findall(r"\b[\w']+\b", sentence.lower())
        informal_words.extend(words)

    formal_words = []

    for sentence in train["formal_text"]:
        words = re.findall(r"\b[\w']+\b", sentence.lower())
        formal_words.extend(words)

    informal_vocab = set(informal_words)
    formal_vocab = set(formal_words)

    print("\n========== VOCABULARY ==========")

    print(f"Informal vocabulary size: {len(informal_vocab)}")
    print(f"Formal vocabulary size:   {len(formal_vocab)}")

    # --------------------------------------------------
    # Most common words
    # --------------------------------------------------

    informal_counter = Counter(informal_words)
    formal_counter = Counter(formal_words)

    print("\n========== MOST COMMON INFORMAL WORDS ==========")

    for word, count in informal_counter.most_common(20):
        print(f"{word:20} {count}")

    print("\n========== MOST COMMON FORMAL WORDS ==========")

    for word, count in formal_counter.most_common(20):
        print(f"{word:20} {count}")

    # --------------------------------------------------
    # Example transformations
    # --------------------------------------------------

    print("\n========== SAMPLE TRANSFORMATIONS ==========")

    for i in range(10):
        print(f"\nExample {i + 1}")
        print("Informal:", train[i]["informal_text"])
        print("Formal:  ", train[i]["formal_text"])

    print("\nAnalysis complete.")


if __name__ == "__main__":
    main()