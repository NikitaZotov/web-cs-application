"""
    Author Zotov Nikita
"""

from enum import Enum
from typing import Dict, List, Optional

from json_client import client
from json_client.constants import sc_types
from json_client.dataclass import ScAddr, ScTemplate
from json_client.sc_keynodes import ScKeynodes
from modules.common.constants import ScAlias
from modules.common.exception import CustomException
from modules.common.searcher import get_content_from_links_set
from modules.rdf_to_sc_translation_module.identifiers import TranslationIdentifiers


class ModelNodesType(Enum):
    iri_node = TranslationIdentifiers.NREL_IRI.value
    literal_node = TranslationIdentifiers.NREL_LITERAL_CONTENT.value


def restore_model_content(links_set_node: ScAddr) -> str:
    return get_content_from_links_set(links_set_node)


def find_nodes_by_iris(iris: List[str]) -> Dict[str, Optional[ScAddr]]:
    return find_model_nodes(iris, ModelNodesType.iri_node)


def find_literal_nodes_by_content(content: List[str]) -> Dict[str, Optional[ScAddr]]:
    return find_model_nodes(content, ModelNodesType.literal_node)


def find_model_nodes(content: List[str], node_type: ModelNodesType) -> Dict[str, Optional[ScAddr]]:
    keynodes = ScKeynodes()
    found_nodes = {}
    links = client.get_link_by_content(content)
    for literal_content, links_with_literal_content in zip(content, links):
        node = None
        for link in links_with_literal_content:
            templ = ScTemplate()
            templ.triple_with_relation(
                [sc_types.NODE_VAR, ScAlias.NODE.value],
                sc_types.EDGE_D_COMMON_VAR,
                link,
                sc_types.EDGE_ACCESS_VAR_POS_PERM,
                keynodes[node_type.value],
            )
            search_results = client.template_search(templ)
            if len(search_results) > 0:
                search_result = search_results[0]
                node = search_result.get(ScAlias.NODE.value)
                break
        found_nodes[literal_content] = node
    return found_nodes


def find_all_triple_with_relation_to_link_elements(source_element: ScAddr, relation: ScAddr) -> List[ScAddr]:
    templ = ScTemplate()
    templ.triple_with_relation(
        source_element,
        sc_types.EDGE_D_COMMON_VAR,
        sc_types.LINK_VAR,
        sc_types.EDGE_ACCESS_VAR_POS_PERM,
        relation,
    )
    search_results = client.template_search(templ)

    elements = []
    if len(search_results) > 0:
        search_result = search_results[0]
        for element_index in range(search_result.size()):
            elements.append(search_result.get(element_index))
    else:
        raise CustomException("Element IRI construction is not found.")

    return elements
