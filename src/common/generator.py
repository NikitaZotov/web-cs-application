"""
    Author Zotov Nikita
"""

from typing import List

from common.constants import ScAlias
from common.identifiers import CommonIdentifiers
from common.searcher import check_edge
from json_client import client
from json_client.constants import sc_types
from json_client.constants.sc_types import ScType
from json_client.dataclass import (
    ScAddr,
    ScConstruction,
    ScIdtfResolveParams,
    ScLinkContent,
    ScLinkContentType,
)
from json_client.sc_keynodes import ScKeynodes


def generate_edge(src: ScAddr, trg: ScAddr, edge_type: ScType) -> ScAddr:
    construction = ScConstruction()
    construction.create_edge(edge_type, src, trg)
    return client.create_elements(construction)[0]


def generate_node(node_type: ScType) -> ScAddr:
    construction = ScConstruction()
    construction.create_node(node_type)
    return client.create_elements(construction)[0]


def generate_node_with_idtf(node_type: ScType, idtf: str) -> ScAddr:
    params = ScIdtfResolveParams(idtf=idtf, type=node_type)
    return client.resolve_keynodes([params])[0]


def set_en_main_idtf(addr: ScAddr, idtf: str) -> ScAddr:
    keynodes = ScKeynodes()

    link = generate_link(idtf)
    generate_edge(keynodes[CommonIdentifiers.LANG_EN.value], link, sc_types.EDGE_ACCESS_CONST_POS_PERM)

    generate_binary_relation(
        addr, sc_types.EDGE_D_COMMON_CONST, link, keynodes[CommonIdentifiers.NREL_MAIN_IDENTIFIER.value]
    )
    return link


def generate_links(contents: List[str]) -> List[ScAddr]:
    links = []
    for content in contents:
        links.append(generate_link(content))
    return links


def generate_link(content: str) -> ScAddr:
    construction = ScConstruction()
    link_content = ScLinkContent(content, ScLinkContentType.STRING.value)
    construction.create_link(sc_types.LINK, link_content)
    return client.create_elements(construction)[0]


def generate_oriented_set(elements: List[ScAddr]) -> ScAddr:
    set_node = generate_node(sc_types.NODE_CONST)
    wrap_in_oriented_set(elements, set_node)
    return set_node


def wrap_in_oriented_set(elements: List[ScAddr], set_node: ScAddr) -> None:
    keynodes = ScKeynodes()
    if len(elements) > 0:
        rrel_one = keynodes[CommonIdentifiers.RREL_ONE.value]
        nrel_sequence = keynodes[CommonIdentifiers.NREL_BASIC_SEQUENCE.value]
        curr_edge = generate_binary_relation(set_node, sc_types.EDGE_ACCESS_CONST_POS_PERM, elements.pop(0), rrel_one)
        while elements:
            next_element = elements.pop(0)
            next_edge = generate_edge(set_node, next_element, sc_types.EDGE_ACCESS_CONST_POS_PERM)
            generate_binary_relation(curr_edge, sc_types.EDGE_D_COMMON_CONST, next_edge, nrel_sequence)
            curr_edge = next_edge


def wrap_in_structure(*elements: ScAddr) -> ScAddr:
    struct_node = generate_node(sc_types.NODE_CONST_STRUCT)
    for elem in elements:
        generate_edge(struct_node, elem, sc_types.EDGE_ACCESS_CONST_POS_PERM)
    return struct_node


def wrap_in_set(elements: List[ScAddr], set_node: ScAddr) -> None:
    for elem in elements:
        if not check_edge(set_node, elem, sc_types.EDGE_ACCESS_VAR_POS_PERM):
            generate_edge(set_node, elem, sc_types.EDGE_ACCESS_CONST_POS_PERM)


def generate_binary_relation(src: ScAddr, edge_type: ScType, trg: ScAddr, *relations: ScAddr) -> ScAddr:
    construction = ScConstruction()
    construction.create_edge(edge_type, src, trg, ScAlias.RELATION_EDGE.value)
    for relation in relations:
        construction.create_edge(sc_types.EDGE_ACCESS_CONST_POS_PERM, relation, ScAlias.RELATION_EDGE.value)
    return client.create_elements(construction)[0]
