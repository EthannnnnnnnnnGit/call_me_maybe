from typing import Any
import json
from pathlib import Path


def make_output_file(lst_json: list[dict[str, Any]],
                     outputfilename: str) -> None:
    output_file = Path(outputfilename)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    try:
        with open(outputfilename, "w") as f:
            json.dump(lst_json, f, indent=4)
    except OSError as e:
        print("An error as occured when writing in the file:", e)
    except json.JSONDecodeError as e:
        print("An error as occured in json format:", e)


def build_json(prompt: str, name: str,
               params: dict[str, Any]) -> dict[str, Any]:
    json = {
        "prompt": prompt,
        "name": name,
        "parameters": params
    }
    return json
