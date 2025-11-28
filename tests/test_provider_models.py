"""
Test script to verify that providers return domain model objects.
This demonstrates the updated provider functionality.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.providers.bedrock import BedrockProvider
from app.providers.vertex import VertexProvider
from app.models import SOAPNote, MedicalCodeResponse


def test_bedrock_soap_note():
    """Test Bedrock provider returns SOAPNote object"""
    print("=" * 80)
    print("Testing Bedrock Provider - SOAP Note Generation")
    print("=" * 80)
    
    try:
        provider = BedrockProvider()
        
        test_text = """
        Patient came in complaining of severe headaches for the past 3 days.
        Blood pressure was 130/85, heart rate 78, temperature 98.6°F.
        Patient appears alert and oriented. No neurological deficits noted.
        Diagnosed with tension headaches likely due to stress.
        Prescribed ibuprofen 400mg as needed and recommended stress management techniques.
        Follow-up in 2 weeks if symptoms persist.
        """
        
        result = provider.generate_soap_note(
            text=test_text,
            patient_id="P12345",
            provider_id="DR001"
        )
        
        # Verify it's a SOAPNote object
        assert isinstance(result, SOAPNote), f"Expected SOAPNote, got {type(result)}"
        
        print(f"✓ Returned type: {type(result).__name__}")
        print(f"✓ Patient ID: {result.patient_id}")
        print(f"✓ Provider ID: {result.provider_id}")
        print(f"✓ AI Provider: {result.ai_provider}")
        print(f"✓ Confidence Score: {result.confidence_score}")
        print(f"\nSubjective: {result.subjective[:100]}...")
        print(f"Objective: {result.objective[:100]}...")
        print(f"Assessment: {result.assessment[:100]}...")
        print(f"Plan: {result.plan[:100]}...")
        
        print("\n✓ Bedrock SOAP Note test PASSED\n")
        return True
        
    except Exception as e:
        print(f"\n✗ Bedrock SOAP Note test FAILED: {e}\n")
        return False


def test_bedrock_medical_codes():
    """Test Bedrock provider returns MedicalCodeResponse object"""
    print("=" * 80)
    print("Testing Bedrock Provider - Medical Code Generation")
    print("=" * 80)
    
    try:
        provider = BedrockProvider()
        
        test_text = """
        Patient with type 2 diabetes mellitus and hypertension.
        Office visit for routine diabetes management.
        Ordered comprehensive metabolic panel and HbA1c.
        """
        
        result = provider.generate_medical_codes(
            text=test_text,
            patient_id="P12345",
            encounter_id="ENC001"
        )
        
        # Verify it's a MedicalCodeResponse object
        assert isinstance(result, MedicalCodeResponse), f"Expected MedicalCodeResponse, got {type(result)}"
        
        print(f"✓ Returned type: {type(result).__name__}")
        print(f"✓ AI Provider: {result.provider}")
        print(f"✓ ICD-10 Codes: {len(result.icd10_codes) if result.icd10_codes else 0}")
        print(f"✓ CPT Codes: {len(result.cpt_codes) if result.cpt_codes else 0}")
        
        if result.icd10_codes:
            print("\nICD-10 Codes:")
            for code in result.icd10_codes[:3]:  # Show first 3
                print(f"  - {code.get('code', 'N/A')}: {code.get('description', 'N/A')}")
        
        if result.cpt_codes:
            print("\nCPT Codes:")
            for code in result.cpt_codes[:3]:  # Show first 3
                print(f"  - {code.get('code', 'N/A')}: {code.get('description', 'N/A')}")
        
        print("\n✓ Bedrock Medical Codes test PASSED\n")
        return True
        
    except Exception as e:
        print(f"\n✗ Bedrock Medical Codes test FAILED: {e}\n")
        return False


def test_vertex_soap_note():
    """Test Vertex provider returns SOAPNote object"""
    print("=" * 80)
    print("Testing Vertex AI Provider - SOAP Note Generation")
    print("=" * 80)
    
    try:
        # Note: This requires Google Cloud credentials
        provider = VertexProvider()
        
        test_text = """
        Patient reports persistent cough for 5 days.
        Vital signs: BP 120/80, HR 72, Temp 99.1°F, SpO2 98%.
        Lungs clear to auscultation bilaterally.
        Diagnosis: Upper respiratory infection.
        Prescribed dextromethorphan for cough suppression.
        """
        
        result = provider.generate_soap_note(
            text=test_text,
            patient_id="P67890",
            provider_id="DR002"
        )
        
        # Verify it's a SOAPNote object
        assert isinstance(result, SOAPNote), f"Expected SOAPNote, got {type(result)}"
        
        print(f"✓ Returned type: {type(result).__name__}")
        print(f"✓ Patient ID: {result.patient_id}")
        print(f"✓ Provider ID: {result.provider_id}")
        print(f"✓ AI Provider: {result.ai_provider}")
        print(f"✓ Confidence Score: {result.confidence_score}")
        
        print("\n✓ Vertex SOAP Note test PASSED\n")
        return True
        
    except Exception as e:
        print(f"\n✗ Vertex SOAP Note test FAILED (may need credentials): {e}\n")
        return False


def test_service_layer():
    """Test that service layer properly passes through domain models"""
    print("=" * 80)
    print("Testing Service Layer Integration")
    print("=" * 80)
    
    try:
        from app.services.llm_service import LLMService
        
        service = LLMService()
        
        test_text = "Patient with headache. BP 120/80. Diagnosed with tension headache."
        
        result = service.generate_soap_note(
            text=test_text,
            provider_name="aws",
            patient_id="TEST123"
        )
        
        assert isinstance(result, SOAPNote), f"Expected SOAPNote, got {type(result)}"
        
        print(f"✓ Service layer returns: {type(result).__name__}")
        print(f"✓ Patient ID preserved: {result.patient_id}")
        
        print("\n✓ Service Layer test PASSED\n")
        return True
        
    except Exception as e:
        print(f"\n✗ Service Layer test FAILED: {e}\n")
        return False


if __name__ == "__main__":
    print("\n" + "=" * 80)
    print("PROVIDER DOMAIN MODEL INTEGRATION TESTS")
    print("=" * 80 + "\n")
    
    results = []
    
    # Test Bedrock provider
    results.append(("Bedrock SOAP", test_bedrock_soap_note()))
    results.append(("Bedrock Codes", test_bedrock_medical_codes()))
    
    # Test Vertex provider (may fail without credentials)
    results.append(("Vertex SOAP", test_vertex_soap_note()))
    
    # Test service layer
    results.append(("Service Layer", test_service_layer()))
    
    # Summary
    print("\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    
    for test_name, passed in results:
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"{test_name:20s}: {status}")
    
    total = len(results)
    passed = sum(1 for _, p in results if p)
    
    print(f"\nTotal: {passed}/{total} tests passed")
    print("=" * 80 + "\n")
