from llm_sdk.llm_sdk import Small_LLM_Model
import numpy as np
from srcs.type_constrained import (
    StringDecoding,
    IntegerDecoding,
    HexDecoding,
    NumberDecoding,
    SpecialDecoding,
    ObjectDecoding,
    ArrayDecoding
)


class DecodingManager:
    def __init__(self, llm: Small_LLM_Model) -> None:
        self.pipelines = {
            "string": StringDecoding(),
            "integer": IntegerDecoding(),
            "hexadecimal": HexDecoding(),
            "number": NumberDecoding(),
            "bool": SpecialDecoding(),
            "null": SpecialDecoding(),
            "object": ObjectDecoding(),
            "array": ArrayDecoding()
        }
        self.decoder = None
        self.llm = llm
        self.logits = llm.get_logits_from_input_ids([0])
        self.ended = False
        self.stop = {"<|im_end|>", "\n", ",", "", "}", ":"}

    def choose_decoder(self, type: list[str]) -> None:
        self.ended = False
        try:
            self.decoder = self.pipelines[type[0]]
            if type[0] == "array":
                self.decoder.reset_settings(type[1])
            elif type[0] == "object":
                self.decoder.reset_settings(type[1], type[2])
            else:
                if type == "bool" or type == "null":
                    self.decoder.reset_settings(type)
                else:
                    self.decoder.reset_settings()
        except KeyError as e:
            print("Unknown type", e)

    def define_mask(self) -> np.array:
        mask = self.decoder.get_mask()
        if not mask:
            return np.full_like(self.logits, 0)
        mask_logits = np.full_like(self.logits, -np.inf)
        for val in mask:
            index = self.llm.encode(val)[0]
            mask_logits[index] = 0
        if ((isinstance(self.decoder, NumberDecoding) or
             isinstance(self.decoder, IntegerDecoding)) and "-" in mask):
            mask_logits[self.llm.encode("-")] = 22
        return mask_logits

    def check_token(self, token: str) -> str:
        for i in range(len(token)):
            if token[i] in self.stop:
                self.ended = True
                return token[:i]
        return token
