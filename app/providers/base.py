from abc import ABC, abstractmethod
from typing import Optional
from ..models import SOAPNote, MedicalCodeResponse

class LLMProvider(ABC):
    """
    Abstract base class for LLM providers (e.g., AWS Bedrock, Google Vertex AI).
    """

    @abstractmethod
    def generate_soap_note(self, text: str, patient_id: Optional[str] = None, 
                          provider_id: Optional[str] = None) -> SOAPNote:
        """
        Generates a SOAP note from the given text.
        
        Args:
            text (str): Raw patient notes or transcript.
            patient_id (Optional[str]): Patient identifier.
            provider_id (Optional[str]): Provider identifier.
            
        Returns:
            SOAPNote: The generated SOAP note as a domain model object.
        """
        pass

    @abstractmethod
    def generate_medical_codes(self, text: str, patient_id: Optional[str] = None,
                              encounter_id: Optional[str] = None) -> MedicalCodeResponse:
        """
        Extracts medical codes (ICD-10, CPT) from the given text.
        
        Args:
            text (str): Clinical text.
            patient_id (Optional[str]): Patient identifier.
            encounter_id (Optional[str]): Encounter identifier.
            
        Returns:
            MedicalCodeResponse: Response containing ICD-10 and CPT codes as domain model objects.
        """
        pass
