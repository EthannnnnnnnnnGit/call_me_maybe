from llm_sdk.llm_sdk import Small_LLM_Model
import numpy as np
from src.decoding_manager import DecodingManager
from src.func_names.func_filter import define_name_prompt
from src.func_names.func_name_decoding import get_name_mask, get_max_size
from src.make_json import build_json
import re
from rich.console import Console
from typing import Any


STOP_CONDITION = {"\"", "<|im_end|>", "\n", ",", ""}


class CallMeMaybe:
    """Manage llm generation and result format.
    Is the core object of the subject"""
    def __init__(self, prompts: list[Any], functions: list[Any]) -> None:
        self.llm = Small_LLM_Model()
        self.prompts = prompts
        self.functions = functions
        self.decoder = DecodingManager(self.llm)
        self.console = Console()

    def types_getter(self, func: dict[str, Any]) -> list[list[str]]:
        """Get type of the parameters"""
        regex_validator = r'^\w+$|^\w+\[\w+\]$|^\w+\[\w+,\s*\w+\]$'
        lst_types: list[Any] = []
        for type in func["parameters"].values():
            type = type["type"]
            if not re.match(regex_validator, type):
                print(f"Syntax Error: Invalid type structure '{type}'")
                continue
            lst_types.append(re.findall(r'\w+', type))
        return lst_types

    def transform_type(self, types: list[str], result: str) -> Any:
        """Transform data into right type"""
        try:
            match types[0]:
                case "number":
                    return float(result)
                case "integer":
                    return int(result)
                case "hex":
                    return hex(int(result))
                case "boolean":
                    return True if result == "True" else False
                case "null":
                    return None if result == "null" else result
                case "array":
                    return [val.strip("\"") for val in
                            result.strip("[]").split(", ")]
                case _:
                    result = result.strip("\"").strip()
                    return result.encode('utf-8').decode('unicode_escape')
        except Exception:
            return result

    def get_func_name(self, prompt: str, mask: np.array, max: int) -> str:
        """Generation of the function names"""
        tensor = self.llm.encode(prompt + "\"")[0].tolist()
        result = ""
        tk = None
        self.console.print("Name : ", end="", style="green")
        while max:
            logits = np.array(self.llm.get_logits_from_input_ids(tensor))
            logits += mask
            index = logits.argmax()
            tk = self.llm.decode(index)

            if tk in STOP_CONDITION:
                break
            print(tk, end="", flush=True)
            result += tk
            tensor += self.llm.encode(tk)[0]
            max -= 1
        print()
        return result

    def param_tensor_getter(self, defined_func: dict[str, Any],
                            question: str) -> np.array:
        """Define prompt for parameters's functions"""
        system = f"<im_start>system\n{defined_func}\n<im_end>"
        user = f"\n<im_start>user\n{question}\n <im_end>\n"
        qwen = "<im_start>assistant\n{\"parameters\": {"
        prompt = system + user + qwen
        tensor = self.llm.encode(prompt)[0].tolist()
        return tensor

    def get_func_params(self, prompt: dict[str, str],
                        defined_func: dict[str, Any]) -> dict[str, Any]:
        """Generation of all parameters of a prompt"""
        lst_types = self.types_getter(defined_func)
        params: dict[str, Any] = {}
        tensor = self.param_tensor_getter(defined_func, prompt["prompt"])
        mask = None
        max = len(self.llm.encode(prompt["prompt"])[0].tolist()) + 5

        for types, arg in zip(lst_types, defined_func["parameters"].keys()):
            tensor += self.llm.encode(f"\"{arg}\": ")[0].tolist()
            self.decoder.choose_decoder(types)
            result = ""
            self.console.print(f"{arg}: ", end="", style="red")

            while max:
                mask = self.decoder.define_mask()
                logits = np.array(self.llm.get_logits_from_input_ids(tensor))
                logits += mask
                index = logits.argmax()
                tk = self.decoder.check_token(self.llm.decode(index))
                result += tk
                tensor += (self.llm.encode(tk)[0].tolist())
                print(tk, end="", flush=True)

                if self.decoder.ended:
                    tensor += self.llm.encode(",")[0].tolist()
                    break

                max -= 1
                self.decoder.decoder.prev = tk

            params[arg] = self.transform_type(types, result)
            print()
        print()
        return params

    def function_getter(self, name: str,
                        functions: list[dict[str,
                                             Any]]) -> dict[str, Any] | None:
        """Check if function is in the list and function
        and return it if it is"""
        for func in functions:
            if func["name"] == name:
                return func
        return None

    def thinker(self) -> list[dict[str, Any]]:
        """Pipeline of generation names functions
        and parameters for all prompts given"""
        lst_results: list[dict[str, Any]] = []
        lst_prompts = define_name_prompt(self.prompts, self.functions)
        func_mask = get_name_mask(self.llm, self.functions)
        max_token = get_max_size(self.llm, self.functions)
        for i, prompt in enumerate(lst_prompts):
            self.console.print("Prompt:", self.prompts[i]["prompt"],
                               style="blue")
            name = self.get_func_name(prompt, func_mask, max_token)
            defined_func = self.function_getter(name, self.functions)
            if not defined_func:
                print("The name of the function is not in the given one.")
                continue
            params = self.get_func_params(self.prompts[i], defined_func)
            lst_results.append(build_json(self.prompts[i]["prompt"],
                                          name, params))
        return lst_results
