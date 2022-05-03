"""
    Author Zotov Nikita
"""

from flask import Flask
from flask_cors import CORS

from json_client import client
from log import get_default_logger
from ..frontend.configurator import BaseConfigurator

cors = CORS()

logger = get_default_logger(__name__)


class Application(Flask):
    def __init__(self):
        super().__init__(__name__, template_folder='templates')
        cors.init_app(self)
        self.logger = logger
        self.config['SECRET_KEY'] = 'ostis'

        self.host: str = ""
        self.port: int = 0

    def prepare(self, configurator: BaseConfigurator) -> None:
        self.host = str(configurator.flask_ip)
        self.port = configurator.flask_port

        platform_base_url = f"ws://{configurator.platform_ip}:{configurator.platform_port}/"
        platform_url = platform_base_url + configurator.platform_url_path

        client.connect(platform_url)
        if not client.is_connected():
            raise ConnectionAbortedError("Please start platform server first")

    def get_url(self) -> str:
        return f"http://{self.host}:{self.port}"

    def start(self) -> None:
        self.run(host=self.host, port=self.port, debug=False)
