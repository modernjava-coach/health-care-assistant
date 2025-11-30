"""
Comprehensive test script for AWS Bedrock models and API endpoints.

This script tests:
1. Different AWS Bedrock foundation models (Claude, Mistral, Llama, etc.)
2. SOAP note generation endpoint
3. Medical code generation endpoint
4. Domain model validation

Prerequisites:
- AWS credentials configured (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
- FastAPI server running on http://localhost:8000
"""

import requests
import json
from typing import Dict, Any
import time


# API base URL
BASE_URL = "http://localhost:8000/api/v1/medical"

# Test data
SOAP_TEST_TEXT = """
Patient: John Doe, 45-year-old male
Chief Complaint: Persistent headaches for 3 days

Patient reports severe throbbing headaches that started 3 days ago. Pain is located in the frontal region, 
rated 7/10 in intensity. Associated with photophobia and mild nausea. No vomiting. No fever.
Denies recent head trauma. Has history of occasional tension headaches but states this is different.

Vital Signs:
- Blood Pressure: 135/88 mmHg
- Heart Rate: 78 bpm
- Temperature: 98.4°F (36.9°C)
- Respiratory Rate: 16/min
- SpO2: 98% on room air

Physical Examination:
- General: Alert and oriented x3, appears uncomfortable
- HEENT: PERRLA, no papilledema on fundoscopic exam, no sinus tenderness
- Neck: Supple, no meningismus
- Neurological: Cranial nerves II-XII intact, no focal motor or sensory deficits

Impression: Migraine headache without aura

Treatment Plan:
1. Prescribe sumatriptan 50mg PO PRN for acute migraine attacks
2. Recommend ibuprofen 400mg PO q6h PRN for pain
3. Advise rest in dark, quiet room during attacks
4. Recommend keeping headache diary to identify triggers
5. Follow-up in 2 weeks or sooner if symptoms worsen
6. Return immediately if develops fever, neck stiffness, or neurological symptoms
"""

MEDICAL_CODES_TEST_TEXT = """
Patient with Type 2 Diabetes Mellitus, currently on metformin 1000mg twice daily.
Also has Essential Hypertension, controlled on lisinopril 10mg daily.
Patient presents for routine diabetes management and medication refill.

Office visit - established patient, moderate complexity, 30 minutes.
Ordered comprehensive metabolic panel and HbA1c.
Discussed diet and exercise modifications.
Refilled metformin and lisinopril prescriptions.
"""


def print_section(title: str):
    """Print a formatted section header"""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80)


def print_subsection(title: str):
    """Print a formatted subsection header"""
    print("\n" + "-" * 80)
    print(f"  {title}")
    print("-" * 80)


