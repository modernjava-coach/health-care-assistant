from llm_provider import LLMProvider
from bedrock_provider import BedrockProvider
from vertex_provider import VertexProvider
import os

class ProviderFactory:
    @staticmethod
    def get_provider(provider_name: str) -> LLMProvider:
        provider_name = provider_name.lower()
        
        if provider_name == "aws" or provider_name == "bedrock":
            return BedrockProvider()
        elif provider_name == "google" or provider_name == "vertex":
            # You might want to load project_id from env here if strictly needed
            return VertexProvider()
        else:
            raise ValueError(f"Unknown provider: {provider_name}. Use 'aws' or 'google'.")
