from fastapi import HTTPException, Query, APIRouter
from pydantic import BaseModel
from typing import List, Dict, Any
from ..services.llm_service import LLMService

# Pydantic Models
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

# Initialize service
llm_service = LLMService()

# API Router
router = APIRouter()

@router.post("/generate-soap", response_model=SOAPResponse)
async def generate_soap_note(
    request: NoteRequest, 
    provider: str = Query("aws", description="Provider to use: 'aws' or 'google'")
):
    try:
        soap_note = llm_service.generate_soap_note(request.text, provider)
        return SOAPResponse(soap_note=soap_note, provider=provider)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/generate-codes", response_model=CodeResponse)
async def generate_medical_codes(
    request: CodeRequest, 
    provider: str = Query("aws", description="Provider to use: 'aws' or 'google'")
):
    try:
        codes = llm_service.generate_medical_codes(request.text, provider)
        return CodeResponse(codes=codes, provider=provider)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
