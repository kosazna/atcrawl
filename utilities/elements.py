# -*- coding: utf-8 -*-

from dataclasses import dataclass
from typing import Union


@dataclass
class Element:
    NAME: Union[str, None] = None
    TAG: Union[str, None] = None
    CLASS: Union[str, None] = None
    ID: Union[str, None] = None
    XPATH: Union[str, None] = None
    ATTRIBUTE: Union[str, None] = None
    LOC: Union[int, None] = None
    DEFAULT: Union[str, None] = None
