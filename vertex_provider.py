import vertexai
from vertexai.generative_models import GenerativeModel, Part
import json
from typing import List, Dict, Any
from llm_provider import LLMProvider
import os

class VertexProvider(LLMProvider):
    def __init__(self, project_id: str = None, location: str = "us-central1"):
        # Initialize Vertex AI. 
        # Assumes GOOGLE_APPLICATION_CREDENTIALS or default credentials are set.
        # project_id can be passed or inferred from credentials.
        vertexai.init(project=project_id, location=location)
        self.model = GenerativeModel("gemini-1.5-pro-001")

    def generate_soap_note(self, text: str) -> str:
        prompt = f"""You are an expert medical scribe. Convert the following raw patient notes or transcripts into a professional, structured SOAP note (Subjective, Objective, Assessment, Plan).
        
        Input Text:
        {text}
        
        Output:
        """
        
        response = self.model.generate_content(prompt)
        return response.text

    def generate_medical_codes(self, text: str) -> List[Dict[str, Any]]:
        prompt = f"""You are a certified medical coder. Extract relevant ICD-10-CM and CPT codes from the provided clinical text.
        Return the output strictly as a JSON list of objects with the following keys:
        - "code": The alphanumeric code (e.g., "R51.9").
        - "description": Brief description of the code.
        - "type": "ICD-10" or "CPT".
        
        Input Text:
        {text}
        
        Output (JSON only):
        """
        
        # Using generation_config to enforce JSON response would be better, 
        # but for simplicity we'll use prompt engineering + parsing similar to Bedrock for now.
        response = self.model.generate_content(prompt)
        response_text = response.text
        
        cleaned_text = response_text.strip()
        if cleaned_text.startswith("```json"):
            cleaned_text = cleaned_text[7:]
        if cleaned_text.endswith("```"):
            cleaned_text = cleaned_text[:-3]
            
        try:
            return json.loads(cleaned_text)
        except json.JSONDecodeError:
            return [{"code": "ERROR", "description": "Failed to parse JSON response", "type": "ERROR"}]
