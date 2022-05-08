from flask import Blueprint, request, jsonify

from app.services.file_service import FileService
from log import get_default_logger

logger = get_default_logger(__name__)

files = Blueprint("files", __name__)
service = FileService()


@files.route("/api/file/upload", methods=['GET', 'POST'])
def upload_file():
    file = request.files["file"]
    file_name = file.filename
    struct_name = file_name.split(".")[0].replace(" ", "_") + "_struct"

    file_content = file.read().decode("utf-8")

    status = service.upload(file_content, struct_name)
    logger.info(f"Upload file \"{file_name}\"")

    return jsonify(method="upload", struct_name=struct_name, status=status)
