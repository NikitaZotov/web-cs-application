"""
    Author Zotov Nikita
"""

from typing import Dict, List, Tuple

from log import get_default_logger
from rdflib import Graph, Literal

from json_client.constants import sc_types
from json_client.dataclass import ScAddr
from json_client.sc_keynodes import ScKeynodes
from modules.common.constants import FileType
from modules.common.exception import CustomException
from modules.common.log_messages import (
    generate_custom_message,
    generate_elements_added_to_structure_message,
    generate_elements_resolved_message,
    generate_finish_message,
    generate_parsed_graph_message,
    generate_relations_in_structure_message,
    generate_start_message,
)
from modules.rdf_to_sc_translation_module.constants import LITERALS, LiteralValues
from modules.rdf_to_sc_translation_module.generator import (
    add_elements_in_set,
    generate_cim_nodes,
    generate_relation_to_link,
    generate_relations_in_structure,
)
from modules.rdf_to_sc_translation_module.identifiers import TranslationIdentifiers
from modules.rdf_to_sc_translation_module.searcher import (
    find_all_triple_with_relation_to_link_elements,
    find_literal_nodes_by_content,
    find_nodes_by_iris,
)

logger = get_default_logger(__name__)


class RdfToScTranslator:
    def __init__(self) -> None:
        self.keynodes = ScKeynodes()

    def translate_initial_model_to_sc(self, rdf_model_text: str, structure: ScAddr) -> None:
        self.translate_graph_to_sc(rdf_model_text, structure, is_diff=False)
        logger.info(generate_finish_message(self.__class__))

    def translate_graph_to_sc(self, rdf_model_text: str, structure: ScAddr, is_diff: bool) -> Graph:
        logger.info(generate_start_message(self.__class__))

        rdf_graph = self.parse_graph(rdf_model_text)
        logger.info(generate_parsed_graph_message(self.__class__))

        resolved_elements, elements_for_addition = self.resolve_elements(rdf_graph, is_diff)
        logger.info(generate_elements_resolved_message(self.__class__))

        add_elements_in_set(elements_for_addition, structure)
        logger.info(generate_elements_added_to_structure_message(self.__class__))

        generate_relations_in_structure(rdf_graph, resolved_elements, structure, is_diff)
        logger.info(generate_relations_in_structure_message(self.__class__))
        return rdf_graph

    def parse_graph(self, rdf_model_text: str) -> Graph:
        try:
            rdf_graph = Graph()
            rdf_graph.parse(data=rdf_model_text, format=FileType.XML.value)
            return rdf_graph
        except Exception as ex:
            raise CustomException(generate_custom_message(self.__class__, str(ex))) from ex

    def resolve_elements(self, parsed_graph: Graph, is_diff: bool) -> Tuple[Dict[str, ScAddr], List[ScAddr]]:
        resolved_elements = {}
        iris_to_resolve = {}
        literals_to_resolve = []
        elements_for_addition = []
        for subj, pred, obj in parsed_graph:
            iris_to_resolve.update({str(subj): False})
            iris_to_resolve.update({str(pred): True})
            if isinstance(obj, Literal):
                literals_to_resolve.append(str(obj))
            else:
                iris_to_resolve.update({str(obj): False})

        resolved_iris, iri_structures_elements = self.resolve_iris(iris_to_resolve, is_diff)
        resolved_literals, literals_structures_elements = self.resolve_literals(literals_to_resolve, is_diff)

        resolved_elements.update(resolved_iris)
        resolved_elements.update(resolved_literals)

        if iri_structures_elements:
            elements_for_addition.append(self.keynodes[TranslationIdentifiers.NREL_IRI.value])
        if literals_structures_elements:
            elements_for_addition.append(self.keynodes[TranslationIdentifiers.NREL_LITERAL_CONTENT.value])

        elements_for_addition.extend(iri_structures_elements)
        elements_for_addition.extend(literals_structures_elements)

        return resolved_elements, elements_for_addition

    def resolve_iris(self, iris: Dict[str, bool], is_diff: bool) -> Tuple[Dict[str, ScAddr], List]:
        nrel_iri = self.keynodes[TranslationIdentifiers.NREL_IRI.value]
        resolved_iris = {}
        elements_for_addition = []
        if is_diff:
            found_nodes = find_nodes_by_iris(list(iris.keys()))
            for node in found_nodes.values():
                if node is not None:
                    elements_for_addition.extend(find_all_triple_with_relation_to_link_elements(node, nrel_iri))
            resolved_iris.update(found_nodes)
        else:
            resolved_iris = {iri: None for iri in list(iris.keys())}

        iris_to_generate = {}
        for iri, addr in resolved_iris.items():
            if addr is None:
                if iris[iri]:  # Checks is element relation
                    node_type = sc_types.NODE_CONST_NOROLE
                else:
                    node_type = sc_types.NODE_CONST
                iris_to_generate.update({iri: node_type})

        generated_iri_nodes = generate_cim_nodes(iris_to_generate, with_idtf=True)
        resolved_iris.update(generated_iri_nodes)

        generated_elements = generate_relation_to_link(generated_iri_nodes, nrel_iri)
        elements_for_addition.extend(generated_elements)

        return resolved_iris, elements_for_addition

    def resolve_literals(self, literals: List[str], is_diff: bool) -> Tuple[Dict[str, ScAddr], List]:
        nrel_literal_content = self.keynodes[TranslationIdentifiers.NREL_LITERAL_CONTENT.value]
        resolved_literals = {
            LiteralValues.TRUE.value: self.keynodes[LITERALS[LiteralValues.TRUE.value]],
            LiteralValues.FALSE.value: self.keynodes[LITERALS[LiteralValues.FALSE.value]],
        }
        elements_for_addition = []

        if is_diff:
            found_literals = find_literal_nodes_by_content(literals)
            for literal_node in found_literals.values():
                if literal_node is not None:
                    elements_for_addition.extend(
                        find_all_triple_with_relation_to_link_elements(literal_node, nrel_literal_content)
                    )
            resolved_literals.update(found_literals)
        else:
            resolved_literals.update({literal: None for literal in literals})
        literals_to_generate = {}

        for literal, addr in resolved_literals.items():
            if addr is None:
                literals_to_generate.update({literal: sc_types.NODE_CONST})

        generated_literals = generate_cim_nodes(literals_to_generate, with_idtf=False)
        resolved_literals.update(generated_literals)

        generated_elements = generate_relation_to_link(generated_literals, nrel_literal_content)
        elements_for_addition.extend(generated_elements)

        return resolved_literals, elements_for_addition
