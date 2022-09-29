
def json_dump(filename, obj, indent=2):
    import json
    with open(filename, "w") as f:
        json.dump(obj, f, indent=indent, ensure_ascii=False)


def json_dumpl(filename, obj):
    import json
    with open(filename, "w") as f:
        for l in obj:
            f.write(json.dumps(l, ensure_ascii=False) + "\n")


def json_readl(filename):
    import json
    with open(filename, "r") as f:
        data = [json.loads(x) for x in f.readlines()]
    return data


def json_read(filename):
    import json
    with open(filename, "r") as f:
        return json.load(f)
