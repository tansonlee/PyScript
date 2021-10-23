from typing import List, Tuple
from parsing.parse_value import parse_value
from parsing.split_program import STRINGQUOTE, split_program
from tokenization.commands import Command, Declaration, Function

from parsing.utility import get_command_type
from parsing.parse_command import parse_command

from tokenization.enums import STRINGQUOTE, COMMENTEND, COMMENTSTART

def parse(file_name: str) -> Tuple[List[Declaration], List[Command]]:
    f = open(file_name, "r")
    program = f.read()
    comments_removed = remove_comments(program)

    parsed_program = parse_program(comments_removed)
    f.close()
    return parsed_program

# account for strings
def remove_comments(program: str) -> str:
    result = ""
    ignore_string = False
    ignore_comment = False
    i = 0
    while i < len(program):
        if not ignore_string:
            if program[i:i+len(COMMENTSTART)] == COMMENTSTART:
                ignore_comment = True
                i += 1
            if program[i:i+len(COMMENTEND)] == COMMENTEND:
                ignore_comment = False
                i += 2
        if not ignore_comment:
            if program[i] == STRINGQUOTE:
                ignore_string = not ignore_string
        if ignore_comment:
            i += 1
            continue
        
        result += program[i]
        i += 1
    return result

def parse_program(program: str) -> Tuple[List[Declaration], List[Command]]:
    declarations, functions, body = split_program(program)
    parsed_declarations = parse_declarations(declarations)
    parsed_functions = parse_functions(functions)
    parsed_body = parse_body(body)
    return (parsed_declarations, parsed_functions, parsed_body)

# returns a list of Declarations
def parse_declarations(declarations: List[Tuple[str, str]]) -> List[Declaration]:
    parsed_declarations = []
    for variable, value in declarations:
        declaration = Declaration(variable, parse_value(value))
        parsed_declarations.append(declaration)
    return parsed_declarations

def parse_functions(functions: List[Tuple[str, List[Tuple[str, str]]]]) -> List[Function]:
    parsed_functions = []
    for name, commands in functions:
        parsed_commands = parse_body(commands)
        new_function = Function(name.strip(), parsed_commands)
        parsed_functions.append(new_function)
    return parsed_functions

def parse_body(body: List[Tuple[str, str]]) -> List[Command]:
    parsed_body = []
    for command, content in body:
        command_type = get_command_type(command)
        parsed_content = parse_command(command_type, content)
        new_command = Command(command_type, parsed_content)
        parsed_body.append(new_command)
    return parsed_body