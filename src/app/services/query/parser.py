"""
    Author Zotov Nikita
"""
from typing import List, Tuple

from json_client.constants import sc_types
from json_client.dataclass import ScTemplate
from json_client.sc_keynodes import ScKeynodes
from modules.common.constants import ScAlias


class ScsQueryParser:
    def __init__(self):
        self._keynodes = ScKeynodes()
        self.semicolon = ";"
        self.var_access_edge = "_->"
        self.var_common_edge = "_=>"
        self.var_relation = "::"
        self.var_prefix = "_"

    def parse(self, query: str) -> Tuple[ScTemplate, List[str]]:
        sentences = query.replace(" ", "").split(self.semicolon)

        edge_number = 0
        template = ScTemplate()
        params = []
        for sentence in sentences:
            edge_alias = ScAlias.ACCESS_EDGE.value + str(edge_number)
            if sentence.count(self.var_access_edge) == 1:
                nodes = sentence.split(self.var_access_edge)

                source, target = nodes[0], nodes[1]
                params.extend([source, target])

                template.triple(
                    self._resolve_param(source),
                    [sc_types.EDGE_ACCESS_VAR_POS_PERM, edge_alias],
                    self._resolve_param(target),
                )
            elif sentence.count(self.var_common_edge) == 1:
                nodes = sentence.split(self.var_common_edge)

                source, nodes = nodes[0], nodes[1]

                nodes = nodes.split(self.var_relation)
                relation, target = nodes[0], nodes[1]
                params.extend([source, relation, target])

                template.triple_with_relation(
                    self._resolve_param(source),
                    [sc_types.EDGE_D_COMMON_VAR, edge_alias],
                    self._resolve_param(target),
                    [sc_types.EDGE_ACCESS_VAR_POS_PERM, edge_alias + 1],
                    self._resolve_param(relation)
                )

            edge_number += 2

        return template, params

    def _is_var(self, node: str) -> bool:
        return node.startswith(self.var_prefix)

    def _resolve_param(self, node: str):
        return [sc_types.UNKNOWN, node] if self._is_var(node) else self._keynodes[node]