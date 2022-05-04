"""
    Author Zotov Nikita
"""

from typing import List, Tuple

from json_client.constants import sc_types
from json_client.dataclass import ScAddr
from json_client.sc_keynodes import ScKeynodes
from modules.rdf_to_sc_translation_module.identifiers import TranslationIdentifiers
from modules.sc_to_rdf_translation_module.test.generator import generate_triple_in_structure, resolve_link


class Uploader:
    def __init__(self):
        self._keynodes = ScKeynodes()

    def upload_structure(self, structure: ScAddr, elements_to_upload: List[Tuple[str, Tuple[str, str]]]):
        for relation_str, pair in elements_to_upload:
            object_str, subject_str = pair

            relation_addr = self._keynodes.__getitem__(relation_str, sc_types.NODE_CONST_NOROLE)
            object_addr = self._keynodes.__getitem__(object_str, sc_types.NODE_CONST)

            if relation_str in (
                TranslationIdentifiers.NREL_LITERAL_CONTENT.value,
                TranslationIdentifiers.NREL_IRI.value,
            ):
                subject_addr = resolve_link(subject_str)
            else:
                subject_addr = self._keynodes.__getitem__(subject_str, sc_types.NODE_CONST)

            generate_triple_in_structure(object_addr, subject_addr, relation_addr, structure)
