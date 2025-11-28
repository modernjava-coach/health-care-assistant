from typing import Optional
from .factory import ProviderFactory
from ..models import SOAPNote, MedicalCodeResponse

class LLMService:
    def generate_soap_note(self, text: str, provider_name: str, 
                          patient_id: Optional[str] = None,
                          provider_id: Optional[str] = None) -> SOAPNote:
        """Generate a SOAP note using the specified provider."""
        provider = ProviderFactory.get_provider(provider_name)
        return provider.generate_soap_note(text, patient_id, provider_id)

    def generate_medical_codes(self, text: str, provider_name: str,
                              patient_id: Optional[str] = None,
                              encounter_id: Optional[str] = None) -> MedicalCodeResponse:
        """Generate medical codes using the specified provider."""
        provider = ProviderFactory.get_provider(provider_name)
        return provider.generate_medical_codes(text, patient_id, encounter_id)
