"""
    Author Zotov Nikita
"""

from json_client.constants import sc_types
from json_client.dataclass import ScAddr, ScTemplate
from json_client.sc_keynodes import ScKeynodes
from modules.rdf_to_sc_translation_module.identifiers import TranslationIdentifiers
from modules.rdf_to_sc_translation_module.test.constants import TestScAlias

template_aliases = (
    TestScAlias.MAIN_NODE.value,
    TestScAlias.NOROLE_RELATION.value,
    TestScAlias.OBJECT.value,
    TestScAlias.OBJECT_LINK.value,
    TestScAlias.MAIN_NODE_IRI_LINK.value,
)


def correct_model_with_one_triple_result_construction(
    structure: ScAddr,
    object_is_literal: bool,
) -> ScTemplate:
    keynodes = ScKeynodes()
    templ = ScTemplate()

    templ.triple(structure, sc_types.EDGE_ACCESS_VAR_POS_PERM, [sc_types.NODE_VAR, TestScAlias.MAIN_NODE.value])
    templ.triple(structure, sc_types.EDGE_ACCESS_VAR_POS_PERM, [sc_types.NODE_VAR_NOROLE, TestScAlias.OBJECT.value])
    templ.triple(structure, sc_types.EDGE_ACCESS_VAR_POS_PERM, [sc_types.LINK_VAR, TestScAlias.OBJECT_LINK.value])
    templ.triple(
        structure, sc_types.EDGE_ACCESS_VAR_POS_PERM, [sc_types.LINK_VAR, TestScAlias.MAIN_NODE_IRI_LINK.value]
    )
    templ.triple(
        structure, sc_types.EDGE_ACCESS_VAR_POS_PERM, [sc_types.NODE_VAR_NOROLE, TestScAlias.NOROLE_RELATION.value]
    )

    templ.triple_with_relation(
        TestScAlias.MAIN_NODE.value,
        [sc_types.EDGE_D_COMMON_VAR, TestScAlias.MAIN_NODE_IRI_COMMON_ARC.value],
        TestScAlias.MAIN_NODE_IRI_LINK.value,
        [sc_types.EDGE_ACCESS_VAR_POS_PERM, TestScAlias.MAIN_NODE_IRI_ACCESS_ARC.value],
        keynodes[TranslationIdentifiers.NREL_IRI.value],
    )
    templ.triple(structure, sc_types.EDGE_ACCESS_VAR_POS_PERM, keynodes[TranslationIdentifiers.NREL_IRI.value])
    if object_is_literal:
        templ.triple_with_relation(
            TestScAlias.OBJECT.value,
            [sc_types.EDGE_D_COMMON_VAR, TestScAlias.OBJECT_CONTENT_OR_IRI_COMMON_ARC.value],
            TestScAlias.OBJECT_LINK.value,
            [sc_types.EDGE_ACCESS_VAR_POS_PERM, TestScAlias.OBJECT_CONTENT_OR_IRI_ACCESS_ARC.value],
            keynodes[TranslationIdentifiers.NREL_LITERAL_CONTENT.value],
        )
        templ.triple(
            structure,
            sc_types.EDGE_ACCESS_VAR_POS_PERM,
            keynodes[TranslationIdentifiers.NREL_LITERAL_CONTENT.value],
        )
    else:
        templ.triple_with_relation(
            TestScAlias.OBJECT.value,
            [sc_types.EDGE_D_COMMON_VAR, TestScAlias.OBJECT_CONTENT_OR_IRI_COMMON_ARC.value],
            TestScAlias.OBJECT_LINK.value,
            [sc_types.EDGE_ACCESS_VAR_POS_PERM, TestScAlias.OBJECT_CONTENT_OR_IRI_ACCESS_ARC.value],
            keynodes[TranslationIdentifiers.NREL_IRI.value],
        )

    templ.triple_with_relation(
        TestScAlias.MAIN_NODE.value,
        [sc_types.EDGE_D_COMMON_VAR, TestScAlias.NOROLE_RELATION_COMMON_ARC.value],
        TestScAlias.OBJECT.value,
        [sc_types.EDGE_ACCESS_VAR_POS_PERM, TestScAlias.NOROLE_RELATION_ACCESS_ARC.value],
        TestScAlias.NOROLE_RELATION.value,
    )

    templ.triple(structure, sc_types.EDGE_ACCESS_VAR_POS_PERM, TestScAlias.MAIN_NODE_IRI_COMMON_ARC.value)
    templ.triple(structure, sc_types.EDGE_ACCESS_VAR_POS_PERM, TestScAlias.MAIN_NODE_IRI_ACCESS_ARC.value)
    templ.triple(structure, sc_types.EDGE_ACCESS_VAR_POS_PERM, TestScAlias.OBJECT_CONTENT_OR_IRI_COMMON_ARC.value)
    templ.triple(structure, sc_types.EDGE_ACCESS_VAR_POS_PERM, TestScAlias.OBJECT_CONTENT_OR_IRI_ACCESS_ARC.value)
    templ.triple(structure, sc_types.EDGE_ACCESS_VAR_POS_PERM, TestScAlias.NOROLE_RELATION_COMMON_ARC.value)
    templ.triple(structure, sc_types.EDGE_ACCESS_VAR_POS_PERM, TestScAlias.NOROLE_RELATION_ACCESS_ARC.value)

    return templ
