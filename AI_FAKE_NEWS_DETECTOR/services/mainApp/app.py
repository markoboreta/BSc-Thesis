import os
from flask import *
from common.classes.class_service.service import Service
from flask import render_template, request, Blueprint, send_from_directory


# Class for the main page
class mainPage(Service):
    def __init__(self, import_name):
        super().__init__(import_name)
        self.set_up_routes()

    def set_up_routes(self):
        @self.route("/", methods=["GET", "POST"])  # home page
        def main():
            return render_template("main_page.html"), 200

# fucntion to run the app


app = mainPage(__name__)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

