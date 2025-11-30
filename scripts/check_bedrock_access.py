#!/usr/bin/env python3
"""
Script to check AWS Bedrock model access and availability.
This helps verify that you have enabled the necessary models in your AWS account.
"""

import boto3
import json
import sys
from typing import List, Dict
from botocore.exceptions import ClientError, NoCredentialsError


class BedrockAccessChecker:
    """Check AWS Bedrock model access and configuration."""
    
    def __init__(self, region_name: str = "us-east-1"):
        self.region_name = region_name
        try:
            self.bedrock_client = boto3.client("bedrock", region_name=region_name)
            self.bedrock_runtime = boto3.client("bedrock-runtime", region_name=region_name)
        except NoCredentialsError:
            print("[X] ERROR: AWS credentials not configured!")
            print("\nPlease configure your AWS credentials using one of these methods:")
            print("  1. Run: aws configure")
            print("  2. Set environment variables: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY")
            print("  3. Use IAM role (if running on EC2/ECS)")
            sys.exit(1)
    
    def check_credentials(self) -> bool:
        """Verify AWS credentials are valid."""
        try:
            sts = boto3.client('sts')
            identity = sts.get_caller_identity()
            print("[OK] AWS Credentials Valid")
            print(f"   Account: {identity['Account']}")
            print(f"   User/Role: {identity['Arn']}")
            return True
        except Exception as e:
            print(f"[X] AWS Credentials Invalid: {e}")
            return False
    
    def list_foundation_models(self) -> List[Dict]:
        """List all available foundation models in the region."""
        try:
            response = self.bedrock_client.list_foundation_models()
            return response.get('modelSummaries', [])
        except ClientError as e:
            print(f"[X] Error listing models: {e}")
            return []
    
    def check_model_access(self, model_id: str) -> bool:
        """Check if a specific model is accessible by attempting to invoke it."""
        try:
            # Try a minimal invocation to test access
            payload = {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 10,
                "messages": [{"role": "user", "content": "test"}]
            }
            
            response = self.bedrock_runtime.invoke_model(
                modelId=model_id,
                body=json.dumps(payload)
            )
            return True
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == 'AccessDeniedException':
                return False
            elif error_code == 'ValidationException':
                print(f"   [!] Model ID invalid or not available in region")
                return False
            else:
                print(f"   [!] Unexpected error: {error_code}")
                return False
    
    def get_model_info(self, model_id: str, models_list: List[Dict]) -> Dict:
        """Get detailed information about a specific model."""
        for model in models_list:
            if model.get('modelId') == model_id:
                return model
        return {}
    
    def run_checks(self):
        """Run all checks and display results."""
        print("=" * 70)
        print("AWS BEDROCK MODEL ACCESS CHECKER")
        print("=" * 70)
        print()
        
        # Check 1: Credentials
        print("[*] Step 1: Checking AWS Credentials...")
        if not self.check_credentials():
            sys.exit(1)
        print()
        
        # Check 2: Region
        print(f"[*] Step 2: Checking Region: {self.region_name}")
        print()
        
        # Check 3: List available models
        print("[*] Step 3: Listing Available Foundation Models...")
        all_models = self.list_foundation_models()
        
        if not all_models:
            print("[X] No models found or unable to list models")
            sys.exit(1)
        
        # Filter Anthropic Claude models
        claude_models = [m for m in all_models if 'anthropic.claude' in m.get('modelId', '')]
        print(f"   Found {len(claude_models)} Claude models in {self.region_name}")
        print()
        
        # Check 4: Test specific models
        print("[*] Step 4: Testing Model Access...")
        print()
        
        # Models to test (in order of priority)
        test_models = [
            {
                "id": "anthropic.claude-3-5-sonnet-20240620-v1:0",
                "name": "Claude 3.5 Sonnet",
                "priority": "REQUIRED"
            },
            {
                "id": "anthropic.claude-3-sonnet-20240229-v1:0",
                "name": "Claude 3 Sonnet",
                "priority": "OPTIONAL"
            },
            {
                "id": "anthropic.claude-3-haiku-20240307-v1:0",
                "name": "Claude 3 Haiku",
                "priority": "OPTIONAL"
            },
            {
                "id": "anthropic.claude-3-opus-20240229-v1:0",
                "name": "Claude 3 Opus",
                "priority": "OPTIONAL"
            }
        ]
        
        accessible_models = []
        inaccessible_models = []
        
        for model in test_models:
            model_id = model['id']
            model_name = model['name']
            priority = model['priority']
            
            print(f"Testing: {model_name} ({priority})")
            print(f"   Model ID: {model_id}")
            
            # Check if model exists in region
            model_info = self.get_model_info(model_id, all_models)
            if not model_info:
                print(f"   [!] Not available in region {self.region_name}")
                print()
                continue
            
            # Check access
            has_access = self.check_model_access(model_id)
            
            if has_access:
                print(f"   [OK] ACCESS GRANTED")
                accessible_models.append(model)
            else:
                print(f"   [X] ACCESS DENIED - Enable in Bedrock Console")
                inaccessible_models.append(model)
            
            print()
        
        # Summary
        print("=" * 70)
        print("SUMMARY")
        print("=" * 70)
        print()
        
        if accessible_models:
            print(f"[OK] Accessible Models ({len(accessible_models)}):")
            for model in accessible_models:
                print(f"   - {model['name']}")
            print()
        
        if inaccessible_models:
            print(f"[X] Inaccessible Models ({len(inaccessible_models)}):")
            for model in inaccessible_models:
                status = "[!] REQUIRED" if model['priority'] == 'REQUIRED' else "[i] Optional"
                print(f"   - {model['name']} - {status}")
            print()
            
            print("[*] To enable models:")
            print("   1. Go to AWS Console → Amazon Bedrock")
            print("   2. Click 'Model access' in left sidebar")
            print("   3. Click 'Manage model access'")
            print("   4. Enable the required models")
            print("   5. Re-run this script to verify")
            print()
        
        # Final verdict
        required_accessible = any(
            m['priority'] == 'REQUIRED' for m in accessible_models
        )
        
        if required_accessible:
            print("[OK] SUCCESS: All required models are accessible!")
            print("     Your application is ready to use AWS Bedrock.")
            return 0
        else:
            print("[X] SETUP INCOMPLETE: Required models not accessible")
            print("    Please enable Claude 3.5 Sonnet in the Bedrock console.")
            return 1


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Check AWS Bedrock model access and availability"
    )
    parser.add_argument(
        "--region",
        default="us-east-1",
        help="AWS region to check (default: us-east-1)"
    )
    
    args = parser.parse_args()
    
    checker = BedrockAccessChecker(region_name=args.region)
    exit_code = checker.run_checks()
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
