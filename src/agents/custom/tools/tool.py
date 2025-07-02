from abc import ABC, abstractmethod

from openai.types.chat import ChatCompletionToolParam


class Tool(ABC):
    function_definition: ChatCompletionToolParam

    @property
    def name(self) -> str:
        return self.function_definition["function"]["name"]

    @abstractmethod
    def __call__(self, *args) -> str:
        ...
