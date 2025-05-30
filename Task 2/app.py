import os
import streamlit as st
import pandas as pd
from typing import Union, List, Dict
import google.generativeai as genai
from dotenv import load_dotenv
from transformers import pipeline
from duckduckgo_search import DDGS
import tempfile
from langchain_community.document_loaders import UnstructuredPDFLoader, UnstructuredWordDocumentLoader, TextLoader
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

# Load environment variables
load_dotenv()

# Configure Google Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

class DuckDuckGoSearch:
    """
    Custom DuckDuckGo search implementation with robust error handling and result processing.
    Uses the duckduckgo_search library to fetch and format search results.
    """
    def __init__(self):
        # Initialize the DuckDuckGo search session
        self.ddgs = DDGS()

    def search(self, query: str, max_results: int = 5) -> str:
        try:
            # Perform the search and get results
            search_results = list(self.ddgs.text(
                query,
                max_results=max_results,
                region='wt-wt',  # Worldwide results
                safesearch='on'
            ))

            if not search_results:
                return "No results found. Try modifying your search query."

            # Format the results into a readable string
            formatted_results = []
            for idx, result in enumerate(search_results, 1):
                # Extract available fields with fallbacks for missing data
                title = result.get('title', 'No title available')
                snippet = result.get('body', result.get('snippet', 'No description available'))
                url = result.get('href', 'No link available')

                # Format each result with available information
                formatted_results.append(
                    f"{title}\n"
                    f"Summary: {snippet}\n"
                    f"URL: {url}\n"
                )

            return "\n\n".join(formatted_results)

        except Exception as e:
            # Provide detailed error information for debugging
            error_msg = f"Search error: {str(e)}"
            print(f"DuckDuckGo search error: {str(e)}")  # For logging
            return error_msg

