from llm_sdk.llm_sdk import Small_LLM_Model
import numpy as np
from src.type_constrained import (
    StringDecoding,
    IntegerDecoding,
    HexDecoding,
    NumberDecoding,
    SpecialDecoding,
    ArrayDecoding,
)


class DecodingManager:
    """Manage constrained decoding and token validation"""
    def __init__(self, llm: Small_LLM_Model) -> None:
        self.pipelines = {
            "string": StringDecoding(),
            "integer": IntegerDecoding(),
            "hex": HexDecoding(),
            "number": NumberDecoding(),
            "boolean": SpecialDecoding("bool"),
            "null": SpecialDecoding("null"),
            "array": ArrayDecoding()
        }
        self.llm = llm
        self.logits = llm.get_logits_from_input_ids([0])
        self.ended = False

    def choose_decoder(self, type: list[str]) -> None:
        """Decide decoder depending of type"""
        self.ended = False
        try:
            self.decoder = self.pipelines[type[0]]
            self.decoder.reset_settings()
        except KeyError as e:
            print("Unknown type", e)

    def define_mask(self) -> np.array:
        """Get the mask and transform it into numpy array"""
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
        """Verify is token is an end condition"""
        if (isinstance(self.decoder, SpecialDecoding) and
                self.decoder.index == 1 and self.decoder.type == "bool"):
            self.decoder.bool = token
            if token == "F":
                self.decoder.len = 5
        for i in range(len(token)):
            if token[i] in self.decoder.stop:
                prev = token[i - 1]
                if i == 0:
                    prev = ""
                if (isinstance(self.decoder, StringDecoding) and
                        (prev != "\"" and self.decoder.prev[-1] != "\"")):
                    continue
                self.ended = True
                if isinstance(self.decoder, ArrayDecoding):
                    return token[:i + 1]
                return token[:i]
        return token
