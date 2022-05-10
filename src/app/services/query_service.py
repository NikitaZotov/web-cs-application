"""
    Author Zotov Nikita
"""
from json_client import client
from json_client.constants import sc_types
from json_client.sc_keynodes import ScKeynodes
from modules.common.exception import CustomException
from modules.common.generator import generate_node, wrap_in_set, set_system_idtf
from .query.parser import ScsQueryParser


class QueryService:
    def __init__(self):
        self._keynodes = ScKeynodes()
        self._parser = ScsQueryParser()

    def execute(self, query: str) -> int:
        try:
            template, aliases = self._parser.parse(query)
            if len(template.triple_list) == 0:
                raise CustomException("Invalid query")

            result = client.template_search(template)

            struct_addr = generate_node(sc_types.NODE_CONST_STRUCT)
            set_system_idtf(struct_addr, str(struct_addr.value))
            for item in result:
                for i in range(0, item.size(), 3):
                    wrap_in_set([item.addrs[i], item.addrs[i + 1], item.addrs[i + 2]], struct_addr)

            return struct_addr.value
        except CustomException as ex:
            raise CustomException(f"Invalid state during search procedure. {ex.msg}")
