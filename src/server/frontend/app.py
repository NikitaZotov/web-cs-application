"""
    Author Zotov Nikita
"""

from flask import Flask
from flask_cors import CORS

from ..frontend.configurator import BaseConfigurator

cors = CORS()


class Application(Flask):
    def __init__(self, configurator: BaseConfigurator):
        super().__init__(__name__, template_folder='templates')
        cors.init_app(self)
        self.configurator = configurator

    def start(self) -> None:
        self.prepare()
        self.run(host=str(self.configurator.flask_ip), port=self.configurator.flask_port, debug=False)

    def prepare(self) -> None:
        pass