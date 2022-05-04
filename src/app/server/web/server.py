"""
    Author Zotov Nikita
"""
from log import get_default_logger
from ..configurator import BaseConfigurator
from ..app import Application
from ..server import Server


class WebServer(Server):
    def __init__(self, app: Application, configurator: BaseConfigurator):
        super().__init__(app, configurator)
        self._logger = get_default_logger(__name__)
