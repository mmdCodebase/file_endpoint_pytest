import boto3
import json
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file

def get_secret():
    """
    Retrieve the secret from AWS Secrets Manager.
    """
    secret_name = os.getenv("SECRET_NAME")
    region_name = os.getenv("REGION_NAME")

    if not secret_name or not region_name:
        raise ValueError("Secret name or region name not found in environment variables.")
    
    # Create a Secrets Manager Client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )
    
    # Retrieve the secret value
    get_secret_value_response = client.get_secret_value(
        SecretId=secret_name
    )
    
    if 'SecretString' in get_secret_value_response:
        secret = get_secret_value_response['SecretString']
        return json.loads(secret)
    else:
        raise ValueError("Secret not found.")