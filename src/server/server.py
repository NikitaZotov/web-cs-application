"""
    Author Zotov Nikita
"""

import threading

from werkzeug.serving import make_server

from .frontend.app import Application
from .frontend.configurator import BaseConfigurator


class ServerThread(threading.Thread):
    def __init__(self, app: Application, configurator: BaseConfigurator):
        threading.Thread.__init__(self)
        self.server = make_server(str(configurator.flask_ip), configurator.flask_port, app)
        self.ctx = app.app_context()
        self.ctx.push()

    def run(self):
        self.server.serve_forever()

    def shutdown(self):
        self.server.shutdown()


class Server:
    def __init__(self, app: Application, configurator: BaseConfigurator):
        self._app = app
        self._configurator = configurator
        self._thread = None

    def start(self):
        self._app.prepare()
        self._thread = ServerThread(self._app, self._configurator)
        self._thread.start()

    def stop(self):
        self._thread.shutdown()
        self._thread = None
