import json
from typing import Any


def raise_on_dupplicate_keys(json_values):
    temp = {}
    for key, val in json_values:
        if key in temp:
            raise KeyError("Invalid json: Dupplicate keys in the json file")
        temp[key] = val
    return temp


def get_json_data(filename: str) -> Any:
    with open(filename, "r") as f:
        prompts = json.load(f,
                            object_pairs_hook=raise_on_dupplicate_keys)
    if not isinstance(prompts, list):
        raise TypeError("The json file should be a list of dict")
    for val in prompts:
        if not isinstance(val, dict):
            raise TypeError("The json file should be a list of dict")
    return prompts


def tests_validator(tests: list[dict[Any]]) -> list[dict[str, str]]:
    for prompt in tests:
        for (key, value) in prompt.items():
            if key != "prompt":
                raise KeyError("The key of the function calling "
                               "test must be \"prompt\"")
            if not isinstance(value, str):
                raise TypeError("The value of the function calling "
                                "test must be a str type")


def functions_validator(functions: list[dict[
        Any]]) -> list[dict[str, Any]]:
    valid_keys = {"name", "description", "parameters", "returns"}
    for function in functions:
        for (key, value) in function.items():
            if key not in valid_keys:
                raise KeyError("The key given is not in "
                               "the valid keys")
            if key == "parameters":
                for param, val in value.items():
                    if not isinstance(param, str):
                        raise KeyError("Parameters should be string")
                    for k, type in val.items():
                        if k != "type":
                            raise KeyError("Parameters key "
                                           "should be \"type\"")
                        if not isinstance(type, str):
                            raise TypeError("Parameters type "
                                            "should be string")
            if key == "returns":
                if value.keys() != {"type"}:
                    raise KeyError("Return ")
                vals = list(value.values())
                if len(vals) != 1 or not isinstance(vals[0], str):
                    raise TypeError("Parameters value should "
                                    "be \"type\": 'str'")
