"""
    Author Zotov Nikita
"""

import unittest

from json_client import client
from json_client.constants import sc_types
from json_client.dataclass import ScConstruction
from json_client.kb_tests import ScTest
from modules.common.constants import COMMON_WAIT_TIME
from modules.common.generator import generate_node
from modules.common.identifiers import CommonIdentifiers, QuestionStatus
from modules.common.utils import call_agent
from modules.sc_to_rdf_translation_module.agents import RdfScModelToRdfTranslationAgent
from modules.sc_to_rdf_translation_module.module import ScToRdfTranslationModule
from modules.sc_to_rdf_translation_module.test.data import Data
from modules.sc_to_rdf_translation_module.test.uploader import Uploader
from modules.sc_to_rdf_translation_module.translator import ScToRdfTranslator


class RdfToScTranslatorTest(ScTest):
    def test_output_model_correct(self):
        construction = ScConstruction()
        construction.create_node(sc_types.NODE_CONST_STRUCT)
        structure = client.create_elements(construction)[0]
        self.assertTrue(structure)

        uploader = Uploader()
        uploader.upload_structure(structure, Data.first_test_elements_to_upload())
        uploader.upload_structure(structure, Data.second_test_elements_to_upload())
        uploader.upload_structure(structure, Data.third_test_elements_to_upload())

        translator = ScToRdfTranslator()
        with open("sample.rdf", encoding="utf-8", mode="w") as file:
            print(translator.translate_to_rdf(structure), file=file)

    def test_little_output_model_correct(self):
        construction = ScConstruction()
        construction.create_node(sc_types.NODE_CONST_STRUCT)
        structure = client.create_elements(construction)[0]
        self.assertTrue(structure)

        uploader = Uploader()
        uploader.upload_structure(structure, Data.first_test_elements_to_upload())

        translator = ScToRdfTranslator()
        translator.translate_to_rdf(structure)


class TranslationModuleTest(ScTest):
    @classmethod
    def setUpClass(cls) -> None:
        client.connect("ws://localhost:8090/ws_json")
        ScToRdfTranslationModule()

    @classmethod
    def tearDownClass(cls) -> None:
        client.disconnect()


class TranslationAgentRdfScModelToRdfTest(TranslationModuleTest):
    def test_wrong_arguments(self):
        result = call_agent({}, [RdfScModelToRdfTranslationAgent.action, CommonIdentifiers.QUESTION.value])
        self.assertTrue(result)

    def test_no_structure_elements(self):
        structure_node = generate_node(sc_types.NODE_CONST_STRUCT)
        links_set_node = generate_node(sc_types.NODE_CONST_STRUCT)
        args = {structure_node: False, links_set_node: False}
        reaction = QuestionStatus.QUESTION_FINISHED_SUCCESSFULLY
        result = call_agent(
            args,
            [RdfScModelToRdfTranslationAgent.action, CommonIdentifiers.QUESTION.value],
            reaction=reaction,
            wait_time=COMMON_WAIT_TIME,
        )
        self.assertTrue(result)

    def test_output_model_correct(self):
        self.correct_construction()

    def correct_construction(self, wait_time=COMMON_WAIT_TIME):
        links_set_node = generate_node(sc_types.NODE_CONST)
        structure_node = generate_node(sc_types.NODE_CONST_STRUCT)

        uploader = Uploader()
        uploader.upload_structure(structure_node, Data.first_test_elements_to_upload())
        uploader.upload_structure(structure_node, Data.second_test_elements_to_upload())

        args = {links_set_node: False, structure_node: False}
        reaction = QuestionStatus.QUESTION_FINISHED_SUCCESSFULLY
        result = call_agent(
            args,
            [RdfScModelToRdfTranslationAgent.action, CommonIdentifiers.QUESTION.value],
            reaction=reaction,
            wait_time=wait_time,
        )
        self.assertTrue(result)


if __name__ == "__main__":
    unittest.main()
