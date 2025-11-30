import boto3
import io
from typing import Optional
from pypdf import PdfReader
from PIL import Image

class OCRService:
    def __init__(self, region_name: str = "us-east-1"):
        self.textract = boto3.client("textract", region_name=region_name)

    def extract_text(self, file_content: bytes, content_type: str) -> str:
        """Extract text from file content based on content type."""
        if "pdf" in content_type.lower():
            return self._extract_from_pdf(file_content)
        elif "image" in content_type.lower():
            return self._extract_from_image(file_content)
        else:
            raise ValueError(f"Unsupported content type: {content_type}")

    def _extract_from_pdf(self, file_content: bytes) -> str:
        """Extract text from PDF using pypdf."""
        try:
            reader = PdfReader(io.BytesIO(file_content))
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            return text.strip()
        except Exception as e:
            # Fallback or error handling
            print(f"Error extracting text from PDF: {e}")
            raise

    def _extract_from_image(self, file_content: bytes) -> str:
        """Extract text from image using Amazon Textract."""
        try:
            response = self.textract.detect_document_text(
                Document={'Bytes': file_content}
            )
            
            text = ""
            for item in response["Blocks"]:
                if item["BlockType"] == "LINE":
                    text += item["Text"] + "\n"
            return text.strip()
        except Exception as e:
            print(f"Error extracting text from image: {e}")
            raise
