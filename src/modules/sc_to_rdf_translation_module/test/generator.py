"""
    Author Zotov Nikita
"""

from json_client import client
from json_client.constants import sc_types
from json_client.constants.sc_types import ScType
from json_client.dataclass import ScAddr, ScConstruction, ScLinkContent, ScLinkContentType, ScTemplate
from modules.common.searcher import check_edge


def generate_triple_in_structure(source: ScAddr, target: ScAddr, relation: ScAddr, structure: ScAddr):
    source_alias = "_source"
    edge_alias = "_edge"
    target_alias = "_target"
    rel_edge = "_rel_edge"

    templ = ScTemplate()
    templ.triple_with_relation(
        [source, source_alias],
        [sc_types.EDGE_D_COMMON_VAR, edge_alias],
        [target, target_alias],
        [sc_types.EDGE_ACCESS_VAR_POS_PERM, rel_edge],
        relation,
    )
    gen_result = client.template_generate(templ, {})

    add_to_set(
        [
            gen_result.get(source_alias),
            gen_result.get(edge_alias),
            gen_result.get(target_alias),
            gen_result.get(rel_edge),
            relation,
        ],
        structure,
    )


def add_to_set(elements, set_addr: ScAddr):
    construction = ScConstruction()
    for element in elements:
        if not check_edge(set_addr, element, sc_types.EDGE_ACCESS_VAR_POS_PERM):
            construction.create_edge(sc_types.EDGE_ACCESS_CONST_POS_PERM, set_addr, element)
    client.create_elements(construction)


def resolve_link(content: str) -> ScAddr:
    link_content = ScLinkContent(content, ScLinkContentType.STRING.value)
    construction = ScConstruction()
    construction.create_link(sc_types.LINK_CONST, link_content)
    return client.create_elements(construction)[0]


def create_node(sc_type: ScType) -> ScAddr:
    construction = ScConstruction()
    construction.create_node(sc_type)
    return client.create_elements(construction)[0]
