"""
    Author Zotov Nikita
"""
from flask import Blueprint

from log import get_default_logger

queries = Blueprint("queries", __name__)

logger = get_default_logger(__name__)



