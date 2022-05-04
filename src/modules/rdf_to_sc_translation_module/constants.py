"""
    Author Zotov Nikita
"""

from enum import Enum

from modules.rdf_to_sc_translation_module.identifiers import LiteralClassesIdentifiers


class LiteralValues(Enum):
    TRUE = "true"
    FALSE = "false"


LITERALS = {
    LiteralValues.TRUE.value: LiteralClassesIdentifiers.CONCEPT_RDF_TRUE.value,
    LiteralValues.FALSE.value: LiteralClassesIdentifiers.CONCEPT_RDF_FALSE.value,
}


FILE_ENCODING = "unicode"

NUM_OF_ELEMENTS_FOR_SINGLE_CREATION = 10000
