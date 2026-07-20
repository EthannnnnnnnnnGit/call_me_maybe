from .Decoding import Decoding


class StringDecoding(Decoding):
    """Manage constrained decoding of string type"""
    def __init__(self) -> None:
        self.stop = {"}", ",", ""}

    def reset_settings(self) -> None:
        self.start = True

    def get_mask(self) -> list[str]:
        if self.start:
            mask = ["\""]
            self.start = False
        else:
            mask = []
        return mask
