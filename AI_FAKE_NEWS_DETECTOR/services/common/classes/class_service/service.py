import os   
from flask_cors import CORS
from flask import  render_template, send_from_directory,request, jsonify, abort
from flask import Flask, render_template, Blueprint
from flask_restful import Api, Resource
import json
import re

# Flask class for the apps
class Service(Flask):
    def __init__(self, import_name,template_folder=None, static_folder=None):
        super().__init__(import_name, template_folder=template_folder, static_folder=static_folder)
        self.configure_app()
        self.configure_cors()
        self.configure_error_handlers()
        self.configure_blueprint_for_templates()
        
    def configure_app(self):
        self.secret_key = "secret_key"

    def configure_cors(self):
        # Configure CORS, enabling cross communication
        CORS(self, resources={r"/*": {"origins": "*"}})
    
    def load_json_data(self, path):
        try:
            with open(path) as data_file:
                data = json.load(data_file)
            return jsonify(data)
        except FileNotFoundError:
            return jsonify({"error": "File not found"}), 404
        except json.JSONDecodeError:
            return jsonify({"error": "Invalid JSON"}), 400
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    # Configuration for the error handler Blueprint 
    def configure_error_handlers(self):
        #common_templates_dir = os.getenv('COMMON_TEMPLATES_DIR')
        common_templates_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), 'common', 'templates')
        errors_bp = Blueprint('errors', __name__, template_folder=common_templates_dir)
        @errors_bp.app_errorhandler(400)
        @errors_bp.app_errorhandler(404)
        @errors_bp.app_errorhandler(405)
        @errors_bp.app_errorhandler(500)
        def handle_error(e):
            error_message = f"You have reached the error {getattr(e, 'code', 'unknown')} page :("
            print(common_templates_dir)
            return render_template("error.html", data=error_message), getattr(e, 'code', 404)
        self.register_blueprint(errors_bp)

    
    def configure_blueprint_for_templates(self):
        #common_static_dir = os.getenv('COMMON_STATIC_DIR')
        common_static_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), 'common', 'static')
        static_bp = Blueprint('static_bp', __name__, static_folder=common_static_dir)
        @static_bp.route('/<path:filename>')
        def get_styles(filename):
            file_path = os.path.join(static_bp.static_folder, filename)
            if not os.path.exists(file_path):
                abort(404)
            return send_from_directory(static_bp.static_folder, filename)

        self.register_blueprint(static_bp)

       
        
