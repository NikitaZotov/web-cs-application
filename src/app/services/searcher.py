"""
    Author Zotov Nikita
"""
from typing import Dict, List

from json_client.constants.sc_types import ScType
from json_client.dataclass import ScAddr, ScTemplateResult


class ModelSpecificationSearcher:
    def get_object(self, object_idtf: str) -> ScAddr:
        raise NotImplementedError

    def get_object_idtf(self, object_addr: ScAddr) -> str:
        raise NotImplementedError

    def resolve_object(self, object_idtf: str, object_type: ScType) -> ScAddr:
        raise NotImplementedError

    def get_classes_idtfs_and_powers(self, struct_addr: ScAddr) -> Dict[str, int]:
        raise NotImplementedError

    def get_class_elements(self, class_addr: ScAddr, struct_addr: ScAddr) -> List[ScTemplateResult]:
        raise NotImplementedError

    def add_element_class(self, object_addr: ScAddr, class_addr: ScAddr, struct_addr: ScAddr) -> bool:
        raise NotImplementedError

    def remove_object_param_by_param_class(self, object_addr: ScAddr, class_addr: ScAddr) -> None:
        raise NotImplementedError

    def remove_object_subject_by_relation(self, object_addr: ScAddr, relation_addr: ScAddr) -> None:
        raise NotImplementedError

    def get_object_param_classes(self, object_addr: ScAddr, struct_addr: ScAddr) -> List[ScTemplateResult]:
        raise NotImplementedError

    def get_object_object_properties(self, object_addr: ScAddr, struct_addr: ScAddr) -> List[ScTemplateResult]:
        raise NotImplementedError

    def get_object_data_properties(self, object_addr: ScAddr, struct_addr: ScAddr) -> List[ScTemplateResult]:
        raise NotImplementedError

    def is_data_property(self, relation_addr: ScAddr, struct_addr: ScAddr) -> bool:
        raise NotImplementedError

    def get_link_content(self, object_addr: ScAddr) -> str:
        raise NotImplementedError

    def generate_link(self, content: str, struct_addr: ScAddr) -> ScAddr:
        raise NotImplementedError

    def get_ontologies(self) -> Dict[int, str]:
        raise NotImplementedError
