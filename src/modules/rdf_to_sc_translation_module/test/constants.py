"""
    Author Zotov Nikita
"""

from enum import Enum


class TestScAlias(Enum):
    MAIN_NODE = "_main_node"
    NOROLE_RELATION = "_norole_relation"
    OBJECT = "_object"
    OBJECT_LINK = "_object_link"
    MAIN_NODE_IRI_LINK = "_main_node_iri_link"
    MAIN_NODE_IRI_COMMON_ARC = "_main_node_iri_common_arc"
    MAIN_NODE_IRI_ACCESS_ARC = "_main_node_iri_access_arc"
    OBJECT_CONTENT_OR_IRI_COMMON_ARC = "_object_content_or_iri_common_arc"
    OBJECT_CONTENT_OR_IRI_ACCESS_ARC = "_object_content_or_iri_access_arc"
    NOROLE_RELATION_COMMON_ARC = "_norole_relation_common_arc"
    NOROLE_RELATION_ACCESS_ARC = "_norole_relation_access_arc"


class TestModels(Enum):
    CORRECT_MODEL_WITH_PRE_PREPARED_LITERALS = """
        <rdf:RDF
            xmlns="http://www.metaphacts.com/resource/"
            xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#"
            xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
            xmlns:cim16="http://iec.ch/TC57/2014/CIM-schema-cim16#">
            <rdf:Description rdf:about="http://datafabric.cc/data/ya#_0516effa-acce-4077-94d5-6b6c48087a04">
                <rdf:type rdf:resource="http://iec.ch/TC57/2014/CIM-schema-cim16#ACLineSegment"/>
                <rdf:type rdf:resource="http://www.w3.org/2002/07/owl#NamedIndividual"/>
                <cim16:Equipment.normallyInService>true</cim16:Equipment.normallyInService>
            </rdf:Description>
        </rdf:RDF>
    """
    CORRECT_MODEL_WITH_GENERATED_LITERALS = """
        <rdf:RDF
            xmlns="http://www.metaphacts.com/resource/"
            xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#"
            xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
            xmlns:cim16="http://iec.ch/TC57/2014/CIM-schema-cim16#">
            <rdf:Description rdf:about="http://datafabric.cc/data/ya#_0516effa-acce-4077-94d5-6b6c48087a04">
                <cim16:ACDCTerminal.sequenceNumber>1</cim16:ACDCTerminal.sequenceNumber>
            </rdf:Description>
        </rdf:RDF>
    """
    CORRECT_MODEL_WITH_GENERATED_LITERALS_1 = """
        <rdf:RDF
            xmlns="http://www.metaphacts.com/resource/"
            xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#"
            xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
            xmlns:cim16="http://iec.ch/TC57/2014/CIM-schema-cim16#">
            <rdf:Description rdf:about="http://datafabric.cc/data/ya#_0516effa-acce-4077-94d5-6b6c48087a04">
                <cim16:ACDCTerminal.sequenceNumber>4</cim16:ACDCTerminal.sequenceNumber>
            </rdf:Description>
        </rdf:RDF>
    """
    CORRECT_MODEL_WITH_GENERATED_LITERALS_2 = """
        <rdf:RDF
            xmlns="http://www.metaphacts.com/resource/"
            xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#"
            xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
            xmlns:cim16="http://iec.ch/TC57/2014/CIM-schema-cim16#">
            <rdf:Description rdf:about="http://datafabric.cc/data/ya#_0516effa-acce-4077-94d5-6b6c48087a04">
                <cim16:ACDCTerminal.sequenceNumber>8</cim16:ACDCTerminal.sequenceNumber>
            </rdf:Description>
        </rdf:RDF>
    """
    CORRECT_MODEL_WITH_RELATION_TO_NAMED_CLASS = """
        <rdf:RDF
            xmlns="http://www.metaphacts.com/resource/"
            xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#"
            xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
            xmlns:cim16="http://iec.ch/TC57/2014/CIM-schema-cim16#">
            <rdf:Description rdf:about="http://datafabric.cc/data/ya#_0516effa-acce-4077-94d5-6b6c48087a04">
                <rdf:type rdf:resource="http://iec.ch/TC57/2014/CIM-schema-cim16#ACLineSegment"/>
            </rdf:Description>
        </rdf:RDF>
    """
    MODEL_WITH_NO_NAMESPACES_DEFINED = """
        <rdf:RDF>
            <rdf:Description rdf:about="http://datafabric.cc/data/ya#_0516effa-acce-4077-94d5-6b6c48087a04">
                <rdf:type rdf:resource="http://iec.ch/TC57/2014/CIM-schema-cim16#ACLineSegment"/>
            </rdf:Description>
        </rdf:RDF>
    """
    MODEL_WITH_UNEXPECTED_END = """
        <rdf:RDF
            xmlns="http://www.metaphacts.com/resource/"
            xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#"
            xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
            xmlns:cim16="http://iec.ch/TC57/2014/CIM-schema-cim16#">
            <rdf:Description rdf:about="http://datafabric.cc/data/ya#_0516effa-acce-4077-94d5-6b6c48087a04">
                <rdf:type rdf:resource="http://iec.ch/TC57/2014/CIM-schema-cim16#ACLineSegment"/>
            </rdf:Description>
   """
