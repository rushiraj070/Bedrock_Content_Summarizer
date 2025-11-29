"""
Amazon Bedrock Text Summarizer
Generates short, medium, and long summaries of input text using Claude.
"""

import os
import sys
import json
import boto3
from botocore.exceptions import ClientError, NoCredentialsError


class BedrockSummarizer:
    """Handles text summarization using Amazon Bedrock."""
    
    def __init__(self, region='us-east-1'):
        """Initialize Bedrock client."""
        self.region = region
        self.bedrock_runtime = None
        self._initialize_client()
    
    def _initialize_client(self):
        """Create Bedrock runtime client."""
        try:
            self.bedrock_runtime = boto3.client(
                service_name='bedrock-runtime',
                region_name=self.region
            )
            print(f"✓ Connected to Bedrock in region: {self.region}\n")
        except NoCredentialsError:
            print("❌ AWS credentials not found. Please configure them first.")
            sys.exit(1)
        except Exception as e:
            print(f"❌ Failed to initialize Bedrock client: {str(e)}")
            sys.exit(1)
    
    def generate_summary(self, text, length_type):
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
                'description': '2-3 sentences',
                'max_tokens': 150
            },
            'medium': {
                'description': '1 paragraph (4-6 sentences)',
                'max_tokens': 300
            },
            'long': {
                'description': 'multiple paragraphs with key details',
                'max_tokens': 600
            }
        }
        
        params = length_params.get(length_type, length_params['medium'])
        
        # Construct prompt
        prompt = f"""Human: Please provide a {length_type} summary of the following text. 
The summary should be {params['description']}.

Text to summarize:
{text}
        
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
                modelId='anthropic.claude-3-haiku-20240307-v1:0',
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
                print(f"🔄 Generating {length} summary...")
                summaries[length] = self.generate_summary(text, length)
                print(f"✓ {length.capitalize()} summary complete")
            except Exception as e:
                print(f"❌ Failed to generate {length} summary: {str(e)}")
                summaries[length] = f"Error: {str(e)}"
        
        return summaries


def print_results(summaries, original_text):
    """Print summaries in a structured format."""
    print("\n" + "=" * 80)
    print("SUMMARIZATION RESULTS")
    print("=" * 80)
    
    print(f"\n📄 Original Text Length: {len(original_text)} characters")
    print(f"   Word Count: {len(original_text.split())} words")
    
    print("\n" + "-" * 80)
    print("SHORT SUMMARY (2-3 sentences)")
    print("-" * 80)
    print(summaries.get('short', 'N/A'))
    print(f"\n   Length: {len(summaries.get('short', ''))} characters")
    
    print("\n" + "-" * 80)
    print("MEDIUM SUMMARY (1 paragraph)")
    print("-" * 80)
    print(summaries.get('medium', 'N/A'))
    print(f"\n   Length: {len(summaries.get('medium', ''))} characters")
    
    print("\n" + "-" * 80)
    print("LONG SUMMARY (detailed)")
    print("-" * 80)
    print(summaries.get('long', 'N/A'))
    print(f"\n   Length: {len(summaries.get('long', ''))} characters")
    
    print("\n" + "=" * 80)



def load_text_from_file(filepath):
    """Load text from a file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"❌ File not found: {filepath}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error reading file: {str(e)}")
        sys.exit(1)


def main():
    """Main execution function."""
    print("=" * 80)
    print("AMAZON BEDROCK TEXT SUMMARIZER")
    print("=" * 80)
    print()
    
    # Check for AWS credentials
    if not os.getenv('AWS_ACCESS_KEY_ID') or not os.getenv('AWS_SECRET_ACCESS_KEY'):
        print("❌ AWS credentials not configured.")
        print("\nPlease set environment variables:")
        print("  set AWS_ACCESS_KEY_ID=your_key")
        print("  set AWS_SECRET_ACCESS_KEY=your_secret")
        print("  set AWS_DEFAULT_REGION=us-east-1")
        sys.exit(1)
    
    # Get input text
    if len(sys.argv) > 1:
        # Load from file if provided
        filepath = sys.argv[1]
        print(f"📂 Loading text from: {filepath}\n")
        text = load_text_from_file(filepath)
    else:
        # Use sample text for demonstration
        print("ℹ️  No input file provided. Using sample text.")
        print("   Usage: python bedrock_summarizer.py <text_file.txt>\n")
        
        text = """
        Artificial intelligence (AI) is transforming the way we live and work. From healthcare to finance, 
        AI technologies are being deployed across industries to improve efficiency, accuracy, and decision-making. 
        Machine learning, a subset of AI, enables computers to learn from data without being explicitly programmed. 
        Deep learning, which uses neural networks with multiple layers, has achieved remarkable success in areas 
        like image recognition, natural language processing, and autonomous vehicles. However, the rapid advancement 
        of AI also raises important ethical questions about privacy, bias, job displacement, and the need for 
        responsible AI development. As AI continues to evolve, it's crucial that we develop frameworks and 
        regulations to ensure these technologies benefit society while minimizing potential harms. The future 
        of AI holds immense promise, but it requires careful consideration of both its capabilities and limitations.
        """
    
    # Validate text length
    if len(text.strip()) < 50:
        print("❌ Text is too short to summarize (minimum 50 characters)")
        sys.exit(1)
    
    # Initialize summarizer
    region = os.getenv('AWS_DEFAULT_REGION', 'us-east-1')
    summarizer = BedrockSummarizer(region=region)
    
    # Generate summaries
    try:
        summaries = summarizer.summarize_all_lengths(text.strip())
        print_results(summaries, text.strip())
        print("\n✓ Summarization complete!")
        
    except Exception as e:
        print(f"\n❌ Summarization failed: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
