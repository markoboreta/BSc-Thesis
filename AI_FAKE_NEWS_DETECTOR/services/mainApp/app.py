import os
from flask import *
from common.classes.class_service.service import Service
from flask import render_template, request, Blueprint, send_from_directory


# Class for the main page
class mainPage(Service):
    def __init__(self, import_name, template, static):
        super().__init__(import_name, template_folder=template, static_folder=static)
        self.set_up_routes()

    def set_up_routes(self):
        @self.route("/", methods=["GET"])  # home page
        def main():
            return render_template("main_page.html"), 200

# fucntion to run the app

base_dir = os.path.abspath(os.path.dirname(__file__))
app = mainPage(__name__, os.path.join(base_dir, 'templates'), os.path.join(base_dir, 'static'))
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

