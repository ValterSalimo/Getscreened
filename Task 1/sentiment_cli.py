import time
import torch
import re
import os
import colorama
import argparse
from colorama import Fore, Back, Style
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification

# Initialize colorama for colored terminal output
colorama.init()

def preprocess_text(text, remove_stopwords=False, lemmatize=False):
    """
    Preprocess text data with configurable options
    
    Args:
        text (str): Text to preprocess
        remove_stopwords (bool): Whether to remove stopwords
        lemmatize (bool): Whether to apply lemmatization
    
    Returns:
        str: Preprocessed text
    """
    # Convert to lowercase
    text = text.lower()
    
    # Remove HTML tags
    text = re.sub(r'<.*?>', '', text)
    
    # Remove URLs
    text = re.sub(r'http\S+|www\S+|https\S+', '', text)
    
    # Remove special characters and numbers (keep only letters and spaces)
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Advanced preprocessing is omitted for simplicity
    # Would require nltk installation
    
    return text

def predict_sentiment(text, model_path="imdb_sentiment_mode\\imdb_sentiment_model", preprocess=True):
    """
    Predict the sentiment of a given text
    
    Args:
        text (str): The text to analyze
        model_path (str): Path to the saved model
        preprocess (bool): Whether to preprocess the text first
    
    Returns:
        tuple: (sentiment, confidence, processing_time)
    """
    start_time = time.time()
    
    # Check if model path exists
    if not os.path.exists(model_path):
        print(f"Model path not found at {model_path}")
        alt_path = "imdb_sentiment_model"
        if os.path.exists(alt_path):
            print(f"Using alternative path: {alt_path}")
            model_path = alt_path
        else:
            print("Model not found. Please check the model path.")
            return "Error", 0.0, 0.0
    
    # Load model and tokenizer
    try:
        model = DistilBertForSequenceClassification.from_pretrained(model_path)
        tokenizer = DistilBertTokenizer.from_pretrained(model_path)
    except Exception as e:
        print(f"Error loading model: {e}")
        return "Error", 0.0, 0.0
    
    # Set device
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = model.to(device)
    model.eval()  # Set model to evaluation mode
    
    # Preprocess text if requested
    if preprocess:
        text = preprocess_text(text)
    
    # Tokenize input
    inputs = tokenizer(
        text,
        padding="max_length",
        truncation=True,
        max_length=256,
        return_tensors="pt"
    ).to(device)
    
    # Get prediction
    with torch.no_grad():
        outputs = model(**inputs)
        probabilities = torch.nn.functional.softmax(outputs.logits, dim=-1)
        predicted_class = torch.argmax(probabilities, dim=1).item()
        confidence = probabilities[0][predicted_class].item()
    
    # Convert class to sentiment
    sentiment = "Positive" if predicted_class == 1 else "Negative"
    
    # Calculate processing time
    processing_time = time.time() - start_time
    
    return sentiment, confidence, processing_time

def analyze_single_review():
    """Interactive mode for sentiment analysis"""
    while True:
        # Display banner
        print(f"\n{Back.BLUE}{Fore.WHITE} Movie Review Sentiment Analysis {Style.RESET_ALL}")
        print("\nEnter your movie review below (or type 'exit' to quit):")
        print("-" * 60)
        
        # Get user input
        review = input("> ")
        
        if review.lower() == 'exit':
            print("Goodbye!")
            break
        
        if not review.strip():
            print(f"{Fore.YELLOW}Please enter a movie review to analyze.{Style.RESET_ALL}")
            continue
        
        # Show processing message
        print(f"{Fore.CYAN}Analyzing sentiment...{Style.RESET_ALL}")
        
        # Get prediction
        try:
            sentiment, confidence, prediction_time = predict_sentiment(review)
            
            # Set colors based on sentiment
            bg_color = Back.GREEN if sentiment == "Positive" else Back.RED
            emoji = "😄" if sentiment == "Positive" else "😞"
            
            # Display results
            print("\n" + "=" * 60)
            print(f"{bg_color} {sentiment} SENTIMENT {Style.RESET_ALL} {emoji}")
            print("-" * 60)
            print(f"Confidence: {Fore.YELLOW}{confidence:.1%}{Style.RESET_ALL}")
            print(f"Processing time: {Fore.CYAN}{prediction_time:.4f}{Style.RESET_ALL} seconds")
            print("=" * 60)
        except Exception as e:
            print(f"{Fore.RED}Error analyzing review: {e}{Style.RESET_ALL}")
        
        print("\nPress Enter to continue or type 'exit' to quit...")
        if input().lower() == 'exit':
            print("Goodbye!")
            break

def analyze_from_file(file_path):
    """Analyze reviews from a file, one per line"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            reviews = f.readlines()
        
        if not reviews:
            print(f"{Fore.YELLOW}No reviews found in file {file_path}{Style.RESET_ALL}")
            return
        
        print(f"\n{Back.BLUE}{Fore.WHITE} Analyzing {len(reviews)} reviews from {file_path} {Style.RESET_ALL}")
        print("-" * 60)
        
        for i, review in enumerate(reviews, 1):
            review = review.strip()
            if not review:
                continue
                
            print(f"Review #{i}: {review[:50]}..." if len(review) > 50 else f"Review #{i}: {review}")
            
            try:
                sentiment, confidence, prediction_time = predict_sentiment(review)
                bg_color = Back.GREEN if sentiment == "Positive" else Back.RED
                emoji = "😄" if sentiment == "Positive" else "😞"
                print(f"{bg_color} {sentiment} {Style.RESET_ALL} ({confidence:.1%}) {emoji} [{prediction_time:.4f}s]")
                print("-" * 60)
            except Exception as e:
                print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
    except FileNotFoundError:
        print(f"{Fore.RED}File not found: {file_path}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Error reading file: {e}{Style.RESET_ALL}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Movie Review Sentiment Analysis CLI')
    parser.add_argument('--file', '-f', help='Path to a file with reviews (one per line)')
    parser.add_argument('--review', '-r', help='Single review to analyze')
    parser.add_argument('--model', '-m', help='Path to model directory', default="imdb_sentiment_mode\\imdb_sentiment_model")
    
    args = parser.parse_args()
    
    if args.file:
        analyze_from_file(args.file)
    elif args.review:
        sentiment, confidence, prediction_time = predict_sentiment(args.review, model_path=args.model)
        bg_color = Back.GREEN if sentiment == "Positive" else Back.RED
        emoji = "😄" if sentiment == "Positive" else "😞"
        
        print(f"\n{bg_color} {sentiment} SENTIMENT {Style.RESET_ALL} {emoji}")
        print(f"Confidence: {confidence:.1%}")
        print(f"Processing time: {prediction_time:.4f} seconds")
    else:
        analyze_single_review()
