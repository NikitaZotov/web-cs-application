"""
    Author Zotov Nikita
"""
import sys

from app.server.rest.routes import app
from app.server.rest.server import RESTServer
from ..rest.configurator import RESTConfigurator


def main(args):
    try:
        configurator = RESTConfigurator()
        configurator.configure(args)
        server = RESTServer(app, configurator)
        server.start()
    except OSError as error:
        print(error)


if __name__ == '__main__':
    main(sys.argv[1:])
