"""
    Author Zotov Nikita
"""
from __future__ import annotations

from typing import List, Dict

from json_client import client
from json_client.constants import sc_types
from json_client.dataclass import ScAddr, ScTemplate
from json_client.sc_keynodes import ScKeynodes
from modules.common.constants import ScAlias
from modules.common.generator import generate_node, set_en_main_idtf, generate_edge, generate_binary_relation
from modules.common.searcher import check_edge, get_element_by_main_idtf, get_en_main_idtf


class CRUDService:
    def __init__(self):
        self._keynodes = ScKeynodes()
        self._class_attributes: Dict[str, List[str]] = {}
        self._class_relations: Dict[str, List[str]] = {}

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

    def add_object_params(self, object_idtf: str, class_idtf: str, param_idtfs: Dict[str, str]) -> bool:
        object_addr = self._get_object(object_idtf)
        if not object_addr.is_valid():
            return False

        class_attributes = self._class_attributes.get(class_idtf)

        for class_idtf, param_idtf in param_idtfs.items():
            if class_idtf is not None and class_idtf not in class_attributes:
                continue

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

    def add_relation_between_objects(self, object_idtf: str, class_idtf: str, rel_subjects: Dict[str, str]) -> bool:
        object_addr = self._get_object(object_idtf)
        if not object_addr.is_valid():
            return False

        class_relations = self._class_relations.get(class_idtf)

        for relation_idtf, subject_idtf in rel_subjects.items():
            if class_relations is not None and relation_idtf not in class_relations:
                continue

            print(relation_idtf)
            print(subject_idtf)
            subject_addr = self._get_object(subject_idtf)
            if not subject_addr.is_valid():
                subject_addr = generate_node(sc_types.NODE_CONST)
                set_en_main_idtf(subject_addr, subject_idtf)

            relation_addr = self._get_object(relation_idtf)
            if not relation_addr.is_valid():
                relation_addr = generate_node(sc_types.NODE_CONST_NOROLE)
                set_en_main_idtf(relation_addr, relation_idtf)

            generate_binary_relation(object_addr, sc_types.EDGE_D_COMMON_CONST, subject_addr, relation_addr)
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

    def _get_object_addr_relations_pairs(self, object_addr: ScAddr) -> Dict[str, List[str]]:
        template = ScTemplate()
        template.triple_with_relation(
            object_addr,
            sc_types.EDGE_D_COMMON_VAR,
            [sc_types.UNKNOWN, ScAlias.NODE.value],
            sc_types.EDGE_ACCESS_VAR_POS_PERM,
            [sc_types.NODE_VAR_NOROLE, ScAlias.RELATION_NODE.value],
        )
        result = client.template_search(template)

        pairs = {}
        for item in result:
            relation_addr = item.get(ScAlias.RELATION_NODE.value)
            subject_addr = item.get(ScAlias.NODE.value)

            relation_idtf = get_en_main_idtf(relation_addr)
            subject_idtf = get_en_main_idtf(subject_addr)

            if relation_idtf and subject_idtf:
                subjects = pairs.get(relation_idtf)
                if subjects is None:
                    pairs.update({relation_idtf: [subject_idtf]})
                else:
                    subjects.append(subject_idtf)

        return pairs

    def get_objects(self, class_idtf: str) -> Dict[str, Dict[str, Dict[str, List[str] | str]]]:
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

            attributes = {}
            attributes.update({"params": self._get_object_addr_params(object_addr)})
            attributes.update({"relations": self._get_object_addr_relations_pairs(object_addr)})
            objects.update({object_idtf: attributes})

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

    def get_objects_relations(self, class_idtf: str) -> List[str]:
        relations_list = self._class_relations.get(class_idtf)
        if relations_list is not None:
            return relations_list

        relations_list = []
        self._class_relations.update({class_idtf: relations_list})

        class_addr = get_element_by_main_idtf(class_idtf)

        if not class_addr.is_valid():
            return []

        template = ScTemplate()
        template.triple(
            class_addr,
            sc_types.EDGE_ACCESS_VAR_POS_PERM,
            [sc_types.NODE_VAR, ScAlias.NODE.value],
        )
        template.triple_with_relation(
            ScAlias.NODE.value,
            sc_types.EDGE_D_COMMON_VAR,
            sc_types.UNKNOWN,
            sc_types.EDGE_ACCESS_VAR_POS_PERM,
            [sc_types.NODE_VAR_NOROLE, ScAlias.RELATION_NODE.value],
        )
        result = client.template_search(template)

        for item in result:
            relation_addr = item.get(ScAlias.RELATION_NODE.value)
            relation_idtf = get_en_main_idtf(relation_addr)
            if relation_idtf.endswith("identifier*"):
                continue

            if relation_idtf not in relations_list:
                relations_list.append(relation_idtf)

        return relations_list

    def update_objects_params_classes(self, class_idtf: str, params_classes: List[str]) -> None:
        self.get_objects_params_classes(class_idtf)

        params_list = self._class_attributes.get(class_idtf)
        if params_list is not None:
            params_list.extend(params_classes)

    def update_objects_relations(self, class_idtf: str, relations: List[str]) -> None:
        self.get_objects_relations(class_idtf)

        relations_list = self._class_relations.get(class_idtf)
        if relations_list is not None:
            relations_list.extend(relations)

    def get_sorted_objects(
            self, class_idtf: str, param_classes: List[str], relations: List[str]
    ) -> Dict[str, Dict[str, List[str]]]:
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

            attributes = {"params": sorted}

            relations_dict = self._get_object_addr_relations_pairs(object_addr)
            sorted = []
            for relation_idtf in relations:
                subjects = relations_dict.get(relation_idtf)

                if subjects is None:
                    sorted.append("")
                else:
                    subjects_str = ""
                    for subject_idtf in subjects:
                        if len(subjects_str) == 0:
                            subjects_str += subject_idtf
                        else:
                            subjects_str += ", " + subject_idtf
                    sorted.append(subjects_str)

            attributes.update({"subjects": sorted})
            objects.update({object_idtf: attributes})

        return objects

    def remove_object(self, object_idtf: str) -> bool:
        object_addr = get_element_by_main_idtf(object_idtf)

        if object_addr.is_valid():
            client.delete_elements([object_addr])
            return True

        return False
