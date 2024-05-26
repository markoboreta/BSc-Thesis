from common.classes.classs_model.model import Model
import os
# class for the model
class PA(Model):
    def __init__(self, modelPath, vectPath):
        super().__init__(modelPath, vectPath)

    def predict_news_article(self, article):
        try:
            prediction = self.verdict(article)
            if prediction[0] == 0:
                return "The news article is highly likely to be fake according to PA."
            else:
                return "The news article is highly likely to be real according to PA."
        except Exception as e:
            return "Error: Not good return on verdict"
        

base_dir = os.path.abspath(os.path.dirname(__file__))
model_path = os.path.join(base_dir, 'model_and_vect', 'PA_model.pkl')
vect_path = os.path.join(base_dir, 'model_and_vect', 'PA_Tfidf.pkl')


PA_Model = PA(model_path, vect_path)