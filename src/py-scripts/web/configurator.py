"""
    Author Zotov Nikita
"""
import argparse
from ipaddress import ip_address

from app.server import constants
from ..web import params
from app.server.configurator import BaseConfigurator


class WebConfigurator(BaseConfigurator):
    def __init__(self):
        super(WebConfigurator, self).__init__()

    def get_server_url(self):
        return f"{constants.HTTP}{self.ip}:{self.port}"

    def configure(self, args):
        self._parser = argparse.ArgumentParser(description="Run server-part of web-server")

        self._parser.add_argument("--ip", help="flask web-server ip", type=ip_address, default=params.FLASK_IP)
        self._parser.add_argument("--port", help="flask web-server port", type=int, default=params.FLASK_PORT)
        self._parser.add_argument(
            "--server_ip", help="ip for connection with REST-server", type=ip_address, default=params.REST_IP
        )
        self._parser.add_argument(
            "--server_port", help="port for connection with REST-server", type=int, default=params.REST_PORT
        )
        self._parser.add_argument(
            "--server_url_path", help="url path for REST-server", type=str, default=params.REST_URL_PATH
        )
        parsed_args = self._parser.parse_args(args)

        self._update_params(parsed_args)
        return parsed_args

    def _update_params(self, parsed_args):
        self.ip = parsed_args.ip
        self.port = parsed_args.port
        self.server_ip = parsed_args.server_ip
        self.server_port = parsed_args.server_port
        self.server_url_path = parsed_args.server_url_path
