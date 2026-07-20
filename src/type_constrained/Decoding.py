from abc import ABC, abstractmethod
from typing import Any


class Decoding(ABC):
    """Format of every constrained decoding class"""
    stop: set[str]
    prev: Any

    @abstractmethod
    def reset_settings(self) -> None:
        """Reset all attributs for a new parameters generation"""
        pass

    @abstractmethod
    def get_mask(self) -> list[str]:
        """Get the mask depending of type generation and previous token"""
        pass
