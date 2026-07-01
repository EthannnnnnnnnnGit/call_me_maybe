from abc import ABC, abstractmethod


class Decoding(ABC):
    @abstractmethod
    def reset_settings(self) -> None:
        pass

    @abstractmethod
    def get_mask(self) -> list[str]:
        pass
