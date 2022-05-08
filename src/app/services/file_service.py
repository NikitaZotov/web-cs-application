"""
    Author Zotov Nikita
"""
from json_client.constants import sc_types
from json_client.sc_keynodes import ScKeynodes
from modules.common.generator import generate_links, generate_oriented_set, generate_node, set_en_main_idtf
from modules.common.identifiers import ActionIdentifiers, CommonIdentifiers, QuestionStatus
from modules.common.utils import call_agent
from modules.tools import divide_content


class FileService:
    def __init__(self):
        self._keynodes = ScKeynodes()

    def upload(self, file_content: str, struct_name: str) -> bool:
        content_list = divide_content(file_content)
        links = generate_links(content_list)
        links_set = generate_oriented_set(links)

        structure = generate_node(sc_types.NODE_CONST_STRUCT)
        set_en_main_idtf(structure, struct_name)
        return call_agent(
            {links_set: False, structure: False},
            [
                ActionIdentifiers.ACTION_TRANSLATE_INPUT_RDF_MODEL_TO_RDF_SC.value,
                CommonIdentifiers.QUESTION.value,
            ],
            reaction=QuestionStatus.QUESTION_FINISHED_SUCCESSFULLY,
            wait_time=50
        )
