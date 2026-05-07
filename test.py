import json


def raise_on_dupplicate_keys(json_file):
    temp = {}
    for key, val in json_file:
        if key in temp:
            raise ValueError("Dupplicate keys")
        temp[key] = val
    return temp


with open("test.json") as f:
    data = json.load(f, object_pairs_hook=raise_on_dupplicate_keys)
for prompt in data:
    print(prompt)
with open("test.json", "w") as r:
    json.dump(data, r, indent=4)
