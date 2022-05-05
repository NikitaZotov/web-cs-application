"""
    Author Zotov Nikita
"""

from enum import Enum


class ActionIdentifiers(Enum):
    ACTION_TRANSLATE_INPUT_RDF_MODEL_TO_RDF_SC = "action_translate_input_rdf_model_to_rdf_sc"
    ACTION_TRANSLATE_RDF_SC_MODEL_TO_RDF = "action_translate_rdf_sc_model_to_rdf"


class CommonIdentifiers(Enum):
    QUESTION = "question"
    EXACT_VALUE = "exact_value"
    RREL_DYNAMIC_ARGUMENT = "rrel_dynamic_argument"
    RREL_ONE = "rrel_1"
    RREL_TWO = "rrel_2"
    NREL_BASIC_SEQUENCE = "nrel_basic_sequence"
    NREL_SYSTEM_IDENTIFIER = "nrel_system_identifier"
    NREL_MAIN_IDENTIFIER = "nrel_main_idtf"
    NREL_ANSWER = "nrel_answer"
    CONCEPT_FILENAME = "concept_filename"
    LANG_EN = "lang_en"


class QuestionStatus(Enum):
    QUESTION_INITIATED = "question_initiated"
    QUESTION_FINISHED = "question_finished"
    QUESTION_FINISHED_SUCCESSFULLY = "question_finished_successfully"
    QUESTION_FINISHED_UNSUCCESSFULLY = "question_finished_unsuccessfully"
