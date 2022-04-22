"""
    Author Zotov Nikita
"""
from http import HTTPStatus

from flask import render_template, send_from_directory, request, jsonify
from werkzeug.exceptions import abort

from server.frontend.app import Application
from server.frontend.configurator import Configurator

configurator = Configurator()
app = Application(configurator)

dir_path = ""


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/download')
def download_file():
    file_name = request.args.get("file")
    if not file_name:
        return jsonify(error="Empty file name"), HTTPStatus.BAD_REQUEST

    return send_from_directory(dir_path, file_name, error="File or directory not found")


@app.route('/set', methods=['POST'])
def set_directory():
    global dir_path
    dir_path = request.args.get("directory")
    if not dir_path:
        return jsonify(error="Empty directory name"), HTTPStatus.BAD_REQUEST

    return jsonify(dir_path=dir_path)


@app.errorhandler(404)
def page_not_found(error):
    return jsonify(error=str(error)), HTTPStatus.BAD_REQUEST


@app.errorhandler(500)
def internal_server_error(error):
    return jsonify(error=str(error)), HTTPStatus.INTERNAL_SERVER_ERROR
