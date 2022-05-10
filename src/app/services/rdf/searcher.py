"""
    Author Zotov Nikita
"""
from typing import Dict, List

from json_client import client
from json_client.constants import sc_types
from json_client.constants.sc_types import ScType
from json_client.dataclass import ScAddr, ScTemplate, ScTemplateResult
from json_client.sc_keynodes import ScKeynodes
from modules.common.constants import ScAlias
from modules.common.generator import set_en_main_idtf, wrap_in_set, generate_edge, generate_node, generate_link
from modules.common.searcher import get_element_by_main_idtf, get_element_by_system_idtf, get_en_main_idtf, \
    get_system_idtf, get_link_content
from modules.rdf_searcher.searcher import RdfConstructionsSearcher
from ...services.rdf.identifiers import RdfIdentifiers
from ...services.searcher import ModelSpecificationSearcher


class RdfModelSpecificationSearcher(ModelSpecificationSearcher):
    def __init__(self):
        self._keynodes = ScKeynodes()
        self._searcher = RdfConstructionsSearcher()

    def get_object(self, object_idtf: str) -> ScAddr:
        object_addr = get_element_by_main_idtf(object_idtf)

        if object_addr.is_valid():
            return object_addr

        object_addr = get_element_by_system_idtf(object_idtf)
        if object_addr.is_valid():
            return object_addr

        links_list = client.get_link_by_content([object_idtf])[0]
        if len(links_list) != 0:
            link = links_list[0]

            template = ScTemplate()
            template.triple_with_relation(
                [sc_types.NODE_VAR, ScAlias.NODE.value],
                sc_types.EDGE_D_COMMON_VAR,
                link,
                sc_types.EDGE_ACCESS_VAR_POS_PERM,
                self._keynodes[RdfIdentifiers.NREL_IRI.value],
            )
            result = client.template_search(template)
            if len(result) != 0:
                return result[0].get(ScAlias.NODE.value)

        return ScAddr(0)

    def get_object_idtf(self, object_addr: ScAddr) -> str:
        object_idtf = get_en_main_idtf(object_addr)
        if object_idtf:
            return object_idtf

        object_idtf = get_system_idtf(object_addr)
        if object_idtf:
            return object_idtf

        iri_str = self._searcher.get_element_iri_str(object_addr)

        if not iri_str:
            return iri_str

        idtfs = iri_str.split("#")

        if len(idtfs) != 0:
            idtf = idtfs[1].replace("_", " ")
            set_en_main_idtf(object_addr, idtf)
            return idtf

        return iri_str

    def resolve_object(self, object_idtf: str, object_type: ScType) -> ScAddr:
        object_addr = self.get_object(object_idtf)
        if not object_addr.is_valid():
            object_addr = generate_node(object_type)
            set_en_main_idtf(object_addr, object_idtf)

        return object_addr

    def get_classes_idtfs_and_powers(self, struct_addr: ScAddr) -> Dict[str, int]:
        template = ScTemplate()
        template.triple(
            self._keynodes[RdfIdentifiers.RDF_NREL_TYPE.value],
            sc_types.EDGE_ACCESS_VAR_POS_PERM,
            [sc_types.EDGE_D_COMMON_VAR, ScAlias.COMMON_EDGE.value],
        )
        template.triple(
            [sc_types.NODE_VAR, ScAlias.NODE.value],
            ScAlias.COMMON_EDGE.value,
            self._keynodes[RdfIdentifiers.OWL_CLASS.value],
        )
        template.triple(
            struct_addr,
            sc_types.EDGE_ACCESS_VAR_POS_PERM,
            ScAlias.COMMON_EDGE.value,
        )
        result = client.template_search(template)

        class_list = {}
        for item in result:
            class_addr = item.get(ScAlias.NODE.value)
            class_idtf = self.get_object_idtf(class_addr)

            if class_idtf:
                class_list.update({class_idtf: self._get_class_power(class_addr, struct_addr)})

            self._visit_subclasses(class_addr, struct_addr, class_list)

        return class_list

    def _visit_subclasses(self, class_addr: ScAddr, struct_addr: ScAddr, class_list: Dict[str, int]) -> None:
        template = ScTemplate()
        template.triple_with_relation(
            class_addr,
            sc_types.EDGE_D_COMMON_VAR,
            [sc_types.NODE_VAR, ScAlias.NODE.value],
            sc_types.EDGE_ACCESS_VAR_POS_PERM,
            self._keynodes[RdfIdentifiers.RDF_SUBCLASS_OF.value],
        )
        result = client.template_search(template)

        for item in result:
            subclass_addr = item.get(ScAlias.NODE.value)

            subclass_idtf = self.get_object_idtf(subclass_addr)
            if subclass_idtf and subclass_idtf not in class_list:
                class_list.update({subclass_idtf: self._get_class_power(subclass_addr, struct_addr)})

            self._visit_subclasses(subclass_addr, struct_addr, class_list)

    def _get_class_power(self, class_addr: ScAddr, struct_addr: ScAddr) -> int:
        return len(self.get_class_elements(class_addr, struct_addr))

    def get_class_elements(self, class_addr: ScAddr, struct_addr: ScAddr) -> List[ScTemplateResult]:
        template = ScTemplate()
        template.triple_with_relation(
            [sc_types.NODE_VAR, ScAlias.NODE.value],
            sc_types.EDGE_D_COMMON_VAR,
            class_addr,
            sc_types.EDGE_ACCESS_VAR_POS_PERM,
            self._keynodes[RdfIdentifiers.RDF_NREL_TYPE.value],
        )
        return client.template_search(template)

    def add_element_class(self, object_addr: ScAddr, class_addr: ScAddr, struct_addr: ScAddr) -> bool:
        template = ScTemplate()
        template.triple_with_relation(
            object_addr,
            sc_types.EDGE_D_COMMON_VAR,
            class_addr,
            sc_types.EDGE_ACCESS_VAR_POS_PERM,
            self._keynodes[RdfIdentifiers.RDF_NREL_TYPE.value],
        )
        if len(client.template_search(template)) == 0:
            common_edge = generate_edge(object_addr, class_addr, sc_types.EDGE_D_COMMON_CONST)
            edge = generate_edge(
                self._keynodes[RdfIdentifiers.RDF_NREL_TYPE.value], common_edge, sc_types.EDGE_ACCESS_CONST_POS_PERM
            )

            wrap_in_set([object_addr, common_edge, edge], struct_addr)
            return True

        return False

    def remove_object_param_by_param_class(self, object_addr: ScAddr, class_addr: ScAddr) -> None:
        template = ScTemplate()
        template.triple_with_relation(
            object_addr,
            [sc_types.EDGE_D_COMMON_VAR, ScAlias.ACCESS_EDGE.value],
            [sc_types.NODE_VAR, ScAlias.NODE.value],
            sc_types.EDGE_ACCESS_VAR_POS_PERM,
            self._keynodes[RdfIdentifiers.RDF_NREL_TYPE.value],
        )
        template.triple_with_relation(
            ScAlias.NODE.value,
            sc_types.EDGE_D_COMMON_VAR,
            class_addr,
            sc_types.EDGE_ACCESS_VAR_POS_PERM,
            self._keynodes[RdfIdentifiers.RDF_NREL_TYPE.value],
        )
        result = client.template_search(template)
        if len(result) != 0:
            client.delete_elements([result[0].get(ScAlias.ACCESS_EDGE.value)])

    def remove_object_subject_by_relation(self, object_addr: ScAddr, relation_addr: ScAddr) -> None:
        template = ScTemplate()
        template.triple_with_relation(
            object_addr,
            [sc_types.EDGE_D_COMMON_VAR, ScAlias.ACCESS_EDGE.value],
            [sc_types.NODE_VAR, ScAlias.NODE.value],
            sc_types.EDGE_ACCESS_VAR_POS_PERM,
            relation_addr,
        )
        result = client.template_search(template)
        for item in result:
            client.delete_elements([item.get(ScAlias.ACCESS_EDGE.value)])

    def get_object_param_classes(self, object_addr: ScAddr, struct_addr: ScAddr) -> List[ScTemplateResult]:
        template = ScTemplate()
        template.triple_with_relation(
            object_addr,
            [sc_types.EDGE_D_COMMON_VAR, ScAlias.ACCESS_EDGE.value],
            [sc_types.NODE_VAR, ScAlias.ELEMENT.value],
            sc_types.EDGE_ACCESS_VAR_POS_PERM,
            self._keynodes[RdfIdentifiers.RDF_NREL_TYPE.value],
        )
        template.triple_with_relation(
            ScAlias.ELEMENT.value,
            sc_types.EDGE_D_COMMON_VAR,
            [sc_types.NODE_VAR, ScAlias.NODE.value],
            sc_types.EDGE_ACCESS_VAR_POS_PERM,
            self._keynodes[RdfIdentifiers.RDF_NREL_TYPE.value],
        )
        template.triple(
            struct_addr,
            sc_types.EDGE_ACCESS_VAR_POS_PERM,
            ScAlias.ACCESS_EDGE.value
        )
        return client.template_search(template)

    def get_object_object_properties(self, object_addr: ScAddr, struct_addr: ScAddr) -> List[ScTemplateResult]:
        template = ScTemplate()
        template.triple_with_relation(
            object_addr,
            sc_types.EDGE_D_COMMON_VAR,
            [sc_types.UNKNOWN, ScAlias.NODE.value],
            [sc_types.EDGE_ACCESS_VAR_POS_PERM, ScAlias.ACCESS_EDGE.value],
            [sc_types.NODE_VAR_NOROLE, ScAlias.RELATION_NODE.value],
        )
        template.triple(
            struct_addr,
            sc_types.EDGE_ACCESS_VAR_POS_PERM,
            ScAlias.ACCESS_EDGE.value,
        )
        return client.template_search(template)

    def get_object_data_properties(self, object_addr: ScAddr, struct_addr: ScAddr) -> List[ScTemplateResult]:
        template = ScTemplate()
        template.triple_with_relation(
            object_addr,
            sc_types.EDGE_D_COMMON_VAR,
            [sc_types.UNKNOWN, ScAlias.ELEMENT.value],
            [sc_types.EDGE_ACCESS_VAR_POS_PERM, ScAlias.ACCESS_EDGE.value],
            [sc_types.NODE_VAR_NOROLE, ScAlias.RELATION_NODE.value],
        )
        template.triple_with_relation(
            ScAlias.ELEMENT.value,
            sc_types.EDGE_D_COMMON_VAR,
            [sc_types.LINK_VAR, ScAlias.NODE.value],
            sc_types.EDGE_ACCESS_VAR_POS_PERM,
            self._keynodes[RdfIdentifiers.NREL_LITERAL_CONTENT.value],
        )
        template.triple(
            struct_addr,
            sc_types.EDGE_ACCESS_VAR_POS_PERM,
            ScAlias.ACCESS_EDGE.value,
        )
        return client.template_search(template)

    def is_data_property(self, relation_addr: ScAddr, struct_addr: ScAddr) -> bool:
        template = ScTemplate()
        template.triple_with_relation(
            sc_types.NODE_VAR,
            sc_types.EDGE_D_COMMON_VAR,
            [sc_types.UNKNOWN, ScAlias.ELEMENT.value],
            [sc_types.EDGE_ACCESS_VAR_POS_PERM, ScAlias.ACCESS_EDGE.value],
            relation_addr,
        )
        template.triple_with_relation(
            ScAlias.ELEMENT.value,
            sc_types.EDGE_D_COMMON_VAR,
            [sc_types.LINK_VAR, ScAlias.NODE.value],
            sc_types.EDGE_ACCESS_VAR_POS_PERM,
            self._keynodes[RdfIdentifiers.NREL_LITERAL_CONTENT.value],
        )
        template.triple(
            struct_addr,
            sc_types.EDGE_ACCESS_VAR_POS_PERM,
            ScAlias.ACCESS_EDGE.value,
        )
        return len(client.template_search(template)) != 0

    def get_link_content(self, object_addr: ScAddr) -> str:
        template = ScTemplate()
        template.triple_with_relation(
            object_addr,
            sc_types.EDGE_D_COMMON_VAR,
            [sc_types.LINK_VAR, ScAlias.NODE.value],
            sc_types.EDGE_ACCESS_VAR_POS_PERM,
            self._keynodes[RdfIdentifiers.NREL_LITERAL_CONTENT.value],
        )
        result = client.template_search(template)

        if len(result) != 0:
            return get_link_content(result[0].get(ScAlias.NODE.value))

        return ""

    def generate_link(self, content: str, struct_addr: ScAddr) -> ScAddr:
        source = generate_node(sc_types.NODE_CONST)
        link = generate_link(content)

        common_edge = generate_edge(source, link, sc_types.EDGE_D_COMMON_CONST)
        edge = generate_edge(
            self._keynodes[RdfIdentifiers.NREL_LITERAL_CONTENT.value], common_edge, sc_types.EDGE_ACCESS_CONST_POS_PERM
        )
        wrap_in_set([source, link, common_edge, edge], struct_addr)

        return source

    def get_ontologies(self) -> Dict[int, str]:
        template = ScTemplate()
        template.triple(
            self._keynodes[RdfIdentifiers.OWL_ONTOLOGY.value],
            sc_types.EDGE_ACCESS_VAR_POS_PERM,
            [sc_types.UNKNOWN, ScAlias.NODE.value],
        )
        result = client.template_search(template)

        ontologies = {}
        for item in result:
            ontology_addr = item.get(ScAlias.NODE.value)
            ontologies.update({ontology_addr.value: self.get_object_idtf(ontology_addr)})

        return ontologies
