"""
    Author Zotov Nikita
"""
from json_client import client
from json_client.sc_keynodes import ScKeynodes
from query.parser import ScsQueryParser


class QueryService:
    def __init__(self):
        self._keynodes = ScKeynodes()
        self._parser = ScsQueryParser()

    def execute(self, query: str):
        template, aliases = self._parser.parse(query)
        client.template_search(template)

