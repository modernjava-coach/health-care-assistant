import os
import sys

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.providers.bedrock import BedrockProvider
from app.core.config import settings

def test_openai_provider():
    print(f"Testing BedrockProvider with model: {settings.BEDROCK_MODEL_ID}")
    
    provider = BedrockProvider()
    
    # Test SOAP Note Generation
    print("\nTesting SOAP Note Generation...")
    soap_note = provider.generate_soap_note(
        "Patient presents with a sore throat and fever of 101. Exam shows tonsillar exudate. Strep test positive. Prescribed Amoxicillin."
    )
    print("SOAP Note Result:")
    print(f"Subjective: {soap_note.subjective}")
    print(f"Assessment: {soap_note.assessment}")
    print(f"Plan: {soap_note.plan}")
    print(f"Provider: {soap_note.ai_provider}")
    
    # Test Medical Code Generation
    print("\nTesting Medical Code Generation...")
    codes = provider.generate_medical_codes(
        "Patient diagnosed with Type 2 Diabetes (E11.9). Prescribed Metformin. Office visit level 3."
    )
    print("Medical Codes Result:")
    for code in codes.icd10_codes:
        print(f"ICD-10: {code.code} - {code.description}")
    for code in codes.cpt_codes:
        print(f"CPT: {code.code} - {code.description}")

if __name__ == "__main__":
    test_openai_provider()
