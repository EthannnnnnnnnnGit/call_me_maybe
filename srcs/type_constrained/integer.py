import numpy as np


class IntegerDecoding:
    def reset_settings(self) -> None:
        self.start = True

    def get_mask(self) -> np.array:
        number = [f"{i}" for i in range(10)]
        if self.start:
            mask = ["-"] + number
            self.start = False
        else:
            mask = number
        return mask
