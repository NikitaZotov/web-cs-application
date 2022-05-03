"""
    Author Zotov Nikita
"""

from typing import Optional

from common.identifiers import CommonIdentifiers
from json_client import client
from json_client.constants import sc_types
from json_client.constants.sc_types import ScType
from json_client.dataclass import ScAddr, ScTemplate, ScTemplateResult
from json_client.sc_keynodes import ScKeynodes
from common.constants import ScAlias


def check_edge(source: ScAddr, target: ScAddr, edge_type: ScType) -> bool:
    templ = ScTemplate()
    templ.triple(source, edge_type, target)
    search_results = client.template_search(templ)
    return len(search_results) > 0


def get_edge(source: ScAddr, target: ScAddr, edge_type: ScType) -> ScAddr:
    templ = ScTemplate()
    templ.triple(source, [edge_type, ScAlias.RELATION_EDGE.value], target)
    search_results = client.template_search(templ)
    if len(search_results) > 0:
        return search_results[0].get(ScAlias.RELATION_EDGE.value)

    return ScAddr(0)


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


def get_element_by_norole_relation(src: ScAddr, norole: ScAddr) -> Optional[ScAddr]:
    search_result = search_norole_relation_template(src, norole)
    return search_result.get(ScAlias.ELEMENT.value) if search_result else None


def search_norole_relation_template(src: ScAddr, norole: ScAddr) -> Optional[ScTemplateResult]:
    templ = ScTemplate()
    templ.triple_with_relation(
        src,
        [sc_types.EDGE_D_COMMON_VAR, ScAlias.ACCESS_EDGE.value],
        [sc_types.UNKNOWN, ScAlias.ELEMENT.value],
        sc_types.EDGE_ACCESS_VAR_POS_PERM,
        norole,
    )
    return get_first_search_template_result(templ)


def get_first_search_template_result(template: ScTemplate) -> Optional[ScTemplateResult]:
    search_results = client.template_search(template)
    if len(search_results) > 0:
        return search_results[0]
    return None


def get_link_content(link: ScAddr) -> str:
    content_part = client.get_link_content(link)
    return content_part.data
