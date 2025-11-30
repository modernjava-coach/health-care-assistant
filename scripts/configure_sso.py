#!/usr/bin/env python3
"""
Helper script to guide AWS SSO configuration.
"""

import subprocess
import sys
import os

def print_header():
    print("=" * 70)
    print("AWS SSO CONFIGURATION HELPER")
    print("=" * 70)
    print()

def check_aws_cli_version():
    try:
        result = subprocess.run(["aws", "--version"], capture_output=True, text=True)
        print(f"[*] Detected: {result.stdout.strip()}")
        if "aws-cli/2" not in result.stdout:
            print("[!] WARNING: It looks like you might not be using AWS CLI v2.")
            print("    SSO requires AWS CLI v2.")
            return False
        return True
    except FileNotFoundError:
        print("[X] AWS CLI not found. Please install AWS CLI v2.")
        return False

def main():
    print_header()
    
    if not check_aws_cli_version():
        sys.exit(1)
        
    print("\nThis script will help you run the 'aws configure sso' command.")
    print("You will need:")
    print("  1. Your SSO Start URL (e.g., https://my-org.awsapps.com/start)")
    print("  2. The AWS Region for SSO (e.g., us-east-1)")
    print()
    
    confirm = input("Ready to start? (y/n): ").lower().strip()
    if confirm != 'y':
        print("Aborted.")
        sys.exit(0)
        
    print("\n[*] Launching 'aws configure sso'...")
    print("    Follow the prompts in the terminal and your browser.")
    print("-" * 70)
    
    try:
        # We use shell=True to ensure it runs properly in the user's shell environment
        # and allows interaction
        subprocess.run("aws configure sso", shell=True, check=True)
        
        print("-" * 70)
        print("[OK] Configuration sequence completed.")
        print("\nTo use this profile, remember to set it:")
        print("  Windows: $env:AWS_PROFILE = 'your-profile-name'")
        print("  Mac/Lin: export AWS_PROFILE=your-profile-name")
        print("\nTo login in the future:")
        print("  aws sso login --profile your-profile-name")
        
    except subprocess.CalledProcessError:
        print("\n[X] Configuration failed or was cancelled.")
    except KeyboardInterrupt:
        print("\n\n[!] Setup cancelled.")

if __name__ == "__main__":
    main()
