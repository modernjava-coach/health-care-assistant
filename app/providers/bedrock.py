import boto3
import json
import re
from typing import Optional, List
from datetime import datetime
from .base import LLMProvider
from ..models import (
    SOAPNote, 
    MedicalCodeResponse,
    ICD10Code,
    CPTCode,
    ICD10Category,
    ICD10CodeType,
    CPTCategory
)

class BedrockProvider(LLMProvider):
    def __init__(self, region_name: Optional[str] = None, model_id: Optional[str] = None):
        from ..core.config import settings
        self.region_name = region_name or settings.AWS_REGION
        self.model_id = model_id or settings.BEDROCK_MODEL_ID
        self.client = boto3.client("bedrock-runtime", region_name=self.region_name)
        self.provider_name = "aws"

    def _invoke_model(self, system_prompt: str, user_message: str) -> str:
        if "anthropic" in self.model_id.lower():
            return self._invoke_claude(system_prompt, user_message)
        else:
            return self._invoke_openai_style(system_prompt, user_message)

    def _invoke_claude(self, system_prompt: str, user_message: str) -> str:
        payload = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 4096,
            "system": system_prompt,
            "messages": [
                {
                    "role": "user",
                    "content": user_message
                }
            ],
            "temperature": 0.0
        }
        return self._call_bedrock(payload)

    def _invoke_openai_style(self, system_prompt: str, user_message: str) -> str:
        # OpenAI/GPT models on Bedrock typically use the standard chat completion format
        # but the specific payload structure for Bedrock's "InvokeModel" might vary slightly
        # depending on the specific model family. 
        # For OpenAI models on Bedrock (via custom models or marketplace), 
        # we assume standard OpenAI chat format.
        
        payload = {
            "messages": [
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ],
            "max_tokens": 4096,
            "temperature": 0.0
        }
        return self._call_bedrock(payload)

    def _call_bedrock(self, payload: dict) -> str:
        try:
            response = self.client.invoke_model(
                modelId=self.model_id,
                body=json.dumps(payload)
            )
            response_body = json.loads(response.get("body").read())
            
            # Handle different response formats
            if "content" in response_body and isinstance(response_body["content"], list):
                # Anthropic format: content[0].text
                return response_body["content"][0]["text"]
            elif "choices" in response_body:
                # OpenAI format: choices[0].message.content
                return response_body["choices"][0]["message"]["content"]
            else:
                # Fallback or error
                print(f"Unknown response format: {response_body.keys()}")
                return str(response_body)
                
        except Exception as e:
            print(f"Error invoking Bedrock model {self.model_id}: {e}")
            raise

    def generate_soap_note(self, text: str, patient_id: Optional[str] = None, 
                          provider_id: Optional[str] = None) -> SOAPNote:
        system_prompt = """You are an expert medical scribe. Convert raw patient notes into a structured SOAP note.
        Return ONLY a JSON object with these exact keys:
        - "subjective": Patient's description of symptoms and concerns
        - "objective": Observable and measurable findings (vitals, exam findings)
        - "assessment": Diagnosis or clinical impression
        - "plan": Treatment plan and follow-up instructions
        - "chief_complaint": Primary reason for visit (optional)
        - "confidence_score": Your confidence in this note (0.0-1.0)
        
        Do not include markdown formatting. Return only the JSON object."""
        
        response_text = self._invoke_model(system_prompt, text)
        
        # Clean and parse JSON
        cleaned_text = response_text.strip()
        if cleaned_text.startswith("```json"):
            cleaned_text = cleaned_text[7:]
        if cleaned_text.startswith("```"):
            cleaned_text = cleaned_text[3:]
        if cleaned_text.endswith("```"):
            cleaned_text = cleaned_text[:-3]
        
        try:
            soap_data = json.loads(cleaned_text.strip())
            
            # Create SOAPNote domain model
            return SOAPNote(
                patient_id=patient_id,
                provider_id=provider_id,
                encounter_date=datetime.utcnow(),
                subjective=soap_data.get("subjective", ""),
                objective=soap_data.get("objective", ""),
                assessment=soap_data.get("assessment", ""),
                plan=soap_data.get("plan", ""),
                chief_complaint=soap_data.get("chief_complaint"),
                generated_by_ai=True,
                ai_provider=self.provider_name,
                confidence_score=soap_data.get("confidence_score", 0.85)
            )
        except (json.JSONDecodeError, KeyError) as e:
            # Fallback: try to parse as plain text with sections
            return self._parse_text_soap_note(response_text, patient_id, provider_id)

    def _parse_text_soap_note(self, text: str, patient_id: Optional[str], 
                             provider_id: Optional[str]) -> SOAPNote:
        """Fallback parser for plain text SOAP notes"""
        sections = {"subjective": "", "objective": "", "assessment": "", "plan": ""}
        
        # Try to extract sections using common patterns
        patterns = {
            "subjective": r"(?:Subjective|S):\s*(.+?)(?=\n(?:Objective|O):|$)",
            "objective": r"(?:Objective|O):\s*(.+?)(?=\n(?:Assessment|A):|$)",
            "assessment": r"(?:Assessment|A):\s*(.+?)(?=\n(?:Plan|P):|$)",
            "plan": r"(?:Plan|P):\s*(.+?)$"
        }
        
        for key, pattern in patterns.items():
            match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
            if match:
                sections[key] = match.group(1).strip()
        
        # If no sections found, put everything in subjective
        if not any(sections.values()):
            sections["subjective"] = text
        
        return SOAPNote(
            patient_id=patient_id,
            provider_id=provider_id,
            encounter_date=datetime.utcnow(),
            subjective=sections["subjective"],
            objective=sections["objective"],
            assessment=sections["assessment"],
            plan=sections["plan"],
            generated_by_ai=True,
            ai_provider=self.provider_name,
            confidence_score=0.7  # Lower confidence for fallback parsing
        )

    def generate_medical_codes(self, text: str, patient_id: Optional[str] = None,
                              encounter_id: Optional[str] = None) -> MedicalCodeResponse:
        system_prompt = """You are a certified medical coder. Extract ICD-10 and CPT codes from the clinical text.
        Return ONLY a JSON object with these keys:
        - "icd10_codes": Array of objects with: code, description, is_primary, confidence_score
        - "cpt_codes": Array of objects with: code, description, units, confidence_score
        
        Example:
        {
          "icd10_codes": [{"code": "E11.9", "description": "Type 2 diabetes", "is_primary": true, "confidence_score": 0.95}],
          "cpt_codes": [{"code": "99213", "description": "Office visit", "units": 1, "confidence_score": 0.90}]
        }
        
        Do not include markdown. Return only JSON."""
        
        response_text = self._invoke_model(system_prompt, text)
        
        # Clean and parse JSON
        cleaned_text = response_text.strip()
        if cleaned_text.startswith("```json"):
            cleaned_text = cleaned_text[7:]
        if cleaned_text.startswith("```"):
            cleaned_text = cleaned_text[3:]
        if cleaned_text.endswith("```"):
            cleaned_text = cleaned_text[:-3]
        
        try:
            codes_data = json.loads(cleaned_text.strip())
            
            # Parse ICD-10 codes
            icd10_codes = []
            for code_dict in codes_data.get("icd10_codes", []):
                try:
                    icd10_codes.append({
                        "code": code_dict.get("code", ""),
                        "description": code_dict.get("description", ""),
                        "is_primary": code_dict.get("is_primary", False),
                        "confidence_score": code_dict.get("confidence_score", 0.8),
                        "generated_by_ai": True
                    })
                except Exception:
                    continue
            
            # Parse CPT codes
            cpt_codes = []
            for code_dict in codes_data.get("cpt_codes", []):
                try:
                    cpt_codes.append({
                        "code": code_dict.get("code", ""),
                        "description": code_dict.get("description", ""),
                        "units": code_dict.get("units", 1),
                        "confidence_score": code_dict.get("confidence_score", 0.8),
                        "generated_by_ai": True
                    })
                except Exception:
                    continue
            
            return MedicalCodeResponse(
                icd10_codes=icd10_codes,
                cpt_codes=cpt_codes,
                provider=self.provider_name
            )
            
        except (json.JSONDecodeError, KeyError) as e:
            # Return empty response on error
            return MedicalCodeResponse(
                icd10_codes=[],
                cpt_codes=[],
                provider=self.provider_name
            )
