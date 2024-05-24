from flask_restful import Resource, Api, reqparse
import requests

# Flask RESTful API for communication between the backend services 

class API_Class(Resource):

    def __init__(self, url):
        self.url = url

    def post(self,  message_data):
        message = message_data['message']
        try:
            payload = {'message': message}
            response = requests.post(self.url, data=payload)
            response.raise_for_status()  # Raise an exception if the request fails
            if response.status_code == 200:
                return response.json(), 200
            else:
                return {'error': f'Request failed with status code {response.status_code}'}, 404
        except requests.exceptions.RequestException as e:
            return {'error': str(e)}, 500

"""
!!!!!!!!!!!! USE BOTTOM URL FOR DOCKER !!!!!!!!!!!! 
"""

# Rettrieve verdict from the predict_NB
#url = "http://127.0.0.1:5002/predict_NB" #test env url
#url = "http://NBapp:5002/predict_NB"
class PredictNB(API_Class):
    def __init__(self):
        super().__init__("http://NBapp:5002/predict_NB")


# Rettrieve verdict from the predict_PA
#url = "http://127.0.0.1:5003/predict_PA"
#url = 'http://PAapp:5003/predict_PA'
class PredictPA(API_Class):
    def __init__(self):
        super().__init__('http://PAapp:5003/predict_PA')
  
# Rettrieve verdict from the predict_LR
#url = "http://127.0.0.1:5001/predict_LR"
#url = 'http://LRapp:5001/predict_LR'
class PredictLR(API_Class):
    def __init__(self):
        super().__init__('http://LRapp:5001/predict_LR')
        

