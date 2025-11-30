"""
Quick start script to enable AWS Bedrock models.
This script provides a simple interface to check access and get setup instructions.
"""

import subprocess
import sys


def print_header():
    print("=" * 70)
    print("AWS BEDROCK MODEL ENABLEMENT - QUICK START")
    print("=" * 70)
    print()


def print_instructions():
    print("📚 SETUP INSTRUCTIONS")
    print("-" * 70)
    print()
    print("To enable AWS Bedrock models, you need to:")
    print()
    print("1️⃣  Log into AWS Console")
    print("   → https://console.aws.amazon.com/bedrock/")
    print()
    print("2️⃣  Navigate to 'Model access' (left sidebar)")
    print()
    print("3️⃣  Click 'Manage model access' (orange button)")
    print()
    print("4️⃣  Enable these models:")
    print("   ✅ Claude 3.5 Sonnet (REQUIRED)")
    print("   ⚪ Claude 3 Sonnet (Optional)")
    print("   ⚪ Claude 3 Haiku (Optional)")
    print()
    print("5️⃣  Click 'Request model access'")
    print()
    print("6️⃣  Wait for approval (usually instant for Claude models)")
    print()
    print("7️⃣  Run verification: python scripts/check_bedrock_access.py")
    print()
    print("-" * 70)
    print()
    print("📖 For detailed instructions, see: BEDROCK_SETUP.md")
    print()


def check_aws_cli():
    """Check if AWS CLI is installed and configured."""
    try:
        result = subprocess.run(
            ["aws", "sts", "get-caller-identity"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            print("✅ AWS CLI is configured")
            return True
        else:
            print("❌ AWS CLI not configured properly")
            print("   Run: aws configure")
            return False
    except FileNotFoundError:
        print("⚠️  AWS CLI not installed")
        print("   Install from: https://aws.amazon.com/cli/")
        return False
    except Exception as e:
        print(f"⚠️  Error checking AWS CLI: {e}")
        return False


def main():
    print_header()
    
    print("🔍 Checking prerequisites...")
    print()
    
    # Check AWS CLI
    aws_configured = check_aws_cli()
    print()
    
    if not aws_configured:
        print("⚠️  Please configure AWS CLI before proceeding")
        print()
    
    # Print instructions
    print_instructions()
    
    # Offer to run the checker
    print("Would you like to run the model access checker now?")
    print("This will verify which models you have access to.")
    print()
    
    try:
        response = input("Run checker? (y/n): ").strip().lower()
        if response == 'y':
            print()
            print("Running model access checker...")
            print()
            subprocess.run([sys.executable, "scripts/check_bedrock_access.py"])
    except KeyboardInterrupt:
        print("\n\nSetup cancelled.")
        sys.exit(0)


if __name__ == "__main__":
    main()
