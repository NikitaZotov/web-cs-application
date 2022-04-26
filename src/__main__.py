"""
    Author Zotov Nikita
"""
import sys

from server.frontend.configurator import Configurator
from server.frontend.routes import app
from server.server import Server


def main(args):
    try:
        configurator = Configurator()
        configurator.configure(args)
        server = Server(app, configurator)
        server.start()
    except OSError as error:
        print(error)


if __name__ == '__main__':
    main(sys.argv[1:])
