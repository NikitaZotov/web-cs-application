"""
    Author Zotov Nikita
"""

from flask import render_template, send_from_directory, request, jsonify

from server.frontend.app import Application
from server.frontend.configurator import Configurator

configurator = Configurator()
app = Application(configurator)

dir_path = ""


# abort(HTTPStatus.BAD_REQUEST, description=status.value)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/download')
def download_file():
    file_name = request.args.get("file")

    return send_from_directory(dir_path, file_name)


@app.route('/set', methods=['POST'])
def set_directory():
    global dir_path
    dir_path = request.args.get("directory")

    return jsonify(dir_path=dir_path)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html', error=error), 404


@app.errorhandler(500)
def internal_server_error(error):
    return render_template("500.html", error=error), 500
