#!/usr/bin/bash

./src/generate_dataset.py

openai tools fine_tunes.prepare_data -f data/acl_dataset.jsonl

head -n 55000 data/acl_dataset.jsonl > data/acl_dataset_train.jsonl
tail -n +55000 data/acl_dataset.jsonl > data/acl_dataset_eval.jsonl