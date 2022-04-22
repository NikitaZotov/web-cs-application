"""
    Author Zotov Nikita
"""
from http import HTTPStatus

from flask import render_template, send_from_directory, request, jsonify

from server.frontend.app import Application

app = Application()

dir_path = ""


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/download')
def download_file():
    file_name = request.args.get("file")
    if not file_name:
        app.logger.debug("Get request for empty file name")
        return jsonify(error="Empty file name"), HTTPStatus.BAD_REQUEST

    app.logger.debug(f"Get file \"{file_name}\" content")
    return send_from_directory(dir_path, file_name)


@app.route('/set', methods=['POST'])
def set_directory():
    global dir_path
    dir_path = request.args.get("directory")
    if not dir_path:
        app.logger.debug("Post request for empty directory name")
        return jsonify(error="Empty directory name"), HTTPStatus.BAD_REQUEST

    app.logger.debug(f"Set directory \"{dir_path}\"")
    return jsonify(dir_path=dir_path)


@app.errorhandler(404)
def page_not_found(error):
    return jsonify(error=str(error)), HTTPStatus.BAD_REQUEST


@app.errorhandler(500)
def internal_server_error(error):
    return jsonify(error=str(error)), HTTPStatus.INTERNAL_SERVER_ERROR
