class StringDecoding:
    def reset_settings(self) -> None:
        self.start = True

    def get_mask(self) -> None:
        if self.start:
            self.start = False
            mask = ["\""]
        else:
            mask = None
        return mask
