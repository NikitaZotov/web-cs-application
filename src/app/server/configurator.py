"""
    Author Zotov Nikita
"""


class BaseConfigurator:
    def __init__(self):
        self.ip: str = ""
        self.port: int = 0
        self.server_ip: str = ""
        self.server_port: int = 0
        self.server_url_path: str = ""

        self._parser = None

    def get_server_url(self):
        raise NotImplementedError

    def configure(self, args):
        raise NotImplementedError
