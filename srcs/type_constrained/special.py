from itertools import zip_longest
import numpy as np


class SpecialDecoding:
    def __init__(self) -> None:
        self.states = {
            "null": [val for val in "\"null\""],
            "bool": [f"{t}{f}" for t, f in zip_longest("\"true\"", "\"false\"",
                                                       fillvalue=",")]
        }
        self.type = None

    def reset_settings(self, type) -> np.array:
        self.type = type
        self.index = 0

    def get_mask(self) -> np.array:
        if self.index < len(self.states[self.type]):
            mask = self.states[self.type][self.index]
        else:
            mask = [","]
        return mask
