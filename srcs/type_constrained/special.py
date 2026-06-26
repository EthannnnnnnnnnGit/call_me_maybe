from itertools import zip_longest


class SpecialDecoding:
    def __init__(self, type: str) -> None:
        self.states = {
            "null": [val for val in "null"],
            "bool": [f"{t}{f}" for t, f in zip_longest("\"true\"", "\"false\"",
                                                       fillvalue=",")]
        }
        self.type = type
        self.stop = {"\"", ""}

    def reset_settings(self) -> None:
        self.index = 0

    def get_mask(self) -> list[str]:
        if self.index < len(self.states[self.type]):
            mask = self.states[self.type][self.index]
        else:
            mask = [","]
        self.index += 1
        return mask
