import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from bs4 import BeautifulSoup

# Download các tài nguyên cần thiết
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
def preprocess_text(text):
    # Remove HTML tags
    text = clean_html_tags(text)
    # Remove special characters and punctuation
    text = re.sub(r'[^\w\s]', '', text)
    # Tokenize the text
    tokens = word_tokenize(text.lower())

    # Specify the file path for the custom stopwords file
    stopwords_file = '/Users/voduytao/Documents/rasa-chatbot/stopwords_vietnamese.txt'

    # Load stopwords from the custom file
    with open(stopwords_file, 'r', encoding='utf-8') as f:
        custom_stopwords = f.read().splitlines()

    # Convert the list of stopwords into a set for faster lookup
    stop_words = set(custom_stopwords)

    tokens = [word for word in tokens if word not in stop_words]
    # Lemmatization
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(word) for word in tokens]
    return ' '.join(tokens)

def clean_html_tags(text):
    if isinstance(text, str):
        soup = BeautifulSoup(text, 'html.parser')
        clean_text = soup.get_text(separator=' ')
        return clean_text
    else:
        return ''