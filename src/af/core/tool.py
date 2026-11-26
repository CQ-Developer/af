from abc import ABC, abstractmethod
from typing import Any


class Tool[R](ABC):
    @property
    @abstractmethod
    def name(self) -> str: ...

    @property
    @abstractmethod
    def description(self) -> str: ...

    @property
    @abstractmethod
    def parameter_schema(self) -> dict[str, Any]: ...

    @abstractmethod
    async def execute(self, p: dict[str, Any]) -> R: ...


class ToolManager(ABC):
    @abstractmethod
    def list_tools(self) -> list[Tool[Any]]: ...

    @abstractmethod
    def load_tool(self, tool: Tool[Any]): ...

    @abstractmethod
    def unload_tool(self, name: str): ...

    @abstractmethod
    def enable_tool(self, name: str): ...

    @abstractmethod
    def disable_tool(self, name: str): ...


class ToolExecuteException(Exception):
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)
