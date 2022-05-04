"""
    Author Zotov Nikita
"""

from modules.rdf_to_sc_translation_module.identifiers import TranslationIdentifiers


class Data:
    @staticmethod
    def first_test_elements_to_upload():
        return [
            (
                TranslationIdentifiers.NREL_IRI.value,
                ("object", "http://datafabric.cc/data/ya#_66a0fb6a-2a69-4825-beb9-8b0a86b6bd25"),
            ),
            (
                "cim_nrel_Equipment_normallyInService",
                ("object", "literal_object"),
            ),
            (
                TranslationIdentifiers.NREL_LITERAL_CONTENT.value,
                ("literal_object", "false"),
            ),
            (
                "rdf_nrel_type",
                ("object", "owl_NamedIndividual"),
            ),
            (
                TranslationIdentifiers.NREL_IRI.value,
                (
                    "owl_NamedIndividual",
                    "http://datafabric.cc/data/ya#_ec11e78d-fc77-44ba-8463-cf35152b7764-owl#NamedIndividual",
                ),
            ),
            (
                "rdf_nrel_type",
                ("object", "cim_ACLineSegment"),
            ),
            (
                TranslationIdentifiers.NREL_IRI.value,
                (
                    "cim_ACLineSegment",
                    "http://datafabric.cc/data/ya#_218c5f60-ad0b-4506-919b-f2397a7b003e-cim16#ACLineSegment",
                ),
            ),
            (
                TranslationIdentifiers.NREL_IRI.value,
                (
                    "cim_nrel_Equipment_normallyInService",
                    "http://datafabric.cc/data/ya#_05b17488-49aa-8c7d-81afa4c788e8-cim16#Equipment_normallyInService",
                ),
            ),
            (
                TranslationIdentifiers.NREL_IRI.value,
                ("rdf_nrel_type", "http://www.w3.org/1999/02/22-rdf-syntax-ns#type"),
            ),
        ]

    @staticmethod
    def second_test_elements_to_upload():
        return [
            (
                TranslationIdentifiers.NREL_IRI.value,
                ("second_object", "http://datafabric.cc/data/ya#_dfe91283-caa7-4650-8c7f-e8391e323419"),
            ),
            (
                "cim_nrel_Equipment_normallyInService",
                ("second_object", "literal_second_object"),
            ),
            (
                TranslationIdentifiers.NREL_LITERAL_CONTENT.value,
                ("literal_second_object", "true"),
            ),
            (
                "cim_nrel_SubGeographicalRegion_Substations",
                ("second_object", "cim_substation_1"),
            ),
            (
                TranslationIdentifiers.NREL_IRI.value,
                ("cim_substation_1", "http://datafabric.cc/data/ya#_9a3f214c-efc3-4769-87a6-63f5854b6590"),
            ),
            (
                "cim_nrel_SubGeographicalRegion_Substations",
                ("second_object", "cim_substation_2"),
            ),
            (
                TranslationIdentifiers.NREL_IRI.value,
                ("cim_substation_2", "http://datafabric.cc/data/ya#_a67bb42f-2ce3-4794-8107-94ccfab696e3"),
            ),
            (
                "cim_nrel_SubGeographicalRegion_Substations",
                ("second_object", "cim_substation_3"),
            ),
            (
                TranslationIdentifiers.NREL_IRI.value,
                ("cim_substation_3", "http://datafabric.cc/data/ya#_ae5f5cbb-7169-4145-a4b7-978d9e5b2db4"),
            ),
            (
                "cim_nrel_SubGeographicalRegion_Substations",
                ("second_object", "cim_substation_4"),
            ),
            (
                TranslationIdentifiers.NREL_IRI.value,
                ("cim_substation_4", "http://datafabric.cc/data/ya#_bdd00090-7338-44a1-9962-6fdba3dedd82"),
            ),
            (
                TranslationIdentifiers.NREL_IRI.value,
                (
                    "cim_nrel_SubGeographicalRegion_Substations",
                    "http://datafabric.cc/data/ya#_bd338-44a1-9962-6fdba3dedd82-cim#SubGeographicalRegion.Substations",
                ),
            ),
        ]

    @staticmethod
    def third_test_elements_to_upload():
        return [
            (
                TranslationIdentifiers.NREL_IRI.value,
                ("third_object", "http://datafabric.cc/data/ya#_bf2d6f1a-2017-4f5b-b1d0-48b3248be06a"),
            ),
            (
                "cim_nrel_ConductingEquipment_BaseVoltage",
                ("third_object", "base_voltage"),
            ),
            (
                TranslationIdentifiers.NREL_IRI.value,
                ("base_voltage", "http://datafabric.cc/data/ya#000-0000006d746c"),
            ),
            (
                TranslationIdentifiers.NREL_IRI.value,
                (
                    "cim_nrel_ConductingEquipment_BaseVoltage",
                    "http://datafabric.cc/data/ya#000-asdadsadsasd0000006d746c-cim16#ConductingEquipment.BaseVoltage",
                ),
            ),
            (
                "cim_nrel_ConductingEquipment_Terminals",
                ("third_object", "cim_terminal_1"),
            ),
            (
                TranslationIdentifiers.NREL_IRI.value,
                ("cim_terminal_1", "http://datafabric.cc/data/ya#_2807f757-c18c-4cfa-a4d3-cc65c3066682"),
            ),
            (
                "cim_nrel_ConductingEquipment_Terminals",
                ("third_object", "cim_terminal_2"),
            ),
            (
                TranslationIdentifiers.NREL_IRI.value,
                ("cim_terminal_2", "http://datafabric.cc/data/ya#_44b7990d-a05b-4667-b0c8-24f0b749fb68"),
            ),
            (
                TranslationIdentifiers.NREL_IRI.value,
                (
                    "cim_nrel_ConductingEquipment_Terminals",
                    "http://datafabric.cc/data/ya#000-asdadsadsasd0000006d746c-cim16#ConductingEquipment.Terminals",
                ),
            ),
            (
                "cim_nrel_SubGeographicalRegion_Substations",
                ("third_object", "cim_substation_6"),
            ),
            (
                TranslationIdentifiers.NREL_IRI.value,
                ("cim_substation_6", "http://datafabric.cc/data/ya#_7051254a-5839-4a76-99db-11c4c0637edc"),
            ),
            (
                "cim_nrel_SubGeographicalRegion_Substations",
                ("third_object", "cim_substation_7"),
            ),
            (
                TranslationIdentifiers.NREL_IRI.value,
                ("cim_substation_7", "http://datafabric.cc/data/ya#_f88b41fe-1f08-4dc8-903c-078c2e4ab00d"),
            ),
            (
                "cim_nrel_IdentifiedObject_name",
                ("third_object", "cim_name"),
            ),
            (
                TranslationIdentifiers.NREL_LITERAL_CONTENT.value,
                ("cim_name", "Пр. 15 кВ Т-1"),
            ),
            (
                TranslationIdentifiers.NREL_IRI.value,
                (
                    "cim_nrel_IdentifiedObject_name",
                    "http://datafabric.cc/data/ya#000-asdadsadsasd0000006d746c-cim16#IdentifiedObject.name",
                ),
            ),
            (
                "cim_nrel_Switch_ratedCurrent",
                ("third_object", "cim_rated"),
            ),
            (
                TranslationIdentifiers.NREL_LITERAL_CONTENT.value,
                ("cim_rated", "8"),
            ),
            (
                TranslationIdentifiers.NREL_IRI.value,
                (
                    "cim_nrel_Switch_ratedCurrent",
                    "http://datafabric.cc/data/ya#000-asdadsadsasd0000006d746c-cim16#Switch.ratedCurrent",
                ),
            ),
            (
                "cim_nrel_Equipment_normallyInService",
                ("second_object", "literal_second_object"),
            ),
            (
                TranslationIdentifiers.NREL_LITERAL_CONTENT.value,
                ("literal_second_object", "true"),
            ),
            (
                "cim_nrel_IdentifiedObject_ChildObjects",
                ("third_object", "cim_child_1"),
            ),
            (
                TranslationIdentifiers.NREL_IRI.value,
                ("cim_child_1", "http://datafabric.cc/data/ya#_2807f757-c18c-4cfa-a4d3-cc65c3066682"),
            ),
            (
                "cim_nrel_IdentifiedObject_ChildObjects",
                ("third_object", "cim_child_2"),
            ),
            (
                TranslationIdentifiers.NREL_IRI.value,
                ("cim_child_2", "http://datafabric.cc/data/ya#_44b7990d-a05b-4667-b0c8-24f0b749fb68"),
            ),
            (
                TranslationIdentifiers.NREL_IRI.value,
                (
                    "cim_nrel_IdentifiedObject_ChildObjects",
                    "http://datafabric.cc/data/ya#000-asdadsadsasd0000006d746c-cim16#IdentifiedObject.ChildObjects",
                ),
            ),
        ]
