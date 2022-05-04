"""
    Author Zotov Nikita
"""

from typing import List

from log import get_default_logger

from json_client.constants import sc_types
from json_client.constants.numeric import LINK_CONTENT_MAX_SIZE
from json_client.dataclass import ScAddr
from modules.common.generator import generate_link, generate_node
from modules.common.identifiers import ActionIdentifiers, CommonIdentifiers
from modules.common.utils import call_agent_without_waiting


logger = get_default_logger(__name__)


def divide_content(content: str) -> List[str]:
    step = LINK_CONTENT_MAX_SIZE
    return [content[index: index + step] for index in range(0, len(content), step)]


def call_prepare_model_version_agent(time_point: str, action: ActionIdentifiers) -> ScAddr:
    link_set_arg = generate_node(sc_types.NODE_CONST)
    time_point_arg = generate_link(time_point)
    args = {time_point_arg: False, link_set_arg: False}
    concepts = [action.value, CommonIdentifiers.QUESTION.value]
    return call_agent_without_waiting(args, concepts)
