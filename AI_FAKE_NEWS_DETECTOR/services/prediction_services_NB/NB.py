import os
from common.classes.classs_model.model import Model

# class for the Naive Bayes model
class NB(Model):
    def __init__(self, modelPath, vectPath):
        super().__init__(modelPath, vectPath)

    def predict_news_article(self, article):
        try:
            prediction = self.verdict(article)
            if prediction[0] == 0:
                return "The news article is highly likely to be fake according to NB."
            else:
                return "The news article is highly likely to be real according to NB."
        except Exception as e:
           return "Error: Not good return on verdict"

base_dir = os.path.abspath(os.path.dirname(__file__))
model_path = os.path.join(base_dir, 'model_and_vect', 'last_naive_model_final.pkl')
vect_path = os.path.join(base_dir, 'model_and_vect', 'last_count_vectorizer_NB_final.pkl')

NB_model = NB(model_path, vect_path)