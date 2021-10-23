from typing import List
from tokenization.commands import Command, Change, Show, Capture, If, While, Skip
from tokenization.value import Value, String, Number, Boolean
from tokenization.value import NBinary, NLiteral, NVariable
from tokenization.value import BCompare, BUnary, BBinary, BLiteral
from tokenization.operators import get_operation_symbol

def print_body(body: List[Command]):
    result = ""
    for command in body:
        result += print_command(command) + "\n"
    return result

def print_command(command: Command):
    type = command.type
    if type == Change:
        return print_change(command.content)
    elif type == Show:
        return print_show(command.content)
    elif type == Capture:
        return print_capture(command.content)
    elif type == If:
        return print_if(command.content)
    elif type == While:
        return print_while(command.content)
    elif type == Skip:
        return print_skip(command.content)

def print_change(content: Change):
    return f"Change({content.variable}, {print_value(content.value)})"

def print_skip(content: Skip):
    return "Skip()"

def print_while(content: While):
    return f"While({print_boolean(content.condition)}, {print_body(content.body)})"

def print_if(content: If):
    return f"If({print_boolean(content.condition)}, {print_body(content.true_part)}, {print_body(content.false_part)})"

def print_capture(content: Capture):
    return f"Capture({content.variable})"

def print_show(content: Show):
    return f"Show({print_value(content.value)})"

def print_value(value: Value):
    type = value.type
    if type == String:
        return f"Value(String, {print_string(value.content)}"
    elif type == Number:
        return f"Value(Number, {print_number(value.content)}"
    elif type == Boolean:
        return f"Value(Boolean, {print_boolean(value.content)}"
    else:
        print(f"unreachable in print_value bad type {type}")

def print_string(content: String):
    return f"String({content.content})"

def print_number(content: Number):
    type = content.type
    value = content.content
    if type == NBinary:
        return f"NBinary({print_operation(value.operation)}, {print_number(value.left)}, {print_number(value.right)})"
    elif type == NLiteral:
        return f"NLiteral({value.value})"
    elif type == NVariable:
        return f"NVariable({value.variable})"

def print_boolean(content: Boolean):
    type = content.type
    value = content.content
    if type == BCompare:
        return f"BCompare({print_operation(value.operation)}, {print_number(value.left)}, {print_number(value.right)})"
    elif type == BUnary:
        return f"BUnary({print_operation(value.operation)}, {print_boolean(value.body)})"
    elif type == BBinary:
        return f"BBinary({print_operation(value.operation)}, {print_boolean(value.left)}, {print_boolean(value.right)})"
    elif type == BLiteral:
        return f"BLiteral({value.value})"

def print_operation(operation):
    return get_operation_symbol(operation)
