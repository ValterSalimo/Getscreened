# Movie Review Sentiment Analysis

A complete toolkit for analyzing sentiment in movie reviews using a fine-tuned DistilBERT model. This project includes both a command-line interface and Jupyter notebook implementations.

## Overview

This application uses a fine-tuned DistilBERT model trained on the IMDB Movie Reviews dataset to classify reviews as either positive or negative. It was developed with both developers and data scientists in mind, offering flexible interfaces for various use cases.

## Quick Start

To get started quickly with the interactive sentiment analyzer:

```bash
python sentiment_cli.py
```

This will launch an interactive interface where you can enter movie reviews and see real-time sentiment analysis results.

## Google Colab Notebook

You can view and run the training notebook directly in Google Colab:
[Open Notebook in Colab](https://drive.google.com/file/d/1_CQ9F4vXWZw6rPhiKYb9VyXEcuisGH4F/view?usp=sharing)

## Setup

1. Install the required dependencies:

```bash
pip install -r requirements.txt
```

2. Make sure the model is available at the correct location:
```
imdb_sentiment_mode/imdb_sentiment_model/
```

## Command Line Interface Options

### 1. Interactive Mode (Recommended)

Simply run the script without any arguments to enter interactive mode:
```bash
python sentiment_cli.py
```

This will start a user-friendly interface where you can:
- Enter movie reviews at the prompt
- Get instant sentiment analysis with color-coded results
- Continue analyzing multiple reviews in the same session
- Type 'exit' to quit the program

### 2. Single Review Analysis

To analyze a single review directly:
```bash
python sentiment_cli.py --review "The movie was fantastic with great performances!"
```

### 3. Batch Processing from File

To analyze multiple reviews from a file (one review per line):
```bash
python sentiment_cli.py --file example_reviews.txt
```

### 4. Specifying Model Path

If your model is in a different location:
```bash
python sentiment_cli.py --model "path/to/your/model" --review "This was a great movie"
```

## Alternative CLI Interfaces

This project also includes the legacy `app.py` interface which provides additional options:

### 1. Analyze a single review:

```bash
python app.py --text "This movie was excellent! The acting was superb and the plot was engaging."
```

### 2. Process multiple reviews and save to CSV:

```bash
python app.py --file "reviews.txt" --output "results.csv"
```

### 3. Additional options:

```bash
python app.py --text "A review" --model_path "./my_custom_model" --no-color
```

## Jupyter Notebook Usage

For interactive usage in a Jupyter notebook:

```python
# Import the widget function
from jupyter_widget import create_sentiment_widget

# Create and display the interactive widget
create_sentiment_widget()
```

A sample notebook (`local_csv_sentiment_analysis.ipynb`) is included that demonstrates the entire workflow from model training to interactive usage.

## Features

- **Text preprocessing** to clean and normalize input text
- **Fast prediction** using cached model loading
- **Interactive command line interface**
- **Batch processing** of multiple reviews from file
- **CSV export** for batch processing results
- **Interactive Jupyter notebook widget**
- **Color-coded output** for better readability
  - Green for positive sentiment
  - Red for negative sentiment
  - Emoji indicators (😄 for positive, 😞 for negative)
- **GPU acceleration** when available
- **Detailed metrics**
  - Sentiment classification (Positive/Negative)
  - Confidence score (percentage)
  - Processing time measurements

## Model Information

The sentiment analysis model is a fine-tuned version of DistilBERT, trained on the IMDB Movie Reviews dataset with 50,000 reviews. The model has been optimized for sentiment classification of movie reviews and achieves high accuracy.

## File Structure

- `sentiment_cli.py` - Modern CLI tool with color-coded output (run without arguments for interactive mode)
- `app.py` - Legacy CLI with CSV export support
- `local_csv_sentiment_analysis.ipynb` - Complete notebook with model training and interactive usage
- `requirements.txt` - All required dependencies
- `example_reviews.txt` - Sample reviews for batch testing
- `imdb_sentiment_mode/imdb_sentiment_model/` - Pre-trained model files

## Usage Examples

### Interactive Mode Demo

```
$ python sentiment_cli.py

 Movie Review Sentiment Analysis 

Enter your movie review below (or type 'exit' to quit):
------------------------------------------------------------
> This movie was absolutely brilliant! Great performances and an engaging plot.
Analyzing sentiment...

============================================================
 Positive SENTIMENT  😄
------------------------------------------------------------
Confidence: 99.8%
Processing time: 0.6841 seconds
============================================================

Press Enter to continue or type 'exit' to quit...
```

## Notes

The CLI tool and Jupyter widget both use the same underlying model and preprocessing pipeline to ensure consistent results across interfaces.
