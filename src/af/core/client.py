from abc import ABC, abstractmethod

from .session import Message


class HttpClient[R](ABC):
    @abstractmethod
    async def send_messages(self, messages: list[Message]) -> R: ...
