from abc import ABC, abstractmethod
from typing import Any


class Decoding(ABC):
    stop: set[str]
    prev: Any

    @abstractmethod
    def reset_settings(self) -> None:
        pass

    @abstractmethod
    def get_mask(self) -> list[str]:
        pass
