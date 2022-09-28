#!/usr/bin/env python3

raise Exception("Abandoned in favor of GPT3")

import torch
from torch.utils.data import Dataset, random_split
from transformers import GPT2Tokenizer, TrainingArguments, Trainer, GPT2LMHeadModel
import utils
import gc

torch.manual_seed(0)

# TODO: change to large
tokenizer = GPT2Tokenizer.from_pretrained(
    'gpt2-medium',
    bos_token='<|startoftext|>', eos_token='<|endoftext|>', pad_token='<|pad|>'
)
model = GPT2LMHeadModel.from_pretrained('gpt2-medium').cuda()
model.resize_token_embeddings(len(tokenizer))

data = utils.json_readl("data/acl_dataset.jsonl")
data = [x for x in data if len(tokenizer.encode(x["prompt"])) <= 1024]
# max_length = max([len(tokenizer.encode(x["prompt"])) for x in data])

gc.collect()
torch.cuda.empty_cache()

class AbstractDataset(Dataset):
    def __init__(self, txt_list, tokenizer):
        self.input_ids = []
        self.attn_masks = []
        self.labels = []
        for x in txt_list:
            encodings_dict = tokenizer(
                x["prompt"], truncation=True,
                max_length=1024, padding="max_length"
            )
            self.input_ids.append(torch.tensor(encodings_dict['input_ids']))
            self.attn_masks.append(torch.tensor(
                encodings_dict['attention_mask'])
            )

    def __len__(self):
        return len(self.input_ids)

    def __getitem__(self, idx):
        return self.input_ids[idx], self.attn_masks[idx]


dataset = AbstractDataset(data, tokenizer)
train_size = int(0.9 * len(dataset))
train_dataset, val_dataset = random_split(
    dataset, [train_size, len(dataset) - train_size]
)

training_args = TrainingArguments(
    output_dir='./results', num_train_epochs=1, logging_steps=100, save_steps=5000,
    per_device_train_batch_size=1, per_device_eval_batch_size=1,
    warmup_steps=10, weight_decay=0.05, logging_dir='./logs', report_to='none'
)

trainer = Trainer(
    model=model, args=training_args, train_dataset=train_dataset,
    eval_dataset=val_dataset,
    data_collator=lambda data: {
        'input_ids': torch.stack([f[0] for f in data]),
        'attention_mask': torch.stack([f[1] for f in data]),
        'labels': torch.stack([f[0] for f in data])
    })
trainer.train()
