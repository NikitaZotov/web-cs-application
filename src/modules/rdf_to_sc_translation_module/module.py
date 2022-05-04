"""
    Author Zotov Nikita
"""

from json_client.sc_module import ScModule
from modules.rdf_to_sc_translation_module.agents import InputRdfModelTranslationAgent


class RdfToScTranslationModule(ScModule):
    def __init__(self) -> None:
        super().__init__([InputRdfModelTranslationAgent])
