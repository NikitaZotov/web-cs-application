"""
    Author Zotov Nikita
"""

from enum import Enum


class TranslationIdentifiers(Enum):
    NREL_IRI = "nrel_iri"
    CONCEPT_IRI = "concept_iri"
    NREL_LITERAL_CONTENT = "nrel_literal_content"
    RDF_NREL_TYPE = "rdf_nrel_type"


class LiteralClassesIdentifiers(Enum):
    CONCEPT_RDF_TRUE = "concept_rdf_true"
    CONCEPT_RDF_FALSE = "concept_rdf_false"
