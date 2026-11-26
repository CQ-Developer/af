from typing import Any, override

from af.core import HttpClient, Message, Provider


def load_provider_deepseek(api_key: str) -> Provider:
    return {
        "name": "deepseek",
        "base_url": "https://api.deepseek.com",
        "api_key": api_key,
        "models": [
            {
                "name": "deepseek-flash",
                "context_length": 1048576,
                "max_tokens": 393216,
                "reasoning_effort": ["none", "low", "high", "max"],
                "input_modalities": ["text", "image"],
            }
        ],
    }


class DeepSeekHttpClient(HttpClient[Any]):
    @override
    async def send_messages(self, messages: list[Message]) -> Any:
        return None
