"""
    Author Zotov Nikita
"""
from json_client import client
from log import get_default_logger
from modules.rdf_to_sc_translation_module.module import RdfToScTranslationModule
from modules.sc_to_rdf_translation_module.module import ScToRdfTranslationModule
from ..configurator import BaseConfigurator
from ..app import Application
from ..server import Server


class RESTServer(Server):
    def __init__(self, app: Application, configurator: BaseConfigurator):
        super().__init__(app, configurator)
        self._logger = get_default_logger(__name__)
        self.connect_platform()

    def connect_platform(self):
        platform_base_url = f"ws://{self._configurator.server_ip}:{self._configurator.server_port}/"
        platform_url = platform_base_url + self._configurator.server_url_path

        client.connect(platform_url)
        self._logger.info(f"Connect to platform on {platform_base_url}")

        if not client.is_connected():
            raise ConnectionAbortedError("Please start platform server first")
        else:
            RdfToScTranslationModule()
            ScToRdfTranslationModule()
