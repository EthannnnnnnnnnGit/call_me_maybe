import numpy as np


class NumberDecoding:
    def reset_settings(self) -> None:
        self.prev = None
        self.decimal = False

    def get_mask(self) -> np.array:
        number = [f"{i}" for i in range(10)]
        match self.prev:
            case None:
                mask = ["-"] + number
            case ".":
                mask = number
                self.decimal = True
            case _:
                if self.decimal:
                    mask = number
                else:
                    mask = number + ["."]
        mask = None
        return mask
