"""
    Author Zotov Nikita
"""
import os

import requests
from http import HTTPStatus

from flask import request, jsonify, render_template, flash, url_for
from werkzeug.utils import redirect

from app.server.app import Application


app = Application(f"{os.path.abspath(os.path.dirname(__file__))}/templates")


@app.route('/')
def start():
    return 'Please, check documentation'


@app.route('/kb/<class_idtf>')
def index(class_idtf):
    response = requests.get(f"{app.get_server_url()}/api/kb/{class_idtf}")

    if response.status_code == HTTPStatus.OK:
        json_object = response.json()
        param_classes = json_object.get("param_classes")
        objects = json_object.get("objects")

        return render_template("index.html", class_idtf=class_idtf, param_classes=param_classes, objects=objects)
    else:
        return jsonify(response=response.text, status=response.status_code)


@app.route('/kb/<class_idtf>/insert', methods=['POST'])
def insert(class_idtf: str):
    if request.method == 'POST':
        object_idtf = request.form['name']
        app.logger.debug(f"Insert object \"{object_idtf}\" of type \"{class_idtf}\"")

        response = requests.post(f"{app.get_server_url()}/api/kb/{class_idtf}/insert", params=request.form)
        if response.status_code == HTTPStatus.OK:
            flash("Object inserted successfully")
            return redirect(url_for('index', class_idtf=class_idtf))
        else:
            return jsonify(response=response.text, status=response.status_code)


@app.route('/kb/<class_idtf>/update/<object_idtf>', methods=['GET', 'POST'])
def update(class_idtf: str, object_idtf: str):
    if request.method == 'POST':
        app.logger.debug(f"Update object \"{object_idtf}\" of type \"{class_idtf}\"")

        response = requests.put(
            f"{app.get_server_url()}/api/kb/{class_idtf}/update/{object_idtf}",
            params=request.form
        )
        if response.status_code == HTTPStatus.OK:
            flash("Object updated successfully")
            return redirect(url_for('index', class_idtf=class_idtf))
        else:
            return jsonify(response=response.text, status=response.status_code)


@app.route('/kb/<class_idtf>/delete/<object_idtf>', methods=['GET', 'POST'])
def delete(class_idtf: str, object_idtf: str):
    app.logger.debug(f"Remove object \"{object_idtf}\" of type \"{class_idtf}\"")
    flash("Object removed successfully")

    response = requests.delete(f"{app.get_server_url()}/api/kb/{class_idtf}/delete/{object_idtf}")
    if response.status_code == HTTPStatus.OK:
        flash("Object removed successfully")
        return redirect(url_for('index', class_idtf=class_idtf))
    else:
        return jsonify(response=response.text, status=response.status_code)


@app.route('/kb/<class_idtf>/add_attribute', methods=['GET', 'POST'])
def add_attribute(class_idtf: str):
    app.logger.debug(f"Update objects attributes of types \"{class_idtf}\"")

    response = requests.post(
        f"{app.get_server_url()}/api/kb/{class_idtf}/add_attribute",
        params={"attribute": request.form["attribute"]}
    )
    if response.status_code == HTTPStatus.OK:
        flash("Attribute added successfully")
        return redirect(url_for('index', class_idtf=class_idtf))
    else:
        return jsonify(response=response.text, status=response.status_code)


@app.errorhandler(400)
def bad_request(error):
    return render_template("400.html", error=error)


@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html", error=error)


@app.errorhandler(500)
def internal_server_error(error):
    return render_template("500.html", error=error)
