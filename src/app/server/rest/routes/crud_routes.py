"""
    Author Zotov Nikita
"""
from http import HTTPStatus

from flask import request, jsonify, Blueprint

from app.services.crud_service import CRUDService
from log import get_default_logger

crud = Blueprint("crud", __name__)
service = CRUDService()
dir_path = ""

logger = get_default_logger(__name__)


@crud.route('/')
def start():
    return 'Please, check documentation'


@crud.route('/api/kb/<class_idtf>')
def index(class_idtf):
    param_classes = service.get_objects_params_classes(class_idtf)
    objects = service.get_objects_with_sorted_params(class_idtf, param_classes)
    logger.debug(f"Get objects of types \"{class_idtf}\"")

    return jsonify(method="get_objects", class_idtf=class_idtf, param_classes=param_classes, objects=objects)


@crud.route('/api/kb/<class_idtf>/insert', methods=['POST'])
def insert(class_idtf: str):
    object_idtf = request.args.get("name")
    logger.debug(f"Insert object \"{object_idtf}\" of type \"{class_idtf}\"")

    status = service.add_object(object_idtf, [class_idtf])
    status &= service.add_object_params(object_idtf, request.args)

    return jsonify(method="insert_object", class_idtf=class_idtf, status=status)


@crud.route('/api/kb/<class_idtf>/update/<object_idtf>', methods=['GET', 'PUT'])
def update(class_idtf: str, object_idtf: str):
    if request.method == 'PUT':
        status = service.update_object_params(object_idtf, request.args)
        logger.debug(f"Update object \"{object_idtf}\" of type \"{class_idtf}\"")

        return jsonify(method="update_object", class_idtf=class_idtf, status=status)


@crud.route('/api/kb/<class_idtf>/delete/<object_idtf>', methods=['GET', 'DELETE'])
def delete(class_idtf: str, object_idtf: str):
    status = service.remove_object(object_idtf)
    logger.debug(f"Remove object \"{object_idtf}\" of type \"{class_idtf}\"")

    return jsonify(method="delete_object", class_idtf=class_idtf, status=status)


@crud.route('/api/kb/<class_idtf>/add_attribute', methods=['GET', 'POST'])
def add_attribute(class_idtf: str):
    service.update_objects_params_classes(class_idtf, [request.args['attribute']])
    logger.debug(f"Update objects attributes of types \"{class_idtf}\"")

    return jsonify(method="add_attribute", class_idtf=class_idtf, status=True)


@crud.errorhandler(400)
def bad_request(error):
    return jsonify(error=str(error)), HTTPStatus.BAD_REQUEST


@crud.errorhandler(404)
def page_not_found(error):
    return jsonify(error=str(error)), HTTPStatus.NOT_FOUND


@crud.errorhandler(500)
def internal_server_error(error):
    return jsonify(error=str(error)), HTTPStatus.INTERNAL_SERVER_ERROR
