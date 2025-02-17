import nltk
import spacy
import string
import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer

# Download required NLTK datasets
nltk.download("punkt")
nltk.download("stopwords")

# Load Spacy model for advanced NLP tasks
nlp = spacy.load("en_core_web_sm")

def clean_text(text):
    """Removes punctuation and converts text to lowercase."""
    text = text.lower()
    text = text.translate(str.maketrans("", "", string.punctuation))
    return text

def preprocess_text(text):
    """Tokenizes, removes stopwords, and stems words in text."""
    stop_words = set(stopwords.words("english"))
    stemmer = PorterStemmer()
    
    tokens = word_tokenize(text)
    tokens = [stemmer.stem(word) for word in tokens if word not in stop_words]
    return " ".join(tokens)

def generate_embeddings(text_series):
    """Converts text data into TF-IDF vector embeddings."""
    vectorizer = TfidfVectorizer(max_features=1000)
    embeddings = vectorizer.fit_transform(text_series)
    return embeddings

if __name__ == "__main__":
    # Sample dataset
    df = pd.DataFrame({"text": ["Natural Language Processing is amazing!", 
                                "AI and ML are revolutionizing technology.", 
                                "Text analytics is an exciting field."]})

    # Preprocess text column
    df["cleaned_text"] = df["text"].apply(clean_text).apply(preprocess_text)
    
    # Generate embeddings
    text_embeddings = generate_embeddings(df["cleaned_text"])

    print("Text preprocessing complete. Sample output:")
    print(df.head())
