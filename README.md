# GetScreened - AI/ML Portfolio Project

A comprehensive AI and Machine Learning portfolio demonstrating expertise in natural language processing, knowledge extraction, and prompt engineering. This project showcases three distinct tasks, each highlighting different aspects of modern AI development.

## 🎯 Project Overview

This repository contains three interconnected tasks that demonstrate proficiency in:
- **Natural Language Processing** (Sentiment Analysis)
- **Information Retrieval & Q&A Systems** (Knowledge Extraction)
- **Advanced Prompt Engineering** (Interview Question Generation)

## 📁 Project Structure

```
getscreened/
├── Task 1/                    # Movie Review Sentiment Analysis
│   ├── sentiment_cli.py       # Command-line interface
│   ├── sentiment_analysis.ipynb # Jupyter notebook
│   ├── imdb_sentiment_model/  # Fine-tuned DistilBERT model
│   └── content/               # IMDB dataset
├── Task 2/                    # Knowledge Extraction Q&A System
│   ├── app.py                 # Streamlit web application
│   └── requirements.txt       # Dependencies
├── Task 3/                    # Prompt Engineering for Interviews
│   ├── task3_complete.py      # Complete implementation
│   └── requirements.txt       # Dependencies
└── README.md                  # This file
```

## 🚀 Quick Start

### Prerequisites
- Python 3.7+
- pip (Python package installer)

### Installation
1. Clone or download this repository
2. Navigate to the project directory:
   ```powershell
   cd getscreened
   ```

## 📋 Task Descriptions

### Task 1: Movie Review Sentiment Analysis
**Technologies:** DistilBERT, Transformers, PyTorch, Colorama

A complete sentiment analysis toolkit for movie reviews using a fine-tuned DistilBERT model trained on the IMDB dataset.

**Features:**
- Pre-trained model for instant sentiment classification
- Interactive command-line interface with colored output
- Jupyter notebook with full training pipeline
- Batch processing capabilities
- Real-time sentiment analysis

**Quick Start:**
```powershell
cd "Task 1"
pip install -r requirements.txt
python sentiment_cli.py
```

**Demo:** Try analyzing reviews like "This movie was absolutely fantastic!" or "Terrible acting and boring plot."

### Task 2: Knowledge Extraction Q&A System
**Technologies:** Streamlit, Hugging Face Transformers, Google Gemini, LangChain, FAISS

An intelligent Q&A system that extracts answers from multiple document sources using advanced NLP models.

**Features:**
- Multiple input sources (text, files, web search)
- Vector embeddings for document processing
- Two AI models: Hugging Face transformers & Google Gemini 2.0
- Interactive web interface
- Support for PDF, DOCX, TXT, and Markdown files

**Quick Start:**
```powershell
cd "Task 2"
pip install -r requirements.txt
# Create .env file with GEMINI_API_KEY="your_api_key_here"
streamlit run app.py
```

### Task 3: Advanced Prompt Engineering
**Technologies:** Google Gemini 2.0, Advanced Prompt Techniques

Demonstrates sophisticated prompt engineering for generating creative and contextual interview questions for technology roles.

**Features:**
- Behavioral interview questions for software engineers
- Technical questions for AI-specialized roles
- Context-aware prompting techniques
- Real-time API integration with Gemini 2.0
- Advanced prompt optimization strategies

**Quick Start:**
```powershell
cd "Task 3"
pip install -r requirements.txt
# Create .env file with GEMINI_API_KEY="your_api_key_here"
python task3_complete.py
```

## 🛠️ Technical Highlights

### Machine Learning & AI
- **Fine-tuned DistilBERT** for sentiment classification
- **Vector embeddings** with FAISS for efficient document retrieval
- **Multi-model architecture** supporting both open-source and proprietary models
- **Advanced prompt engineering** with context-aware techniques

### Software Engineering
- **Modular design** with clean separation of concerns
- **Interactive CLIs** with colored output and user-friendly interfaces
- **Web applications** using Streamlit for intuitive user experiences
- **Comprehensive error handling** and input validation

### Development Practices
- **Environment management** with .env files for API keys
- **Comprehensive documentation** with clear setup instructions
- **Requirements management** with detailed dependency specifications
- **Cross-platform compatibility** with Windows PowerShell support

## 📊 Performance & Capabilities

### Task 1 - Sentiment Analysis
- **Model:** Fine-tuned DistilBERT on IMDB dataset
- **Accuracy:** High performance on movie review sentiment classification
- **Speed:** Real-time inference with GPU/CPU optimization
- **Interface:** Both programmatic API and interactive CLI

### Task 2 - Q&A System
- **Document Sources:** Text files, PDFs, web search, Wikipedia
- **Models:** HuggingFace DistilBERT + Google Gemini 2.0
- **Processing:** Vector embeddings with FAISS indexing
- **Interface:** Modern web UI with file upload and search capabilities

### Task 3 - Prompt Engineering
- **LLM:** Google Gemini 2.0 Flash
- **Techniques:** Few-shot learning, context injection, role-based prompting
- **Output:** Structured interview questions with difficulty progression
- **Specialization:** Technical and behavioral question generation

## 🔧 Configuration

### API Keys Required
- **Google Gemini API Key** (for Tasks 2 and 3)
  - Obtain from [Google AI Studio](https://makersuite.google.com/app/apikey)
  - Add to `.env` file as `GEMINI_API_KEY="your_key_here"`

### Environment Setup
Each task includes its own `requirements.txt` file. Install dependencies per task:
```powershell
pip install -r "Task X/requirements.txt"
```

## 📚 Additional Resources

- **Task 1:** [Google Colab Notebook](https://drive.google.com/file/d/1_CQ9F4vXWZw6rPhiKYb9VyXEcuisGH4F/view?usp=sharing) for model training
- **Task 2:** Supports multiple document formats and search engines
- **Task 3:** Comprehensive prompt engineering examples and techniques

## 🤝 Usage Examples

### Sentiment Analysis
```python
# Analyze a movie review
python sentiment_cli.py
# Enter: "The cinematography was breathtaking and the story was compelling!"
# Output: ✅ POSITIVE (95.2% confidence)
```

### Knowledge Q&A
```python
# Ask questions about uploaded documents
# Upload a PDF about machine learning
# Ask: "What are the main types of machine learning algorithms?"
# Get contextual answers from the document
```

### Interview Questions
```python
# Generate technical interview questions
python task3_complete.py
# Generates: System design questions, AI ethics scenarios, algorithm challenges
```

## 📈 Future Enhancements

- Integration of additional language models (Claude, GPT)
- Multi-language support for sentiment analysis
- Advanced document preprocessing with OCR
- Real-time collaborative Q&A sessions
- Interview question difficulty adaptation based on candidate responses

---

**Created with:** Python, Transformers, Streamlit, Google Gemini, and modern ML/AI practices
**Author:** Portfolio demonstration project
**Date:** May 2025
