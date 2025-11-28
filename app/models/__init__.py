"""
Domain models for the Healthcare AI Assistant.

This package contains Pydantic models for:
- SOAP notes (Subjective, Objective, Assessment, Plan)
- ICD-10 codes (International Classification of Diseases)
- CPT codes (Current Procedural Terminology)
"""

from .soap_note import (
    SOAPNote,
    SOAPNoteType,
    SOAPNoteRequest,
    SOAPNoteResponse
)

from .icd10_code import (
    ICD10Code,
    ICD10CodeSet,
    ICD10Category,
    ICD10CodeType
)

from .cpt_code import (
    CPTCode,
    CPTCodeSet,
    CPTCategory,
    CPTModifier,
    MedicalCodeRequest,
    MedicalCodeResponse
)

__all__ = [
    # SOAP Note models
    "SOAPNote",
    "SOAPNoteType",
    "SOAPNoteRequest",
    "SOAPNoteResponse",
    
    # ICD-10 models
    "ICD10Code",
    "ICD10CodeSet",
    "ICD10Category",
    "ICD10CodeType",
    
    # CPT models
    "CPTCode",
    "CPTCodeSet",
    "CPTCategory",
    "CPTModifier",
    "MedicalCodeRequest",
    "MedicalCodeResponse",
]
