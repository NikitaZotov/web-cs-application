"""
    Author Zotov Nikita
"""
import os.path
from http import HTTPStatus

from flask import send_from_directory, request, jsonify

from server.frontend.app import Application

app = Application()
dir_path = ""


@app.route('/')
def index():
    return "Please, check documentation"


@app.route('/download')
def download_file():
    file_name = request.args.get("file")
    if not file_name:
        app.logger.debug("Get request for empty file name")
        return jsonify(error="Empty file name"), HTTPStatus.BAD_REQUEST

    app.logger.debug(f"Get file \"{file_name}\" content")
    return send_from_directory(dir_path, file_name)


@app.route('/check')
def check_file():
    file_name = request.args.get("file")
    if not file_name:
        app.logger.debug("Get request for empty file name")
        return jsonify(error="Empty file name"), HTTPStatus.BAD_REQUEST

    if os.path.exists(dir_path + "/" + file_name):
        return jsonify(
            file_path=dir_path + file_name,
            status=True,
            link_url=app.get_url() + f"/download?file={file_name}"
        )
    else:
        return jsonify(
            file_path=dir_path + file_name,
            status=False
        )


@app.route('/set', methods=['POST', 'GET'])
def set_directory():
    global dir_path
    dir_path = request.args.get("directory")
    if not dir_path:
        app.logger.debug("Post request for empty directory name")
        return jsonify(error="Empty directory name", status=False), HTTPStatus.BAD_REQUEST

    app.logger.debug(f"Set directory \"{dir_path}\"")
    return jsonify(dir_path=dir_path, status=True)


@app.errorhandler(400)
def bad_request(error):
    return jsonify(error=str(error)), HTTPStatus.BAD_REQUEST


@app.errorhandler(404)
def page_not_found(error):
    return jsonify(error=str(error)), HTTPStatus.NOT_FOUND


@app.errorhandler(500)
def internal_server_error(error):
    return jsonify(error=str(error)), HTTPStatus.INTERNAL_SERVER_ERROR
