from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from provider_factory import ProviderFactory
import uvicorn

app = FastAPI(title="Healthcare AI Assistant", description="API for SOAP Note and Medical Code Generation using AWS Bedrock and Google Vertex AI")

# --- Pydantic Models ---
class NoteRequest(BaseModel):
    text: str

class SOAPResponse(BaseModel):
    soap_note: str
    provider: str

class CodeRequest(BaseModel):
    text: str

class CodeResponse(BaseModel):
    codes: List[Dict[str, Any]]
    provider: str

# --- Endpoints ---

@app.post("/generate-soap", response_model=SOAPResponse)
async def generate_soap_note(
    request: NoteRequest, 
    provider: str = Query("aws", description="Provider to use: 'aws' or 'google'")
):
    try:
        llm_provider = ProviderFactory.get_provider(provider)
        soap_note = llm_provider.generate_soap_note(request.text)
        return SOAPResponse(soap_note=soap_note, provider=provider)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate-codes", response_model=CodeResponse)
async def generate_medical_codes(
    request: CodeRequest, 
    provider: str = Query("aws", description="Provider to use: 'aws' or 'google'")
):
    try:
        llm_provider = ProviderFactory.get_provider(provider)
        codes = llm_provider.generate_medical_codes(request.text)
        return CodeResponse(codes=codes, provider=provider)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
