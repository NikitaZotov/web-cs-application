"""
    Author Zotov Nikita
"""

import unittest

from json_client import client
from json_client.constants import sc_types
from json_client.dataclass import ScConstruction
from json_client.kb_tests import ScTest
from modules.common.constants import COMMON_WAIT_TIME
from modules.common.generator import generate_links, generate_node, generate_oriented_set
from modules.common.identifiers import CommonIdentifiers, QuestionStatus
from modules.common.utils import call_agent
from modules.rdf_to_sc_translation_module.module import RdfToScTranslationModule
from modules.rdf_to_sc_translation_module.test.constants import TestModels
from modules.rdf_to_sc_translation_module.test.templates import (
    correct_model_with_one_triple_result_construction,
    template_aliases,
)
from modules.rdf_to_sc_translation_module.translator import RdfToScTranslator
from modules.tools import divide_content


class RdfToScTranslatorTest(ScTest):
    def test_input_model_correct_construction_with_pre_prepared_literals(self):
        elements_to_delete = []
        construction = ScConstruction()
        construction.create_node(sc_type=sc_types.NODE_CONST)
        structure = client.create_elements(construction)[0]
        model = TestModels.CORRECT_MODEL_WITH_PRE_PREPARED_LITERALS.value
        translator = RdfToScTranslator()
        translator.translate_initial_model_to_sc(model, structure)
        template = correct_model_with_one_triple_result_construction(structure, True)
        search_results = client.template_search(template)
        self.assertEqual(len(search_results), 1)
        for alias in template_aliases:
            elements_to_delete.append(search_results[0].get(alias))
        elements_to_delete.append(structure)
        status = client.delete_elements(elements_to_delete)
        self.assertTrue(status)

    def test_input_model_correct_construction_with_generated_literals(self):
        elements_to_delete = []
        construction = ScConstruction()
        construction.create_node(sc_type=sc_types.NODE_CONST)
        structure = client.create_elements(construction)[0]
        model = TestModels.CORRECT_MODEL_WITH_GENERATED_LITERALS.value
        translator = RdfToScTranslator()
        translator.translate_initial_model_to_sc(model, structure)
        template = correct_model_with_one_triple_result_construction(structure, True)
        search_results = client.template_search(template)
        self.assertEqual(len(search_results), 1)
        for alias in template_aliases:
            elements_to_delete.append(search_results[0].get(alias))
        elements_to_delete.append(structure)
        status = client.delete_elements(elements_to_delete)
        self.assertTrue(status)

    def test_input_model_correct_construction_with_relation_to_named_class(self):
        elements_to_delete = []
        construction = ScConstruction()
        construction.create_node(sc_type=sc_types.NODE_CONST)
        structure = client.create_elements(construction)[0]
        model = TestModels.CORRECT_MODEL_WITH_RELATION_TO_NAMED_CLASS.value
        translator = RdfToScTranslator()
        translator.translate_initial_model_to_sc(model, structure)
        template = correct_model_with_one_triple_result_construction(structure, False)
        search_results = client.template_search(template)
        self.assertEqual(len(search_results), 1)
        for alias in template_aliases:
            elements_to_delete.append(search_results[0].get(alias))
        elements_to_delete.append(structure)
        status = client.delete_elements(elements_to_delete)
        self.assertTrue(status)


class TranslationModuleTest(ScTest):
    @classmethod
    def setUpClass(cls) -> None:
        client.connect("ws://localhost:8090/ws_json")
        RdfToScTranslationModule()

    @classmethod
    def tearDownClass(cls) -> None:
        client.disconnect()


def correct_construction(action_idtf: str, content: str, wait_time=COMMON_WAIT_TIME) -> bool:
    divided_model = generate_links(divide_content(content))
    links_set_node = generate_oriented_set(divided_model)
    structure_node = generate_node(sc_types.NODE_CONST_STRUCT)
    args = {links_set_node: False, structure_node: False}
    reaction = QuestionStatus.QUESTION_FINISHED_SUCCESSFULLY
    result = call_agent(
        args,
        [action_idtf, CommonIdentifiers.QUESTION.value],
        reaction=reaction,
        wait_time=wait_time,
    )
    return result


if __name__ == "__main__":
    unittest.main()
