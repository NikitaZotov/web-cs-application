"""
    Author Zotov Nikita
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, TypedDict, Union

from json_client.constants import common
from json_client.constants.exceptions import CommonErrorMessages, InvalidValueError, LinkContentOversizeError
from json_client.constants.numeric import LINK_CONTENT_MAX_SIZE
from json_client.constants.sc_types import ScType


class ScAddr:
    def __init__(self, value: int) -> None:
        self.value = value

    def is_valid(self) -> bool:
        return self.value != 0

    def is_equal(self, other: ScAddr) -> bool:
        return self.value is other.value


ScTripleCallback = Callable[[ScAddr, ScAddr, ScAddr], None]
ScEventCallbackFunc = ScTripleCallback


@dataclass
class ScEventParams:
    addr: ScAddr
    event_type: common.ScEventType
    callback: ScEventCallbackFunc


@dataclass
class ScEvent:
    id: int = 0
    event_type: common.ScEventType = None
    callback: ScEventCallbackFunc = None


ScTemplateParamValue = Union[str, ScAddr, ScType]
ScTemplateParam = Union[List[ScTemplateParamValue], ScTemplateParamValue]
ScTemplateGenParams = Dict[str, ScAddr]


class ScTemplateValue(TypedDict):
    value: ScTemplateParamValue
    alias: Optional[str]


class ScTemplateTriple(TypedDict):
    src: ScTemplateValue
    edge: ScTemplateValue
    trg: ScTemplateValue
    is_required: bool


# fmt: off
class ScTemplate:
    def __init__(self) -> None:
        self.triple_list = []

    def triple(
            self,
            param1: ScTemplateParam,
            param2: ScTemplateParam,
            param3: ScTemplateParam,
            is_required=True
    ) -> None:
        p1, p2, p3 = tuple(map(self._split_template_param, [param1, param2, param3]))

        self.triple_list.append(ScTemplateTriple(src=p1, edge=p2, trg=p3, is_required=is_required))

    def triple_with_relation(
            self,
            param1: ScTemplateParam,
            param2: ScTemplateParam,
            param3: ScTemplateParam,
            param4: ScTemplateParam,
            param5: ScTemplateParam,
    ) -> None:
        template_value = self._split_template_param(param2)
        alias = template_value.get(common.ALIAS)
        value = template_value.get(common.VALUE)
        if not alias:
            alias = f"edge_1_{len(self.triple_list)}"
        self.triple(param1, [value, alias], param3)
        self.triple(param5, param4, alias)

    @staticmethod
    def _split_template_param(param: ScTemplateParam) -> ScTemplateValue:
        if isinstance(param, list):
            if len(param) != 2:
                raise InvalidValueError("Invalid number of values for remplacement. Use [ScType | ScAddr, string]")
            value, alias = param
            if not isinstance(value, (ScAddr, ScType)) or not isinstance(alias, str):
                raise InvalidValueError("First parameter should be ScAddr or ScType. The second one - string")
            return ScTemplateValue(value=value, alias=alias)
        return ScTemplateValue(value=param, alias=None)
# fmt: on


class ScTemplateResult:
    def __init__(self, addrs: List[ScAddr], aliases: List[str]) -> None:
        self.addrs = addrs
        self.indecies = aliases

    def size(self) -> int:
        return len(self.addrs)

    def get(self, alias_or_index: Union[str, int]) -> ScAddr:
        if isinstance(alias_or_index, str):
            return self.addrs[self.indecies[alias_or_index]]
        return self.addrs[alias_or_index]

    def for_each_triple(self, func: ScTripleCallback):
        for i in range(0, self.size(), 3):
            func(self.addrs[i], self.addrs[i + 1], self.addrs[i + 2])


class ScIdtfResolveParams(TypedDict):
    idtf: str
    type: Optional[ScType]


class ScLinkContentType(Enum):
    INT = 0
    FLOAT = 1
    STRING = 2
    BINARY = 3


@dataclass
class ScLinkContent:
    data: Union[str, int]
    content_type: ScLinkContentType
    addr: ScAddr = None

    def __post_init__(self):
        if len(str(self.data)) > LINK_CONTENT_MAX_SIZE:
            raise LinkContentOversizeError(CommonErrorMessages.LINK_OVERSIZE.value)

    def type_to_str(self):
        if self.content_type == ScLinkContentType.BINARY.value:
            return common.BINARY
        if self.content_type == ScLinkContentType.INT.value:
            return common.INT
        if self.content_type == ScLinkContentType.FLOAT.value:
            return common.FLOAT
        return common.STRING


@dataclass
class ScConstructionCommand:
    el_type: ScType
    data: Any


class ScConstruction:
    def __init__(self) -> None:
        self.aliases = {}
        self.commands = []

    def create_node(self, sc_type: ScType, alias: str = None) -> None:
        if not sc_type.is_node():
            raise InvalidValueError("You should pass node type there")
        cmd = ScConstructionCommand(sc_type, None)
        if alias:
            self.aliases[alias] = len(self.commands)
        self.commands.append(cmd)

    def create_edge(self, sc_type: ScType, src: Union[str, ScAddr], trg: Union[str, ScAddr], alias: str = None) -> None:
        if not sc_type.is_edge():
            raise InvalidValueError("You should pass edge type there")
        cmd = ScConstructionCommand(sc_type, {common.SOURCE: src, common.TARGET: trg})
        if alias:
            self.aliases[alias] = len(self.commands)
        self.commands.append(cmd)

    def create_link(self, sc_type: ScType, content: ScLinkContent, alias: str = None) -> None:
        if not sc_type.is_link():
            raise InvalidValueError("You should pass link type there")
        cmd = ScConstructionCommand(sc_type, {common.CONTENT: content.data, common.TYPE: content.content_type})
        if alias:
            self.aliases[alias] = len(self.commands)
        self.commands.append(cmd)

    def get_index(self, alias: str) -> int:
        return self.aliases[alias]


class Response(TypedDict):
    id: int
    status: bool
    event: bool
    payload: Any
