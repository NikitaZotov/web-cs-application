"""
    Author Zotov Nikita
"""
import argparse
from ipaddress import ip_address

from server import constants
from web import params
from server.configurator import BaseConfigurator


class WebConfigurator(BaseConfigurator):
    def __init__(self):
        super(WebConfigurator, self).__init__()

    def get_server_url(self):
        return f"{constants.HTTP}{self.ip}:{self.port}"

    def configure(self, args):
        self._parser = argparse.ArgumentParser(description="Run server-part of web-server")

        self._parser.add_argument("--flask_ip", help="flask server ip", type=ip_address, default=params.FLASK_IP)
        self._parser.add_argument("--flask_port", help="flask server port", type=int, default=params.FLASK_PORT)
        self._parser.add_argument(
            "--rest_ip", help="ip for connection with REST-server", type=ip_address, default=params.REST_IP
        )
        self._parser.add_argument(
            "--rest_port", help="port for connection with REST-server", type=int, default=params.REST_PORT
        )
        self._parser.add_argument(
            "--rest_url_path", help="url path for REST-server", type=str, default=params.REST_URL_PATH
        )
        parsed_args = self._parser.parse_args(args)

        self._update_params(parsed_args)
        return parsed_args

    def _update_params(self, parsed_args):
        self.ip = parsed_args.flask_ip
        self.port = parsed_args.flask_port
        self.server_ip = parsed_args.rest_ip
        self.server_port = parsed_args.rest_port
        self.server_url_path = parsed_args.rest_url_path
