"""
    Author Zotov Nikita
"""

from json_client.sc_module import ScModule
from modules.sc_to_rdf_translation_module.agents import RdfScModelToRdfTranslationAgent


class ScToRdfTranslationModule(ScModule):
    def __init__(self) -> None:
        super().__init__([RdfScModelToRdfTranslationAgent])
