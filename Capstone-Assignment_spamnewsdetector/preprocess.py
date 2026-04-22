# ============================================================
# Project  : AI Spam News Detector
# File     : preprocess.py
# Purpose  : NLP text preprocessing utilities
# Student  : ___________________________
# Roll No  : ___________________________
# Date     : ___________________________
# ============================================================

import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

# Download required NLTK data (runs once)
nltk.download('stopwords', quiet=True)
nltk.download('punkt', quiet=True)

stemmer = PorterStemmer()
stop_words = set(stopwords.words('english'))


def clean_text(text: str) -> str:
    """
    Full NLP preprocessing pipeline:
    1. Lowercase
    2. Remove URLs, HTML tags, special characters
    3. Remove stopwords
    4. Apply Porter Stemming
    """
    if not isinstance(text, str):
        return ""

    # Lowercase
    text = text.lower()

    # Remove URLs
    text = re.sub(r'https?://\S+|www\.\S+', '', text)

    # Remove HTML tags
    text = re.sub(r'<.*?>', '', text)

    # Remove special characters, numbers, punctuation
    text = re.sub(r'[^a-z\s]', '', text)

    # Tokenize
    tokens = text.split()

    # Remove stopwords and short tokens, apply stemming
    tokens = [
        stemmer.stem(word)
        for word in tokens
        if word not in stop_words and len(word) > 2
    ]

    return ' '.join(tokens)


if __name__ == '__main__':
    sample = "Breaking News! Scientists discover <b>new</b> planet - https://example.com"
    print("Original :", sample)
    print("Processed:", clean_text(sample))
