import os, logging
from flask_cors import CORS
from flask import  render_template, send_from_directory
from flask import Flask, render_template, Blueprint
from flask_restful import Api, Resource

# Flask class for the apps
class Service(Flask):
    def __init__(self, import_name):
        super().__init__(import_name)
        self.configure_app()
        self.configure_cors()
        self.configure_logging()
        self.configure_error_handlers()
        self.configure_blueprint_for_templates()
        
    def configure_app(self):
        # Set the secret key for the Flask app, this is just for development purposes
        self.secret_key = "your_secret_key"

    def configure_cors(self):
        # Configure CORS, enabling cross communication
        CORS(self, resources={r"/*": {"origins": "*"}})

    def configure_logging(self):
        # Set log level and configure logging
        self.logger.setLevel(logging.INFO)
        log_file = logging.FileHandler("app.log")
        self.logger.addHandler(log_file)
    
    # Configuration for the error handler Blueprint 
    def configure_error_handlers(self):
        common_templates_dir = os.getenv('COMMON_TEMPLATES_DIR')
        #common_templates_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), 'common', 'templates')
        self.logger.info(f"Templates directory: {common_templates_dir}")
        errors_bp = Blueprint('errors', __name__, template_folder=common_templates_dir)
        @errors_bp.app_errorhandler(400)
        @errors_bp.app_errorhandler(404)
        @errors_bp.app_errorhandler(405)
        @errors_bp.app_errorhandler(500)
        def handle_error(e):
            error_message = f"You have reached the error {getattr(e, 'code', 'unknown')} page :("
            self.logger.exception(f"Error {getattr(e, 'code', 'unknown')} occurred during a request.")
            return render_template("error.html", data=error_message), getattr(e, 'code', 500)
        self.register_blueprint(errors_bp)

    # Configuration for the styles Blueprint
    def configure_blueprint_for_templates(self):
        common_static_dir = os.getenv('COMMON_STATIC_DIR')
        #common_static_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), 'common', 'static')
        self.logger.info(f"Static directory: {common_static_dir}")
        static_bp = Blueprint('static_bp', __name__, static_folder=common_static_dir)
        @static_bp.route('/<path:filename>')
        def get_styles(filename):
            return send_from_directory(static_bp.static_folder, filename)
        self.register_blueprint(static_bp)

       
        
