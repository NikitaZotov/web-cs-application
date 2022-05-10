"""
    Author Zotov Nikita
"""
from http import HTTPStatus

import requests
from flask import Blueprint, current_app, request, render_template, flash

from log import get_default_logger

queries = Blueprint("queries", __name__)

logger = get_default_logger(__name__)


@queries.route("/kb/query/search", methods=['GET', 'POST'])
def search_structure():
    struct_idtf = ""
    if request.method == "POST":
        server_url = current_app.config["SERVER_URL"]
        route_path = f"{server_url}/api/kb/query/search"

        response = requests.get(route_path, params={"query": request.form.get("content")})

        if response.status_code == HTTPStatus.OK:
            json_object = response.json()
            struct_idtf = json_object.get("struct_id")

            if not bool(json_object.get("status")):
                struct_idtf = ""
                flash(json_object.get("error"))
        else:
            flash("Invalid query")

    return render_template("search_structure.html", struct_idtf=struct_idtf)
