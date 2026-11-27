from abc import ABC, abstractmethod
from typing import Literal, NotRequired, TypedDict


class Model(TypedDict):
    name: str
    context_length: int
    max_tokens: int
    reasoning_effort: list[str]
    input_modalities: list[
        Literal[
            "text",
            "image",
        ]
    ]


class Provider(TypedDict):
    name: str
    base_url: str
    api_key: NotRequired[str]
    protocol_type: NotRequired[
        Literal[
            "openai/chat-completion",
            "openai/response",
            "anthropic/message",
        ]
    ]
    models: list[Model]


class ProviderManager(ABC):
    @abstractmethod
    async def load_providers(self) -> list[Provider]: ...
