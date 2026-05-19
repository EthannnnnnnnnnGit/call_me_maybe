from llm_sdk.llm_sdk import Small_LLM_Model
from typing import Any
import json
import numpy as np


temp = Small_LLM_Model()
STOP_CONDITION = {"\"", "<|im_end|>", "\n", ",", ""}


def constrained_decoding(llm: Small_LLM_Model, funcs: list[dict]) -> np.array:
    logits = np.array(llm.get_logits_from_input_ids([0, 0, 1]))
    mask = np.full_like(logits, -np.inf)
    authorized = set()
    for func in funcs:
        authorized.update([i for i in llm.encode(func["name"])[0]])
    authorized.add(llm.encode("\"")[0])
    for tensor in authorized:
        mask[tensor] = 0
    return mask


def define_prompts(prompts: list[dict[str, str]],
                   functions: list[dict[str, Any]]) -> list[str]:
    lst_prompts: list[str] = []
    prompts_function: str = ""
    for func in functions:
        prompts_function += (json.dumps(func) + "\n")
    system = f"""<|im_start|>system {prompts_function}, only return json
    <|im_end|>"""
    for prompt in prompts:
        temp = (system + "<im_start>user" +
                prompt["prompt"] + "<im_end>" + "<im_start>assistant {\"name\":")
        lst_prompts.append(temp)
    return lst_prompts


def get_thinking(llm: Small_LLM_Model, prompt: str, mask) -> str:
    tensor = llm.encode(prompt + "\"")
    tensor = [t for t in tensor[0]]
    result = "\""
    count = 0
    tk = None
    while count < 8 and tk not in STOP_CONDITION:
        logits = np.array(llm.get_logits_from_input_ids(tensor))
        logits += mask
        index = logits.argmax()
        tk = llm.decode(index)
        result += tk
        tensor += [t for t in llm.encode(tk)[0]]
        count += 1
    return result


def get_func(llm: Small_LLM_Model,
             functions: list[dict]) -> dict[str, np.array]:
    dict_func = {}
    for func in functions:
        dict_func[func["name"]] = [i for i in llm.encode(json.dumps(func))[0]]
    return dict_func


def get_params(llm: Small_LLM_Model, name: str,
               dict_func: dict[str, np.array]) -> None:
    try:
        func = dict_func[name]
    except KeyError:
        print("Wrong function name")
    tensor = llm.encode(func + "\"")
    tensor = [t for t in tensor[0]]
    result = "\""
    count = 0
    tk = None
    while count < 8 and tk not in STOP_CONDITION:
        logits = np.array(llm.get_logits_from_input_ids(tensor))
        logits += mask
        index = logits.argmax()
        tk = llm.decode(index)
        result += tk
        tensor += [t for t in llm.encode(tk)[0]]
        count += 1
    return result


def thinker(prompts: list[dict[str, str]],
            functions: list[dict[str, Any]]) -> None:
    llm = Small_LLM_Model()
    mask = constrained_decoding(llm, functions)
    lst_prompts = define_prompts(prompts, functions)
    dict_func = get_func()
    for prompt in lst_prompts:
        name = get_thinking(llm, prompt, mask)
        get_params(llm, name.strip("\""), dict_func)
