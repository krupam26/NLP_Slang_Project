from datasets import load_dataset

print("Loading dataset...")

ds = load_dataset("Bendang/Informal-Standard-English-Corpus")

print("\nDataset loaded successfully!")
print(ds)

print("\nDataset columns:")
print(ds.column_names)

print("\nFirst example:")
print(ds["train"][0])