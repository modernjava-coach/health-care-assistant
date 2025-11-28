import boto3
import json
from typing import List, Dict, Any
from llm_provider import LLMProvider

class BedrockProvider(LLMProvider):
    def __init__(self, region_name: str = "us-east-1"):
        self.client = boto3.client("bedrock-runtime", region_name=region_name)
        self.model_id = "anthropic.claude-3-5-sonnet-20240620-v1:0"

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

        response = self.client.invoke_model(
            modelId=self.model_id,
            body=json.dumps(payload)
        )

        response_body = json.loads(response.get("body").read())
        return response_body["content"][0]["text"]

    def generate_soap_note(self, text: str) -> str:
        system_prompt = """You are an expert medical scribe. Your task is to convert raw patient notes or transcripts into a professional, structured SOAP note (Subjective, Objective, Assessment, Plan).
        - Maintain a professional medical tone.
        - Do not invent information not present in the text.
        - Use standard medical abbreviations where appropriate.
        """
        return self._invoke_claude(system_prompt, text)

    def generate_medical_codes(self, text: str) -> List[Dict[str, Any]]:
        system_prompt = """You are a certified medical coder. Your task is to extract relevant ICD-10-CM and CPT codes from the provided clinical text.
        Return the output strictly as a JSON list of objects with the following keys:
        - "code": The alphanumeric code (e.g., "R51.9").
        - "description": Brief description of the code.
        - "type": "ICD-10" or "CPT".
        
        Do not include any markdown formatting or conversational text. Just the JSON array.
        """
        
        response_text = self._invoke_claude(system_prompt, text)
        
        # Attempt to clean and parse JSON if the model adds backticks
        cleaned_text = response_text.strip()
        if cleaned_text.startswith("```json"):
            cleaned_text = cleaned_text[7:]
        if cleaned_text.endswith("```"):
            cleaned_text = cleaned_text[:-3]
            
        try:
            return json.loads(cleaned_text)
        except json.JSONDecodeError:
            # Fallback or error handling
            return [{"code": "ERROR", "description": "Failed to parse JSON response", "type": "ERROR"}]
