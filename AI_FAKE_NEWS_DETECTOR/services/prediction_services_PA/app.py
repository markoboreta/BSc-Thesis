import os
import re
from common.classes.class_service.service import Service
from common.classes.class_service.service_api import PredictNB, PredictLR
from flask_restful import Api
"""
Comment code below for docker to run
"""
#from prediction_services_PA.PA import PA_Model
from PA import PA_Model
from flask import request, render_template, jsonify
from common.classes.class_service.service import Service


class PAApp(Service):
    def __init__(self, import_name, template, static):
        super().__init__(import_name, template_folder=template, static_folder=static)
        self.set_up_routes()
        self.api = Api(self)
        self.api.add_resource(PredictNB, '/api/predict_nb')
        self.api.add_resource(PredictLR, '/api/predict_lr')
  
    def set_up_routes(self):

        # route for the main page of the 
        @self.route("/PA_page", methods=["GET"])
        def PA_page():
                return render_template("Model_1.html")
        
        @self.route("/predict_PA", methods=["POST", "GET"])
        def predict_PA():
            if request.method == "POST":
                data = request.form.get("message", "")
                is_any_text = re.search('[a-zA-Z]', data)
                #print(is_any_text)
                if not data or not is_any_text: 
                    # If message data is missing or invalid, return an error response
                    return jsonify(error="Invalid input. Please provide a message."), 415
                try:
                    # Process the received data
                    processed_result = PA_Model.predict_news_article(data)
                    print(processed_result)
                    return jsonify(result=processed_result), 200
                except Exception as e:
                    # Handle any exceptions and return an error response
                    error_message = f"Error occurred while processing data: {str(e)}"
                    return jsonify(error=error_message), 500
            else:
                print("Method not allowed.")
                return jsonify(error="Method not allowed."), 405

        # get the data from json files for the graphs
        @self.route('/getPAData')
        def get_graph_data():
            if request.method == "GET":
                this_dir = os.path.abspath(os.path.dirname(__file__))
                file_path = os.path.join(this_dir, 'static', 'TF.json')
                #print(file_path)
                return self.load_json_data(file_path)
        
        @self.route('/getWCData')
        def get_WC_data():
             if request.method == "GET":
                this_dir = os.path.abspath(os.path.dirname(__file__))
                file_path = os.path.join(this_dir, 'static', 'WC.json')
                return self.load_json_data(file_path)

        @self.route("/PA/get_result", methods=["POST", "GET"])
        def predict_toegther():
            #print('here')
            # Check if the request method is POST
            if request.method == "POST":
                data = request.form.get("message", "")
                predict_lr = PredictLR()
                predict_nb = PredictNB()
                is_any_text = re.search('[a-zA-Z]', data)
                if not data or not is_any_text:
                    return jsonify(error="Invalid input. Please provide a message."), 415
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
app = PAApp(__name__, os.path.join(base_dir, 'templates'), os.path.join(base_dir, 'static'))
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5003, debug=True)
