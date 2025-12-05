import boto3
import os

def check_creds():
    print(f"AWS_ACCESS_KEY_ID env: {os.environ.get('AWS_ACCESS_KEY_ID')}")
    print(f"AWS_SECRET_ACCESS_KEY env: {os.environ.get('AWS_SECRET_ACCESS_KEY')}")
    print(f"AWS_PROFILE env: {os.environ.get('AWS_PROFILE')}")
    
    try:
        session = boto3.Session()
        creds = session.get_credentials()
        if creds:
            print("Credentials found via boto3 chain.")
            print(f"Access Key: {creds.access_key}")
        else:
            print("No credentials found via boto3 chain.")
    except Exception as e:
        print(f"Error checking creds: {e}")

if __name__ == "__main__":
    check_creds()
