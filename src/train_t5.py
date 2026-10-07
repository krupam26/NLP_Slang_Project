from datasets import load_from_disk
from transformers import (
    T5Tokenizer,
    T5ForConditionalGeneration,
    DataCollatorForSeq2Seq,
    Seq2SeqTrainingArguments,
    Seq2SeqTrainer,
)


# --------------------------------------------------
# Configuration
# --------------------------------------------------

MODEL_NAME = "t5-small"

DATASET_PATH = "data/processed/informal_formal"

OUTPUT_DIR = "models/t5-informal-formal"

MAX_INPUT_LENGTH = 128
MAX_TARGET_LENGTH = 128


# --------------------------------------------------
# Load dataset
# --------------------------------------------------

print("Loading processed dataset...")

dataset = load_from_disk(DATASET_PATH)

print(dataset)


# --------------------------------------------------
# Load tokenizer and model
# --------------------------------------------------

print("\nLoading T5 tokenizer...")

tokenizer = T5Tokenizer.from_pretrained(MODEL_NAME)

print("Loading T5 model...")

model = T5ForConditionalGeneration.from_pretrained(MODEL_NAME)


# --------------------------------------------------
# Prepare input format
# --------------------------------------------------

def preprocess_function(examples):

    inputs = [
        "convert informal to formal: " + text
        for text in examples["informal_text"]
    ]

    targets = examples["formal_text"]

    model_inputs = tokenizer(
        inputs,
        max_length=MAX_INPUT_LENGTH,
        truncation=True,
    )

    labels = tokenizer(
        text_target=targets,
        max_length=MAX_TARGET_LENGTH,
        truncation=True,
    )

    model_inputs["labels"] = labels["input_ids"]

    return model_inputs


print("\nTokenizing dataset...")

tokenized_dataset = dataset.map(
    preprocess_function,
    batched=True,
    remove_columns=dataset["train"].column_names,
)

print("Tokenization complete.")


# --------------------------------------------------
# Data collator
# --------------------------------------------------

data_collator = DataCollatorForSeq2Seq(
    tokenizer=tokenizer,
    model=model,
)


# --------------------------------------------------
# Training configuration
# --------------------------------------------------

training_args = Seq2SeqTrainingArguments(
    output_dir=OUTPUT_DIR,

    # CPU-friendly settings
    per_device_train_batch_size=4,
    per_device_eval_batch_size=4,

    # Start small for the first experiment
    num_train_epochs=1,

    learning_rate=5e-5,

    weight_decay=0.01,

    logging_steps=100,

    eval_strategy="epoch",

    save_strategy="epoch",

    save_total_limit=2,

    predict_with_generate=True,

    report_to="none",

    fp16=False,

    dataloader_num_workers=0,
)


# --------------------------------------------------
# Trainer
# --------------------------------------------------

trainer = Seq2SeqTrainer(
    model=model,
    args=training_args,

    train_dataset=tokenized_dataset["train"],
    eval_dataset=tokenized_dataset["validation"],

    processing_class=tokenizer,

    data_collator=data_collator,
)


# --------------------------------------------------
# Train
# --------------------------------------------------

print("\n====================================")
print("Starting T5 training")
print("====================================")

trainer.train()


# --------------------------------------------------
# Save final model
# --------------------------------------------------

print("\nSaving model...")

trainer.save_model(OUTPUT_DIR)
tokenizer.save_pretrained(OUTPUT_DIR)

print("\n====================================")
print("Training complete!")
print("Model saved to:")
print(OUTPUT_DIR)
print("====================================")