"""
Amazon Bedrock Content Summarizer - Streamlit Web App
Interactive web interface for text summarization.
"""

import streamlit as st
import os
from main import BedrockSummarizer, validate_aws_credentials, get_text_stats


# Page configuration
st.set_page_config(
    page_title="Bedrock Content Summarizer",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #FF9900;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .summary-box {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .stat-box {
        background-color: #e8f4f8;
        padding: 1rem;
        border-radius: 0.5rem;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)


def initialize_session_state():
    """Initialize session state variables."""
    if 'summaries' not in st.session_state:
        st.session_state.summaries = None
    if 'input_text' not in st.session_state:
        st.session_state.input_text = ""


def main():
    """Main application function."""
    initialize_session_state()
    
    # Header
    st.markdown('<div class="main-header">📝 Bedrock Content Summarizer</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Generate AI-powered summaries using Amazon Bedrock</div>', unsafe_allow_html=True)
    
    # Sidebar - Configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # AWS Region
        region = st.selectbox(
            "AWS Region",
            ["us-east-1", "us-west-2", "eu-central-1", "ap-southeast-1"],
            index=0
        )
        
        # Model Selection
        model = st.selectbox(
            "Claude Model",
            [
                "anthropic.claude-3-haiku-20240307-v1:0",
                "anthropic.claude-3-sonnet-20240229-v1:0",
                "anthropic.claude-3-opus-20240229-v1:0"
            ],
            index=0,
            help="Haiku: Fast & economical | Sonnet: Balanced | Opus: Best quality"
        )
        
        st.divider()
        
        # AWS Credentials Check
        st.header("🔐 Credentials")
        is_valid, message = validate_aws_credentials()
        
        if is_valid:
            st.success("✓ AWS credentials configured")
        else:
            st.error("✗ AWS credentials missing")
            st.info("Set environment variables:\n- AWS_ACCESS_KEY_ID\n- AWS_SECRET_ACCESS_KEY")
        
        st.divider()
        
        # About
        st.header("ℹ️ About")
        st.markdown("""
        This app uses Amazon Bedrock's Claude models to generate:
        - **Short**: 2-3 sentences
        - **Medium**: 1 paragraph
        - **Long**: Detailed summary
        """)
    
    # Main content area
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("📄 Input Text")
        
        # Text input options
        input_method = st.radio(
            "Input Method",
            ["Type/Paste Text", "Upload File", "Use Sample"],
            horizontal=True
        )
        
        input_text = ""
        
        if input_method == "Type/Paste Text":
            input_text = st.text_area(
                "Enter text to summarize",
                height=300,
                placeholder="Paste your text here..."
            )
        
        elif input_method == "Upload File":
            uploaded_file = st.file_uploader(
                "Choose a text file",
                type=['txt', 'md']
            )
            if uploaded_file:
                input_text = uploaded_file.read().decode('utf-8')
                st.text_area("File content", input_text, height=300, disabled=True)
        
        else:  # Use Sample
            try:
                with open('samples/sample-text.txt', 'r', encoding='utf-8') as f:
                    input_text = f.read()
                st.text_area("Sample text", input_text, height=300, disabled=True)
            except FileNotFoundError:
                st.warning("Sample file not found. Please use another input method.")
        
        # Text statistics
        if input_text:
            stats = get_text_stats(input_text)
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                st.metric("Characters", f"{stats['characters']:,}")
            with col_b:
                st.metric("Words", f"{stats['words']:,}")
            with col_c:
                st.metric("Lines", stats['lines'])
        
        # Summarize button
        summarize_btn = st.button(
            "🚀 Generate Summaries",
            type="primary",
            use_container_width=True,
            disabled=not input_text or not is_valid
        )
    
    with col2:
        st.header("✨ Summaries")
        
        if summarize_btn and input_text:
            try:
                with st.spinner("Generating summaries..."):
                    summarizer = BedrockSummarizer(region=region, model_id=model)
                    st.session_state.summaries = summarizer.summarize_all_lengths(input_text)
                st.success("✓ Summaries generated successfully!")
            except Exception as e:
                st.error(f"Error: {str(e)}")
                st.session_state.summaries = None
        
        # Display summaries
        if st.session_state.summaries:
            summaries = st.session_state.summaries
            
            # Short Summary
            with st.expander("📌 Short Summary (2-3 sentences)", expanded=True):
                st.markdown(f'<div class="summary-box">{summaries["short"]}</div>', unsafe_allow_html=True)
                st.caption(f"Length: {len(summaries['short'])} characters")
            
            # Medium Summary
            with st.expander("📄 Medium Summary (1 paragraph)", expanded=True):
                st.markdown(f'<div class="summary-box">{summaries["medium"]}</div>', unsafe_allow_html=True)
                st.caption(f"Length: {len(summaries['medium'])} characters")
            
            # Long Summary
            with st.expander("📚 Long Summary (detailed)", expanded=True):
                st.markdown(f'<div class="summary-box">{summaries["long"]}</div>', unsafe_allow_html=True)
                st.caption(f"Length: {len(summaries['long'])} characters")
            
            # Download options
            st.divider()
            st.subheader("💾 Download Summaries")
            
            # Prepare download content
            download_content = f"""BEDROCK CONTENT SUMMARIZER - RESULTS
{'=' * 60}

SHORT SUMMARY
{'-' * 60}
{summaries['short']}

MEDIUM SUMMARY
{'-' * 60}
{summaries['medium']}

LONG SUMMARY
{'-' * 60}
{summaries['long']}
"""
            
            st.download_button(
                label="📥 Download All Summaries",
                data=download_content,
                file_name="summaries.txt",
                mime="text/plain",
                use_container_width=True
            )
        else:
            st.info("👈 Enter text and click 'Generate Summaries' to see results")


if __name__ == "__main__":
    main()
