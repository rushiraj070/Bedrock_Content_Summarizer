"""
Amazon Bedrock Setup and Test Script
This script configures AWS credentials and tests the Bedrock connection.
"""

import os
import sys
import boto3
from botocore.exceptions import ClientError, NoCredentialsError


def load_env_variables():
    """Load AWS credentials from environment variables."""
    required_vars = ['AWS_ACCESS_KEY_ID', 'AWS_SECRET_ACCESS_KEY']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"❌ Missing environment variables: {', '.join(missing_vars)}")
        print("\nPlease set the following environment variables:")
        print("  - AWS_ACCESS_KEY_ID")
        print("  - AWS_SECRET_ACCESS_KEY")
        print("  - AWS_DEFAULT_REGION (optional, defaults to us-east-1)")
        return False
    
    print("✓ AWS credentials loaded from environment variables")
    return True


def test_bedrock_connection():
    """Test connection to Amazon Bedrock by listing available models."""
    try:
        # Get region from environment or use default
        region = os.getenv('AWS_DEFAULT_REGION', 'us-east-1')
        print(f"✓ Using AWS region: {region}")
        
        # Create Bedrock client
        bedrock = boto3.client(
            service_name='bedrock',
            region_name=region
        )
        
        print("\n🔍 Fetching available Bedrock foundation models...")
        
        # List foundation models
        response = bedrock.list_foundation_models()
        models = response.get('modelSummaries', [])
        
        if not models:
            print("⚠️  No models found. Check your AWS region and permissions.")
            return False
        
        print(f"\n✓ Successfully connected to Amazon Bedrock!")
        print(f"✓ Found {len(models)} available models:\n")
        
        # Display models in a formatted way
        for model in models:
            model_id = model.get('modelId', 'N/A')
            model_name = model.get('modelName', 'N/A')
            provider = model.get('providerName', 'N/A')
            print(f"  • {model_name}")
            print(f"    ID: {model_id}")
            print(f"    Provider: {provider}")
            print()
        
        return True
        
    except NoCredentialsError:
        print("❌ AWS credentials not found or invalid")
        return False
    except ClientError as e:
        error_code = e.response['Error']['Code']
        error_msg = e.response['Error']['Message']
        print(f"❌ AWS Error ({error_code}): {error_msg}")
        
        if error_code == 'UnrecognizedClientException':
            print("\n💡 Tip: Check that your AWS credentials are correct")
        elif error_code == 'AccessDeniedException':
            print("\n💡 Tip: Ensure your IAM user has Bedrock permissions")
        
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        return False


def main():
    """Main setup and test function."""
    print("=" * 60)
    print("Amazon Bedrock Setup & Connection Test")
    print("=" * 60)
    print()
    
    # Check for required environment variables
    if not load_env_variables():
        sys.exit(1)
    
    # Test Bedrock connection
    if test_bedrock_connection():
        print("\n" + "=" * 60)
        print("✓ Setup complete! You're ready to use Amazon Bedrock.")
        print("=" * 60)
        sys.exit(0)
    else:
        print("\n" + "=" * 60)
        print("❌ Setup failed. Please check the errors above.")
        print("=" * 60)
        sys.exit(1)


if __name__ == "__main__":
    main()
