from abc import ABC, abstractmethod
from typing import Literal, TypedDict


class Message(TypedDict):
    timestamp: int
    message_id: str
    index: int


class SystemMessage(Message):
    type: Literal["system"]
    content: str


class UserMessage(Message):
    type: Literal["user"]
    content: str


class ImageMessage(Message):
    type: Literal["image"]


class Base64ImageMessage(ImageMessage):
    base64: str


class UrlImageMessage(ImageMessage):
    url: str


class UploadImageMessage(ImageMessage):
    file_id: str


class AssistantMessage(Message):
    type: Literal["assistant"]
    content: str


class ReasoningMessage(Message):
    type: Literal["reasoning"]
    content: str


class ToolMessage(Message):
    type: Literal["tool"]
    call_id: str


class ToolCallMessage(ToolMessage):
    name: str
    argument: str


class ToolResultMessage(ToolMessage):
    result: str


class SessionManager(ABC):
    @abstractmethod
    async def list_sessions(self): ...

    @abstractmethod
    async def load_session(self, session_id: str) -> list[Message]: ...

    @abstractmethod
    async def create_session(self) -> str: ...

    @abstractmethod
    async def delete_session(self, session_id: str): ...

    @abstractmethod
    async def fork_session(self, session_id: str, message_id: str): ...

    @abstractmethod
    async def append_messages(self, session_id: str, messages: list[Message]): ...
