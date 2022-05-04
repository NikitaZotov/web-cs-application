"""
    Author Zotov Nikita
"""

from typing import List, Optional

from json_client import client
from json_client.constants import sc_types
from json_client.constants.sc_types import ScType
from json_client.dataclass import ScAddr, ScTemplate, ScTemplateResult
from json_client.sc_keynodes import ScKeynodes
from modules.common.constants import ScAlias
from modules.common.identifiers import CommonIdentifiers
from modules.common.templates import template_next_element_of_oriented_set


def check_edge(source: ScAddr, target: ScAddr, edge_type: ScType) -> bool:
    templ = ScTemplate()
    templ.triple(source, edge_type, target)
    search_results = client.template_search(templ)
    return len(search_results) > 0


def get_system_idtf(addr: ScAddr) -> str:
    keynodes = ScKeynodes()
    nrel_system_idtf = keynodes[CommonIdentifiers.NREL_SYSTEM_IDENTIFIER.value]

    templ = ScTemplate()
    templ.triple_with_relation(
        addr,
        sc_types.EDGE_D_COMMON_VAR,
        [sc_types.LINK_VAR, ScAlias.LINK.value],
        sc_types.EDGE_ACCESS_VAR_POS_PERM,
        nrel_system_idtf,
    )
    result = get_first_search_template_result(templ)
    if result:
        return get_link_content(result.get(ScAlias.LINK.value))

    return ""


def get_en_main_idtf_link(addr: ScAddr) -> ScAddr:
    keynodes = ScKeynodes()

    template = ScTemplate()
    template.triple_with_relation(
        addr,
        sc_types.EDGE_D_COMMON_VAR,
        [sc_types.LINK_VAR, ScAlias.LINK.value],
        sc_types.EDGE_ACCESS_VAR_POS_PERM,
        keynodes[CommonIdentifiers.NREL_MAIN_IDENTIFIER.value]
    )
    template.triple(
        keynodes[CommonIdentifiers.LANG_EN.value],
        sc_types.EDGE_ACCESS_VAR_POS_PERM,
        ScAlias.LINK.value,
    )
    idtf_results = client.template_search(template)

    if len(idtf_results) != 0:
        return idtf_results[0].get(ScAlias.LINK.value)

    return ScAddr(0)


def get_en_main_idtf(addr: ScAddr) -> str:
    link = get_en_main_idtf_link(addr)
    if link.is_valid():
        return get_link_content(link)

    return ""


def get_element_by_main_idtf(idtf: str) -> ScAddr:
    keynodes = ScKeynodes()

    links = client.get_link_by_content([idtf])[0]

    for link in links:
        template = ScTemplate()
        template.triple_with_relation(
            [sc_types.UNKNOWN, ScAlias.NODE.value],
            sc_types.EDGE_D_COMMON_VAR,
            link,
            sc_types.EDGE_ACCESS_VAR_POS_PERM,
            keynodes[CommonIdentifiers.NREL_MAIN_IDENTIFIER.value],
        )
        result = client.template_search(template)
        if len(result) != 0:
            return result[0].get(ScAlias.NODE.value)

    return ScAddr(0)


def get_element_by_system_idtf(idtf: str) -> ScAddr:
    keynodes = ScKeynodes()

    links = client.get_link_by_content([idtf])[0]
    if len(links) == 0:
        return ScAddr(0)

    template = ScTemplate()
    template.triple_with_relation(
        [sc_types.NODE_VAR, ScAlias.NODE.value],
        sc_types.EDGE_D_COMMON_VAR,
        links[0],
        sc_types.EDGE_ACCESS_VAR_POS_PERM,
        keynodes[CommonIdentifiers.NREL_SYSTEM_IDENTIFIER.value],
    )
    result = client.template_search(template)
    if len(result) == 0:
        return ScAddr(0)

    return result[0].get(ScAlias.NODE.value)


def get_power_of_set(source: ScAddr) -> int:
    edge_type = sc_types.EDGE_ACCESS_VAR_POS_PERM
    target = sc_types.UNKNOWN
    templ = ScTemplate()
    templ.triple(source, edge_type, target)
    search_results = client.template_search(templ)
    return len(search_results)


def get_element_by_role_relation(src: ScAddr, role: ScAddr) -> Optional[ScAddr]:
    search_result = search_role_relation_template(src, role)
    return search_result.get(ScAlias.ELEMENT.value) if search_result else None


def search_role_relation_template(src: ScAddr, role: ScAddr) -> Optional[ScTemplateResult]:
    templ = ScTemplate()
    templ.triple_with_relation(
        src,
        [sc_types.EDGE_ACCESS_VAR_POS_PERM, ScAlias.ACCESS_EDGE.value],
        [sc_types.UNKNOWN, ScAlias.ELEMENT.value],
        sc_types.EDGE_ACCESS_VAR_POS_PERM,
        role,
    )
    return get_first_search_template_result(templ)


def get_structure_elements(structure: ScAddr) -> List[ScAddr]:
    structure_elements = []
    for target in (sc_types.LINK_VAR, sc_types.NODE_VAR):
        templ = ScTemplate()
        templ.triple(structure, sc_types.EDGE_ACCESS_VAR_POS_PERM, target)
        search_results = client.template_search(templ)
        for result in search_results:
            structure_elements.append(result.get(2))
    return structure_elements


def get_elements_from_oriented_set(set_node: ScAddr) -> List[ScAddr]:
    def get_next_element(access_edge: ScAddr = None):
        if access_edge:
            elem_search_result = search_next_element_template(set_node, access_edge)
        else:
            keynodes = ScKeynodes()
            elem_search_result = search_role_relation_template(set_node, keynodes[CommonIdentifiers.RREL_ONE.value])
        if elem_search_result is None:
            return None
        elements.append(elem_search_result.get(ScAlias.ELEMENT.value))
        return elem_search_result.get(ScAlias.ACCESS_EDGE.value)

    elements = []
    elements_count = get_power_of_set(set_node)
    if elements_count:
        edge = get_next_element()
        while edge:
            edge = get_next_element(edge)
    return elements


def search_next_element_template(set_node: ScAddr, prev_element_edge: ScAddr) -> Optional[ScTemplateResult]:
    templ = template_next_element_of_oriented_set(set_node, prev_element_edge)
    return get_first_search_template_result(templ)


def get_first_search_template_result(template: ScTemplate) -> Optional[ScTemplateResult]:
    search_results = client.template_search(template)
    if len(search_results) > 0:
        return search_results[0]
    return None


def get_content_from_links_set(links_set_node: ScAddr) -> str:
    links = get_elements_from_oriented_set(links_set_node)
    parts = []
    for link in links:
        parts.append(get_link_content(link))
    return "".join(parts)


def get_link_content(link: ScAddr) -> str:
    content_part = client.get_link_content(link)
    return content_part.data


def get_action_answer(action: ScAddr) -> ScAddr:
    templ = ScTemplate()
    keynodes = ScKeynodes()
    templ.triple_with_relation(
        action,
        [sc_types.EDGE_D_COMMON_VAR, ScAlias.RELATION_EDGE.value],
        [sc_types.NODE_VAR_STRUCT, ScAlias.ELEMENT.value],
        sc_types.EDGE_ACCESS_VAR_POS_PERM,
        keynodes[CommonIdentifiers.NREL_ANSWER.value],
    )
    result = get_first_search_template_result(templ)
    return result.get(ScAlias.ELEMENT.value) if result else ScAddr(0)
