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
        self._parser = argparse.ArgumentParser(description="Run server-part of application")

        self._parser.add_argument("--flask_ip", help="flask server ip", type=ip_address, default=params.FLASK_IP)
        self._parser.add_argument("--flask_port", help="flask server port", type=int, default=params.FLASK_PORT)
        parsed_args = self._parser.parse_args(args)

        self._update_params(parsed_args)
        return parsed_args

    def _update_params(self, parsed_args):
        self.flask_ip = parsed_args.flask_ip
        self.flask_port = parsed_args.flask_port
