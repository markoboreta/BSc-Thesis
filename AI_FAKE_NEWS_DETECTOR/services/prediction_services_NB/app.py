import os
from flask import Flask, render_template, request, jsonify
from flask import  request
from flask_cors import CORS
from flask import request, jsonify
from flask import request, render_template
from common.classes.class_service.service_api import PredictPA, PredictLR
from flask_restful import Api
"""
Comment code below for docker to run
"""
#from prediction_services_NB.NB import NB_model
from NB import NB_model
from common.classes.class_service.service import Service
import re


# Class for the service
class NBApp(Service):
    def __init__(self, import_name, template, static):
        super().__init__(import_name, template_folder=template, static_folder=static)
        self.set_up_routes()
        self.api = Api(self)
        self.api.add_resource(PredictPA, '/api/predict_pa')
        self.api.add_resource(PredictLR, '/api/predict_lr')
  
    def set_up_routes(self):
        # route for the main page of the 
        @self.route("/NB_page", methods=["GET"])
        def NB_page():
            return render_template("Model_3.html")
        
        @self.route('/getNBData')
        def get_graph_data():
            if request.method == "GET":
                this_dir = os.path.abspath(os.path.dirname(__file__))
                file_path = os.path.join(this_dir, 'static', 'TF.json')
                return self.load_json_data(file_path)

        @self.route('/getWCData')
        def get_WC_data():
             if request.method == "GET":
                this_dir = os.path.abspath(os.path.dirname(__file__))
                file_path = os.path.join(this_dir, 'static', 'WC.json')
                return self.load_json_data(file_path)
        
        # predicition of the NB
        @self.route("/predict_NB", methods=["POST", "GET"])
        def predict_NB():
            if request.method == "POST":
                data = request.form.get("message", "")
                is_any_text = re.search('[a-zA-Z]', data)
                if not data or not is_any_text:
                    # If message data is missing or invalid, return an error response
                    return (jsonify(error="Invalid input. Please provide a message."), 415)
                try:
                    # Process the received data
                    processed_result = NB_model.predict_news_article(data)
                    print(processed_result)
                    return jsonify(result=processed_result), 200
                except Exception as e:
                    error_message = f"Error occurred while processing data: {str(e)}"
                    return jsonify(error=error_message), 500
            else:
                print("Method not allowed.")
                return jsonify(error="Method not allowed."), 405

        
        # get the results from API
        @self.route("/NB/get_result", methods=["POST", "GET"])
        def predict_toegther():
            if request.method == "POST":
                data = request.form.get("message", "")
                
                predict_lr = PredictLR()
                predict_pa = PredictPA()
                is_any_text = re.search('[a-zA-Z]', data)
                if not data or not is_any_text:
                   return jsonify(error="Invalid input. Please provide a message."), 415
                try:
                    pa_response = predict_pa.post({"message" : data})
                    lr_response = predict_lr.post({"message" : data})

                    if lr_response[1] != 200:
                        return lr_response
                    if pa_response[1] != 200:
                        return pa_response
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


base_dir = os.path.abspath(os.path.dirname(__file__))
app = NBApp(__name__, os.path.join(base_dir, 'templates'), os.path.join(base_dir, 'static'))
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=False)