class DocumentLoader:
    """
    Document loader for loading text data from various sources.
    Supports loading from files, provided text, web search, or predefined examples.
    """
    def __init__(self):
        # Initialize with default documents
        self.default_documents = {
            "solar_energy": "Solar energy is one of the most abundant renewable resources available today. It is generated by converting sunlight into electricity. Solar panels, also known as photovoltaic panels, capture sunlight and convert it into usable electricity through the photovoltaic effect. This clean energy source produces no emissions during operation and is becoming increasingly cost-effective. Solar power can be used in large utility-scale installations or small residential systems, making it versatile for various applications.",
            "ai_ethics": "AI Ethics encompasses the moral principles and guidelines governing the development and use of artificial intelligence systems. Key concerns include privacy, bias and fairness, transparency, accountability, and the impact on employment. As AI becomes more integrated into daily life, ensuring these systems are designed with ethical considerations becomes increasingly important. Some propose regulatory frameworks while others advocate for industry self-regulation. The field continues to evolve as new AI capabilities emerge.",
            "renewable_energy": "Renewable energy comes from naturally replenished sources such as sunlight, wind, water, and geothermal heat. Unlike fossil fuels, renewable energy sources won't deplete over time. Major types include solar, wind, hydroelectric, biomass, and geothermal power. The renewable energy sector is growing rapidly worldwide as countries seek to reduce carbon emissions and combat climate change. Technological advances continue to make renewable energy increasingly cost-competitive with conventional energy sources."
        }
        self.current_document = ""
        self.document_source = "None"
        self.ddg_search = DuckDuckGoSearch()
        # For vector store
        self.vector_store = None
        self.embeddings = None

    def load_from_text(self, text: str) -> str:
        """Load document from provided text string"""
        self.current_document = text
        self.document_source = "User input"
        return self.current_document
        
    def load_from_file(self, file) -> str:
        """Load document from uploaded file"""
        try:
            # For simple text files
            if file.name.endswith('.txt') or file.name.endswith('.md'):
                text = file.getvalue().decode("utf-8")
                self.current_document = text
                self.document_source = file.name
                return self.current_document
            
            # For structured documents like PDF and DOCX
            with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.name)[1]) as tmp:
                tmp.write(file.getvalue())
                temp_path = tmp.name
            
            # Choose appropriate loader based on file extension
            try:
                if temp_path.endswith('.pdf'):
                    loader = UnstructuredPDFLoader(temp_path)
                elif temp_path.endswith('.docx'):
                    loader = UnstructuredWordDocumentLoader(temp_path)
                else:
                    loader = TextLoader(temp_path)
                
                # Load the document
                docs = loader.load()
                
                # Combine all pages/sections
                text_content = "\n\n".join([doc.page_content for doc in docs])
                
                # Create vector store for advanced retrieval if content is substantial
                if len(text_content) > 100:
                    self.embeddings = HuggingFaceEmbeddings()
                    self.vector_store = FAISS.from_documents(docs, self.embeddings)
                
                self.current_document = text_content
                self.document_source = file.name
                
            finally:
                # Clean up temporary file
                if os.path.exists(temp_path):
                    os.remove(temp_path)
                    
            return self.current_document
            
        except Exception as e:
            error_msg = f"File loading error: {str(e)}"
            print(error_msg)  # For logging
            return error_msg

    def load_from_example(self, example_key: str) -> str:
        """Load from predefined example documents"""
        if example_key in self.default_documents:
            self.current_document = self.default_documents[example_key]
            self.document_source = f"Example: {example_key}"
            return self.current_document
        else:
            return "Example not found. Please select a valid example."
    
    def load_from_web_search(self, query: str, source: str = "duckduckgo", max_results: int = 3) -> str:
        """Load document from web search"""
        try:
            # Remove any code path for 'wikipedia'
            content = self.ddg_search.search(query, max_results)
            source_name = "DuckDuckGo Search"
            self.current_document = content
            self.document_source = f"{source_name}: {query}"
            return self.current_document
        except Exception as e:
            error_msg = f"Web search error: {str(e)}"
            print(error_msg)  # For logging
            return error_msg
            
    def get_relevant_context(self, query: str, max_chars: int = 8000) -> str:
        """Get the most relevant context for a query using vector search if available"""
        if self.vector_store and self.embeddings:
            try:
                # Use vector search to retrieve relevant document parts
                docs = self.vector_store.similarity_search(query, k=3)
                relevant_text = "\n\n".join([doc.page_content for doc in docs])
                
                # If the combined text is too long, truncate it
                if len(relevant_text) > max_chars:
                    return relevant_text[:max_chars] + "..."
                return relevant_text
            except Exception as e:
                print(f"Vector search error: {str(e)}")
                # Fall back to the full document
                
        # If no vector store or error occurred, return full document or part of it
        if len(self.current_document) > max_chars:
            return self.current_document[:max_chars] + "..."
        return self.current_document

    def get_current_document(self) -> str:
        """Return the currently loaded document"""
        return self.current_document

    def get_document_source(self) -> str:
        """Return the source of the currently loaded document"""
        return self.document_source

@st.cache_resource
def get_hf_pipeline():
    return pipeline(
        "question-answering",
        model="distilbert-base-cased-distilled-squad",
        tokenizer="distilbert-base-cased-distilled-squad"
    )

class HuggingFaceQA:
    """
    Question-Answering system using Hugging Face transformers library.
    Uses a pre-trained model for extractive QA.
    """
    def __init__(self):
        try:
            # Use cached pipeline
            self.qa_pipeline = get_hf_pipeline()
        except Exception as e:
            print(f"Failed to initialize QA pipeline: {str(e)}")
            self.qa_pipeline = None

    def answer_question(self, question: str, context: str) -> Dict:
        """
        Answer a question based on the provided context using
        Hugging Face's question-answering pipeline
        """
        try:
            if not self.qa_pipeline:
                return {"answer": "QA pipeline not initialized", "score": 0.0}
                
            result = self.qa_pipeline(
                question=question,
                context=context
            )
            return result
        except Exception as e:
            error_msg = f"QA error: {str(e)}"
            print(error_msg)  # For logging
            return {"answer": error_msg, "score": 0.0}

