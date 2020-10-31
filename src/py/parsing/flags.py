from __future__ import annotations
from enum import Enum
from typing import List, Tuple

class StatementFlags(Enum):
    PASS = '#'
    RAW = ':'
    EXEC = '$'

    @classmethod
    def get_all_prefixes(cls)-> List[str]:
        retVal = []
        for i in cls:
            retVal.append(i.value)

        return retVal

    # Parsing Functions:
    @staticmethod
    def get_flags(statement) -> Tuple[str, List[StatementFlags]]:
        retVal = []
        prefixes = StatementFlags.get_all_prefixes()

        while True:
            found = False
            for i in prefixes:
                if statement.startswith(i):
                    retVal.append(StatementFlags(i))
                    statement = statement[1:]
                    found = True
                    break

            if not found: break

        return statement.strip(), retVal