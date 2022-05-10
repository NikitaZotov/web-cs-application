"""
    Author Zotov Nikita
"""

import unittest

from json_client import client
from json_client.constants import sc_types
from json_client.kb_tests import ScTest
from json_client.sc_keynodes import ScKeynodes
from modules.common.generator import generate_node, generate_edge
from ...query.parser import ScsQueryParser


class ScQueryParserTest(ScTest):
    def test_simple_query(self):
        keynodes = ScKeynodes()
        parser = ScsQueryParser()

        class_addr = keynodes.__getitem__("test_node", sc_types.NODE_CONST_CLASS)

        for _ in range(0, 2):
            element_addr = generate_node(sc_types.NODE_CONST)
            generate_edge(class_addr, element_addr, sc_types.EDGE_ACCESS_CONST_POS_PERM)

        template, params = parser.parse("test_node _-> _var;")
        result = client.template_search(template)

        self.assertTrue(len(result) == 2)
        self.assertTrue(len(params) == 2)

        for item in result:
            client.delete_elements([item.get(1)])


class ScsQueryParserModuleTest(ScTest):
    @classmethod
    def setUpClass(cls) -> None:
        client.connect("ws://localhost:8090/ws_json")

    @classmethod
    def tearDownClass(cls) -> None:
        client.disconnect()


if __name__ == "__main__":
    unittest.main()
