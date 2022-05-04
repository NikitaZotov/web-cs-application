"""
    Copyright (c) 2022 Intelligent Semantic Systems LLC, All rights reserved.
    Author Nikita Zotov
"""

from log import get_default_logger

from json_client.constants import common, sc_types
from json_client.dataclass import ScAddr, ScEvent
from json_client.sc_agent import ScAgent
from modules.common.exception import CustomException
from modules.common.generator import generate_binary_relation, generate_event
from modules.common.identifiers import ActionIdentifiers, CommonIdentifiers, QuestionStatus
from modules.common.log_messages import (
    generate_finish_message,
    generate_no_action_argument_message,
    generate_start_message,
)
from modules.common.searcher import get_element_by_role_relation
from modules.common.utils import finish_action_status, validate_action
from modules.sc_to_rdf_translation_module.generator import fill_model_links_set
from modules.sc_to_rdf_translation_module.translator import ScToRdfTranslator

logger = get_default_logger(__name__)


class RdfScModelToRdfTranslationAgent(ScAgent):
    action = ActionIdentifiers.ACTION_TRANSLATE_RDF_SC_MODEL_TO_RDF.value

    def register(self) -> ScEvent:
        return generate_event(
            RdfScModelToRdfTranslationAgent.keynodes[QuestionStatus.QUESTION_INITIATED.value],
            common.ScEventType.ADD_OUTGOING_EDGE,
            RdfScModelToRdfTranslationAgent.run_impl,
        )

    @staticmethod
    def run_impl(action_class: ScAddr, edge: ScAddr, action_node: ScAddr) -> None:  # pylint: disable=W0613
        if validate_action(RdfScModelToRdfTranslationAgent.action, action_node):
            logger.info(generate_start_message(RdfScModelToRdfTranslationAgent))
            keynodes = RdfScModelToRdfTranslationAgent.keynodes
            try:
                rdf_sc_model = get_element_by_role_relation(action_node, keynodes[CommonIdentifiers.RREL_ONE.value])
                model_links_set = get_element_by_role_relation(action_node, keynodes[CommonIdentifiers.RREL_TWO.value])
                if rdf_sc_model is None or model_links_set is None:
                    raise CustomException(generate_no_action_argument_message(RdfScModelToRdfTranslationAgent))

                translator = ScToRdfTranslator()
                rdf_model = translator.translate_to_rdf(rdf_sc_model)
                fill_model_links_set(rdf_model, model_links_set)
                generate_binary_relation(
                    action_node,
                    sc_types.EDGE_D_COMMON_CONST,
                    model_links_set,
                    keynodes[CommonIdentifiers.NREL_ANSWER.value],
                )
                finish_action_status(action_node)
            except CustomException as ex:
                finish_action_status(action_node, False)
                logger.error(str(ex))
            logger.info(generate_finish_message(RdfScModelToRdfTranslationAgent))
