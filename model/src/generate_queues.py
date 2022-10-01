#!/usr/bin/env python3

import copy
import json
import random
import hashlib
import itertools

with open("data/abstracts_and_titles_pruned.jsonl", "r") as f:
    data = [json.loads(x) for x in f.readlines()]


UIDs = [
    "harare", "lusaka", "sahara", "cardiff", "hanoi",
    "caracas", "montevideo", "washington", "kampala", "funafuti",
    "ashgabat", "ankara", "tiraspol", "lome", "bangkok",
    "dodoma", "dushanbe", "damascus", "bern", "stockholm",
    "paramaribo", "khartoum", "madrid", "juba", "seoul",
    "pretoria", "hargeisa", "mogadishu", "honiara", "ljubljana",
    "bratislava", "philipsburg", "singapore", "freetown", "belgrade",
]

# removing pair_rank_ref
MODES = [
    "pair_rank_noref", "pair_direct_noref", "pair_direct_ref",
    "all_rank_noref", "all_rank_ref", "all_direct_noref", "all_direct_ref",
]

for uid in UIDs[:2]:
    # shuffling
    data_copy = copy.deepcopy(data)
    seed = int(hashlib.sha1(uid.encode("utf-8")).hexdigest(), 16)
    random.seed(seed)
    random.shuffle(data_copy)

    modes = random.choices(MODES, k=len(data))
    queue_out = []
    for mode, line in zip(modes, data):
        if mode in {"pair_rank_noref", "pair_direct_noref"}:
            combinations = list(itertools.combinations(enumerate(line["titles"]), 2))
            queue_out_micro = []

            for (title_a_i, title_a), (title_b_i, title_b) in combinations:
                # randomly swap order
                if random.choice([False, True]):
                    title_a, title_b = title_b, title_a
                    title_a_i, title_b_i = title_b_i, title_a_i

                obj_out = {
                    "abstract": line["abstract"], "mode": mode,
                    "titles": [title_a, title_b],
                    "titles_order": [title_a_i, title_b_i],
                }
                queue_out_micro.append(obj_out)
            random.shuffle(queue_out_micro)
            queue_out += queue_out_micro
        elif mode in {"pair_direct_ref"}:
            queue_out_micro = []
            title_a = line["titles"][0]
            title_a_i = 0
            for (title_b_i, title_b) in enumerate(line["titles"]):
                obj_out = {
                    "abstract": line["abstract"], "mode": mode,
                    "titles": [title_a, title_b],
                    "titles_order": [title_a_i, title_b_i],
                }
                queue_out_micro.append(obj_out)
            random.shuffle(queue_out_micro)
            queue_out += queue_out_micro
        elif mode in {"all_rank_noref", "all_direct_noref"}:
            titles_copy = copy.deepcopy(list(enumerate(line["titles"])))
            random.shuffle(titles_copy)
            obj_out = {
                "abstract": line["abstract"], "mode": mode,
                "titles": [x[1] for x in titles_copy],
                "titles_order": [x[0] for x in titles_copy],
            }
            queue_out.append(obj_out)
        elif mode in {"all_rank_ref", "all_direct_ref"}:
            titles_copy = copy.deepcopy(list(enumerate(line["titles"][1:])))
            random.shuffle(titles_copy)
            obj_out = {
                "abstract": line["abstract"], "mode": mode,
                "titles": [line["titles"][0]] + [x[1] for x in titles_copy],
                "titles_order": [0] + [x[0] for x in titles_copy],
            }
            queue_out.append(obj_out)

            # todo shuffle
        with open(f"queues/{uid}.jsonl", "w") as f:
            f.write("\n".join([json.dumps(x) for x in queue_out]))