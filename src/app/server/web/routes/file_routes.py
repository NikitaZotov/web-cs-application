import io
import os
from http import HTTPStatus

import requests
from flask import Blueprint, request, render_template, current_app, flash
from werkzeug.datastructures import FileStorage
from werkzeug.utils import redirect

from log import get_default_logger

files = Blueprint("files", __name__)

logger = get_default_logger(__name__)


@files.route("/file/upload", methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        content = request.form.get("content")

        server_url = current_app.config["SERVER_URL"]
        route_path = f"{server_url}/api/file/upload"

        if content is not None:
            file_storage = form_file(content)
            response = requests.post(route_path, files={"file": file_storage})
        else:
            if "file" not in request.files:
                flash("File was not inserted")
                return redirect(request.url)

            response = requests.post(route_path, files=request.files)

        if response.status_code == HTTPStatus.OK:
            json_object = response.json()
            return json_object

    return render_template("input_file.html")


def form_file(text: str) -> FileStorage:
    stream = io.StringIO(text)
    file_storage = FileStorage(stream)

    return file_storage
