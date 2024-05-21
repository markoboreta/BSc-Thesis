from common.classes.classs_model.model import Model

# class for the model
class PA(Model):
    def __init__(self, modelPath, vectPath):
        super().__init__(modelPath, vectPath)

    def predict_news_article(self, article):
        prediction = super().verdict(article)
        if prediction[0] == 0:
            return "The news article is highly likely to be fake according to PA."
        else:
            return "The news article is highly likely to be real according to PA."
        


model_path = 'model_and_vect/PA_model.pkl'
vect_path = 'model_and_vect/PA_Tfidf.pkl'

PAModel = PA(model_path, vect_path)