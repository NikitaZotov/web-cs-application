from flask import Blueprint, request, jsonify

from app.services.file_service import FileService
from log import get_default_logger

logger = get_default_logger(__name__)

files = Blueprint("files", __name__)
service = FileService()


@files.route("/api/file/upload", methods=['GET', 'POST'])
def upload_file():
    file_name = request.args.get("file_name")
    struct_name = request.args.get("struct_name")

    status = service.upload(file_name, struct_name)
    logger.info(f"Upload file \"{file_name}\"")

    return jsonify(method="upload", struct_name=struct_name, status=status)
