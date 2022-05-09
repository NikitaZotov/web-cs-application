"""
    Author Zotov Nikita
"""
from http import HTTPStatus

from flask import request, jsonify, Blueprint

from log import get_default_logger
from ..services import RdfServiceContainer

crud = Blueprint("crud", __name__)
service = RdfServiceContainer.get_crud_service()

logger = get_default_logger(__name__)


@crud.route('/')
def start():
    return 'Please, check documentation'


@crud.route('/api/kb')
def index():
    struct_id = int(request.args.get("struct_id"))
    class_idtf = request.args.get("class_idtf")

    param_classes = service.get_objects_params_classes(class_idtf, struct_id)
    relations = service.get_objects_relations(class_idtf, struct_id)
    objects = service.get_sorted_objects(class_idtf, struct_id, param_classes, relations)
    logger.debug(f"Get objects of types \"{class_idtf}\"")

    return jsonify(
        method="get_objects", class_idtf=class_idtf, param_classes=param_classes, relations=relations, objects=objects
    )


@crud.route('/api/kb/classes/<int:struct_id>')
def get_classes(struct_id):
    classes = service.get_structure_classes(struct_id)
    logger.debug(f"Get classes from structure \"{struct_id}\"")

    return jsonify(method="get_classes", struct_id=struct_id, classes=classes)


@crud.route('/api/kb/insert', methods=['POST'])
def insert():
    params = {}
    params.update(request.args)
    class_idtf = request.args.get("class_idtf")
    struct_id = int(request.args.get("struct_id"))
    object_idtf = request.args.get("name")

    filter_params(params)

    logger.debug(f"Insert object \"{object_idtf}\" of type \"{class_idtf}\"")

    status = service.add_object(object_idtf, struct_id, [class_idtf])
    status &= service.add_object_params(object_idtf, class_idtf, struct_id, params)
    status &= service.add_relation_between_objects(object_idtf, class_idtf, struct_id, params)

    return jsonify(method="insert_object", class_idtf=class_idtf, status=status)


@crud.route('/api/kb/update/<object_idtf>', methods=['GET', 'PUT'])
def update(object_idtf: str):
    params = {}
    params.update(request.args)
    struct_id = int(request.args.get("struct_id"))
    class_idtf = request.args.get("class_idtf")

    filter_params(params)

    status = service.update_object_params(object_idtf, struct_id, params)
    logger.debug(f"Update object \"{object_idtf}\" of type \"{class_idtf}\"")

    return jsonify(method="update_object", class_idtf=class_idtf, status=status)


@crud.route('/api/kb/delete/<object_idtf>', methods=['GET', 'DELETE'])
def delete(object_idtf: str):
    class_idtf = request.args.get("class_idtf")

    status = service.remove_object(object_idtf)
    logger.debug(f"Remove object \"{object_idtf}\" of type \"{class_idtf}\"")

    return jsonify(method="delete_object", class_idtf=class_idtf, status=status)


@crud.route('/api/kb/add_attribute', methods=['GET', 'POST'])
def add_attribute():
    struct_id = int(request.args.get("struct_id"))
    class_idtf = request.args.get("class_idtf")

    service.update_objects_params_classes(class_idtf, struct_id, [request.args['attribute']])
    logger.debug(f"Update objects attributes of types \"{class_idtf}\"")

    return jsonify(method="add_attribute", class_idtf=class_idtf, status=True)


@crud.route('/api/kb/add_relation', methods=['GET', 'POST'])
def add_relation():
    struct_id = int(request.args.get("struct_id"))
    class_idtf = request.args.get("class_idtf")

    service.update_objects_relations(class_idtf, struct_id, [request.args['relation']])
    logger.debug(f"Update objects relations of types \"{class_idtf}\"")

    return jsonify(method="add_relation", class_idtf=class_idtf, status=True)


@crud.errorhandler(400)
def bad_request(error):
    return jsonify(error=str(error)), HTTPStatus.BAD_REQUEST


@crud.errorhandler(404)
def page_not_found(error):
    return jsonify(error=str(error)), HTTPStatus.NOT_FOUND


@crud.errorhandler(500)
def internal_server_error(error):
    return jsonify(error=str(error)), HTTPStatus.INTERNAL_SERVER_ERROR


def filter_params(params):
    params.pop("class_idtf")
    params.pop("struct_id")
