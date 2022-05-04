"""
    Author Zotov Nikita
"""

from typing import List, Dict

from common.constants import ScAlias
from common.generator import generate_node, set_en_main_idtf, generate_edge
from common.searcher import get_element_by_main_idtf, check_edge, get_en_main_idtf
from json_client import client
from json_client.constants import sc_types
from json_client.dataclass import ScAddr, ScTemplate
from json_client.sc_keynodes import ScKeynodes


class CRUDService:
    def __init__(self):
        self._keynodes = ScKeynodes()
        self._class_attributes: Dict[str, List[str]] = {}

    def add_object(self, object_idtf: str, class_idtfs: List[str]) -> bool:
        object_addr = self._get_object(object_idtf)
        if object_addr.is_valid():
            return False

        object_addr = generate_node(sc_types.NODE_CONST)
        set_en_main_idtf(object_addr, object_idtf)

        for class_idtf in class_idtfs:
            class_addr = self._get_object(class_idtf)
            if not class_addr.is_valid():
                class_addr = generate_node(sc_types.NODE_CONST_CLASS)
                set_en_main_idtf(class_addr, class_idtf)

            if not check_edge(class_addr, object_addr, sc_types.EDGE_ACCESS_VAR_POS_PERM):
                generate_edge(class_addr, object_addr, sc_types.EDGE_ACCESS_CONST_POS_PERM)

        return True

    def _get_object(self, object_idtf: str) -> ScAddr:
        return get_element_by_main_idtf(object_idtf)

    def add_object_params(self, object_idtf: str, param_idtfs: Dict[str, str]) -> bool:
        object_addr = self._get_object(object_idtf)
        if not object_addr.is_valid():
            return False

        for class_idtf, param_idtf in param_idtfs.items():
            if class_idtf.endswith('name'):
                continue

            param_addr = self._get_object(param_idtf)
            if not param_addr.is_valid():
                param_addr = generate_node(sc_types.NODE_CONST_CLASS)
                set_en_main_idtf(param_addr, param_idtf)

            if not check_edge(param_addr, object_addr, sc_types.EDGE_ACCESS_VAR_POS_PERM):
                generate_edge(param_addr, object_addr, sc_types.EDGE_ACCESS_CONST_POS_PERM)

            class_addr = self._get_object(class_idtf)
            if not class_addr.is_valid():
                class_addr = generate_node(sc_types.NODE_CONST_CLASS)
                set_en_main_idtf(class_addr, class_idtf)

            if not check_edge(class_addr, param_addr, sc_types.EDGE_ACCESS_VAR_POS_PERM):
                generate_edge(class_addr, param_addr, sc_types.EDGE_ACCESS_CONST_POS_PERM)

        return True

    def update_object_params(self, object_idtf: str, param_idtfs: Dict[str, str]) -> bool:
        object_addr = self._get_object(object_idtf)
        if not object_addr.is_valid():
            return False

        for class_idtf, param_idtf in param_idtfs.items():
            if class_idtf.endswith('name'):
                continue

            param_addr = self._get_object(param_idtf)
            if not param_addr.is_valid():
                param_addr = generate_node(sc_types.NODE_CONST_CLASS)
                set_en_main_idtf(param_addr, param_idtf)

            class_addr = self._get_object(class_idtf)
            if not class_addr.is_valid():
                class_addr = generate_node(sc_types.NODE_CONST_CLASS)
                set_en_main_idtf(class_addr, class_idtf)

            self.remove_object_param_by_param_class(object_addr, class_addr)

            if not check_edge(param_addr, object_addr, sc_types.EDGE_ACCESS_VAR_POS_PERM):
                generate_edge(param_addr, object_addr, sc_types.EDGE_ACCESS_CONST_POS_PERM)

            if not check_edge(class_addr, param_addr, sc_types.EDGE_ACCESS_VAR_POS_PERM):
                generate_edge(class_addr, param_addr, sc_types.EDGE_ACCESS_CONST_POS_PERM)

    def remove_object_param_by_param_class(self, object_addr: ScAddr, class_addr: ScAddr) -> None:
        template = ScTemplate()
        template.triple(
            [sc_types.NODE_VAR_CLASS, ScAlias.NODE.value],
            [sc_types.EDGE_ACCESS_VAR_POS_PERM, ScAlias.ACCESS_EDGE.value],
            object_addr
        )
        template.triple(
            class_addr,
            sc_types.EDGE_ACCESS_VAR_POS_PERM,
            ScAlias.NODE.value
        )
        result = client.template_search(template)
        if len(result) != 0:
            client.delete_elements([result[0].get(ScAlias.ACCESS_EDGE.value)])

    def get_object_params(self, object_idtf: str) -> Dict[str, str]:
        object_addr = self._get_object(object_idtf)

        if not object_addr.is_valid():
            return {}

        return self._get_object_addr_params(object_addr)

    def _get_object_addr_params(self, object_addr: ScAddr) -> Dict[str, str]:
        template = ScTemplate()
        template.triple(
            [sc_types.NODE_VAR, ScAlias.ELEMENT.value],
            sc_types.EDGE_ACCESS_VAR_POS_PERM,
            object_addr
        )
        template.triple(
            [sc_types.NODE_VAR, ScAlias.NODE.value],
            sc_types.EDGE_ACCESS_VAR_POS_PERM,
            ScAlias.ELEMENT.value
        )
        result = client.template_search(template)

        params = {}
        for item in result:
            class_addr = item.get(ScAlias.NODE.value)
            param_addr = item.get(ScAlias.ELEMENT.value)

            class_idtf = get_en_main_idtf(class_addr)
            param_idtf = get_en_main_idtf(param_addr)

            if class_idtf and param_idtf:
                params.update({class_idtf: param_idtf})

        return params

    def get_objects(self, class_idtf: str) -> Dict[str, Dict[str, str]]:
        class_addr = get_element_by_main_idtf(class_idtf)

        if not class_addr.is_valid():
            return {}

        template = ScTemplate()
        template.triple(
            class_addr,
            sc_types.EDGE_ACCESS_VAR_POS_PERM,
            [sc_types.NODE_VAR, ScAlias.NODE.value]
        )
        result = client.template_search(template)

        objects = {}
        for item in result:
            object_addr = item.get(ScAlias.NODE.value)
            object_idtf = get_en_main_idtf(object_addr)

            objects.update({object_idtf: self._get_object_addr_params(object_addr)})

        return objects

    def get_objects_params_classes(self, class_idtf: str) -> List[str]:
        params_list = self._class_attributes.get(class_idtf)
        if params_list is not None:
            return params_list

        params = []
        self._class_attributes.update({class_idtf: params})

        class_addr = get_element_by_main_idtf(class_idtf)

        if not class_addr.is_valid():
            return []

        PARAM_CLASS = "_class"
        template = ScTemplate()
        template.triple(
            class_addr,
            sc_types.EDGE_ACCESS_VAR_POS_PERM,
            [sc_types.NODE_VAR, ScAlias.NODE.value]
        )
        template.triple(
            [sc_types.NODE_VAR_CLASS, ScAlias.ELEMENT.value],
            sc_types.EDGE_ACCESS_VAR_POS_PERM,
            ScAlias.NODE.value
        )
        template.triple(
            [sc_types.NODE_VAR_CLASS, PARAM_CLASS],
            sc_types.EDGE_ACCESS_VAR_POS_PERM,
            ScAlias.ELEMENT.value
        )
        result = client.template_search(template)

        for item in result:
            class_addr = item.get(PARAM_CLASS)
            class_idtf = get_en_main_idtf(class_addr)

            if class_idtf not in params:
                params.append(class_idtf)

        return params

    def update_objects_params_classes(self, class_idtf: str, params_classes: List[str]) -> None:
        self.get_objects_params_classes(class_idtf)

        params_list = self._class_attributes.get(class_idtf)
        if params_list is not None:
            params_list.extend(params_classes)

    def get_objects_with_sorted_params(self, class_idtf: str, param_classes: List[str]) -> Dict[str, List[str]]:
        class_addr = get_element_by_main_idtf(class_idtf)

        if not class_addr.is_valid():
            return {}

        template = ScTemplate()
        template.triple(
            class_addr,
            sc_types.EDGE_ACCESS_VAR_POS_PERM,
            [sc_types.NODE_VAR, ScAlias.NODE.value]
        )
        result = client.template_search(template)

        objects = {}
        for item in result:
            object_addr = item.get(ScAlias.NODE.value)
            object_idtf = get_en_main_idtf(object_addr)

            params_dict = self._get_object_addr_params(object_addr)
            sorted = []
            for class_idtf in param_classes:
                param_idtf = params_dict.get(class_idtf)

                if param_idtf is None:
                    sorted.append("")
                else:
                    sorted.append(param_idtf)

            objects.update({object_idtf: sorted})

        return objects

    def remove_object(self, object_idtf: str) -> bool:
        object_addr = get_element_by_main_idtf(object_idtf)

        if object_addr.is_valid():
            client.delete_elements([object_addr])
            return True

        return False
