"""
    Author Zotov Nikita
"""

from flask import Flask
from flask_cors import CORS

from log import get_default_logger

cors = CORS()

logger = get_default_logger(__name__)


class Application(Flask):
    def __init__(self):
        super().__init__(__name__, template_folder='templates')
        cors.init_app(self)
        self.logger = logger
        self.host: str = ""
        self.port: int = 0

    def prepare(self, host: str, port: int) -> None:
        self.host = host
        self.port = port

    def get_url(self) -> str:
        return f"http://{self.host}:{self.port}"

    def start(self) -> None:
        self.run(host=self.host, port=self.port, debug=False)
