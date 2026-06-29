from .Decoding import Decoding


class SpecialDecoding(Decoding):
    def __init__(self, type: str) -> None:
        self.states = {
            "null": [val for val in "null"],
            "bool": {"T": "true", "F": "false"}
        }
        self.type = type
        self.stop = {",", ""}

    def reset_settings(self) -> None:
        self.index = 0
        self.bool = ""
        self.len = 4
        self.prev = None

    def get_mask(self) -> list[str]:
        if self.index < self.len:
            if self.type == "null":
                mask = self.states[self.type][self.index]
            else:
                if self.index == 0:
                    mask = ["F", "T"]
                else:
                    mask = self.states[self.type][self.bool][self.index]
        else:
            mask = [","]
        self.index += 1
        return mask
