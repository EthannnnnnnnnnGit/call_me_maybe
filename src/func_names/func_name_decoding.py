import numpy as np
from llm_sdk.llm_sdk import Small_LLM_Model
from typing import Any


def get_name_mask(llm: Small_LLM_Model,
                  funcs: list[dict[str, Any]]) -> np.array:
    logits = np.array(llm.get_logits_from_input_ids([0, 0, 1]))
    mask = np.full_like(logits, -np.inf)
    authorized = set()
    for func in funcs:
        authorized.update([i for i in llm.encode(func["name"])[0]])
    authorized.add(llm.encode("\"")[0])
    for tensor in authorized:
        mask[tensor] = 0
    return mask