class GeminiQA:
    """
    QA system using Google's Gemini API.
    Handles API communication and response processing.
    """
    def __init__(self, model_name="gemini-2.0-flash"):
        self.model_name = model_name
        try:
            self.model = genai.GenerativeModel(model_name)
        except Exception as e:
            error_msg = f"Error initializing Gemini model: {str(e)}"
            print(error_msg)
            self.model = None

    def answer_question(self, question: str, context: str) -> str:
        """
        Answer a question based on the provided context using Google's Gemini API
        """
        try:
            if not self.model:
                return "Gemini model not initialized"
            
            # Create a prompt that includes the context and question
            prompt = f"""
            Context:
            {context}
            
            Question:
            {question}
            
            Answer the question based ONLY on the information provided in the context above.
            If the answer cannot be found in the context, state "I cannot answer this based on the provided context."
            """
            
            response = self.model.generate_content(prompt)
            return response.text if hasattr(response, 'text') else "No response generated"
            
        except Exception as e:
            error_msg = f"Error generating response: {str(e)}"
            print(error_msg)  # For logging
            return error_msg

def create_qa_prompt(question: str, context: str) -> str:
    """
    Creates a prompt for question answering, structuring the request
    to get accurate answers based on the provided context.
    """
    return f"""
    Answer the following question based on the provided context:
    
    Context: {context}
    
    Question: {question}
    
    Answer:
    """

def log_qa_activity(question: str, context: str, answer: str, method: str):
    """
    Creates an expandable log of QA activities in the Streamlit interface
    for transparency and debugging purposes.
    """
    with st.expander("View QA Activity Log"):
        st.write(f"### QA Process ({method}):")
        
        st.write("**Context Used:**")
        st.code(context, language="text")
        
        st.write("**Question:**")
        st.code(question, language="text")
        
        st.write("**Generated Answer:**")
        st.code(answer, language="text")

# Initialize Streamlit app
st.set_page_config(page_title="Knowledge QA System", layout="wide")

# Title and description
st.title("🧠 Knowledge Extraction Q&A System")
st.write("""
Experience an advanced Q&A system for extracting context-based insights. 
Upload a document, choose an example, or provide your own text, then 
ask questions to get targeted answers directly from your content.
""")

