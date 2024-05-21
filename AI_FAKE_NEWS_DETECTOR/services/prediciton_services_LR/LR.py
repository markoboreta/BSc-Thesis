from collections import defaultdict
from common.classes.classs_model.model import Model



# class for the model
class LR(Model):
    def __init__(self, modelPath, vectPath):
        super().__init__(modelPath, vectPath)

    def predict_news_article(self, article):
        try:
            print(">>>>>>>>>>ARTICLE\n\n", len(article))
            prediction = self.verdict(article)
            if prediction[0] == 0:
                return "The news article is highly likely to be fake according to LR."
            else:
                return "The news article is highly likely to be real according to LR."
        except Exception as e:
            return None
        
model_path = 'model_and_vect/single_LR_plain_NEW.pkl'
vect_path = 'model_and_vect/single_LR_vect_plain_NEW.pkl'

LRModel = LR(model_path, vect_path)

