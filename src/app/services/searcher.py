"""
    Author Zotov Nikita
"""
from typing import Dict, List

from json_client.dataclass import ScAddr, ScTemplateResult


class ModelSpecificationSearcher:
    def get_object(self, object_idtf: str) -> ScAddr:
        raise NotImplementedError

    def get_object_idtf(self, object_addr: ScAddr) -> str:
        raise NotImplementedError

    def get_classes_idtfs_and_powers(self, struct_addr: ScAddr) -> Dict[str, int]:
        raise NotImplementedError

    def get_class_elements(self, class_addr: ScAddr, struct_addr: ScAddr) -> List[ScTemplateResult]:
        raise NotImplementedError

    def get_link_content(self, object_addr: ScAddr) -> str:
        raise NotImplementedError
