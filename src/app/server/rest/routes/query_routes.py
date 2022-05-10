"""
    Author Zotov Nikita
"""
from flask import Blueprint, request, jsonify

from log import get_default_logger
from modules.common.exception import CustomException
from ..services import RdfServiceContainer

logger = get_default_logger(__name__)

queries = Blueprint("queries", __name__)
service = RdfServiceContainer.get_query_service()


@queries.route("/api/kb/query/search")
def search_structure():
    query = request.args.get("query")
    try:
        struct_id = service.execute(query)
        return jsonify(method="query_search", struct_id=struct_id, status=True)
    except CustomException as ex:
        return jsonify(method="query_search", error=ex, struct_id=0, status=False)
