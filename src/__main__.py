"""
    Author Zotov Nikita
"""

from server.frontend.routes import app


def main():
    try:
        app.start()
    except OSError as error:
        print(error)


if __name__ == '__main__':
    main()
