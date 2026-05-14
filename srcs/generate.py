from llm_sdk.llm_sdk import Small_LLM_Model
from typing import Any
import json
import numpy as np
from enum import Enum


class STOP_CONDITION(Enum):
    


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


def parse_logits(llm: Small_LLM_Model) -> np.array:
    temp = llm.get_logits_from_input_ids([1])
    lst: list = []
    for i in range(len(temp)):
        lst.append(llm.decode([i]))
    return np.array(lst)


def get_thinking(llm: Small_LLM_Model, prompt: str, vocab: np.array) -> None:
    tensor = llm.encode(prompt)
    tensor = [t for t in tensor[0]]
    result = ""
    for i in range(8):
        logits = np.array(llm.get_logits_from_input_ids(tensor))
        index = logits.argmax()
        tk = vocab[index]
        result += tk
        tensor += [t for t in llm.encode(tk)[0]]
    print(result)


def thinker(prompts: list[dict[str, str]],
            functions: list[dict[str, Any]]) -> None:
    llm = Small_LLM_Model()
    lst_prompts = define_prompts(prompts, functions)
    vocab = parse_logits(llm)
    for prompt in lst_prompts:
        get_thinking(llm, prompt, vocab)
