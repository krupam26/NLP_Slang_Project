from datasets import load_dataset, DatasetDict
from pathlib import Path


DATASET_NAME = "Bendang/Informal-Standard-English-Corpus"

PROCESSED_DIR = Path("data/processed")
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


def clean_example(example):
    informal = example["informal_english"].strip()
    formal = example["normalized_english"].strip()

    return {
        "informal_text": informal,
        "formal_text": formal,
    }


def main():
    print("Loading dataset...")

    ds = load_dataset(DATASET_NAME)

    print("\nOriginal dataset:")
    print(ds)

    # Rename and clean columns
    ds = ds.map(
        clean_example,
        remove_columns=ds["train"].column_names
    )

    # Remove empty examples
    ds = ds.filter(
        lambda x: len(x["informal_text"]) > 0
        and len(x["formal_text"]) > 0
    )

    # Remove duplicate pairs
    ds = ds["train"].to_pandas().drop_duplicates()

    # Convert back to Hugging Face Dataset
    from datasets import Dataset

    ds = Dataset.from_pandas(ds, preserve_index=False)

    print("\nAfter cleaning:")
    print(ds)

    # Split:
    # 80% training
    # 10% validation
    # 10% testing
    split = ds.train_test_split(
        test_size=0.2,
        seed=42
    )

    train_data = split["train"]

    temp = split["test"].train_test_split(
        test_size=0.5,
        seed=42
    )

    validation_data = temp["train"]
    test_data = temp["test"]

    final_dataset = DatasetDict({
        "train": train_data,
        "validation": validation_data,
        "test": test_data,
    })

    print("\nFinal dataset:")
    print(final_dataset)

    print("\nNumber of examples:")
    print(f"Train:      {len(train_data)}")
    print(f"Validation: {len(validation_data)}")
    print(f"Test:       {len(test_data)}")

    # Save dataset
    output_path = PROCESSED_DIR / "informal_formal"

    final_dataset.save_to_disk(str(output_path))

    print("\nDataset saved to:")
    print(output_path)

    # Show examples
    print("\nSample examples:")
    for i in range(min(5, len(train_data))):
        print(f"\nExample {i + 1}")
        print("Informal:", train_data[i]["informal_text"])
        print("Formal:  ", train_data[i]["formal_text"])


if __name__ == "__main__":
    main()