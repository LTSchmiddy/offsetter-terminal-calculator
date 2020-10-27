#Global Values:
from __future__ import annotations
from typing import List, Tuple
import os

import parsing
from parsing import StatementFlags, Response
import calc_settings

# For use with the user input
from math import *

settings = calc_settings.Settings(os.path.join(os.path.expanduser("~"), "offsetter.json"))

# Runs all parsing functions:
def parse_expression_to_python(expression: str, flags: List[StatementFlags]) -> str:
    expression = parsing.parse_hex_bin(expression, settings)

    if settings.auto_walrus and not StatementFlags.EXEC in flags :
        expression = parsing.parse_auto_walrus(expression)

    return expression

def load_script(path):
    pass


def calculate_response_str(eval_statement: str, eval_scope: dict = {}, add_flags: List[StatementFlags] = None) -> Response:
    result = None

    eval_statement, flags = StatementFlags.get_flags(eval_statement)
    if add_flags is not None:
        flags.extend(add_flags)


    # This will allow the user to add comments to their input history.
    if StatementFlags.PASS in flags:
        return Response(flags)

    py_code = ""

    try:
        if StatementFlags.RAW in flags:
            py_code = eval_statement
        else:
            py_code = parse_expression_to_python(eval_statement, flags)

        if settings.log_py_code:
            print(py_code)

        # Run a python statement as is:
        if StatementFlags.EXEC in flags:
            exec(py_code, globals(), eval_scope)
            return Response(flags, py_code)

        # Wrapping the entire expression in parentheses ensures that eval()
        # treats py_code as a single expression, and ensures that the
        # walrus operator ( :=  ), which allows assigning variables inside of
        # expressions, will work correctly. I can't think of any downsides.

        result = eval(f"({py_code})", globals(), eval_scope)

    except SyntaxError as e:
        return Response(flags, py_code, True, e)

    except NameError as e:
        return Response(flags, py_code, True, e)

    except ValueError as e:
        return Response(flags, py_code, True, e)

    return Response(flags, py_code,False, result)


if __name__ == '__main__':
    local_scope = {}

    print("\n--- Offsetter Terminal Calculator: ---\n")
    while True:
        # eval_statement = input("> ")
        response = calculate_response_str(input("> "))
        if StatementFlags.PASS in response.flags or StatementFlags.EXEC in response.flags:
            continue

        if response.error:
            print(f"{response.of_type.__name__}: {str(response.value)}")
            continue

        print_str = f" = {response.value}"

        if response.as_hex != "":
            print_str += f" -> {response.as_hex}"

        if response.as_bin != "":
            print_str += f" -> {response.as_bin}"

        print(print_str + "\n")

