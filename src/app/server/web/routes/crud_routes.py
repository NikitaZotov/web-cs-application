"""
    Author Zotov Nikita
"""
import os

import requests
from http import HTTPStatus

from flask import request, jsonify, render_template, flash, url_for, Blueprint, current_app
from werkzeug.utils import redirect

from log import get_default_logger

crud = Blueprint("crud", __name__, template_folder=f"{os.path.abspath(os.path.dirname(__file__))}/../templates")
logger = get_default_logger(__name__)


@crud.route('/')
def start():
    return render_template("index.html")


@crud.route('/kb/<class_idtf>')
def index(class_idtf):
    server_url = current_app.config["SERVER_URL"]
    response = requests.get(f"{server_url}/api/kb/{class_idtf}")

    if response.status_code == HTTPStatus.OK:
        json_object = response.json()
        param_classes = json_object.get("param_classes")
        relations = json_object.get("relations")
        objects = json_object.get("objects")

        return render_template(
            "show_objects.html",
            class_idtf=class_idtf,
            param_classes=param_classes,
            relations=relations,
            objects=objects,
        )
    else:
        return jsonify(response=response.text, status=response.status_code)


@crud.route('/kb/classes/<int:struct_id>')
def get_classes(struct_id):
    logger.debug(f"Get classes from structure \"{struct_id}\"")

    server_url = current_app.config["SERVER_URL"]
    response = requests.get(f"{server_url}/api/kb/classes/{struct_id}")
    if response.status_code == HTTPStatus.OK:
        json_object = response.json()
        return render_template("show_classes_list.html", classes=json_object.get("classes"))
    else:
        return jsonify(response=response.text, status=response.status_code)


@crud.route('/kb/<class_idtf>/insert', methods=['POST'])
def insert(class_idtf: str):
    object_idtf = request.form['name']
    logger.debug(f"Insert object \"{object_idtf}\" of type \"{class_idtf}\"")

    server_url = current_app.config["SERVER_URL"]
    response = requests.post(f"{server_url}/api/kb/{class_idtf}/insert", params=request.form)
    if response.status_code == HTTPStatus.OK:
        flash("Object inserted successfully")
        return redirect(url_for('crud.show_objects', class_idtf=class_idtf))
    else:
        return jsonify(response=response.text, status=response.status_code)


@crud.route('/kb/<class_idtf>/update/<object_idtf>', methods=['GET', 'POST'])
def update(class_idtf: str, object_idtf: str):
    logger.debug(f"Update object \"{object_idtf}\" of type \"{class_idtf}\"")

    server_url = current_app.config["SERVER_URL"]
    response = requests.put(
        f"{server_url}/api/kb/{class_idtf}/update/{object_idtf}",
        params=request.form
    )
    if response.status_code == HTTPStatus.OK:
        flash("Object updated successfully")
        return redirect(url_for('crud.show_objects', class_idtf=class_idtf))
    else:
        return jsonify(response=response.text, status=response.status_code)


@crud.route('/kb/<class_idtf>/delete/<object_idtf>', methods=['GET', 'POST'])
def delete(class_idtf: str, object_idtf: str):
    logger.debug(f"Remove object \"{object_idtf}\" of type \"{class_idtf}\"")

    server_url = current_app.config["SERVER_URL"]
    response = requests.delete(f"{server_url}/api/kb/{class_idtf}/delete/{object_idtf}")
    if response.status_code == HTTPStatus.OK:
        flash("Object removed successfully")
        return redirect(url_for('crud.show_objects', class_idtf=class_idtf))
    else:
        return jsonify(response=response.text, status=response.status_code)


@crud.route('/kb/<class_idtf>/add_attribute', methods=['GET', 'POST'])
def add_attribute(class_idtf: str):
    logger.debug(f"Update objects attributes of types \"{class_idtf}\"")

    server_url = current_app.config["SERVER_URL"]
    response = requests.post(
        f"{server_url}/api/kb/{class_idtf}/add_attribute",
        params={"attribute": request.form["attribute"]}
    )
    if response.status_code == HTTPStatus.OK:
        flash("Attribute added successfully")
        return redirect(url_for('crud.show_objects', class_idtf=class_idtf))
    else:
        return jsonify(response=response.text, status=response.status_code)


@crud.route('/kb/<class_idtf>/add_relation', methods=['GET', 'POST'])
def add_relations(class_idtf: str):
    logger.debug(f"Update objects relations of types \"{class_idtf}\"")

    server_url = current_app.config["SERVER_URL"]
    response = requests.post(
        f"{server_url}/api/kb/{class_idtf}/add_relation",
        params={"relation": request.form["relation"]}
    )
    if response.status_code == HTTPStatus.OK:
        flash("Relation added successfully")
        return redirect(url_for('crud.show_objects', class_idtf=class_idtf))
    else:
        return jsonify(response=response.text, status=response.status_code)


@crud.errorhandler(400)
def bad_request(error):
    return render_template("400.html", error=error)


@crud.errorhandler(404)
def page_not_found(error):
    return render_template("404.html", error=error)


@crud.errorhandler(500)
def internal_server_error(error):
    return render_template("500.html", error=error)
