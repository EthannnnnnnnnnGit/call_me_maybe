from .Decoding import Decoding


class StringDecoding(Decoding):
    def __init__(self) -> None:
        self.stop = {",",  "}", ""}

    def reset_settings(self) -> None:
        self.start = True

    def get_mask(self) -> list[str]:
        if self.start:
            self.start = False
            mask = ["\""]
        else:
            mask = []
        return mask