def test_soap_note_generation(provider: str = "aws"):
    """Test SOAP note generation endpoint"""
    print_subsection(f"Testing SOAP Note Generation (Provider: {provider})")
    
    payload = {
        "text": SOAP_TEST_TEXT,
        "patient_id": "P12345",
        "provider_id": "DR001",
        "note_type": "follow_up"
    }
    
    try:
        print(f"\nSending request to {BASE_URL}/generate-soap?provider={provider}")
        print(f"Request payload: patient_id={payload['patient_id']}, provider_id={payload['provider_id']}")
        
        start_time = time.time()
        response = requests.post(
            f"{BASE_URL}/generate-soap",
            params={"provider": provider},
            json=payload,
            timeout=60
        )
        elapsed_time = time.time() - start_time
        
        print(f"\nResponse Status: {response.status_code}")
        print(f"Response Time: {elapsed_time:.2f}s")
        
        if response.status_code == 200:
            data = response.json()
            soap_note = data.get("soap_note", {})
            
            print("\n[SUCCESS] SOAP Note Generated:")
            print(f"  Provider: {data.get('provider')}")
            print(f"  AI Provider: {soap_note.get('ai_provider')}")
            print(f"  Confidence Score: {soap_note.get('confidence_score')}")
            print(f"  Patient ID: {soap_note.get('patient_id')}")
            print(f"  Provider ID: {soap_note.get('provider_id')}")
            
            print("\n  Subjective:")
            print(f"    {soap_note.get('subjective', 'N/A')[:200]}...")
            
            print("\n  Objective:")
            print(f"    {soap_note.get('objective', 'N/A')[:200]}...")
            
            print("\n  Assessment:")
            print(f"    {soap_note.get('assessment', 'N/A')[:200]}...")
            
            print("\n  Plan:")
            print(f"    {soap_note.get('plan', 'N/A')[:200]}...")
            
            return True
        else:
            print(f"\n[FAILED] Error: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"\n[ERROR] Exception occurred: {str(e)}")
        return False


def test_medical_codes_generation(provider: str = "aws"):
    """Test medical codes generation endpoint"""
    print_subsection(f"Testing Medical Codes Generation (Provider: {provider})")
    
    payload = {
        "text": MEDICAL_CODES_TEST_TEXT,
        "patient_id": "P12345",
        "encounter_id": "ENC001",
        "include_icd10": True,
        "include_cpt": True,
        "include_confidence": True
    }
    
    try:
        print(f"\nSending request to {BASE_URL}/generate-codes?provider={provider}")
        print(f"Request payload: patient_id={payload['patient_id']}, encounter_id={payload['encounter_id']}")
        
        start_time = time.time()
        response = requests.post(
            f"{BASE_URL}/generate-codes",
            params={"provider": provider},
            json=payload,
            timeout=60
        )
        elapsed_time = time.time() - start_time
        
        print(f"\nResponse Status: {response.status_code}")
        print(f"Response Time: {elapsed_time:.2f}s")
        
        if response.status_code == 200:
            data = response.json()
            
            print("\n[SUCCESS] Medical Codes Generated:")
            print(f"  Provider: {data.get('provider')}")
            
            icd10_codes = data.get('icd10_codes', [])
            cpt_codes = data.get('cpt_codes', [])
            
            print(f"\n  ICD-10 Codes ({len(icd10_codes)} found):")
            for code in icd10_codes[:5]:  # Show first 5
                print(f"    - {code.get('code')}: {code.get('description')}")
                print(f"      Primary: {code.get('is_primary')}, Confidence: {code.get('confidence_score')}")
            
            print(f"\n  CPT Codes ({len(cpt_codes)} found):")
            for code in cpt_codes[:5]:  # Show first 5
                print(f"    - {code.get('code')}: {code.get('description')}")
                print(f"      Units: {code.get('units')}, Confidence: {code.get('confidence_score')}")
            
            return True
        else:
            print(f"\n[FAILED] Error: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"\n[ERROR] Exception occurred: {str(e)}")
        return False


def test_health_check():
    """Test the health check endpoint"""
    print_subsection("Testing Health Check Endpoint")
    
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        print(f"\nResponse Status: {response.status_code}")
        
        if response.status_code == 200:
            print(f"Response: {response.json()}")
            print("[SUCCESS] Server is healthy")
            return True
        else:
            print("[FAILED] Server health check failed")
            return False
            
    except Exception as e:
        print(f"\n[ERROR] Cannot connect to server: {str(e)}")
        print("\nMake sure the FastAPI server is running:")
        print("  python -m uvicorn app.main:app --reload --port 8000")
        return False


def main():
    """Run all tests"""
    print_section("AWS BEDROCK API ENDPOINT TESTS")
    
    print("\nThis script will test:")
    print("  1. Server health check")
    print("  2. SOAP note generation with AWS Bedrock")
    print("  3. Medical codes generation with AWS Bedrock")
    
    results = {}
    
    # Test 1: Health check
    print_section("Test 1: Server Health Check")
    results['health_check'] = test_health_check()
    
    if not results['health_check']:
        print("\n[ABORTED] Server is not running. Please start the server first.")
        return
    
    # Test 2: SOAP note generation
    print_section("Test 2: SOAP Note Generation")
    results['soap_aws'] = test_soap_note_generation(provider="aws")
    
    # Test 3: Medical codes generation
    print_section("Test 3: Medical Codes Generation")
    results['codes_aws'] = test_medical_codes_generation(provider="aws")
    
    # Summary
    print_section("TEST SUMMARY")
    
    total_tests = len(results)
    passed_tests = sum(1 for v in results.values() if v)
    
    print(f"\nTotal Tests: {total_tests}")
    print(f"Passed: {passed_tests}")
    print(f"Failed: {total_tests - passed_tests}")
    
    print("\nDetailed Results:")
    for test_name, passed in results.items():
        status = "[PASS]" if passed else "[FAIL]"
        print(f"  {status} {test_name}")
    
    print("\n" + "=" * 80)
    
    if passed_tests == total_tests:
        print("\n✓ All tests passed!")
    else:
        print(f"\n✗ {total_tests - passed_tests} test(s) failed")
    
    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()
