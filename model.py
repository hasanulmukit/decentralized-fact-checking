!pip install transformers datasets sklearn

from datasets import load_dataset
import pandas as pd

# For demonstration, assume you have a CSV with columns: "claim", "evidence", "label" (1 for true, 0 for false)
df = pd.read_csv("fact_check_dataset.csv")
dataset = load_dataset('csv', data_files={'train': 'fact_check_dataset.csv'})['train']

from transformers import AutoTokenizer, AutoModelForSequenceClassification, TrainingArguments, Trainer

model_name = "distilbert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=2)

def preprocess_function(examples):
    return tokenizer(examples['claim'], examples['evidence'], truncation=True, padding="max_length", max_length=128)

tokenized_dataset = dataset.map(preprocess_function, batched=True)

training_args = TrainingArguments(
    output_dir="./results",
    evaluation_strategy="epoch",
    learning_rate=2e-5,
    per_device_train_batch_size=16,
    num_train_epochs=2,
    weight_decay=0.01,
    push_to_hub=False,
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset,
    eval_dataset=tokenized_dataset,
)

trainer.train()

model.save_pretrained("factcheck_model")
tokenizer.save_pretrained("factcheck_model")

from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

tokenizer = AutoTokenizer.from_pretrained("factcheck_model")
model = AutoModelForSequenceClassification.from_pretrained("factcheck_model")

def get_fact_check_score(claim, evidence):
    inputs = tokenizer(claim, evidence, return_tensors="pt", truncation=True, padding="max_length", max_length=128)
    outputs = model(**inputs)
    probs = torch.nn.functional.softmax(outputs.logits, dim=1)
    # Assume index 1 is "true" and index 0 is "false"
    truth_score = probs[0][1].item() * 100  # Convert to a percentage score
    return truth_score

# Example:
score = get_fact_check_score("Example claim", "Supporting evidence")
print(f"Fact-check score: {score:.2f}")
