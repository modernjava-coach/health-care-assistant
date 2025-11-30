import sys
import os
from unittest.mock import MagicMock, patch

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.llm_service import LLMService
from app.models import SOAPNote, MedicalCodeResponse

def test_langchain_pipeline():
    print("Testing LangChain Pipeline...")
    
    # Mock OCR Service and Chain Factories
    with patch('app.services.llm_service.OCRService') as MockOCR, \
         patch('app.services.llm_service.get_soap_note_chain') as MockSoapChain, \
         patch('app.services.llm_service.get_medical_code_chain') as MockCodeChain:
        
        # Setup Mocks
        mock_ocr = MockOCR.return_value
        mock_ocr.extract_text.return_value = "Patient has a sore throat and fever. Strep test positive."
        
        mock_soap_chain = MockSoapChain.return_value
        mock_soap_response = SOAPNote(
            subjective="Patient has sore throat",
            objective="Fever",
            assessment="Strep throat",
            plan="Antibiotics",
            generated_by_ai=True
        )
        mock_soap_chain.invoke.return_value = mock_soap_response
        
        mock_code_chain = MockCodeChain.return_value
        mock_codes_response = MedicalCodeResponse(
            icd10_codes=[],
            cpt_codes=[],
            provider="aws"
        )
        mock_code_chain.invoke.return_value = mock_codes_response
        
        # Initialize Service (now uses mocks)
        service = LLMService()

        # 1. Test Text-based SOAP
        print("\n1. Testing Text-based SOAP Generation...")
        soap = service.generate_soap_note("Raw text input")
        print(f"Result: {soap.assessment}")
        assert soap.assessment == "Strep throat"

        # 2. Test File-based SOAP (Mocked OCR)
        print("\n2. Testing File-based SOAP Generation (Mocked OCR)...")
        soap_file = service.generate_soap_note_from_file(b"fake_pdf_bytes", "application/pdf")
        print(f"Result: {soap_file.assessment}")
        assert soap_file.assessment == "Strep throat"
        mock_ocr.extract_text.assert_called_with(b"fake_pdf_bytes", "application/pdf")

        print("\nSuccess! Pipeline wiring is correct.")

if __name__ == "__main__":
    test_langchain_pipeline()
