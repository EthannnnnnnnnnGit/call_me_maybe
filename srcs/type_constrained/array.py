from typing import Any


class ArrayDecoding:
    def reset_settings(self, decoder: Any) -> None:
        self.type = decoder
        self.type.reset_settings()
        self.prev = None

    def get_mask(self) -> list[str]:
        match self.prev:
            case None:
                mask = ["["]
            case _:
                mask = self.type.get_mask()
        return mask
