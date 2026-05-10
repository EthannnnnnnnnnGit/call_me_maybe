from pydantic import Basemodel
from enum import Enum
from typing import Any
import numpy as np


class OutputState(Enum):
    PROMPT = "{\"prompt\":"
    NAME = "\"name\":"
    PARAMETERS = "\"parameters\":"
    END = "}"
    NEXT = ","


class ConstrainedDecoding(Basemodel):
    state: OutputState = OutputState.PROMPT
    is_last_prompt: bool = True


    @staticmethod
    def determine_mask(logits: list[float]) -> list[float]:
        pass
        

    def get_masked_logtis(self, logits: list[float]) -> list[float]:
        mask = self.determine_mask(logits)
