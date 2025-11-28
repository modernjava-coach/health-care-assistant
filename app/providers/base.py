from abc import ABC, abstractmethod
from typing import List, Dict, Any

class LLMProvider(ABC):
    """
    Abstract base class for LLM providers (e.g., AWS Bedrock, Google Vertex AI).
    """

    @abstractmethod
    def generate_soap_note(self, text: str) -> str:
        """
        Generates a SOAP note from the given text.
        
        Args:
            text (str): Raw patient notes or transcript.
            
        Returns:
            str: The generated SOAP note.
        """
        pass

    @abstractmethod
    def generate_medical_codes(self, text: str) -> List[Dict[str, Any]]:
        """
        Extracts medical codes (ICD-10, CPT) from the given text.
        
        Args:
            text (str): Clinical text.
            
        Returns:
            List[Dict[str, Any]]: A list of dictionaries representing the codes.
            Example: [{"code": "R51", "description": "Headache", "type": "ICD-10"}]
        """
        pass
