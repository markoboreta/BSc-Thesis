import re
import string
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
    def __init__(self, modelPath:str, vectPath:str):
        self.lemmatizer = WordNetLemmatizer()
        self.model = self.load_model(modelPath)
        self.vect = self.load_vect(vectPath)
        self.stop_words = set(stopwords.words('english'))


    def load_model(self, modelpath:str):
        if modelpath.endswith('.pkl'):
            try:
                with open(modelpath, "rb") as f:
                    model = pickle.load(f)
                return model
            except:
                print("Error opening this file.")
        else:
            print('Model not pickeled file!')
    
    def load_vect(self, vectPath:str): 
        if vectPath.endswith('.pkl'):
            try:
                with open(vectPath, "rb") as f:
                    vect = pickle.load(f)
                return vect
            except:
                print("Error opening this file.")
        else:
            print('Vector not pickeled file!')
        

    def remove_special(self, text):
        if isinstance(text, str):
            text = text.lower()
            # Remove URLs, HTML tags, special characters, and digits
            pattern = r'\[.*?\]|https?://\S+|www\.\S+|<.*?>+|\w*\d\w*|[%s]' % re.escape(string.punctuation)
            text = re.sub(pattern, ' ', text)
            text = re.sub(r'\W+', ' ', text)
            text = text.replace('\n', ' ')
            return text.strip()
        return ""

    # Remove special characters, tokenize and remove stop words
    def preprocess_text(self, text):
        text = self.remove_special(text)
        try:
            if text:
                tokenized = word_tokenize(text)
                stop_words = set(stopwords.words('english'))
                return ' '.join([self.lemmatizer.lemmatize(w) for w in tokenized if w not in self.stop_words])
        except:
            print("Error, data is not textual most likely")
            return "Error, unable to proceed, data provided is not OK."
        return 
    
    # Return the verdcit of the models
    def verdict(self, text):
        if not text or text.isspace():
            print("Here 1")
            print("Invalid input - article is empty or not provided.")
            return 1
        
        preprocessed_article = self.preprocess_text(text)
        print(preprocessed_article)

        if not preprocessed_article or preprocessed_article.isspace():
            print("Here 2")
            print("Invalid input - preprocessing resulted in empty content.")
            return 1
        else:
            print("Here 3")
            article_vector = self.vect.transform([preprocessed_article])
            prediction = self.model.predict(article_vector)
            return prediction # return the verdict model has made, numerical value 1 or 0
    
