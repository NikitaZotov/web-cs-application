"""
    Author Zotov Nikita
"""
from flask import Blueprint, request, jsonify

from log import get_default_logger
from ..services import RdfServiceContainer

logger = get_default_logger(__name__)

files = Blueprint("files", __name__)
service = RdfServiceContainer.get_file_service()


@files.route("/api/file/upload", methods=['GET', 'POST'])
def upload_file():
    file = request.files["file"]
    file_content = file.read().decode("utf-8")
    name = request.args.get("name")

    status, struct_id = service.upload(file_content, name)
    logger.info("Upload file")

    return jsonify(method="upload", struct_id=struct_id, status=status)


@files.route("/api/file/download", methods=['GET', 'POST'])
def download_file():
    struct_id = int(request.args.get("struct_id"))

    status, content = service.download(struct_id)
    logger.info("Download file")

    return jsonify(method="upload", struct_id=struct_id, status=status, content=content)
