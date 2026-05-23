from llm_sdk.llm_sdk import Small_LLM_Model
import numpy as np


class Masking:
    def __init__(self, llm: Small_LLM_Model):
        self.logits = llm.get_logits_from_input_ids([0])
        self.llm = llm

    def define_mask(self, mask: list[str]) -> np.array:
        mask_logits = np.full_like(self.logits, -np.inf)
        for val in mask:
            index = self.llm.encode(val)[0]
            mask_logits[index] = 0
        return mask_logits
