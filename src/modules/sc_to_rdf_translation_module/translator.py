"""
    Copyright (c) 2022 Intelligent Semantic Systems LLC, All rights reserved.
    Author Nikita Zotov
"""

import logging
from typing import Tuple

from log import get_default_logger
from rdflib import Graph, Literal, Namespace
from rdflib.resource import Resource

from json_client import client
from json_client.dataclass import ScAddr
from json_client.sc_keynodes import ScKeynodes
from modules.common.log_messages import (
    generate_custom_message,
    generate_finish_message,
    generate_resolved_graph_message,
    generate_start_message,
)
from modules.common.searcher import get_system_idtf
from modules.rdf_to_sc_translation_module.identifiers import TranslationIdentifiers
from modules.rdf_searcher.searcher import RdfConstructionsSearcher

logger = get_default_logger(__name__)


class ScToRdfTranslator:
    def __init__(self) -> None:
        self._keynodes = ScKeynodes()

    def translate_to_rdf(self, structure: ScAddr) -> str:
        logger.info(generate_start_message(self.__class__))
        rdf_graph = self._resolve_element_iris_in_structure(structure)

        rdf_model = rdf_graph.serialize(None, format="xml", encoding="utf-8").decode("utf-8")
        logger.info(generate_resolved_graph_message(self.__class__))

        logger.info(generate_finish_message(self.__class__))
        return rdf_model

    def _resolve_element_iris_in_structure(self, structure: ScAddr) -> Graph:
        rdf_graph = Graph()

        searcher = RdfConstructionsSearcher()
        searcher.find_elements_iris_in_structure(structure)

        for element_addr, iri_addr, _ in searcher:
            iri_str = client.get_link_content(iri_addr).data
            logger.debug(generate_custom_message(self.__class__, f"Resolve element with iri {iri_str}"))
            iri_element = rdf_graph.resource(iri_str)

            self._resolve_linked_elements_iris_in_structure(iri_element, element_addr, structure, rdf_graph)

        return rdf_graph

    def _resolve_linked_elements_iris_in_structure(
        self, iri_element: Resource, element_addr: ScAddr, structure: ScAddr, rdf_graph: Graph
    ):
        logger.info(generate_custom_message(self.__class__, "Resolve linked elements"))
        searcher = RdfConstructionsSearcher()
        searcher.find_linked_elements_in_structure(element_addr, structure)

        element_searcher = RdfConstructionsSearcher()
        for _, element_type_addr, relation_addr in searcher:
            if not get_system_idtf(relation_addr):
                continue

            relation_uri = self._resolve_relation_uri(relation_addr, structure, rdf_graph)

            element_searcher.find_element_iris_in_structure(element_type_addr, structure)
            for _, iri_addr, _ in element_searcher:
                iri_str = client.get_link_content(iri_addr).data
                iri = rdf_graph.resource(iri_str)
                iri_element.add(relation_uri, iri)
                logging.debug(generate_custom_message(self.__class__, f"Resolved predicated element iri: {iri_str}"))

            element_searcher.find_element_literals_in_structure(element_type_addr, structure)
            for _, literal_addr, _ in element_searcher:
                literal_str = client.get_link_content(literal_addr).data
                iri_element.add(relation_uri, Literal(literal_str))
                logging.debug(generate_custom_message(self.__class__, f"Resolved literal: {literal_str}"))

    def _resolve_relation_uri(self, relation_addr: ScAddr, structure: ScAddr, rdf_graph: Graph):
        relation_idtf = get_system_idtf(relation_addr)
        logging.debug(generate_custom_message(self.__class__, f"Resolved predicate: {relation_idtf}"))
        prefix, predicate = self._get_prefix_predicate(relation_idtf)

        iri_str = self._get_relation_uri_str_in_structure(relation_addr, structure)
        namespace = Namespace(self._check_iri_str(iri_str, prefix))
        rdf_graph.namespace_manager.bind(prefix, namespace)

        return namespace[predicate]

    def _get_prefix_predicate(self, relation_idtf: str) -> Tuple[str, str]:
        prefix_predicate = relation_idtf.split("_", 1)
        prefix = prefix_predicate[0]
        if prefix == "cim":
            prefix += "16"
        predicate = prefix_predicate[1].replace("nrel_", "").replace("_", ".")

        return prefix, predicate

    def _get_relation_uri_str_in_structure(self, relation_addr: ScAddr, structure: ScAddr):
        searcher = RdfConstructionsSearcher()
        iri_str = searcher.get_element_iri_str_in_structure(relation_addr, structure)

        if self._keynodes[TranslationIdentifiers.RDF_NREL_TYPE.value] != relation_addr:
            return iri_str.split("#", 1)[0] + "#"

        return iri_str

    def _check_iri_str(self, iri_str: str, prefix: str) -> str:
        if iri_str == "#":
            resolved_iri_str = RdfConstructionsSearcher().get_element_iri_str(self._keynodes[prefix])
            if str != "":
                return resolved_iri_str

        return iri_str
