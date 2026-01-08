from abc import ABC, abstractmethod


class LLMProvider(ABC):
    @abstractmethod
    def generate_test_code(self, prompt: str) -> str:
        pass
