"""
    Author Zotov Nikita
"""
import sys

from app.server.app import Application
from app.server.registrator import Registrator
from app.server.web.routes.crud_routes import crud
from app.server.web.routes.file_routes import files
from app.server.web.server import WebServer
from ..web.configurator import WebConfigurator


def main(args):
    try:
        configurator = WebConfigurator()
        configurator.configure(args)

        app = Application()
        registrator = Registrator(app)
        registrator.register([crud, files])
        server = WebServer(app, configurator)
        server.start()
    except OSError as error:
        print(error)


if __name__ == '__main__':
    main(sys.argv[1:])
