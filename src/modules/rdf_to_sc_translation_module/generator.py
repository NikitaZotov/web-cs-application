"""
    Author Zotov Nikita
"""

from typing import Dict, List, Optional

from rdflib import Graph

from json_client import client
from json_client.constants import sc_types
from json_client.constants.sc_types import ScType
from json_client.dataclass import (
    ScAddr,
    ScConstruction,
    ScIdtfResolveParams,
    ScLinkContent,
    ScLinkContentType,
    ScTemplate,
)
from json_client.sc_keynodes import ScKeynodes
from modules.common.constants import ScAlias
from modules.common.identifiers import CommonIdentifiers
from modules.rdf_to_sc_translation_module.constants import NUM_OF_ELEMENTS_FOR_SINGLE_CREATION


def generate_rdf_triple_in_structure(subj: ScAddr, obj: ScAddr, pred: ScAddr, struct: ScAddr) -> None:
    templ = ScTemplate()
    templ.triple_with_relation(
        subj,
        [sc_types.EDGE_D_COMMON_VAR, ScAlias.COMMON_EDGE.value],
        obj,
        [sc_types.EDGE_ACCESS_VAR_POS_PERM, ScAlias.ACCESS_EDGE.value],
        pred,
    )
    templ.triple(struct, sc_types.EDGE_ACCESS_VAR_POS_PERM, ScAlias.COMMON_EDGE.value)
    templ.triple(struct, sc_types.EDGE_ACCESS_VAR_POS_PERM, ScAlias.ACCESS_EDGE.value)

    client.template_generate(templ, {})


def generate_relations_in_structure(parsed_graph: Graph, resolved: Dict[str, ScAddr], structure: ScAddr) -> None:
    def process_graph_tripple(subj, pred, obj, constr):
        subj_addr = resolved[str(subj)]
        obj_addr = resolved[str(obj)]
        pred_addr = resolved[str(pred)]

        common_alias = f"{ScAlias.COMMON_EDGE.value}_{str(subj)}_{str(obj)}_{str(pred)}"
        access_alias = f"{ScAlias.ACCESS_EDGE.value}_{str(subj)}_{str(obj)}_{str(pred)}"

        _update_construction(constr, subj_addr, obj_addr, pred_addr, structure, common_alias, access_alias)

    generation_counter = 0
    construction = ScConstruction()
    for subj, pred, obj in parsed_graph:
        if generation_counter == NUM_OF_ELEMENTS_FOR_SINGLE_CREATION:
            generation_counter = 0

            client.create_elements(construction)
            construction = ScConstruction()
        process_graph_tripple(subj, pred, obj, construction)
        generation_counter += 1

    client.create_elements(construction)


def _update_construction(
    const: ScConstruction,
    subj: ScAddr,
    obj: ScAddr,
    pred: ScAddr,
    structure: ScAddr,
    common_alias: str,
    access_alias: str,
) -> None:
    const.create_edge(sc_types.EDGE_D_COMMON_CONST, subj, obj, common_alias)
    const.create_edge(sc_types.EDGE_ACCESS_CONST_POS_PERM, pred, common_alias, access_alias)
    const.create_edge(sc_types.EDGE_ACCESS_CONST_POS_PERM, structure, common_alias)
    const.create_edge(sc_types.EDGE_ACCESS_CONST_POS_PERM, structure, access_alias)


def generate_cim_nodes(nodes_to_generate: Dict[str, ScType], with_idtf=False) -> Dict[str, ScAddr]:
    nodes_to_generate_list_chunks = _chunks(list(nodes_to_generate.items()))
    content_with_idtf = []
    nodes_with_idtf = []
    content_empty_idtf = []
    empty_nodes = []
    for chunk in nodes_to_generate_list_chunks:
        params_for_resolving = []
        construction = ScConstruction()

        for content, node_type in chunk:
            if with_idtf:
                params = get_params_for_resolve_idtf(content, node_type)
                if params:
                    params_for_resolving.append(params)
                    content_with_idtf.append(content)
                else:
                    construction.create_node(node_type)
                    content_empty_idtf.append(content)
            else:
                construction.create_node(node_type)
                content_empty_idtf.append(content)

        nodes_with_idtf.extend(client.resolve_keynodes(params_for_resolving))
        empty_nodes.extend(client.create_elements(construction))

    cim_nodes_with_idtf = dict(zip(content_empty_idtf, empty_nodes))
    cim_nodes_with_idtf.update(zip(content_with_idtf, nodes_with_idtf))
    return cim_nodes_with_idtf


def generate_relation_to_link(nodes_to_generate: Dict[str, ScAddr], relation: ScAddr) -> List[ScAddr]:
    nodes_to_generate_list_chunks = _chunks(list(nodes_to_generate.items()))
    generated_elements = []
    for chunk in nodes_to_generate_list_chunks:
        construction = ScConstruction()
        for content, node in chunk:
            link_content_alias = f"{ScAlias.LINK.value}_{content}"
            common_edge_content_alias = f"{ScAlias.COMMON_EDGE.value}_{content}"

            link_content = ScLinkContent(content, ScLinkContentType.STRING.value)
            construction.create_link(sc_types.LINK, link_content, link_content_alias)

            construction.create_edge(sc_types.EDGE_D_COMMON_CONST, node, link_content_alias, common_edge_content_alias)
            construction.create_edge(sc_types.EDGE_ACCESS_CONST_POS_PERM, relation, common_edge_content_alias)

            generated_elements.append(node)
        generated_elements.extend(client.create_elements(construction))
    return generated_elements


def get_params_for_resolve_idtf(content: str, node_type: ScType) -> Optional[ScIdtfResolveParams]:
    prefix, part = None, None
    nrel_pref = "nrel_" if node_type == sc_types.NODE_CONST_NOROLE else ""

    cim_substr = "schema-cim16#"
    if cim_substr in content:
        prefix = "cim_"
        part = content.split(cim_substr, 1)[1]
        if "." in part:
            part = part.replace(".", "_")
            node_type = sc_types.NODE_CONST_NOROLE
            nrel_pref = "nrel_"

    owl_substr = "owl#"
    if owl_substr in content:
        part = content.split(owl_substr, 1)[1]
        if "-" not in part:
            prefix = "owl_"

    rdf_substr = "rdf-syntax-ns#"
    if rdf_substr in content:
        prefix = "rdf_"
        part = content.split(rdf_substr, 1)[1]

    rdf_substr = "rdf-schema#"
    if rdf_substr in content:
        prefix = "rdf_"
        part = content.split(rdf_substr, 1)[1]

    if prefix:
        return ScIdtfResolveParams(idtf=f"{prefix}{nrel_pref}{part}", type=node_type)

    return None


def add_elements_in_set(elements: List[ScAddr], elements_set: ScAddr) -> None:
    elements_list_chunks = _chunks(elements)
    for chunk in elements_list_chunks:
        construction = ScConstruction()
        for element in chunk:
            construction.create_edge(sc_types.EDGE_ACCESS_CONST_POS_PERM, elements_set, element)
        client.create_elements(construction)


def _chunks(elements: list):
    for i in range(0, len(elements), NUM_OF_ELEMENTS_FOR_SINGLE_CREATION):
        yield elements[i: i + NUM_OF_ELEMENTS_FOR_SINGLE_CREATION]
