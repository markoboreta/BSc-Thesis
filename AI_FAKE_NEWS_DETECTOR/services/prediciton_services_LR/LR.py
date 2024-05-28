from collections import defaultdict
from common.classes.classs_model.model import Model
import os


# class for the model
class LR(Model):
    def __init__(self, modelPath, vectPath):
        super().__init__(modelPath, vectPath)

    # will return the verdict as a readable user output
    def predict_news_article(self, article):
        try:
            #print("text received: ", article)
            prediction = self.verdict(article)
            if prediction[0] == 0:
                return "The news article is highly likely to be fake according to LR."
            else:
                return "The news article is highly likely to be real according to LR."
        except Exception as e:
            return "Error: Not good return on verdict"
        
base_dir = os.path.abspath(os.path.dirname(__file__))
model_path = os.path.join(base_dir, 'model_and_vect', 'LR_model.pkl')
vect_path = os.path.join(base_dir, 'model_and_vect', 'LR_vect.pkl')

LR_model = LR(model_path, vect_path)

