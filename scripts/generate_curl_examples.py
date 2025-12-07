"""
Script to generate curl commands and test the FastAPI endpoints.
This will create curl examples for documentation.
"""
import subprocess
import json
import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
BASE_URL = "http://localhost:8000/api/v1/medical"

def run_curl_command(curl_cmd):
    """Execute a curl command and return the response"""
    try:
        result = subprocess.run(
            curl_cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=60
        )
        return result.stdout, result.stderr, result.returncode
    except Exception as e:
        return "", str(e), 1

def test_soap_upload_endpoint():
    """Test SOAP note generation with file upload"""
    print("\n" + "="*80)
    print("cURL Command: SOAP Note Generation (File Upload)")
    print("="*80)
    
    image_path = PROJECT_ROOT / "sample_note.png"
    
    curl_cmd = f'''curl -X POST "{BASE_URL}/generate-soap-upload?provider=aws" ^
  -F "file=@{image_path}" ^
  -F "patient_id=P001"'''
    
    print("\nCommand:")
    print(curl_cmd)
    
    # Execute the command
    stdout, stderr, returncode = run_curl_command(curl_cmd)
    
    print("\nResponse:")
    if returncode == 0 and stdout:
        try:
            response_json = json.loads(stdout)
            print(json.dumps(response_json, indent=2))
        except:
            print(stdout)
    else:
        print(f"Error: {stderr}")
    
    return curl_cmd, stdout

def test_codes_upload_endpoint():
    """Test medical code generation with file upload"""
    print("\n" + "="*80)
    print("cURL Command: Medical Code Generation (File Upload)")
    print("="*80)
    
    image_path = PROJECT_ROOT / "realistic_note.png"
    
    curl_cmd = f'''curl -X POST "{BASE_URL}/generate-codes-upload?provider=aws" ^
  -F "file=@{image_path}" ^
  -F "patient_id=P002"'''
    
    print("\nCommand:")
    print(curl_cmd)
    
    # Execute the command
    stdout, stderr, returncode = run_curl_command(curl_cmd)
    
    print("\nResponse:")
    if returncode == 0 and stdout:
        try:
            response_json = json.loads(stdout)
            print(json.dumps(response_json, indent=2))
        except:
            print(stdout)
    else:
        print(f"Error: {stderr}")
    
    return curl_cmd, stdout

def test_soap_text_endpoint():
    """Test SOAP note generation with text input"""
    print("\n" + "="*80)
    print("cURL Command: SOAP Note Generation (Text Input)")
    print("="*80)
    
    curl_cmd = f'''curl -X POST "{BASE_URL}/generate-soap?provider=aws" ^
  -H "Content-Type: application/json" ^
  -d "{{\\\"text\\\": \\\"Patient presents with severe headache and sensitivity to light. Reports nausea but no vomiting. Pain level 8/10. BP 130/85, Pulse 88, Temp 98.6F.\\\", \\\"patient_id\\\": \\\"P001\\\"}}"'''
    
    print("\nCommand:")
    print(curl_cmd)
    
    # Execute the command
    stdout, stderr, returncode = run_curl_command(curl_cmd)
    
    print("\nResponse:")
    if returncode == 0 and stdout:
        try:
            response_json = json.loads(stdout)
            print(json.dumps(response_json, indent=2))
        except:
            print(stdout)
    else:
        print(f"Error: {stderr}")
    
    return curl_cmd, stdout

def save_curl_examples():
    """Save curl examples to a file"""
    output_file = PROJECT_ROOT / "curl_examples.md"
    
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("# FastAPI Endpoint cURL Examples\n\n")
        f.write("## Prerequisites\n\n")
        f.write("Make sure the FastAPI server is running:\n")
        f.write("```bash\n")
        f.write("uvicorn app.main:app --reload\n")
        f.write("```\n\n")
        
        f.write("## 1. Generate SOAP Note from Text\n\n")
        f.write("```bash\n")
        f.write(f'''curl -X POST "http://localhost:8000/api/v1/medical/generate-soap?provider=aws" \\
  -H "Content-Type: application/json" \\
  -d '{{"text": "Patient presents with severe headache and sensitivity to light. Reports nausea but no vomiting. Pain level 8/10. BP 130/85, Pulse 88, Temp 98.6F.", "patient_id": "P001"}}'\n''')
        f.write("```\n\n")
        
        f.write("## 2. Generate SOAP Note from Image Upload\n\n")
        f.write("**Windows (PowerShell):**\n")
        f.write("```powershell\n")
        f.write(f'''curl -X POST "http://localhost:8000/api/v1/medical/generate-soap-upload?provider=aws" `
  -F "file=@sample_note.png" `
  -F "patient_id=P001"\n''')
        f.write("```\n\n")
        
        f.write("**Linux/Mac:**\n")
        f.write("```bash\n")
        f.write(f'''curl -X POST "http://localhost:8000/api/v1/medical/generate-soap-upload?provider=aws" \\
  -F "file=@sample_note.png" \\
  -F "patient_id=P001"\n''')
        f.write("```\n\n")
        
        f.write("## 3. Generate Medical Codes from Text\n\n")
        f.write("```bash\n")
        f.write(f'''curl -X POST "http://localhost:8000/api/v1/medical/generate-codes?provider=aws" \\
  -H "Content-Type: application/json" \\
  -d '{{"text": "Patient diagnosed with migraine headache. Treatment plan includes Sumatriptan 100mg.", "patient_id": "P001", "encounter_id": "E001"}}'\n''')
        f.write("```\n\n")
        
        f.write("## 4. Generate Medical Codes from Image Upload\n\n")
        f.write("**Windows (PowerShell):**\n")
        f.write("```powershell\n")
        f.write(f'''curl -X POST "http://localhost:8000/api/v1/medical/generate-codes-upload?provider=aws" `
  -F "file=@realistic_note.png" `
  -F "patient_id=P002" `
  -F "encounter_id=E002"\n''')
        f.write("```\n\n")
        
        f.write("**Linux/Mac:**\n")
        f.write("```bash\n")
        f.write(f'''curl -X POST "http://localhost:8000/api/v1/medical/generate-codes-upload?provider=aws" \\
  -F "file=@realistic_note.png" \\
  -F "patient_id=P002" \\
  -F "encounter_id=E002"\n''')
        f.write("```\n\n")
    
    print(f"\n[SUCCESS] Saved curl examples to: {output_file}")

def main():
    print("\n" + "="*80)
    print("GENERATING cURL EXAMPLES FOR FASTAPI ENDPOINTS")
    print("="*80)
    
    # Save curl examples
    save_curl_examples()
    
    print("\n" + "="*80)
    print("NOTE: To test these commands, start the FastAPI server first:")
    print("  uvicorn app.main:app --reload")
    print("="*80)

if __name__ == "__main__":
    main()
