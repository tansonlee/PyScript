
from typing import Dict, List, Union
from tokenization.commands import Capture, Change, Declaration, Command, Run, Show, Skip, While, If, Function
from tokenization.enums import PLUS, MINUS, DIVIDE, MULTIPLY, MOD
from tokenization.enums import AND, OR, NOT
from tokenization.enums import EQUAL, NOTEQUAL, LESSTHAN, GREATERTHAN
from tokenization.enums import TRUEBOOL, FALSEBOOL, BooleanLiterals

from tokenization.value import BBinary, BCompare, BLiteral, BUnary, Boolean, BooleanTypes, DataTypes, NBinary, NLiteral, NVariable, Number, NumberTypes, String, Value

# import parsing.parse_value
# parse_value = parsing.parse_value.parse_value
from parsing.parse_value import parse_number

ConcreteTypes = Union[str, bool, int]

# converts native True, False to TRUEBOOL and FALSEBOOL
def get_boolean_display(bool: bool) -> BooleanLiterals:
    if bool:
        return TRUEBOOL
    else:
        return FALSEBOOL

def interpret(declarations: List[Declaration], functions: List[Function], program: List[Command]):
    state = declarations_to_state(declarations)
    functions = get_functions_table(functions)
    for command in program:
        interpret_command(command, state, functions)

def declarations_to_state(declarations: List[Declaration]) -> Dict[str, Dict]:
    result = {}
    for declaration in declarations:
        variable = declaration.variable
        type = declaration.value.type
        value = interpret_value(declaration.value, result)
        result[variable] = {
            "type": type,
            "value": value
        }
    return result

def get_functions_table(functions: List[Function]):
    result = {}
    for function in functions:
        result[function.name] = function.body
    return result

def interpret_command(command: Command, state, functions):
    type = command.type
    if type == Change:
        interpret_change(command.content, state)
    elif type == Show:
        interpret_show(command.content, state)
    elif type == Capture:
        interpret_capture(command.content, state)
    elif type == If:
        interpret_if(command.content, state, functions)
    elif type == While:
        interpret_while(command.content, state, functions)
    elif type == Skip:
        interpret_skip(command.content, state)
    elif type == Run:
        interpret_run(command.content, state, functions)
    else:
        print(f"unreachable in interpret_command bad type {type}")

def interpret_value(value: Value, state) -> ConcreteTypes:
    if value.type == String:
        return interpret_string(value.content, state)
    elif value.type == Number:
        return interpret_number(value.content, state)
    elif value.type == Boolean:
        return interpret_boolean(value.content, state)

def interpret_change(content: Change, state):
    value = interpret_value(content.value, state)
    store(value, content.variable, state)

def interpret_show(content: Show, state):
    print(interpret_value(content.value, state))

def interpret_capture(content: Capture, state):
    user_input = input()
    parsed_input = parse_number(user_input)
    value = interpret_number(parsed_input, state)
    store(value, content.variable, state)

def interpret_if(content: If, state, functions):
    condition = interpret_boolean(content.condition, state)
    if condition:
        for command in content.true_part:
            interpret_command(command, state, functions)
    else:
        for command in content.false_part:
            interpret_command(command, state, functions)

def interpret_while(content: While, state, functions):
    condition = interpret_boolean(content.condition, state)
    while condition:
        for command in content.body:
            interpret_command(command, state, functions)
        condition = interpret_boolean(content.condition, state)

def interpret_skip(content: Skip, state):
    # do nothing
    pass

def interpret_run(content: Run, state, functions):
    function_name = content.function
    function_body = functions[function_name]
    for command in function_body:
        interpret_command(command, state, functions)

def store(value, variable, state):
    if variable not in state:
        print("variable is not declared")
        exit(1)
    state[variable]["value"] = value

def interpret_string(value: String, state) -> str:
    return value.content

def interpret_number(value: Number, state) -> int:
    type = value.type
    if type == NBinary:
        return interpret_nbinary(value.content, state)
    elif type == NLiteral:
        return interpret_nliteral(value.content, state)
    elif type == NVariable:
        return interpret_nvariable(value.content, state)
    else:
        print("unreachable in interpret_number")

def interpret_nbinary(value: NBinary, state) -> int:
    left = interpret_number(value.left, state)
    right = interpret_number(value.right, state)
    type = value.operation
    if type == PLUS:
        return left + right
    elif type == MINUS:
        return left - right
    elif type == MULTIPLY:
        return left * right
    elif type == DIVIDE:
        return left // right
    elif type == MOD:
        return left % right

def interpret_nliteral(value: NLiteral, state) -> int:
    return value.value

def interpret_nvariable(value: NVariable, state) -> int:
    return lookup(value.variable, state)

def lookup(variable: str, state: Dict[str, Dict]) -> ConcreteTypes:
    if variable not in state:
        print(f"variable {variable} is not declared")
    return state[variable]["value"]

def interpret_boolean(value: Boolean, state) -> bool:
    type = value.type
    if type == BCompare:
        return interpret_bcompare(value.content, state)
    elif type == BUnary:
        return interpret_bunary(value.content, state)
    elif type == BBinary:
        return interpret_bbinary(value.content, state)
    elif type == BLiteral:
        return interpret_bliteral(value.content, state)
    else:
        print("unreachable in interpret_boolean")

def interpret_bliteral(value: BLiteral, state):
    return value.value

def interpret_bbinary(value: BBinary, state):
    left = interpret_boolean(value.left, state)
    right = interpret_boolean(value.right, state)
    type = value.operation
    if type == AND:
        return left and right
    elif type == OR:
        return left or right
    else:
        print("unreachable in interpret_bbinary")

def interpret_bunary(value: BUnary, state):
    interpreted = interpret_boolean(value.body, state)
    type = value.operation
    if type == NOT:
        return not interpreted

def interpret_bcompare(value: BCompare, state):
    left = interpret_number(value.left, state)
    right = interpret_number(value.right, state)
    type = value.operation
    if type == EQUAL:
        return left == right
    elif type == NOTEQUAL:
        return left != right
    elif type == LESSTHAN:
        return left < right
    elif type == GREATERTHAN:
        return left > right
