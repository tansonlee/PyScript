from parsing.utility import get_type, is_simple_number, is_single_boolean_token, is_single_number_token, is_single_word
from tokenization.operators import get_operation_type, number_operators, boolean_binary_operators, boolean_unary_operators, boolean_comparison_operators

from tokenization.value import Value, String, Number, Boolean, NBinary, NLiteral, NVariable, BCompare, BUnary, BBinary, BLiteral


from tokenization.enums import TRUEBOOL, FALSEBOOL
from tokenization.enums import ENCLOSENUMBER

def parse_value(value: str) -> Value:
    type = get_type(value)
    content = None
    if type == Number:
        content = parse_number(value)
    elif type == Boolean:
        content = parse_boolean(value)
    elif type == String:
        content = parse_string(value)
    else:
        print(f"unreachable in parse_value bad type: {type}")

    return Value(type, content)

def parse_number(string: str) -> Number:
    string = string.strip()

    if is_simple_number(string):
        return Number(NLiteral, NLiteral(int(string)))

    if is_single_word(string):
        return Number(NVariable, NVariable(string))

    if not (string[0] == ENCLOSENUMBER and string[-1] == ENCLOSENUMBER):
        print(f"bad number: ({string})")

    # remove the starting and ending 
    string = string.strip()[1:-1]
    operator = ""
    left = ""
    right = ""
    for i in range(len(string)):
        for current_operator in number_operators:
            if string[i:i+len(current_operator)] != current_operator:
                continue

            left = string[0:i].strip()
            right = string[i+len(current_operator):].strip()
            operator = current_operator
            if is_single_number_token(left) and is_single_number_token(right):
                parsed_number = NBinary(get_operation_type(operator), parse_number(left), parse_number(right))
                return Number(NBinary, parsed_number)


def boolean(value: str) -> bool:
    if value == FALSEBOOL:
        return False
    if value == TRUEBOOL:
        return True
    print(f"unreachable in boolean, {value}")

def parse_boolean(string: str) -> Boolean:
    string = string.strip()

    # boolean literals
    if string == TRUEBOOL or string == FALSEBOOL:
        return Boolean(BLiteral, BLiteral(boolean(string)))

    # strip the starting and ending "|"
    string = string.strip()[1:-1]

    # boolean unary operators
    first_space = string.find(" ")
    for current_operation in boolean_unary_operators:
        if string[0:first_space] == current_operation:
            parsed_boolean = BUnary(get_operation_type(current_operation), parse_boolean(string[first_space:].strip()))
            return Boolean(BUnary, parsed_boolean)

    # boolean binary operators
    for i in range(len(string)):
        for current_operation in boolean_binary_operators:
            if string[i:i+len(current_operation)] == current_operation:
                left = string[:i].strip()
                right = string[i+len(current_operation):].strip()
                if is_single_boolean_token(left) and is_single_boolean_token(right):
                    parsed_boolean = BBinary(get_operation_type(current_operation), parse_boolean(left), parse_boolean(right))
                    return Boolean(BBinary, parsed_boolean)

    # boolean comparison operators
    for i in range(len(string)):
        for current_operation in boolean_comparison_operators:
            if string[i:i+len(current_operation)] == current_operation:
                left = string[:i].strip()
                right = string[i+len(current_operation):].strip()
                if is_single_number_token(left) and is_single_number_token(right):
                    parsed_boolean = BCompare(get_operation_type(current_operation), parse_number(left), parse_number(right))
                    return Boolean(BCompare, parsed_boolean)
    
    print(f"unreachable in parse_boolean, bad value {string}")

def parse_string(value) -> str:
    
    return String(value[1:-1])
