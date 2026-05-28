class IntegerDecoding:
    def reset_settings(self) -> None:
        self.start = True

    def get_mask(self) -> list[str]:
        number = [f"{i}" for i in range(10)]
        if self.start:
            mask = ["-"] + number
            self.start = False
        else:
            mask = number
        return mask
