"""
    Author Zotov Nikita
"""
import os.path
from http import HTTPStatus

from flask import send_from_directory, request, jsonify, flash

from app.server.app import Application
from app.services.service import CRUDService

app = Application()
service = CRUDService()
dir_path = ""


@app.route('/')
def start():
    return 'Please, check documentation'


@app.route('/api/kb/<class_idtf>')
def index(class_idtf):
    param_classes = service.get_objects_params_classes(class_idtf)
    objects = service.get_objects_with_sorted_params(class_idtf, param_classes)
    app.logger.debug(f"Get objects of types \"{class_idtf}\"")

    return jsonify(method="get_objects", class_idtf=class_idtf, param_classes=param_classes, objects=objects)


@app.route('/api/kb/<class_idtf>/insert', methods=['POST'])
def insert(class_idtf: str):
    object_idtf = request.args.get("name")
    app.logger.debug(f"Insert object \"{object_idtf}\" of type \"{class_idtf}\"")

    status = service.add_object(object_idtf, [class_idtf])
    status &= service.add_object_params(object_idtf, request.args)

    return jsonify(method="insert_object", class_idtf=class_idtf, status=status)


@app.route('/api/kb/<class_idtf>/update/<object_idtf>', methods=['GET', 'PUT'])
def update(class_idtf: str, object_idtf: str):
    if request.method == 'PUT':
        status = service.update_object_params(object_idtf, request.args)
        app.logger.debug(f"Update object \"{object_idtf}\" of type \"{class_idtf}\"")

        return jsonify(method="update_object", class_idtf=class_idtf, status=status)


@app.route('/api/kb/<class_idtf>/delete/<object_idtf>', methods=['GET', 'DELETE'])
def delete(class_idtf: str, object_idtf: str):
    status = service.remove_object(object_idtf)
    app.logger.debug(f"Remove object \"{object_idtf}\" of type \"{class_idtf}\"")

    return jsonify(method="delete_object", class_idtf=class_idtf, status=status)


@app.route('/api/kb/<class_idtf>/add_attribute', methods=['GET', 'POST'])
def add_attribute(class_idtf: str):
    service.update_objects_params_classes(class_idtf, [request.args['attribute']])
    app.logger.debug(f"Update objects attributes of types \"{class_idtf}\"")

    return jsonify(method="add_attribute", class_idtf=class_idtf, status=True)


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
