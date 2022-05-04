"""
    Author Zotov Nikita
"""

from typing import Any


def generate_custom_message(obj: Any, message: str) -> str:
    return f"{obj.__name__}: {message}"


def generate_start_message(obj: Any) -> str:
    return f"{obj.__name__}: has started"


def generate_finish_message(obj: Any) -> str:
    return f"{obj.__name__}: has finished"


def generate_no_action_argument_message(obj: Any) -> str:
    return f"{obj.__name__}: cannot find action arguments"


def generate_empty_link_message(obj: Any) -> str:
    return f"{obj.__name__}: empty link"


def generate_registered_message(obj: Any) -> str:
    return f"{obj.__name__}: registered"


def generate_unregistered_message(obj: Any) -> str:
    return f"{obj.__name__}: unregistered"


def generate_parsed_graph_message(obj: Any) -> str:
    return f"{obj.__name__}: parsed the rdf graph"


def generate_elements_resolved_message(obj: Any) -> str:
    return f"{obj.__name__}: elements resolved"


def generate_elements_added_to_structure_message(obj: Any) -> str:
    return f"{obj.__name__}: elements added to set"


def generate_relations_in_structure_message(obj: Any) -> str:
    return f"{obj.__name__}: relations generated in set"


def generate_resolved_graph_message(obj: Any):
    return f"{obj.__name__}: resolved the rdf graph"
