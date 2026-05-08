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
        temp = (system + "<im_start>user" + prompts_function + prompt["prompt"] + "<im_end>")
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
    for i in range(3):
        logits = np.array(llm.get_logits_from_input_ids(tensor))
        index = logits.argmax()
        tk = vocab[index]
        result += tk
        tensor += [t for t in llm.encode(tk)[0]]


def thinker(prompts: list[dict[str, str]],
            functions: list[dict[str, Any]]) -> None:
    llm = Small_LLM_Model()
    lst_prompts = define_prompts(prompts, functions)
    vocab = parse_logits(llm)
    print(vocab)
    print()
    for prompt in lst_prompts:
        print(prompt)
        print()
        get_thinking(llm, prompt, vocab)
