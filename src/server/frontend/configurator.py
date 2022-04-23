"""
    Author Zotov Nikita
"""

import argparse
from ipaddress import ip_address
from server import params


class BaseConfigurator:
    def __init__(self):
        self.flask_ip = params.FLASK_IP
        self.flask_port = params.FLASK_PORT
        self.platform_ip = params.PLATFORM_IP
        self.platform_port = params.PLATFORM_PORT
        self.platform_url_path = params.PLATFORM_URL_PATH

        self._parser = None

    def get_server_url(self):
        raise NotImplementedError

    def configure(self, args):
        raise NotImplementedError


class Configurator(BaseConfigurator):
    def __init__(self):
        super(Configurator, self).__init__()

    def get_server_url(self):
        return f"{params.HTTP}{self.flask_ip}:{self.flask_port}"

    def configure(self, args):
        self._parser = argparse.ArgumentParser(description="Run server-part of NLP-module")

        self._parser.add_argument("--flask_ip", help="flask server ip", type=ip_address, default=params.FLASK_IP)
        self._parser.add_argument("--flask_port", help="flask server port", type=int, default=params.FLASK_PORT)
        self._parser.add_argument(
            "--platform_ip", help="ip for connection with platform", type=ip_address, default=params.PLATFORM_IP
        )
        self._parser.add_argument(
            "--platform_port", help="port for connection with platform", type=int, default=params.PLATFORM_PORT
        )
        self._parser.add_argument(
            "--platform_url_path", help="url path for platform", type=str, default=params.PLATFORM_URL_PATH
        )
        parsed_args = self._parser.parse_args(args)

        self._update_params(parsed_args)
        return parsed_args

    def _update_params(self, parsed_args):
        self.flask_ip = parsed_args.flask_ip
        self.flask_port = parsed_args.flask_port
        self.platform_ip = parsed_args.platform_ip
        self.platform_port = parsed_args.platform_port
        self.platform_url_path = parsed_args.platform_url_path
