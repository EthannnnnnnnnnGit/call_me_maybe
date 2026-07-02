from .Decoding import Decoding


class NumberDecoding(Decoding):
    def __init__(self) -> None:
        self.stop = {",", "}", ""}
        self.numbers = [f"{i}" for i in range(10)]

    def reset_settings(self) -> None:
        self.prev: None | str = None
        self.frac = False
        self.exponent = False

    def get_mask(self) -> list[str]:
        match self.prev:
            case None:
                mask = ["-"] + self.numbers
            case "e" | "E":
                self.exponent = True
                self.frac = False
                mask = self.numbers
            case "-" | "+":
                mask = self.numbers
            case ".":
                self.frac = True
                mask = self.numbers
            case _:
                tmp = [","]
                if not self.frac:
                    tmp.append(".")
                if not self.exponent:
                    tmp += ["e", "E"]
                mask = tmp + self.numbers
        return mask
