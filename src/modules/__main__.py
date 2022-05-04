"""
    Copyright (c) 2022 Intelligent Semantic Systems LLC, All rights reserved.
    Author Nikiforov Sergei
    Author Nikita Zotov
"""

from json_client import client
from modules.rdf_to_sc_translation_module.module import RdfToScTranslationModule
from modules.sc_to_rdf_translation_module.module import ScToRdfTranslationModule

if __name__ == "__main__":
    client.connect("ws://localhost:8090/ws_json")
    RdfToScTranslationModule()
    ScToRdfTranslationModule()
