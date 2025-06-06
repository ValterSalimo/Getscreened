# Knowledge Extraction Q&A System

This application demonstrates a Q&A system using Hugging Face transformers and Google Gemini for knowledge extraction from provided documents.

## Features

- Load documents from multiple sources:
  - Example texts
  - User input
  - File upload (TXT, PDF, DOCX, MD)
  - Web search (DuckDuckGo and Wikipedia)
- Advanced document processing with vector embeddings
- Extract answers to user questions using context-based Q&A
- Two available models:
  - Hugging Face transformers (distilbert-base-cased-distilled-squad)
  - Google Gemini 2.0 Flash

## Setup

1. Create a `.env` file with your Google Gemini API key:
   ```
   GEMINI_API_KEY="your_api_key_here"
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

3. Run the Streamlit application:
   ```
   streamlit run app.py
   ```

## Usage

1. Select a document source:
   - Example Documents: Choose from predefined examples
   - Paste Text: Enter your own text
   - Upload File: Upload TXT, PDF, DOCX, or MD files
   - Web Search: Search Wikipedia or DuckDuckGo for content
2. Choose a Q&A model (Google Gemini or Hugging Face Transformers)
3. Enter your question in the text field
4. Click "Get Answer" to extract knowledge from the document

## Example

- Document: "Solar energy is one of the most abundant renewable resources available today. It is generated by converting sunlight into electricity."
- Question: "What is solar energy?"
- Expected Answer: "Solar energy is generated by converting sunlight into electricity."
