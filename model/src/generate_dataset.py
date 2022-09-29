#!/usr/bin/env python3

import pandas as pd
import json
from langdetect import detect as detect_lang
import tqdm

data = pd.read_parquet("data/acl_corpus_full-text.parquet")
# shuffle data
data = data.sample(frac = 1, random_state = 0)

fout = open("data/acl_dataset.jsonl", "w")

saved = set()

sizes = list()

for line_i, line in tqdm.tqdm(data.iterrows(), total=data.shape[0]):
    title = line["title"]
    abstract = line["abstract"]
    if len(title) == 0 or len(abstract) == 0:
        continue
    abstract_words = len(abstract.split())
    if abstract_words > 2000 or abstract_words < 5:
        continue
    
    line_hash = abstract + "|||" + title
    if line_hash in saved:
        continue
    saved.add(line_hash)

    # abstract language detection is more robust
    abstract_lang = detect_lang(abstract)
    if abstract_lang != "en":
        # print(abstract_lang, title, abstract[:100])
        continue

    # TODO add better separators
    line_out = {
        "prompt": abstract + " \n\n###\n\n",
        "completion": " " + title + " ###",
    }

    sizes.append(len(abstract.split()))
    fout.write(json.dumps(line_out, ensure_ascii=False) + "\n")

# make sure to flush
fout.close()

print("Abstract sizes")
sizes.sort(reverse=True) 
print(sizes[:10])
print(sizes[-10:])