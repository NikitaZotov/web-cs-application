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

    status, struct_id = service.upload(file_content)
    logger.info("Upload file")

    return jsonify(method="upload", struct_id=struct_id, status=status)
