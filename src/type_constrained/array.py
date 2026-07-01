from .Decoding import Decoding


class ArrayDecoding(Decoding):
    def __init__(self) -> None:
        self.stop = {"]"}

    def reset_settings(self) -> None:
        self.prev = None
        self.is_value = False

    def get_mask(self) -> list[str]:
        match self.prev:
            case None:
                mask = ["["]
            case "[" | ",":
                mask = ["\""]
            case "\"":
                if self.is_value:
                    mask = [",", "]"]
                    self.is_value = False
                else:
                    mask = []
                    self.is_value = True
            case _:
                mask = []
        return mask
