from datasets import load_from_disk
import sacrebleu

from src.converter import slang_to_formal


DATASET_PATH = "data/processed/informal_formal"


def main():
    print("Loading test dataset...")

    dataset = load_from_disk(DATASET_PATH)
    test_data = dataset["test"]

    print(f"Test examples: {len(test_data)}")

    predictions = []
    references = []

    print("\nRunning rule-based baseline...")

    for example in test_data:
        informal = example["informal_text"]
        formal = example["formal_text"]

        prediction = slang_to_formal(informal)

        predictions.append(prediction)
        references.append(formal)

    # BLEU expects references as a list of reference corpora.
    bleu = sacrebleu.corpus_bleu(
        predictions,
        [references]
    )

    print("\n========== BASELINE RESULTS ==========")
    print(f"BLEU score: {bleu.score:.2f}")

    # Show examples
    print("\n========== SAMPLE PREDICTIONS ==========")

    for i in range(min(10, len(test_data))):
        print(f"\nExample {i + 1}")

        print("Input:")
        print(test_data[i]["informal_text"])

        print("\nExpected:")
        print(test_data[i]["formal_text"])

        print("\nBaseline:")
        print(predictions[i])

        print("-" * 60)


if __name__ == "__main__":
    main()