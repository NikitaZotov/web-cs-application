"""
    Author Zotov Nikita
"""
from typing import Tuple

from json_client.constants import sc_types
from json_client.dataclass import ScAddr
from json_client.sc_keynodes import ScKeynodes
from modules.common.generator import generate_links, generate_oriented_set, generate_node, generate_edge
from modules.common.identifiers import ActionIdentifiers, CommonIdentifiers, QuestionStatus
from modules.common.searcher import get_content_from_links_set
from modules.common.utils import call_agent
from modules.tools import divide_content
from .rdf.identifiers import RdfIdentifiers


class FileService:
    def __init__(self):
        self._keynodes = ScKeynodes()

    def upload(self, file_content: str, name: str) -> Tuple[bool, int]:
        content_list = divide_content(file_content)
        links = generate_links(content_list)
        links_set = generate_oriented_set(links)

        structure = self._keynodes.__getitem__(name, sc_types.NODE_CONST_STRUCT)
        generate_edge(
            self._keynodes.__getitem__(RdfIdentifiers.OWL_ONTOLOGY.value, sc_types.NODE_CONST_CLASS),
            structure,
            sc_types.EDGE_ACCESS_CONST_POS_PERM
        )

        return call_agent(
            {links_set: False, structure: False},
            [
                ActionIdentifiers.ACTION_TRANSLATE_INPUT_RDF_MODEL_TO_RDF_SC.value,
                CommonIdentifiers.QUESTION.value,
            ],
            reaction=QuestionStatus.QUESTION_FINISHED_SUCCESSFULLY,
            wait_time=50
        ), structure.value

    def download(self, struct_id: int) -> Tuple[bool, str]:
        links_set = generate_node(sc_types.NODE_CONST)
        structure = ScAddr(struct_id)

        result = call_agent(
            {structure: False, links_set: False},
            [
                ActionIdentifiers.ACTION_TRANSLATE_RDF_SC_MODEL_TO_RDF.value,
                CommonIdentifiers.QUESTION.value
            ],
            reaction=QuestionStatus.QUESTION_FINISHED_SUCCESSFULLY,
            wait_time=50,
        )
        return result, get_content_from_links_set(links_set)
