import os
import logging
import json
import requests
from flask import Flask, render_template, request, jsonify
from flask import  request, Blueprint, send_from_directory, Response
from flask_cors import CORS
from flask import request, jsonify
from flask import request, render_template, abort
from common.classes.class_service.service import Service
from common.classes.class_service.service_api import PredictPA, PredictLR
from flask_restful import Api
from NB import NBModel
from common.classes.class_service.service import Service


# Class for the service
class NBApp(Service):
    def __init__(self, import_name):
        super().__init__(import_name)
        self.set_up_routes()
        self.api = Api(self)
        self.api.add_resource(PredictPA, '/api/predict_pa')
        self.api.add_resource(PredictLR, '/api/predict_lr')
  
    def set_up_routes(self):
        # route for the main page of the 
        @self.route("/NB_page", methods=["GET", "POST"])
        def NB_page():
            return render_template("Model_3.html")
        
        
        @self.route("/predict_NB", methods=["POST"])
        def predict_NB():
            if request.method == "POST":
                data = request.form.get("message", "")
                print('here')
                if not data:
                    # If message data is missing or invalid, return an error response
                    return jsonify(error="Invalid input. Please provide a message."), 400
                try:
                    # Process the received data
                    processed_result = NBModel.predict_news_article(data)
                    print(processed_result)
                    return jsonify(result=processed_result), 200
                except Exception as e:
                    error_message = f"Error occurred while processing data: {str(e)}"
                    return jsonify(error=error_message), 500
            else:
                print("Not goot method")

        # to be added for the json formatt
        @self.route('/getNBData')
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

        @self.route("/NB/get_result", methods=["POST"])
        def predict_toegther():
            if request.method == "POST":
                data = request.form.get("message", "")
                predict_lr = PredictLR()
                predict_pa = PredictPA()
                
                if not data:
                    return jsonify(error="Error: Invalid input. Please provide a 'message' field in JSON format."), 400
                try:
                    pa_response = predict_pa.post({"message" : data})
                    lr_response = predict_lr.post({"message" : data})

                    if lr_response[1] != 200:
                        return jsonify(lr_response) 
                    if pa_response[1] != 200:
                        return jsonify(pa_response)
                    
                    # Combine the results from all models
                    combined_result = {
                        "result1": lr_response[0],
                        "result2": pa_response[0]
                    }
                    return jsonify(result=combined_result), 200

                except Exception as e:
                    error_message = f"Error occurred while processing data: {str(e)}"
                    return jsonify(error=error_message), 500

            else:
                return jsonify(error="Method not allowed."), 405


app = NBApp(__name__)
app.run(host="0.0.0.0", port=5002, debug=True) 
