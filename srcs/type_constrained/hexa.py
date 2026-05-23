import numpy as np


class HexDecoding:
    def reset_settings(self) -> None:
        self.bases = [
            [val for val in "abcdef"],
            [val for val in "ABCDEF"],
            [val for val in "0123456789"]
        ]

    def get_mask(self) -> np.array:
        mask = []
        for base in self.bases:
            mask += base
        return mask
