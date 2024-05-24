import json
import re
import os
from flask import Flask, render_template, request, jsonify
from prediciton_services_LR.LR import LRModel 
#from LR import LRModel 
from common.classes.class_service.service import Service
from common.classes.class_service.service_api import PredictPA, PredictNB
from flask_restful import Api


# Class for the service
class LRApp(Service):
    def __init__(self, import_name, template, static):
        super().__init__(import_name, template_folder=template, static_folder=static)
        self.set_up_routes()
        self.api = Api(self)
        self.api.add_resource(PredictNB, '/api/predict_nb')
        self.api.add_resource(PredictPA, '/api/predict_pa')
        
    def set_up_routes(self):

        # route for the main page of the 
        @self.route("/LR_page", methods=["GET"])
        def LR_page():
            if request.method == "POST" or request.method == "GET":
                return render_template("Model_2.html")
        
        @self.route('/getTFData')
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

        @self.route("/predict_LR", methods=["POST", "GET"])
        def predict_LR():
            if request.method == "POST":
                data = request.form.get("message", "")
                is_any_text = re.search('[a-zA-Z]', data)
                if not data or not is_any_text:
                    # If message data is missing or invalid, return an error response
                    return (jsonify(error="Invalid input. Please provide a message."), 415)
                try:
                    # Process the received data
                    processed_result = LRModel.predict_news_article(data)
                    print(processed_result)
                    return jsonify(result=processed_result), 200
                except Exception as e:
                    error_message = f"Error occurred while processing data: {str(e)}"
                    return jsonify(error=error_message), 500
            else:
                print("Method not allowed.")
                return jsonify(error="Method not allowed."), 405

        @self.route("/LR/get_result", methods=["POST", "GET"])
        def predict_toegther():
            if request.method == "POST":
                predict_nb = PredictNB()
                predict_pa = PredictPA()
                data = request.form.get("message", "")
                is_any_text = re.search('[a-zA-Z]', data)
                if not data or not is_any_text:
                    return jsonify(error="Invalid input. Please provide a message."), 415
                try:
                    pa_response = predict_pa.post({"message" : data})
                    nb_response = predict_nb.post({"message" : data})
                    if nb_response[1] != 200:
                        return nb_response
                    if pa_response[1] != 200:
                        return pa_response
                    combined_result = {
                        "result1" : nb_response[0],
                        "result2" : pa_response[0]
                    }
                    return jsonify(result=combined_result), 200
                except Exception as e:
                    error_message = f"Error occurred while processing data: {str(e)}"
                    print(error_message)
                    return jsonify(error=error_message), 500
            else:
                return jsonify(error="Method not allowed."), 405
            
base_dir = os.path.abspath(os.path.dirname(__file__))
app = LRApp(__name__, os.path.join(base_dir, 'templates'), os.path.join(base_dir, 'static'))
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=False)