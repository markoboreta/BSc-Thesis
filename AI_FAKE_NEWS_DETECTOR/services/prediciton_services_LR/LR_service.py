import re
import string
import sys
import pickle
#from model_classs.model import model
from collections import defaultdict
from common.classes.classs_model.model import Model
import pandas as pd
from flask import Flask, render_template, request, jsonify
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords, wordnet as wn
from nltk import pos_tag
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk




# class for the model
class LR(Model):
    def __init__(self, modelPath, vectPath):
        super().__init__(modelPath, vectPath)

    def predict_news_article(self, article):
        prediction = super().verdict(article)
        print(prediction)
        if prediction[0] == 0:
            return "The news article is highly likely to be real according to LR."
        else:
            return "The news article is highly likely to be fake according to LR."
        
model_path = 'model_and_vect/single_LR_plain_NEW.pkl'
vect_path = 'model_and_vect/single_LR_vect_plain_NEW.pkl'

LRModel = LR(model_path, vect_path)

