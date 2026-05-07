from llm_sdk.llm_sdk import Small_LLM_Model
from typing import Any
import json
import numpy as np


def define_prompts(prompts: list[dict[str, str]],
                   functions: list[dict[str, Any]]) -> list[str]:
    system = """<|im_start|>system
    You should choose between one of the function given in the prompt,
    depending of the full prompt I am giving.
    You must decide depending on the the description function and the name.
    <|im_end|>"""
    lst_prompts: list[str] = []
    prompts_function: str = ""
    for func in functions:
        prompts_function += (json.dumps(func, indent=4) + "\n")
    for prompt in prompts:
        temp = system + prompts_function + prompt["prompt"]
        lst_prompts.append(temp)
    return lst_prompts


def parse_logits(llm: Small_LLM_Model) -> list:
    print(llm.get_path_to_tokenizer_file())


def get_thinking(llm: Small_LLM_Model, prompt: str, choice) -> None:
    np.array()


def thinker(prompts: list[dict[str, str]],
            functions: list[dict[str, Any]]) -> None:
    llm = Small_LLM_Model()
    lst_prompts = define_prompts(prompts, functions)
    choice = parse_logits(llm)
    for prompt in lst_prompts:
        get_thinking(llm, prompt, choice)
