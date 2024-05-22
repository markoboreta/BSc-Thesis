import os
import logging
import json
import re
from flask import Flask, render_template, request, jsonify
from flask import  request, Blueprint, send_from_directory, Response
from flask_cors import CORS
from flask import request, jsonify
from flask import request, render_template, abort
from common.classes.class_service.service import Service
from common.classes.class_service.service_api import PredictNB, PredictLR
from flask_restful import Api
import requests
#from prediction_services_PA.PA import PAModel
from PA import PAModel
from flask import request, render_template, jsonify
from common.classes.class_service.service import Service


class PA_App(Service):
    def __init__(self, import_name, template, static):
        super().__init__(import_name, template_folder=template, static_folder=static)
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
                is_any_text = re.search('[a-zA-Z]', data)
                print(is_any_text)
                print(">>>>>>>>>>DATA\n\n", len(data))
                if not data or not is_any_text: 
                    # If message data is missing or invalid, return an error response
                    return jsonify(error="Invalid input. Please provide a message."), 415
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
            if request.method == "GET":
                return self.load_json_data("static/WC.json")
        
        @self.route('/getWCData')
        def get_WC_data():
             if request.method == "GET":
                return self.load_json_data("static/TF.json")

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
                        return nb_response
                    if lr_response[1] != 200:
                        return lr_response
                    
                    combined_result = {
                        "result1": lr_response[0],
                        "result2": nb_response[0]
                    }
                    return jsonify(result=combined_result), 200
                except Exception as e:
                    error_message = f"Error occurred while processing data: {str(e)}"
                    return jsonify(error=error_message), 500
            else:
                # If the request method is not POST, return a 405 Method Not Allowed error
                return jsonify(error="Method not allowed."), 405

base_dir = os.path.abspath(os.path.dirname(__file__))
app = PA_App(__name__, os.path.join(base_dir, 'templates'), os.path.join(base_dir, 'static'))
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5003, debug=True)
