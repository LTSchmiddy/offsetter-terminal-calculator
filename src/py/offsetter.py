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


def calculate_response(eval_statement: str, eval_scope: dict = {}, add_flags: List[StatementFlags] = None) -> Response:
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

    except Exception as e:
        return Response(flags, py_code, True, e)

    return Response(flags, py_code, False, result)

def format_response(response: Response):
    if StatementFlags.PASS in response.flags or StatementFlags.EXEC in response.flags:
        return ""

    if response.is_error:
        return f"{response.of_type.__name__}: {str(response.value)}"

    retVal = f" = {response.value}"

    if response.as_hex != "":
        retVal += f" -> {response.as_hex}"

    if response.as_bin != "":
        retVal += f" -> {response.as_bin}"
    
    return retVal

def calculate_formatted_response(*args, **kwargs):
    result = format_response(calculate_response(*args, **kwargs))
    print(result)
    return result

def main():
    local_scope = {}

    print("\n--- Offsetter Terminal Calculator: ---\n")
    while True:
        # eval_statement = input("> ")
        response = calculate_response(input("> "), local_scope)
        print_str = format_response(response)

        if print_str is not None:
            print(print_str + "\n")

print("Python Loaded")
if __name__ == '__main__':
    main()

