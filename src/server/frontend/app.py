"""
    Author Zotov Nikita
"""

from flask import Flask
from flask_cors import CORS

from ..frontend.configurator import BaseConfigurator

cors = CORS()


class Application(Flask):
    def __init__(self):
        super().__init__(__name__, template_folder='templates')
        cors.init_app(self)

    def start(self, configurator: BaseConfigurator) -> None:
        self.prepare()
        self.run(host=str(configurator.flask_ip), port=configurator.flask_port, debug=False)

    def prepare(self) -> None:
        pass
