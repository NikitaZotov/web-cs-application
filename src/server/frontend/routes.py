"""
    Author Zotov Nikita
"""
import os.path
from http import HTTPStatus

from flask import send_from_directory, request, jsonify, render_template, flash, url_for
from werkzeug.utils import redirect

from server.backend.service import Service
from server.frontend.app import Application

app = Application()
service = Service()
dir_path = ""


@app.route('/kb/<class_idtf>')
def index(class_idtf):
    param_classes = service.get_objects_params_classes(class_idtf)
    objects = service.get_objects_with_sorted_params(class_idtf, param_classes)

    return render_template("index.html", class_idtf=class_idtf, param_classes=param_classes, objects=objects)


@app.route('/kb/<class_idtf>/insert', methods=['POST'])
def insert(class_idtf: str):
    if request.method == 'POST':
        object_idtf = request.form['name']

        service.add_object(object_idtf, [class_idtf])
        service.add_object_params(object_idtf, request.form)

        flash("Object inserted successfully")

        return redirect(url_for('index', class_idtf=class_idtf))


@app.route('/kb/<class_idtf>/update/<object_idtf>', methods=['GET', 'POST'])
def update(class_idtf: str, object_idtf: str):
    if request.method == 'POST':
        service.update_object_params(object_idtf, request.form)
        flash("Object updated successfully")

        return redirect(url_for('index', class_idtf=class_idtf))


@app.route('/kb/<class_idtf>/delete/<object_idtf>', methods=['GET', 'POST'])
def delete(class_idtf: str, object_idtf: str):
    service.remove_object(object_idtf)
    flash("Object removed successfully")

    return redirect(url_for('index', class_idtf=class_idtf))


@app.route('/kb/<class_idtf>/add_attribute', methods=['GET', 'POST'])
def add_attribute(class_idtf: str):
    service.update_objects_params_classes(class_idtf, [request.form['attribute']])
    flash("Attribute added successfully")

    return redirect(url_for('index', class_idtf=class_idtf))


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
