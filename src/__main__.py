"""
    Author Zotov Nikita
"""
import sys

from server.frontend.configurator import Configurator
from server.frontend.routes import app


def main(args):
    try:
        configurator = Configurator()
        configurator.configure(args)
        app.start(configurator)
    except OSError as error:
        print(error)


if __name__ == '__main__':
    args = sys.argv[1:]
    main(args)
