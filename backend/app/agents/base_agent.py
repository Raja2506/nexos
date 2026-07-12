from abc import ABC, abstractmethod
from typing import Any, Dict


class BaseAgent(ABC):
    """
    Every agent in NexOS inherits from this class.
    It defines the common 'shape' all agents must follow.
    """

    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    async def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Every agent MUST implement this method.
        Takes structured input, returns structured output.
        """
        raise NotImplementedError

    def log(self, message: str) -> None:
        """Simple shared logging so every agent prints consistently."""
        print(f"[{self.name}] {message}")