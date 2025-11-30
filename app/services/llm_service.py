from typing import Optional
from ..chains.soap_chain import get_soap_note_chain
from ..chains.medical_code_chain import get_medical_code_chain
from .ocr_service import OCRService
from ..models import SOAPNote, MedicalCodeResponse

class LLMService:
    def __init__(self):
        self.ocr_service = OCRService()
        self.soap_chain = get_soap_note_chain()
        self.medical_code_chain = get_medical_code_chain()

    def generate_soap_note(self, text: str, provider_name: str = "aws", 
                          patient_id: Optional[str] = None,
                          provider_id: Optional[str] = None) -> SOAPNote:
        """Generate a SOAP note using LangChain."""
        # Note: provider_name is now less relevant if we default to Bedrock, 
        # but we keep the signature for compatibility or future multi-provider support.
        
        result = self.soap_chain.invoke({"text": text})
        
        # Enrich with metadata
        result.patient_id = patient_id
        result.provider_id = provider_id
        result.ai_provider = provider_name
        
        return result

    def generate_medical_codes(self, text: str, provider_name: str = "aws",
                              patient_id: Optional[str] = None,
                              encounter_id: Optional[str] = None) -> MedicalCodeResponse:
        """Generate medical codes using LangChain."""
        
        result = self.medical_code_chain.invoke({"text": text})
        
        # Enrich with metadata
        result.provider = provider_name
        
        return result

    def generate_soap_note_from_file(self, file_content: bytes, content_type: str,
                                    patient_id: Optional[str] = None,
                                    provider_id: Optional[str] = None) -> SOAPNote:
        """Generate SOAP note from file (Image/PDF)."""
        text = self.ocr_service.extract_text(file_content, content_type)
        return self.generate_soap_note(text, patient_id=patient_id, provider_id=provider_id)

    def generate_medical_codes_from_file(self, file_content: bytes, content_type: str,
                                        patient_id: Optional[str] = None,
                                        encounter_id: Optional[str] = None) -> MedicalCodeResponse:
        """Generate medical codes from file (Image/PDF)."""
        text = self.ocr_service.extract_text(file_content, content_type)
        return self.generate_medical_codes(text, patient_id=patient_id, encounter_id=encounter_id)

