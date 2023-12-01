from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass
class ModelOutput:
    message: str
    is_final_output: bool = False


class IBaseClass(ABC):
    @abstractmethod
    def predict(self, user_input: str) -> ModelOutput:
        pass
