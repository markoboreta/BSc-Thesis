import os
import logging
import json
import requests
from flask import Flask, render_template, request, jsonify
from flask import  request
from flask_cors import CORS
from LR_service import LRModel 
from flask import request, jsonify
from flask import request, render_template, abort
from common.classes.class_service.service import Service
from common.classes.class_service.service_api import PredictPA, PredictNB
from flask_restful import Api


# Class for the service
class LRApp(Service):
    def __init__(self, import_name):
        super().__init__(import_name)
        self.set_up_routes()
        self.api = Api(self)
        self.api.add_resource(PredictNB, '/api/predict_nb')
        self.api.add_resource(PredictPA, '/api/predict_pa')
        
    
    def set_up_routes(self):
        # route for the main page of the 
        @self.route("/LR_page", methods=["GET", "POST"])
        def LR_page():
            if request.method == "POST" or request.method == "GET":
                return render_template("Model_2.html")
        
        @self.route('/getTFData')
        def get_graph_data():
            # Load JSON data from file
            with open("static/TF.json") as data_file:
                data = json.load(data_file)
            # Return JSON response
            return jsonify(data)
        
        @self.route('/getWCData')
        def get_WC_data():
            # Load JSON data from file
            with open("static/WC.json") as data_file:
                data = json.load(data_file)
            # Return JSON response
            return jsonify(data)

        @self.route("/predict_LR", methods=["POST"])
        def predict_LR():
            if request.method == "POST":
                # Retrieve the text data from the form field named "message"
                data = request.form.get("message", "")
                print(type(data))
                # Check if the received data is empty or invalid
                if not data:
                    return jsonify(error="Invalid input. Please provide a message."), 400
                try:
                    # Process the received data using the LR model
                    processed_result_lr = LRModel.predict_news_article(data)
                    print(processed_result_lr)
                    return jsonify(result=processed_result_lr), 200
                except Exception as e:
                    error_message = f"Error occurred while processing data: {str(e)}"
                    return jsonify(error=error_message), 500
            else:
                print("Not goot method")

        @self.route("/LR/get_result", methods=["POST"])
        def predict_toegther():
            if request.method == "POST":
                predict_nb = PredictNB()
                predict_pa = PredictPA()
                # Retrieve the text data from the form field named "message"
                data = request.form.get("message", "")
                # Check if the received data is empty or invalid
                if not data:
                    return jsonify(error="Invalid input. Please provide a message."), 400
                try:
                    # Make a request to the PredictNB class
                    pa_response = predict_pa.post({"message" : data})
                    nb_response = predict_nb.post({"message" : data})
                    if nb_response[1] != 200:
                        return nb_response
                    if pa_response[1] != 200:
                        return pa_response
                    # Combine the results from all models
                    combined_result = {
                        "result1" : nb_response[0],
                        "result2" : pa_response[0]
                    }

                    # Response, send 200 as OK
                    return jsonify(result=combined_result), 200
                except Exception as e:
                    # Handle errors
                    error_message = f"Error occurred while processing data: {str(e)}"
                    return jsonify(error=error_message), 500
            else:
                # Return a 405 Method Not Allowed error if the method is not POST
                return jsonify(error="Method not allowed."), 405

if __name__ == "__main__":
    app = LRApp(__name__)
    app.run(host="0.0.0.0", port=5001, debug=True)