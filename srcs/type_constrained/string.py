class StringDecoding:
    def __init__(self):
        self.stop = {"\"",  ""}

    def reset_settings(self) -> None:
        self.start = True

    def get_mask(self) -> list[str]:
        if self.start:
            self.start = False
            mask = ["\""]
        else:
            mask = []
        return mask
