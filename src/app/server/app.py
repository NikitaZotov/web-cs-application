"""
    Author Zotov Nikita
"""

from flask import Flask
from flask_cors import CORS

from app.server.configurator import BaseConfigurator
from log import get_default_logger

cors = CORS()

logger = get_default_logger(__name__)


class Application(Flask):
    def __init__(self, template_folder: str = ""):
        super().__init__(__name__, template_folder=template_folder)
        cors.init_app(self)
        self.logger = logger
        self.config['SECRET_KEY'] = 'ostis'

        self.host: str = ""
        self.port: int = 0
        self.server_host: str = ""
        self.server_port: int = 0

    def prepare(self, configurator: BaseConfigurator) -> None:
        self.host = str(configurator.ip)
        self.port = configurator.port
        self.server_host = str(configurator.server_ip)
        self.server_port = configurator.server_port

        self.config["URL"] = self.get_url()
        self.config["SERVER_URL"] = self.get_server_url()

    def get_url(self) -> str:
        return f"http://{self.host}:{self.port}"

    def get_server_url(self) -> str:
        return f"http://{self.server_host}:{self.server_port}"

    def start(self) -> None:
        self.run(host=self.host, port=self.port, debug=False)
