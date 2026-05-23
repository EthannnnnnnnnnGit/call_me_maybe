import numpy as np


class NumberDecoding:
    def reset_settings(self) -> None:
        self.prev: None | str = None
        self.frac = False
        self.exponent = False

    def get_mask(self) -> np.array:
        numbers = [f"{i}" for i in range(10)]
        match self.prev:
            case None:
                mask = ["-"] + numbers
            case "e" | "E":
                self.exponent = True
                self.frac = False
                mask = numbers + ["-", "+"]
            case "-" | "+":
                mask = numbers
            case ".":
                self.frac = True
                mask = numbers
            case _:
                tmp: list = [","]
                if not self.frac:
                    tmp.append(".")
                if not self.exponent:
                    tmp += ["e", "E"]
                mask = tmp + numbers
        return mask
