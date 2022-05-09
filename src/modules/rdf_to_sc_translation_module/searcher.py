"""
    Author Zotov Nikita
"""

from enum import Enum
from json_client.dataclass import ScAddr
from modules.common.searcher import get_content_from_links_set
from modules.rdf_to_sc_translation_module.identifiers import TranslationIdentifiers


class ModelNodesType(Enum):
    iri_node = TranslationIdentifiers.NREL_IRI.value
    literal_node = TranslationIdentifiers.NREL_LITERAL_CONTENT.value


def restore_model_content(links_set_node: ScAddr) -> str:
    return get_content_from_links_set(links_set_node)
