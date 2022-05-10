"""
    Author Zotov Nikita
"""
from typing import List


class ConceptsFilter:
    def __init__(self):
        self._excluded = ["main identifier*", "nrel_iri", "name", "owl_Class"]

    def clear(self, concepts: List[str]) -> List[str]:
        for exclude in self._excluded:
            if exclude in concepts:
                concepts.remove(exclude)

        return concepts
