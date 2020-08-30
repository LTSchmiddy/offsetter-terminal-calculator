from __future__ import annotations
from typing import List, Tuple
from parsing.flags import StatementFlags

class Response:
    py_code: str
    error: bool
    value: object
    of_type: type
    flags: List[StatementFlags]

    def __init__(self, p_flags=None, p_py_code: str = "", p_error: bool = False, p_result: object = None):
        if p_flags is None:
            p_flags = []

        self.error = p_error

        self.value = p_result
        self.of_type = type(self.value)

        self.flags = p_flags

    @property
    def as_hex(self) -> str:
        try:
            return hex(self.value)
        except TypeError:
            return ""

    @property
    def as_bin(self) -> str:
        try:
            return bin(self.value)
        except TypeError:
            return ""