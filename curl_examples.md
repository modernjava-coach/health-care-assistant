# FastAPI Endpoint cURL Examples

## Prerequisites

Make sure the FastAPI server is running:
```bash
uvicorn app.main:app --reload
```

## 1. Generate SOAP Note from Text

```bash
curl -X POST "http://localhost:8000/api/v1/medical/generate-soap?provider=aws" \
  -H "Content-Type: application/json" \
  -d '{"text": "Patient presents with severe headache and sensitivity to light. Reports nausea but no vomiting. Pain level 8/10. BP 130/85, Pulse 88, Temp 98.6F.", "patient_id": "P001"}'
```

## 2. Generate SOAP Note from Image Upload

**Windows (PowerShell):**
```powershell
curl -X POST "http://localhost:8000/api/v1/medical/generate-soap-upload?provider=aws" `
  -F "file=@sample_note.png" `
  -F "patient_id=P001"
```

**Linux/Mac:**
```bash
curl -X POST "http://localhost:8000/api/v1/medical/generate-soap-upload?provider=aws" \
  -F "file=@sample_note.png" \
  -F "patient_id=P001"
```

## 3. Generate Medical Codes from Text

```bash
curl -X POST "http://localhost:8000/api/v1/medical/generate-codes?provider=aws" \
  -H "Content-Type: application/json" \
  -d '{"text": "Patient diagnosed with migraine headache. Treatment plan includes Sumatriptan 100mg.", "patient_id": "P001", "encounter_id": "E001"}'
```

## 4. Generate Medical Codes from Image Upload

**Windows (PowerShell):**
```powershell
curl -X POST "http://localhost:8000/api/v1/medical/generate-codes-upload?provider=aws" `
  -F "file=@realistic_note.png" `
  -F "patient_id=P002" `
  -F "encounter_id=E002"
```

**Linux/Mac:**
```bash
curl -X POST "http://localhost:8000/api/v1/medical/generate-codes-upload?provider=aws" \
  -F "file=@realistic_note.png" \
  -F "patient_id=P002" \
  -F "encounter_id=E002"
```

