from typing import List, Dict, Any
from .factory import ProviderFactory

class LLMService:
    def generate_soap_note(self, text: str, provider_name: str) -> str:
        provider = ProviderFactory.get_provider(provider_name)
        return provider.generate_soap_note(text)

    def generate_medical_codes(self, text: str, provider_name: str) -> List[Dict[str, Any]]:
        provider = ProviderFactory.get_provider(provider_name)
        return provider.generate_medical_codes(text)
