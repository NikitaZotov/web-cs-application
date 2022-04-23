"""
    Author Zotov Nikita
"""

from enum import Enum
from typing import List, Optional

from json_client import client
from json_client.constants.sc_types import ScType
from json_client.dataclass import ScAddr, ScIdtfResolveParams


class ScKeynodes(dict):
    _instance = {}

    def __new__(cls):
        if not isinstance(cls._instance, cls):
            cls._instance = dict.__new__(cls)
        return cls._instance

    def __getitem__(self, identifier: str, sc_type: Optional[ScType] = None) -> ScAddr:
        addr = self._instance.get(identifier)
        if addr is None:
            params = ScIdtfResolveParams(idtf=identifier, type=sc_type)
            addr = client.resolve_keynodes([params])[0]
            self._instance[identifier] = addr
        return addr

    def resolve_identifiers(self, identifiers: List[Enum]) -> None:
        idtf_list = []
        for idtf_class in identifiers:
            idtf_list.extend([idtf.value for idtf in idtf_class])
        idtf_list = set(idtf_list)
        params_list = [ScIdtfResolveParams(idtf=idtf, type=None) for idtf in idtf_list]
        addrs = client.resolve_keynodes(params_list)
        self._instance.update(zip(idtf_list, addrs))
