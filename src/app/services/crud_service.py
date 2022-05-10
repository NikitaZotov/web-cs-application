"""
    Author Zotov Nikita
"""
from __future__ import annotations

from typing import List, Dict, Tuple

from json_client import client
from json_client.constants import sc_types
from json_client.dataclass import ScAddr, ScTemplate
from json_client.sc_keynodes import ScKeynodes
from modules.common.constants import ScAlias
from modules.common.generator import generate_node, set_en_main_idtf, generate_binary_relation_in_structure
from ..services.searcher import ModelSpecificationSearcher


class CRUDService:
    def __init__(self, searcher: ModelSpecificationSearcher):
        self._keynodes = ScKeynodes()
        self._attributes: Dict[str, List[str]] = {}
        self._object_properties: Dict[str, List[str]] = {}
        self._data_properties: Dict[str, List[str]] = {}

        self._searcher = searcher

    def add_object(self, object_idtf: str, struct_id: int, class_idtfs: List[str]) -> bool:
        struct_addr = ScAddr(struct_id)

        object_addr = self._searcher.get_object(object_idtf)
        if object_addr.is_valid():
            return False

        object_addr = generate_node(sc_types.NODE_CONST)
        set_en_main_idtf(object_addr, object_idtf)

        for class_idtf in class_idtfs:
            class_addr = self._searcher.resolve_object(class_idtf, sc_types.NODE_CONST_CLASS)
            self._searcher.add_element_class(object_addr, class_addr, struct_addr)

        return True

    def get_structure_classes(self, struct_id: int) -> Dict[str, int]:
        return self._searcher.get_classes_idtfs_and_powers(ScAddr(struct_id))

    def add_object_params(self, object_idtf: str, class_idtf: str, struct_id: int, param_idtfs: Dict[str, str]) -> bool:
        struct_addr = ScAddr(struct_id)

        object_addr = self._searcher.get_object(object_idtf)
        if not object_addr.is_valid():
            return False

        class_attributes = self._attributes.get(class_idtf)

        for class_idtf, param_idtf in param_idtfs.items():
            if class_idtf not in class_attributes:
                continue

            param_addr = self._searcher.resolve_object(param_idtf, sc_types.NODE_CONST_CLASS)
            self._searcher.add_element_class(object_addr, param_addr, struct_addr)

            class_addr = self._searcher.resolve_object(class_idtf, sc_types.NODE_CONST_CLASS)
            self._searcher.add_element_class(param_addr, class_addr, struct_addr)

        return True

    def add_object_object_properties(
            self, object_idtf: str, class_idtf: str, struct_id: int, rel_subjects: Dict[str, str]
    ) -> bool:
        struct_addr = ScAddr(struct_id)

        object_addr = self._searcher.get_object(object_idtf)
        if not object_addr.is_valid():
            return False

        class_relations = self._object_properties.get(class_idtf)

        for relation_idtf, subject_idtf in rel_subjects.items():
            if class_relations is not None and relation_idtf not in class_relations:
                continue

            relation_addr = self._searcher.resolve_object(relation_idtf, sc_types.NODE_CONST_NOROLE)
            subject_addr = self._searcher.resolve_object(subject_idtf, sc_types.NODE_CONST)

            generate_binary_relation_in_structure(object_addr, subject_addr, relation_addr, struct_addr)

        return True

    def add_object_data_properties(
            self, object_idtf: str, class_idtf: str, struct_id: int, rel_subjects: Dict[str, str]
    ) -> bool:
        struct_addr = ScAddr(struct_id)

        object_addr = self._searcher.get_object(object_idtf)
        if not object_addr.is_valid():
            return False

        class_relations = self._data_properties.get(class_idtf)

        for relation_idtf, subject_idtf in rel_subjects.items():
            if class_relations is not None and relation_idtf not in class_relations:
                continue

            relation_addr = self._searcher.resolve_object(relation_idtf, sc_types.NODE_CONST_NOROLE)
            subject_addr = self._searcher.generate_link(subject_idtf, struct_addr)

            generate_binary_relation_in_structure(object_addr, subject_addr, relation_addr, struct_addr)

        return True

    def update_object_params(self, object_idtf: str, struct_id: int, param_idtfs: Dict[str, str]) -> bool:
        struct_addr = ScAddr(struct_id)

        object_addr = self._searcher.get_object(object_idtf)
        if not object_addr.is_valid():
            return False

        for class_idtf, param_idtf in param_idtfs.items():
            if class_idtf not in self._attributes:
                continue

            if not param_idtf:
                continue

            param_addr = self._searcher.resolve_object(param_idtf, sc_types.NODE_CONST)
            class_addr = self._searcher.resolve_object(class_idtf, sc_types.NODE_CONST)

            self._searcher.remove_object_param_by_param_class(object_addr, class_addr)

            self._searcher.add_element_class(object_addr, param_addr, struct_addr)
            self._searcher.add_element_class(param_addr, class_addr, struct_addr)

        return True

    def update_object_object_properties(
            self, object_idtf: str, class_idtf: str, struct_id: int, relation_idtfs: Dict[str, str]
    ) -> bool:
        struct_addr = ScAddr(struct_id)

        object_addr = self._searcher.get_object(object_idtf)
        if not object_addr.is_valid():
            return False

        properties = self._object_properties.get(class_idtf)
        for relation_idtf, subject_idtf in relation_idtfs.items():
            if relation_idtf not in properties:
                continue

            if not subject_idtf:
                continue

            relation_addr = self._searcher.resolve_object(relation_idtf, sc_types.NODE_CONST_CLASS)
            subject_addr = self._searcher.resolve_object(subject_idtf, sc_types.NODE_CONST_CLASS)

            self._searcher.remove_object_subject_by_relation(object_addr, relation_addr)

            generate_binary_relation_in_structure(object_addr, subject_addr, relation_addr, struct_addr)

        return True

    def update_object_data_properties(
            self, object_idtf: str, class_idtf: str, struct_id: int, relation_idtfs: Dict[str, str]
    ) -> bool:
        struct_addr = ScAddr(struct_id)

        object_addr = self._searcher.get_object(object_idtf)
        if not object_addr.is_valid():
            return False

        properties = self._data_properties.get(class_idtf)
        for relation_idtf, subject_idtf in relation_idtfs.items():
            if relation_idtf not in properties:
                continue

            if not subject_idtf:
                continue

            relation_addr = self._searcher.resolve_object(relation_idtf, sc_types.NODE_CONST_CLASS)
            subject_addr = self._searcher.generate_link(subject_idtf, struct_addr)

            self._searcher.remove_object_subject_by_relation(object_addr, relation_addr)

            generate_binary_relation_in_structure(object_addr, subject_addr, relation_addr, struct_addr)

        return True

    def update_objects_params_classes(self, class_idtf: str, struct_id: int, params_classes: List[str]) -> None:
        self.get_objects_params_classes(class_idtf, struct_id)

        params_list = self._attributes.get(class_idtf)
        if params_list is not None:
            params_list.extend(params_classes)

    def update_objects_object_properties(self, class_idtf: str, struct_id: int, relations: List[str]) -> None:
        self.get_objects_properties(class_idtf, struct_id)

        relations_list = self._object_properties.get(class_idtf)
        if relations_list is not None:
            relations_list.extend(relations)

    def update_objects_data_properties(self, class_idtf: str, struct_id: int, relations: List[str]) -> None:
        self.get_objects_properties(class_idtf, struct_id)

        relations_list = self._data_properties.get(class_idtf)
        if relations_list is not None:
            relations_list.extend(relations)

    def get_object_params(self, object_idtf: str, struct_id: int) -> Dict[str, str]:
        object_addr = self._searcher.get_object(object_idtf)

        if not object_addr.is_valid():
            return {}

        return self._get_object_addr_params(object_addr, struct_id)

    def _get_object_addr_params(self, object_addr: ScAddr, struct_id: int) -> Dict[str, str]:
        template = ScTemplate()
        template.triple(
            [sc_types.NODE_VAR, ScAlias.ELEMENT.value],
            [sc_types.EDGE_ACCESS_VAR_POS_PERM, ScAlias.ACCESS_EDGE.value],
            object_addr
        )
        template.triple(
            [sc_types.NODE_VAR, ScAlias.NODE.value],
            sc_types.EDGE_ACCESS_VAR_POS_PERM,
            ScAlias.ELEMENT.value
        )
        template.triple(
            ScAddr(struct_id),
            sc_types.EDGE_ACCESS_VAR_POS_PERM,
            ScAlias.ACCESS_EDGE.value,
        )
        result = client.template_search(template)

        params = {}
        for item in result:
            class_addr = item.get(ScAlias.NODE.value)
            param_addr = item.get(ScAlias.ELEMENT.value)

            class_idtf = self._searcher.get_object_idtf(class_addr)
            param_idtf = self._searcher.get_object_idtf(param_addr)

            if class_idtf and param_idtf:
                params.update({class_idtf: param_idtf})

        return params

    def _get_object_addr_object_properties(self, object_addr: ScAddr, struct_id: int) -> Dict[str, List[str]]:
        result = self._searcher.get_object_object_properties(object_addr, ScAddr(struct_id))

        pairs = {}
        for item in result:
            relation_addr = item.get(ScAlias.RELATION_NODE.value)
            subject_addr = item.get(ScAlias.NODE.value)

            relation_idtf = self._searcher.get_object_idtf(relation_addr)
            subject_idtf = self._searcher.get_object_idtf(subject_addr)

            if relation_idtf:
                subjects = pairs.get(relation_idtf)

                if subject_idtf:
                    if subjects is None:
                        pairs.update({relation_idtf: [subject_idtf]})
                    else:
                        subjects.append(subject_idtf)

        return pairs

    def _get_object_addr_data_properties(self, object_addr: ScAddr, struct_id: int) -> Dict[str, List[str]]:
        result = self._searcher.get_object_object_properties(object_addr, ScAddr(struct_id))

        pairs = {}
        for item in result:
            relation_addr = item.get(ScAlias.RELATION_NODE.value)
            subject_addr = item.get(ScAlias.NODE.value)

            relation_idtf = self._searcher.get_object_idtf(relation_addr)

            if relation_idtf:
                subjects = pairs.get(relation_idtf)

                content = self._searcher.get_link_content(subject_addr)
                if content is not None and content:
                    if subjects is None:
                        pairs.update({relation_idtf: [str(content)]})
                    else:
                        subjects.append(str(content))

        return pairs

    def get_objects_params_classes(self, class_idtf: str, struct_id: int) -> List[str]:
        params_list = self._attributes.get(class_idtf)
        if params_list is not None:
            return params_list

        params = []
        self._attributes.update({class_idtf: params})

        class_addr = self._searcher.get_object(class_idtf)
        if not class_addr.is_valid():
            return []

        elements_result = self._searcher.get_class_elements(class_addr, ScAddr(struct_id))
        for element_item in elements_result:
            result = self._searcher.get_object_param_classes(element_item.get(ScAlias.NODE.value), ScAddr(struct_id))

            for item in result:
                class_addr = item.get(ScAlias.NODE.value)
                class_idtf = self._searcher.get_object_idtf(class_addr)

                if class_idtf not in params:
                    params.append(class_idtf)

        return params

    def get_objects_properties(self, class_idtf: str, struct_id: int) -> Tuple[List[str], List[str]]:
        struct_addr = ScAddr(struct_id)

        object_properties = self._object_properties.get(class_idtf)
        data_properties = self._data_properties.get(class_idtf)

        if object_properties is not None and data_properties is not None:
            return object_properties, data_properties

        object_properties = []
        self._object_properties.update({class_idtf: object_properties})

        data_properties = []
        self._data_properties.update({class_idtf: data_properties})

        class_addr = self._searcher.get_object(class_idtf)
        if not class_addr.is_valid():
            return [], []

        elements_result = self._searcher.get_class_elements(class_addr, ScAddr(struct_id))
        for element_item in elements_result:
            template = ScTemplate()
            template.triple_with_relation(
                element_item.get(ScAlias.NODE.value),
                sc_types.EDGE_D_COMMON_VAR,
                [sc_types.UNKNOWN, ScAlias.ELEMENT.value],
                [sc_types.EDGE_ACCESS_VAR_POS_PERM, ScAlias.ACCESS_EDGE.value],
                [sc_types.NODE_VAR_NOROLE, ScAlias.RELATION_NODE.value],
            )
            template.triple(
                struct_addr,
                sc_types.EDGE_ACCESS_VAR_POS_PERM,
                ScAlias.ACCESS_EDGE.value,
            )
            result = client.template_search(template)

            for item in result:
                relation_addr = item.get(ScAlias.RELATION_NODE.value)
                relation_idtf = self._searcher.get_object_idtf(relation_addr)

                if self._searcher.is_data_property(relation_addr, struct_addr):
                    if relation_idtf not in data_properties:
                        data_properties.append(relation_idtf)
                elif relation_idtf not in object_properties:
                    object_properties.append(relation_idtf)

        return object_properties, data_properties

    def get_sorted_objects(
            self,
            class_idtf: str,
            struct_id: int,
            param_classes: List[str],
            object_properties: List[str],
            data_properties: List[str],
    ) -> Dict[str, Dict[str, List[str]]]:
        class_addr = self._searcher.get_object(class_idtf)

        if not class_addr.is_valid():
            return {}

        result = self._searcher.get_class_elements(class_addr, ScAddr(struct_id))

        objects = {}
        for item in result:
            object_addr = item.get(ScAlias.NODE.value)
            object_idtf = self._searcher.get_object_idtf(object_addr)

            params_dict = self._get_object_addr_params(object_addr, struct_id)
            sorted_list = []
            self._add_params_to_list(param_classes, params_dict, sorted_list)
            attributes = {"params": sorted_list}

            sorted_list = []
            relations_dict = self._get_object_addr_object_properties(object_addr, struct_id)
            self._add_properties_to_list(object_properties, relations_dict, sorted_list)

            relations_dict = self._get_object_addr_data_properties(object_addr, struct_id)
            self._add_properties_to_list(data_properties, relations_dict, sorted_list)

            attributes.update({"subjects": sorted_list})
            objects.update({object_idtf: attributes})

        return objects

    def _add_params_to_list(
            self, param_classes: List[str], params_dict: Dict[str, str], sorted_list: List[str]
    ) -> None:
        for class_idtf in param_classes:
            param_idtf = params_dict.get(class_idtf)

            if param_idtf is None:
                sorted_list.append("")
            else:
                sorted_list.append(param_idtf)

    def _add_properties_to_list(
            self, relations: List[str], relations_dict: Dict[str, List[str]], sorted_list: List[str]
    ) -> None:
        for relation_idtf in relations:
            subjects = relations_dict.get(relation_idtf)

            if subjects is None:
                sorted_list.append("")
            else:
                subjects_str = ""
                for subject_idtf in subjects:
                    if len(subjects_str) == 0:
                        subjects_str += subject_idtf
                    else:
                        subjects_str += ", " + subject_idtf
                sorted_list.append(subjects_str)

    def remove_object(self, object_idtf: str) -> bool:
        object_addr = self._searcher.get_object(object_idtf)

        if object_addr.is_valid():
            client.delete_elements([object_addr])
            return True

        return False

    def get_structure_idtf(self, struct_id: int) -> str:
        return self._searcher.get_object_idtf(ScAddr(struct_id))

    def get_structures(self) -> Dict[int, str]:
        return self._searcher.get_ontologies()
