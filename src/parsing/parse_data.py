import json
from typing import Any


def raise_on_dupplicate_keys(json_values: list[tuple[Any, Any]]) -> Any:
    temp = {}
    for key, val in json_values:
        if key in temp:
            raise KeyError("Invalid json: Dupplicate keys in the json file")
        temp[key] = val
    return temp


def get_json(filename: str) -> list[dict[str, Any]]:
    with open(filename, "r") as f:
        json_data = json.load(f, object_pairs_hook=raise_on_dupplicate_keys)
        if not isinstance(json_data, list):
            raise TypeError("The function definition file should be "
                            "a list of dict")
        if len(json_data) == 0:
            raise ValueError("The list should have at least one value")
        for data in json_data:
            if not isinstance(data, dict):
                raise TypeError("The function definition file should be a "
                                "list of dict")
    return json_data
