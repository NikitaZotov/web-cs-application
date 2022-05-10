"""
    Author Zotov Nikita
"""
import sys

from app.server.app import Application
from app.server.registrator import Registrator
from app.server.rest.routes.crud_routes import crud
from app.server.rest.routes.file_routes import files
from app.server.rest.routes.query_routes import queries
from app.server.rest.server import RESTServer
from ..rest.configurator import RESTConfigurator


def main(args):
    try:
        configurator = RESTConfigurator()
        configurator.configure(args)

        app = Application()
        registrator = Registrator(app)
        registrator.register([crud, files, queries])
        server = RESTServer(app, configurator)
        server.start()
    except OSError as error:
        print(error)


if __name__ == '__main__':
    main(sys.argv[1:])
