import io
from http import HTTPStatus

import requests
from flask import Blueprint, request, render_template, current_app, flash, send_file
from werkzeug.datastructures import FileStorage
from werkzeug.utils import redirect

from log import get_default_logger

files = Blueprint("files", __name__)

logger = get_default_logger(__name__)


@files.route("/file/upload", methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        content = request.form.get("content")
        name = request.form.get("title")

        server_url = current_app.config["SERVER_URL"]
        route_path = f"{server_url}/api/file/upload"

        if content is not None:
            file_storage = form_file(content)
            response = requests.post(route_path, files={"file": file_storage}, params={"name": name})
        else:
            if "file" not in request.files:
                flash("File was not inserted")
                return redirect(request.url)

            response = requests.post(route_path, files=request.files, params={"name": name})

        if response.status_code == HTTPStatus.OK:
            json_object = response.json()
            struct_id = json_object.get("struct_id")

            url = current_app.config["URL"]
            return redirect(f"{url}/kb/classes/{struct_id}")

    return render_template("input_file.html")


@files.route("/file/download", methods=['GET'])
def download_file():
    server_url = current_app.config["SERVER_URL"]
    route_path = f"{server_url}/api/file/download"

    response = requests.get(route_path, params=request.args)

    if response.status_code == HTTPStatus.OK:
        json_object = response.json()
        sio = io.StringIO(json_object.get("content"))
        bio = io.BytesIO(sio.read().encode('utf8'))

        return send_file(bio, download_name="ontology.xml")


def form_file(text: str) -> FileStorage:
    stream = io.StringIO(text)
    file_storage = FileStorage(stream)

    return file_storage
