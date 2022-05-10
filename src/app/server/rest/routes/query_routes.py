"""
    Author Zotov Nikita
"""
from flask import Blueprint

from log import get_default_logger
from ..services import RdfServiceContainer

logger = get_default_logger(__name__)

queries = Blueprint("queries", __name__)
service = RdfServiceContainer


