from flask_restful import Resource, Api, reqparse
import requests

# Flask-Restful API for communication between the backend services 

# Rettrieve data from the predict_NB
class PredictNB(Resource):
    def post(self, message_data):
        message = message_data['message']

        try:
            # test env
            #url = "http://127.0.0.1:5002/predict_NB"
            # Docker env for production
            url = 'http://NBapp:5002/predict_NB'
            payload = {'message': message}
            response = requests.post(url, data=payload)
            response.raise_for_status()  # Raise an exception if the request fails
            if response.status_code == 200:
                return response.json(), 200
            else:
                return {'error': f'Request failed with status code {response.status_code}'}, 404
        except requests.exceptions.RequestException as e:
            return {'error': str(e)}, 500


# Rettrieve data from the predict_PA
class PredictPA(Resource):
    def post(self, message_data):
        message = message_data['message']

        try:
            # test env
            #url = "http://127.0.0.1:5003/predict_PA"
            url = 'http://PAapp:5003/predict_PA'
            payload = {'message': message}
            response = requests.post(url, data=payload)
            response.raise_for_status()  # Raise an exception if the request fails
            if response.status_code == 200:
                return response.json(), 200
            else:
                return {'error': f'Request failed with status code {response.status_code}'}, response.status_code
        except requests.exceptions.RequestException as e:
            return {'error': str(e)}, 500

# Rettrieve data from the predict_LR
class PredictLR(Resource):
    def post(self, message_data):
        message = message_data['message']

        try:
            # test env
            #url = "http://127.0.0.1:5001/predict_LR"
            url = 'http://LRapp:5001/predict_LR'
            payload = {'message': message}
            response = requests.post(url, data=payload)
            response.raise_for_status()  # Raise an exception if the request fails
            if response.status_code == 200:
                return response.json(), 200
            else:
                return {'error': f'Request failed with status code {response.status_code}'}, response.status_code
        except requests.exceptions.RequestException as e:
            return {'error': str(e)}, 500
        

