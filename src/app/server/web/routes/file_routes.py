from http import HTTPStatus

import requests
from flask import Blueprint, request, render_template, current_app, flash
from werkzeug.utils import redirect

from log import get_default_logger

files = Blueprint("files", __name__)

logger = get_default_logger(__name__)


@files.route("/file/upload", methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file_key = "file"
        if file_key not in request.files:
            flash("File was not inserted")
            return redirect(request.url)

        server_url = current_app.config["SERVER_URL"]
        response = requests.post(f"{server_url}/api/file/upload", files=request.files)

        if response.status_code == HTTPStatus.OK:
            json_object = response.json()

            return json_object

    return render_template("input_file.html")
