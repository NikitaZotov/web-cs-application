from http import HTTPStatus

import requests
from flask import Blueprint, request, render_template, current_app

from log import get_default_logger

files = Blueprint("files", __name__)

logger = get_default_logger(__name__)


@files.route("/file/upload", methods=['GET', 'POST'])
def upload_file():
    file_key = "file"
    if file_key in request.files:
        file = request.files[file_key]

        server_url = current_app.config["SERVER_URL"]
        response = requests.post(f"{server_url}/api/file/upload", params={"file_name": file.name})

        if response.status_code == HTTPStatus.OK:
            json_object = response.json()

            # здесь должна быть форма загрузки файла (ввести имя файла и структура)
            return render_template("file_form.html")
        else:
            return response
