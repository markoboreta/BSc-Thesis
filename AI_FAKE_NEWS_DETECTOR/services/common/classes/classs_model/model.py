import re
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import  wordnet as wn
from nltk.corpus import stopwords
import nltk
import pickle

# Download NLTK resources if not already downloaded
nltk.download("punkt")
nltk.download("wordnet")
nltk.download("averaged_perceptron_tagger")
nltk.download("stopwords")


# Class for each model
class Model:
    def __init__(self, model_path:str, vect_path:str):
        self.lemmatizer = WordNetLemmatizer()
        self.model = self.load_pickle(model_path)
        self.vect = self.load_pickle(vect_path)
        self.stop_words = set(stopwords.words('english'))


    def load_pickle(self, model_path):
        if model_path.endswith('.pkl'):
            try:
                with open(model_path, "rb") as f:
                    model = pickle.load(f)
                return model
            except:
                print("Error opening this file.")
        else:
            print('Model not pickeled file!')

    # remove special characters
    def remove_special(self, text):
        if isinstance(text, str):
            text = text.lower()
            # Remove URLs, HTML tags, special characters, and digits
            pattern = r'https?://\S+|www\.\S+|<.*?>|\d+|\W+'
            text = re.sub(pattern, ' ', text)
            text = re.sub(r'\W+', ' ', text)
            text = text.replace('\n', ' ')
            return text.strip()
        return ""

    # Remove special characters, tokenize and remove stop words
    def preprocess_text(self, text):
        try:
            #print("text type received: ", type(text))
            text = self.remove_special(text)
            #print("after removing special", text)
            if text:
                tokenized = word_tokenize(text)
                #print("tokenized ", tokenized)
                #print("joined ", ' '.join([self.lemmatizer.lemmatize(w) for w in tokenized if w not in self.stop_words]))                
                return ' '.join([self.lemmatizer.lemmatize(w) for w in tokenized if w not in self.stop_words])
        except:
            print("Error, data is not textual most likely")
            return "Error, unable to proceed, data provided is not OK."
        return 
    
    # Return the verdcit of the models
    def verdict(self, text):
        try:
            if not text or text.isspace():
                print("Invalid input - article is empty or not provided.")
                return -1
            preprocessed_article = self.preprocess_text(text)
            #print(preprocessed_article)
            if not preprocessed_article or preprocessed_article.isspace():
                return -1
            article_vector = self.vect.transform([preprocessed_article])
            prediction = self.model.predict(article_vector)
            return prediction  # return the verdict model has made, numerical value 1 or 0
        except Exception as e:
                print(f"Error during vector transformation or prediction: {e}")
                return ValueError("Error during vector transformation or prediction")
 
