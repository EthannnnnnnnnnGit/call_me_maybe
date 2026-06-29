from .Decoding import Decoding


class IntegerDecoding(Decoding):
    def __init__(self) -> None:
        self.stop = {",", "}", ""}
        self.number = [f"{i}" for i in range(10)]

    def reset_settings(self) -> None:
        self.start = True

    def get_mask(self) -> list[str]:
        if self.start:
            mask = ["-"] + self.number
            self.start = False
        else:
            mask = self.number + [","]
        return mask
