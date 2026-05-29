import json
from typing import Any


def raise_on_dupplicate_keys(json_values):
    temp = {}
    for key, val in json_values:
        if key in temp:
            raise KeyError("Invalid json: Dupplicate keys in the json file")
        temp[key] = val
    return temp


def get_json(filename: str) -> list[dict[str, Any]]:
    try:
        with open(filename, "r") as f:
            json_data = json.load(f,
                                  object_pairs_hook=raise_on_dupplicate_keys)
            if not isinstance(list):
                raise TypeError("The function definition file should be "
                                "a list of dict")
            for data in json_data:
                if not isinstance(dict):
                    raise TypeError("The function definition file should be a "
                                    "list of dict")
    except TypeError as e:
        print(e)
    except json.JSONDecodeError as e:
        print(e)
    except OSError as e:
        print(e)
