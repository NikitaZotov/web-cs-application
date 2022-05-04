"""
    Author Zotov Nikita
"""

from __future__ import annotations

from typing import List, Tuple

from json_client import client
from json_client.constants import sc_types
from json_client.constants.sc_types import ScType
from json_client.dataclass import ScAddr, ScTemplate, ScTemplateResult
from json_client.sc_keynodes import ScKeynodes
from modules.rdf_to_sc_translation_module.identifiers import TranslationIdentifiers


class ConstructionsSearcher:
    SOURCE_ALIAS = "_source"
    EDGE_ALIAS = "_edge"
    TARGET_ALIAS = "_target"
    RELATION_ALIAS = "_relation"
    REL_EDGE_ALIAS = "_relation_edge"
    TIMESTAMP_NODE_ALIAS = "_timestamp"

    def __init__(self):
        self._found_results: List[ScTemplateResult] = []
        self._iter_counter = -1

    def find_relation_triples_in_structure(
        self, source_param: ScAddr | ScType, target_type: ScType, relation_param: ScAddr | ScType, structure: ScAddr
    ) -> None:
        templ = ScTemplate()
        templ.triple_with_relation(
            [source_param, ConstructionsSearcher.SOURCE_ALIAS],
            [sc_types.EDGE_D_COMMON_VAR, ConstructionsSearcher.EDGE_ALIAS],
            [target_type, ConstructionsSearcher.TARGET_ALIAS],
            [sc_types.EDGE_ACCESS_VAR_POS_PERM, ConstructionsSearcher.REL_EDGE_ALIAS],
            [relation_param, ConstructionsSearcher.RELATION_ALIAS],
        )
        templ.triple(
            structure,
            sc_types.EDGE_ACCESS_VAR_POS_PERM,
            ConstructionsSearcher.EDGE_ALIAS,
        )
        templ.triple(
            structure,
            sc_types.EDGE_ACCESS_VAR_POS_PERM,
            ConstructionsSearcher.REL_EDGE_ALIAS,
        )
        self._found_results = client.template_search(templ)

    def find_relation_triples(
        self, source_param: ScAddr | ScType, target_type: ScType, relation_param: ScAddr | ScType
    ) -> None:
        templ = ScTemplate()
        templ.triple_with_relation(
            [source_param, ConstructionsSearcher.SOURCE_ALIAS],
            [sc_types.EDGE_D_COMMON_VAR, ConstructionsSearcher.EDGE_ALIAS],
            [target_type, ConstructionsSearcher.TARGET_ALIAS],
            [sc_types.EDGE_ACCESS_VAR_POS_PERM, ConstructionsSearcher.REL_EDGE_ALIAS],
            [relation_param, ConstructionsSearcher.RELATION_ALIAS],
        )
        self._found_results = client.template_search(templ)

    def find_relation_triples_with_links_in_structure(
        self, source_param: ScAddr | ScType, relation_param: ScAddr | ScType, structure: ScAddr
    ) -> None:
        self.find_relation_triples_in_structure(source_param, sc_types.LINK_VAR, relation_param, structure)

    def find_relation_triples_with_links(self, source_param: ScAddr | ScType, relation_param: ScAddr | ScType) -> None:
        self.find_relation_triples(source_param, sc_types.LINK_VAR, relation_param)

    def find_relation_triples_with_nodes_in_structure(self, source: ScAddr, structure: ScAddr) -> None:
        self.find_relation_triples_in_structure(source, sc_types.NODE_VAR, sc_types.NODE_VAR_NOROLE, structure)

    def __iter__(self):
        self._iter_counter = -1
        return self

    def __next__(self) -> Tuple[ScAddr, ScAddr, ScAddr]:
        if self._iter_counter < self.size():
            self._iter_counter += 1
            return self[self._iter_counter]

        raise StopIteration

    def __getitem__(self, index: int) -> Tuple[ScAddr, ScAddr, ScAddr]:
        if len(self._found_results) > index:
            result = self._found_results[index]
            return (
                result.get(ConstructionsSearcher.SOURCE_ALIAS),
                result.get(ConstructionsSearcher.TARGET_ALIAS),
                result.get(ConstructionsSearcher.RELATION_ALIAS),
            )

        raise StopIteration

    def size(self) -> int:
        return len(self._found_results)


class RdfConstructionsSearcher(ConstructionsSearcher):
    def __init__(self):
        super().__init__()
        self._keynodes = ScKeynodes()

    def find_elements_iris_in_structure(self, structure: ScAddr) -> None:
        self.find_relation_triples_with_links_in_structure(
            sc_types.NODE_VAR, self._keynodes[TranslationIdentifiers.NREL_IRI.value], structure
        )

    def find_element_iris_in_structure(self, addr: ScAddr, structure: ScAddr) -> None:
        self.find_relation_triples_with_links_in_structure(
            addr, self._keynodes[TranslationIdentifiers.NREL_IRI.value], structure
        )

    def find_element_iris(self, addr: ScAddr) -> None:
        self.find_relation_triples_with_links(addr, self._keynodes[TranslationIdentifiers.NREL_IRI.value])

    def find_linked_elements_in_structure(self, addr: ScAddr, structure: ScAddr) -> None:
        self.find_relation_triples_with_nodes_in_structure(addr, structure)

    def find_element_literals_in_structure(self, addr: ScAddr, structure: ScAddr) -> None:
        self.find_relation_triples_with_links_in_structure(
            addr, self._keynodes[TranslationIdentifiers.NREL_LITERAL_CONTENT.value], structure
        )

    def get_element_iri_str_in_structure(self, relation_addr: ScAddr, structure: ScAddr) -> str:
        self.find_element_iris_in_structure(relation_addr, structure)
        if self.size() == 1:
            _, iri, _ = self[0]
            return client.get_link_content(iri).data

        return ""

    def get_element_iri_str(self, relation_addr: ScAddr) -> str:
        self.find_element_iris(relation_addr)
        if self.size() == 1:
            _, iri, _ = self[0]
            return client.get_link_content(iri).data

        return ""
