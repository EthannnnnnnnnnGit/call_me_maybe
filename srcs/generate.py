from llm_sdk.llm_sdk import Small_LLM_Model
import numpy as np
from srcs.decoding_manager import DecodingManager
from srcs.func_names.func_filter import define_name_prompt
from srcs.func_names.func_name_decoding import get_name_mask
from srcs.make_json import build_json
import re
from rich.console import Console


STOP_CONDITION = {"\"", "<|im_end|>", "\n", ",", ""}


class CallMeMaybe:
    def __init__(self, prompts, functions):
        self.llm = Small_LLM_Model()
        self.prompts = prompts
        self.functions = functions
        self.decoder = DecodingManager(self.llm)
        self.console = Console()

    def types_getter(self, func: dict) -> list[list[str]]:
        regex_validator = r'^\w+$|^\w+\[\w+\]$|^\w+\[\w+,\s*\w+\]$'
        lst_types = []
        for type in func["parameters"].values():
            type = type["type"]
            if not re.match(regex_validator, type):
                print(f"Syntax Error: Invalid type structure '{type}'")
                continue
            lst_types.append(re.findall(r'\w+', type))
        return lst_types

    def transform_type(self, types: list[str], result):
        match types[0]:
            case "list":
                return eval(result)
            case "number" | "integer":
                if "." in result:
                    return float(result)
                return int(result)
            case _:
                return result

    def get_func_name(self, prompt: str, mask: np.array) -> str:
        tensor = self.llm.encode(prompt + "\"")
        tensor = [t for t in tensor[0]]
        result = ""
        count = 0
        tk = None
        self.console.print("Name : ", end="", style="green")
        while count < 20:
            logits = np.array(self.llm.get_logits_from_input_ids(tensor))
            logits += mask
            index = logits.argmax()
            tk = self.llm.decode(index)
            if tk in STOP_CONDITION:
                break
            print(tk, end="", flush=True)
            result += tk
            tensor += self.llm.encode(tk)[0]
            count += 1
        print()
        return result

    def param_tensor_getter(self, defined_func, question) -> np.array:
        system = f"<im_start>system\n{defined_func}\n<im_end>"
        user = f"\n<im_start>user\n{question}\n <im_end>\n"
        qwen = "<im_start>assistant\n{\"parameters\": {"
        prompt = system + user + qwen
        tensor = self.llm.encode(prompt)[0].tolist()
        return tensor

    def get_func_params(self, name: str, prompt: str,
                        defined_func: dict[str, np.array]) -> list[str]:
        lst_types = self.types_getter(defined_func)
        params = {}
        tensor = self.param_tensor_getter(defined_func, prompt["prompt"])
        mask = None
        for types, arg in zip(lst_types, defined_func["parameters"].keys()):
            tensor += self.llm.encode(f"\"{arg}\": ")[0].tolist()
            self.decoder.choose_decoder(types)
            count = 0
            result = ""
            self.console.print(f"{arg}: ", end="", style="red")
            while count < 24:
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
                count += 1
                self.decoder.decoder.prev = tk
            params[arg] = self.transform_type(types, result)
            print()
        print()
        return params

    def function_getter(self, name: str, functions: list[dict]) -> dict | None:
        for func in functions:
            if func["name"] == name:
                return func
        return None

    def thinker(self) -> list[dict]:
        lst_results: list = []
        lst_prompts = define_name_prompt(self.prompts, self.functions)
        func_mask = get_name_mask(self.llm, self.functions)
        for i, prompt in enumerate(lst_prompts):
            self.console.print("Prompt:", self.prompts[i]["prompt"],
                               style="blue")
            name = self.get_func_name(prompt, func_mask)
            defined_func = self.function_getter(name, self.functions)
            if not defined_func:
                print("The name of the function is not in the given one.")
                continue
            params = self.get_func_params(name, self.prompts[i], defined_func)
            lst_results.append(build_json(self.prompts[i]["prompt"],
                                          name, params))
        return lst_results
