from abc import ABC, abstractmethod
from typing import Any, Literal, NotRequired, TypedDict


class TextBlock(TypedDict):
    type: Literal["text"]
    text: str


class UrlImageBlock(TypedDict):
    type: Literal["url_image"]
    url: str


class FileImageBlock(TypedDict):
    type: Literal["file_image"]
    file_id: str


class Base64ImageBlock(TypedDict):
    type: Literal["base64_image"]
    media_type: str
    data: str


class ReasoningBlock(TypedDict):
    type: Literal["reasoning"]
    reasoning: str
    signature: NotRequired[str]


class ToolCallBlock(TypedDict):
    type: Literal["tool_call"]
    call_id: str
    tool_name: str
    arguments: dict[str, Any]


class ToolResultBlock(TypedDict):
    type: Literal["tool_result"]
    call_id: str
    result: list[TextBlock | UrlImageBlock | FileImageBlock | Base64ImageBlock]


class MessageMetadata(TypedDict):
    id: str
    pid: str
    timestamp: int


class SystemMessage(TypedDict):
    _meta: MessageMetadata
    role: Literal["system"]
    content: list[TextBlock]


class UserMessage(TypedDict):
    _meta: MessageMetadata
    role: Literal["user"]
    content: list[TextBlock | UrlImageBlock | FileImageBlock | Base64ImageBlock | ToolResultBlock]


class AssistantMessage(TypedDict):
    _meta: MessageMetadata
    role: Literal["assistant"]
    content: list[TextBlock | ReasoningBlock | ToolCallBlock]


Message = SystemMessage | UserMessage | AssistantMessage


class MessageTreeNode(TypedDict):
    data: Message
    sub_nodes: list[MessageTreeNode]


class Session(ABC):
    @abstractmethod
    async def load_tree(self) -> MessageTreeNode: ...

    @abstractmethod
    async def expand_context(self, message: Message) -> list[Message]: ...

    @abstractmethod
    async def append_message(self, message: Message) -> None: ...


class SessionManager(ABC):
    @abstractmethod
    async def list_sessions(self) -> list[Session]: ...

    @abstractmethod
    async def create_session(self) -> Session: ...

    @abstractmethod
    async def delete_session(self, session: Session) -> None: ...

    @abstractmethod
    async def fork_session(self, session: Session) -> Session: ...
