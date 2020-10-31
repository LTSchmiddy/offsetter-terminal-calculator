from __future__ import annotations
from parsing.flags import StatementFlags
from parsing.response import Response

from calc_settings import Settings

# import main

hex_chars = '0123456789abcdefABCDEF'


def parse_hex_bin(exp: str, settings: Settings) -> str:
    outstr = ""
    c_pos = 0
    while c_pos < len(exp):
        if exp[c_pos] != "0":
            outstr += exp[c_pos]
            c_pos += 1
            continue

        # Possible beginning of a hex or binary value.

        if c_pos + 1 >= len(exp):
            # Nope. End of string.
            outstr += exp[c_pos]
            break

        mode = exp[c_pos + 1].lower()
        if mode == "x" and settings.convert_hex:
            # Ok, we a hex. let's assemble this sucker:
            new_hex = "0x"
            c_pos += 2

            while c_pos < len(exp) and exp[c_pos] in hex_chars:
                new_hex += exp[c_pos]
                c_pos += 1

            outstr += f"{int(new_hex, 16)}"

        elif mode == "b" and settings.convert_binary:
            # Ok, we a binary. let's assemble this sucker:
            new_binary = "0b"
            c_pos += 2

            while c_pos < len(exp) and exp[c_pos] in "01":
                new_binary += exp[c_pos]
                c_pos += 1

            outstr += f"{int(new_binary, 2)}"

        else:
            # Nope. Not a '0x' or '0b':
            outstr += exp[c_pos] + exp[c_pos + 1]
            c_pos += 2


    return outstr


# Automatically converts = into := for expressions
def parse_auto_walrus(exp):
    outstr = ""
    c_pos = 0

    inside_quotes = False
    inside_double_quotes = False

    is_quoted = lambda: inside_quotes or inside_double_quotes
    get_char = lambda index: "" if index < 0 or index >= len(exp) else exp[index]

    while c_pos < len(exp):
        # i = exp[c_pos]
        i = get_char(c_pos)
        b_char = get_char(c_pos - 1)
        a_char = get_char(c_pos + 1)

        # We don't want any equals signs inside strings to be be converted.
        # So, we're going to keep track of those.
        if i == "'" and not inside_double_quotes and b_char != "\\":
            inside_quotes = not inside_quotes
            outstr += "'"

        elif i == "\"" and not inside_quotes and b_char != "\\":
            inside_double_quotes = not inside_double_quotes
            outstr += "\""

        # Process other characters
        elif i != "=":
            outstr += i

        elif is_quoted():
            outstr += "="


        else:

            # if we've made it this far, we've found an unquoted = sign.
            # now we need to check if it's a combination symbol:
            convert = False
            if b_char == "" or a_char == "":
                pass

            # prior characters that indicate a multi-char operator
            # **= and //= are covered by *= and /= checking.
            elif b_char in "!=<>-+*/%:":
                pass

            # follow-up character that indicates a multi-char operator:
            elif a_char == "=":
                pass
            else:
                convert = True

            if convert:
                outstr += ":="
            else:
                outstr += "="

        c_pos += 1

    return outstr
