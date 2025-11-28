from ..providers.base import LLMProvider
from ..providers.bedrock import BedrockProvider
from ..providers.vertex import VertexProvider

class ProviderFactory:
    @staticmethod
    def get_provider(provider_name: str) -> LLMProvider:
        if provider_name.lower() == "aws":
            return BedrockProvider()
        elif provider_name.lower() == "google":
            return VertexProvider()
        else:
            raise ValueError(f"Unknown provider: {provider_name}")
