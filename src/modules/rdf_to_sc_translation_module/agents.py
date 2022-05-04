"""
    Author Zotov Nikita
"""

from log import get_default_logger

from json_client.constants import common
from json_client.dataclass import ScAddr, ScEvent
from json_client.sc_agent import ScAgent
from modules.common.exception import CustomException
from modules.common.generator import generate_event
from modules.common.identifiers import ActionIdentifiers, CommonIdentifiers, QuestionStatus
from modules.common.log_messages import (
    generate_empty_link_message,
    generate_finish_message,
    generate_no_action_argument_message,
    generate_start_message,
)
from modules.common.searcher import get_element_by_role_relation
from modules.common.utils import finish_action_status, validate_action
from modules.rdf_to_sc_translation_module.searcher import restore_model_content
from modules.rdf_to_sc_translation_module.translator import RdfToScTranslator

logger = get_default_logger(__name__)


class InputRdfModelTranslationAgent(ScAgent):
    action = ActionIdentifiers.ACTION_TRANSLATE_INPUT_RDF_MODEL_TO_RDF_SC.value

    def register(self) -> ScEvent:
        return generate_event(
            InputRdfModelTranslationAgent.keynodes[QuestionStatus.QUESTION_INITIATED.value],
            common.ScEventType.ADD_OUTGOING_EDGE,
            InputRdfModelTranslationAgent.run_impl,
        )

    @staticmethod
    def run_impl(action_class: ScAddr, edge: ScAddr, action_node: ScAddr) -> None:  # pylint: disable=W0613
        if validate_action(InputRdfModelTranslationAgent.action, action_node):
            logger.info(generate_start_message(InputRdfModelTranslationAgent))
            keynodes = InputRdfModelTranslationAgent.keynodes
            try:
                model_links_set = get_element_by_role_relation(action_node, keynodes[CommonIdentifiers.RREL_ONE.value])
                structure = get_element_by_role_relation(action_node, keynodes[CommonIdentifiers.RREL_TWO.value])
                if model_links_set is None or structure is None:
                    raise CustomException(generate_no_action_argument_message(InputRdfModelTranslationAgent))
                rdf_model = restore_model_content(model_links_set)
                if not rdf_model:
                    raise CustomException(generate_empty_link_message(InputRdfModelTranslationAgent))
                translator = RdfToScTranslator()
                translator.translate_initial_model_to_sc(rdf_model, structure)
                finish_action_status(action_node)
            except CustomException as ex:
                finish_action_status(action_node, False)
                logger.error(str(ex))
            logger.info(generate_finish_message(InputRdfModelTranslationAgent))
