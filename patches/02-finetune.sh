#!/usr/bin/env python3

openai api fine_tunes.create -t data/acl_dataset_train.jsonl -v data/acl_dataset_eval.jsonl --batch_size 2 -m ada --n_epochs 3