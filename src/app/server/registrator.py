from typing import List

from flask import Blueprint

from app.server.app import Application


class Registrator:
    def __init__(self, app: Application):
        self._app = app

    def register(self, blueprints: List[Blueprint]):
        for blueprint in blueprints:
            self._app.logger.info(f"Register {blueprint.name} blueprint")
            self._app.register_blueprint(blueprint)