# Initialize the components
try:    # Initialize document loader and QA models
    doc_loader = DocumentLoader()
    hf_qa = HuggingFaceQA()
    gemini_qa = GeminiQA()

    # Move model selection here
    model_option = st.sidebar.radio(
        "Choose QA Model",
        ["Google Gemini", "Hugging Face Transformers"]
    )
    
    # Sidebar for document loading options
    st.sidebar.header("Document Source")
    source_option = st.sidebar.radio(
        "Choose document source",
        ["Paste Text", "Upload File", "Web Search"]
    )

    document = ""
    # Document loading area
    if source_option == "Paste Text":
        user_text = st.sidebar.text_area(
            "Paste your document text here",
            height=250,
            placeholder="Paste your document here..."
        )
        if user_text:
            document = doc_loader.load_from_text(user_text)
        
    elif source_option == "Upload File":
        uploaded_file = st.sidebar.file_uploader(
            "Upload a document", 
            type=["txt", "md", "pdf", "docx"]
        )
        if uploaded_file:
            with st.spinner("Processing document..."):
                document = doc_loader.load_from_file(uploaded_file)
            
    elif source_option == "Web Search":
        max_results = st.sidebar.slider(
            "Number of results", 
            min_value=1, 
            max_value=10, 
            value=5
        )
        col_center = st.columns([1, 2, 1])
        with col_center[1]:
            st.markdown("<h3 style='text-align:center;'>❓ Ask a Question</h3>", unsafe_allow_html=True)
            user_question = st.text_input(
                "Enter your question:",
                placeholder="Ask about the document or perform a web search...",
                key="web_search_input"
            )
            if st.button("Get Answer", key="qa_answer_btn"):
                if source_option == "Web Search" and not document and user_question:
                    with st.spinner(f"Searching DuckDuckGo..."):
                        source = "duckduckgo"
                        document = doc_loader.load_from_web_search(
                            user_question, 
                            source=source, 
                            max_results=max_results
                        )
                
                if not document:
                    st.warning("No document available. Please provide text, upload a file, or enter a search question.")
                elif not user_question:
                    st.warning("Please enter a question.")
                else:
                    with st.spinner("Extracting knowledge..."):
                        try:
                            if model_option == "Google Gemini":
                                answer = gemini_qa.answer_question(user_question, document)
                                method = "Google Gemini"
                            else:
                                result = hf_qa.answer_question(user_question, document)
                                answer = result["answer"]
                                confidence = f"{result.get('score', 0.0):.2f}"
                                method = f"Hugging Face (confidence: {confidence})"
                        
                            st.success("Answer extracted!")
                            st.markdown("### Answer:")
                            st.markdown(answer)
                            
                            log_qa_activity(
                                user_question,
                                document[:500] + "..." if len(document) > 500 else document,
                                answer,
                                method
                            )
                        except Exception as e:
                            st.error(f"An error occurred during knowledge extraction: {str(e)}")

    # Main content area - Document display and QA interface
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.subheader("📄 Document Content")
        if document:
            st.markdown(f"**Source:** {doc_loader.get_document_source()}")
            st.text_area("", document, height=300, disabled=True)
        else:
            if source_option in ["Paste Text", "Upload File"]:
                st.info("Please select or upload a document to begin.")

    with col2:
        if source_option != "Web Search":
            st.markdown("<h3 style='text-align:center;'>❓ Ask a Question</h3>", unsafe_allow_html=True)
            user_question = st.text_input(
                "Enter your question:",
                placeholder="Ask about the document or perform a web search...",
                key="main_question_input"
            )
            
            if st.button("Get Answer", key="qa_answer_btn"):
                if source_option == "Web Search" and not document and user_question:
                    with st.spinner(f"Searching DuckDuckGo..."):
                        source = "duckduckgo"
                        document = doc_loader.load_from_web_search(
                            user_question, 
                            source=source, 
                            max_results=max_results
                        )
                
                if not document:
                    st.warning("No document available. Please provide text, upload a file, or enter a search question.")
                elif not user_question:
                    st.warning("Please enter a question.")
                else:
                    with st.spinner("Extracting knowledge..."):
                        try:
                            if model_option == "Google Gemini":
                                answer = gemini_qa.answer_question(user_question, document)
                                method = "Google Gemini"
                            else:
                                result = hf_qa.answer_question(user_question, document)
                                answer = result["answer"]
                                confidence = f"{result.get('score', 0.0):.2f}"
                                method = f"Hugging Face (confidence: {confidence})"
                        
                            st.success("Answer extracted!")
                            st.markdown("### Answer:")
                            st.markdown(answer)
                            
                            log_qa_activity(
                                user_question,
                                document[:500] + "..." if len(document) > 500 else document,
                                answer,
                                method
                            )
                        except Exception as e:
                            st.error(f"An error occurred during knowledge extraction: {str(e)}")

    # Add helpful tips
    with st.expander("💡 Tips for Better Questions"):
        st.write("""
        - Ask specific questions related to the content in the document
        - Try different phrasings if you don't get the expected answer
        - Break complex questions into simpler ones
        - Questions like "What is X?", "How does X work?", or "When was X discovered?" work best        - The system can only answer based on information in the provided document
        """)

except Exception as e:
    st.error(f"""
    Failed to initialize the application: {str(e)}


    """)

# Footer
st.markdown("---")
st.caption(
    "Powered by Google Gemini, Hugging Face Transformers, and Streamlit | "
    "Created for knowledge extraction and Q&A demonstration"
)
