"""
    Author Zotov Nikita
"""

from json_client.constants import sc_types
from json_client.dataclass import ScAddr
from json_client.sc_keynodes import ScKeynodes
from modules.common.generator import generate_edge, generate_links, generate_node_with_idtf, wrap_in_oriented_set
from modules.common.identifiers import CommonIdentifiers
from modules.tools import divide_content


def generate_filename_construction(filename: str, target_node: ScAddr) -> None:
    keynodes = ScKeynodes()
    filename_node = generate_node_with_idtf(sc_types.NODE_CONST, filename)
    concept_filename = keynodes[CommonIdentifiers.CONCEPT_FILENAME.value]
    generate_edge(filename_node, target_node, sc_types.EDGE_ACCESS_CONST_POS_PERM)
    generate_edge(concept_filename, filename_node, sc_types.EDGE_ACCESS_CONST_POS_PERM)


def fill_model_links_set(rdf_model: str, model_links_set: ScAddr) -> None:
    rdf_model_chunks = divide_content(rdf_model)
    links = generate_links(rdf_model_chunks)
    wrap_in_oriented_set(links, model_links_set)
