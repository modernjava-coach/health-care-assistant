import sys
import os
import io
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from PIL import Image, ImageDraw

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Wrap imports in a context manager to provide dummy credentials ONLY during import
# this satisfies ChatBedrock validation without polluting the environment for other tests
with patch.dict(os.environ, {
    "AWS_ACCESS_KEY_ID": "testing",
    "AWS_SECRET_ACCESS_KEY": "testing", 
    "AWS_DEFAULT_REGION": "us-east-1"
}):
    from app.main import app
    from app.models import SOAPNote
    # Import the actual service instance used by the API
    from app.api.routes import llm_service

def create_dummy_medical_image():
    """Create a simple image with medical text."""
    img = Image.new('RGB', (800, 600), color='white')
    d = ImageDraw.Draw(img)
    # We can't easily load fonts without knowing system paths, so we'll just rely on the fact 
    # that we are mocking the OCR anyway. The image content doesn't matter for the mock, 
    # but it matters that it IS a valid image file.
    d.text((10, 10), "Patient: Jane Doe", fill=(0, 0, 0))
    d.text((10, 30), "Subjective: C/O Migraine", fill=(0, 0, 0))
    
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)
    return img_byte_arr

def test_image_upload_endpoint():
    print("Testing /generate-soap-upload with Image...")

    # Mock the services
    # We must patch the INSTANCE because it's already initialized in app.api.routes
    with patch.object(llm_service, 'ocr_service') as mock_ocr_service, \
         patch.object(llm_service, 'soap_chain') as mock_soap_chain:
        
        # Setup OCR Mock
        mock_ocr_service.extract_text.return_value = "Patient: Jane Doe\nSubjective: C/O Migraine"
        
        # Setup LLM Mock
        # The chain invoke method
        mock_response = SOAPNote(
            subjective="Patient reports migraine",
            objective="None recorded",
            assessment="Migraine",
            plan="Rest",
            generated_by_ai=True,
            ai_provider="aws"
        )
        mock_soap_chain.invoke.return_value = mock_response

        # Create Test Client
        client = TestClient(app)
        
        # Create Image
        img_bytes = create_dummy_medical_image()
        
        # Make Request
        response = client.post(
            "/api/v1/medical/generate-soap-upload",
            files={"file": ("note.png", img_bytes, "image/png")},
            data={"patient_id": "P123", "provider": "aws"}
        )
        
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print("Response:")
            print(f"Subjective: {data['soap_note']['subjective']}")
            print(f"Assessment: {data['soap_note']['assessment']}")
            print(f"Provider: {data['provider']}")
            
            assert data['soap_note']['assessment'] == "Migraine"
            print("\nSUCCESS: Image upload and processing flow verified.")
        else:
            print(f"Error: {response.text}")
            raise Exception("Test failed")

if __name__ == "__main__":
    test_image_upload_endpoint()
