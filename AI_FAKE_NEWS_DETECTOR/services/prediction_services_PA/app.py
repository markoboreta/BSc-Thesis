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
from common.classes.class_service.service_api import PredictNB, PredictLR
from flask_restful import Api
import requests
from PA import PAModel
from flask import request, render_template, jsonify
from common.classes.class_service.service import Service


class PA_App(Service):
    def __init__(self, import_name):
        super().__init__(import_name)
        self.set_up_routes()
        self.api = Api(self)
        self.api.add_resource(PredictNB, '/api/predict_nb')
        self.api.add_resource(PredictLR, '/api/predict_lr')
  
    def set_up_routes(self):
        # route for the main page of the 
        @self.route("/PA_page", methods=["GET", "POST"])
        def PA_page():
            if request.method == "POST" or request.method == "GET":
                return render_template("Model_1.html")
        
        @self.route("/predict_PA", methods=["POST"])
        def predict_PA():
            if request.method == "POST":
                data = request.form.get("message", "")
                if not data:
                    # If message data is missing or invalid, return an error response
                    return jsonify(error="Invalid input. Please provide a message."), 400
                try:
                    # Process the received data
                    processed_result = PAModel.predict_news_article(data)
                    print(processed_result)
                    return jsonify(result=processed_result), 200
                except Exception as e:
                    # Handle any exceptions (e.g., model prediction error) and return an error response
                    error_message = f"Error occurred while processing data: {str(e)}"
                    return jsonify(error=error_message), 500
            else:
                print("Not goot method")
        
        @self.route('/getPAData')
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

        @self.route("/PA/get_result", methods=["POST"])
        def predict_toegther():
            print('here')
            # Check if the request method is POST
            if request.method == "POST":
                
                data = request.form.get("message", "")
                predict_lr = PredictLR()
                predict_nb = PredictNB()
                if not data:
                    return jsonify(error="Invalid input. Please provide a message."), 400
                try:
                    
                    lr_response = predict_lr.post({"message": data})
                    nb_response = predict_nb.post({"message": data}) 
                    
                    if nb_response[1] != 200:
                        return jsonify(nb_response)
                    if lr_response[1] != 200:
                        return jsonify(lr_response)
                    
                    combined_result = {
                        "result1": lr_response[0],
                        "result2": nb_response[0]
                    }

                    # Return the combined result with a 200 OK response
                    return jsonify(result=combined_result), 200
                except Exception as e:
                    # Handle any exceptions (e.g., model prediction error or failed requests)
                    error_message = f"Error occurred while processing data: {str(e)}"
                    return jsonify(error=error_message), 500
            else:
                # If the request method is not POST, return a 405 Method Not Allowed error
                return jsonify(error="Method not allowed."), 405


app = PA_App(__name__)
app.run(host="0.0.0.0", port=5003, debug=True)
