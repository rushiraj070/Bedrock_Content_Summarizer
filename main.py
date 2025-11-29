"""
Amazon Bedrock Content Summarizer - Main Module
Core functionality for text summarization using Amazon Bedrock.
"""

import os
import json
import boto3
from botocore.exceptions import ClientError, NoCredentialsError


class BedrockSummarizer:
    """Handles text summarization using Amazon Bedrock."""
    
    def __init__(self, region='us-east-1', model_id='anthropic.claude-3-haiku-20240307-v1:0'):
        """
        Initialize Bedrock client.
        
        Args:
            region (str): AWS region for Bedrock
            model_id (str): Bedrock model ID to use
        """
        self.region = region
        self.model_id = model_id
        self.bedrock_runtime = None
        self._initialize_client()
    
    def _initialize_client(self):
        """Create Bedrock runtime client."""
        try:
            self.bedrock_runtime = boto3.client(
                service_name='bedrock-runtime',
                region_name=self.region
            )
        except NoCredentialsError:
            raise Exception("AWS credentials not found. Please configure them first.")
        except Exception as e:
            raise Exception(f"Failed to initialize Bedrock client: {str(e)}")
    
    def generate_summary(self, text, length_type='medium'):
        """
        Generate a summary of specified length.
        
        Args:
            text (str): The text to summarize
            length_type (str): 'short', 'medium', or 'long'
        
        Returns:
            str: The generated summary
        """
        # Define summary parameters
        length_params = {
            'short': {
                'description': '2-3 sentences that capture the main point',
                'max_tokens': 150
            },
            'medium': {
                'description': '1 paragraph (4-6 sentences) covering key points',
                'max_tokens': 300
            },
            'long': {
                'description': 'multiple paragraphs with comprehensive details',
                'max_tokens': 600
            }
        }
        
        params = length_params.get(length_type, length_params['medium'])
        
        # Construct prompt
        prompt = f"""Please provide a {length_type} summary of the following text. 
The summary should be {params['description']}.

Text to summarize:
{text}

Summary:"""
        
        # Prepare request body for Claude 3
        request_body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": params['max_tokens'],
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.5,
            "top_p": 0.9
        }
        
        try:
            # Invoke the model
            response = self.bedrock_runtime.invoke_model(
                modelId=self.model_id,
                contentType='application/json',
                accept='application/json',
                body=json.dumps(request_body)
            )
            
            # Parse response
            response_body = json.loads(response['body'].read())
            summary = response_body['content'][0]['text'].strip()
            
            return summary
            
        except ClientError as e:
            error_code = e.response['Error']['Code']
            error_msg = e.response['Error']['Message']
            raise Exception(f"Bedrock API Error ({error_code}): {error_msg}")
        except KeyError as e:
            raise Exception(f"Unexpected response format: {str(e)}")
        except Exception as e:
            raise Exception(f"Failed to generate summary: {str(e)}")
    
    def summarize_all_lengths(self, text):
        """
        Generate short, medium, and long summaries.
        
        Args:
            text (str): The text to summarize
        
        Returns:
            dict: Dictionary with 'short', 'medium', and 'long' summaries
        """
        summaries = {}
        
        for length in ['short', 'medium', 'long']:
            try:
                summaries[length] = self.generate_summary(text, length)
            except Exception as e:
                summaries[length] = f"Error: {str(e)}"
        
        return summaries


def validate_aws_credentials():
    """
    Validate that AWS credentials are configured.
    
    Returns:
        tuple: (bool, str) - (is_valid, message)
    """
    if not os.getenv('AWS_ACCESS_KEY_ID') or not os.getenv('AWS_SECRET_ACCESS_KEY'):
        return False, "AWS credentials not configured. Please set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY."
    return True, "AWS credentials found."


def get_text_stats(text):
    """
    Get statistics about the text.
    
    Args:
        text (str): The text to analyze
    
    Returns:
        dict: Statistics including character count, word count, etc.
    """
    return {
        'characters': len(text),
        'words': len(text.split()),
        'lines': len(text.splitlines())
    }
