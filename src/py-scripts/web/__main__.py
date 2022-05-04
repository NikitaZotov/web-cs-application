"""
    Author Zotov Nikita
"""
import sys

from app.server.web.routes import app
from app.server.web.server import WebServer
from ..web.configurator import WebConfigurator


def main(args):
    try:
        configurator = WebConfigurator()
        configurator.configure(args)
        server = WebServer(app, configurator)
        server.start()
    except OSError as error:
        print(error)


if __name__ == '__main__':
    main(sys.argv[1:])
