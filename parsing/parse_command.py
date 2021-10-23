from typing import List
import parsing.parse

from parsing.parse_value import parse_boolean, parse_value
from parsing.split_program import split_body
from parsing.utility import get_body_size, get_first_open_bracket
from tokenization.commands import CommandTypes, Run
from tokenization.commands import Change, Command, Show, Capture, If, While, Skip
from tokenization.commands import CommandTypes

def parse_command(command: CommandTypes, content: str) -> CommandTypes:
    if command == Change:
        return parse_change(content)
    elif command == Show:
        return parse_show(content)
    elif command == Capture:
        return parse_capture(content)
    elif command == If:
        return parse_if(content)
    elif command == While:
        return parse_while(content)
    elif command == Skip:
        return parse_skip(content)
    elif command == Run:
        return parse_run(content)
    print("unreachable in parse_command")

# (change) <variable> <value>
def parse_change(content: str) -> Change:
    content = content.strip()
    first_space = content.find(" ")
    variable = content[:first_space].strip()
    value = content[first_space:].strip()

    return Change(variable, parse_value(value))

# show <value>
def parse_show(content: str) -> Show:
    return Show(parse_value(content.strip()))

# capture <variable name>
def parse_capture(content: str) -> Capture:
    return Capture(content.strip())

# if <boolean> { <commands> ... } { <commands> ... }
def parse_if(content: str) -> If:
    condition, true_statement, false_statement = split_if(content)
    return If(parse_boolean(condition), split_parse_body(true_statement), split_parse_body(false_statement))

def parse_while(content: str) -> While:
    condition, body = split_while(content)
    return While(parse_boolean(condition), split_parse_body(body))

def parse_skip(content: str) -> Skip:
    return Skip()

def parse_run(content: str) -> Run:
    return Run(content.strip())

def split_if(content: str):
    # get the condition
    end_of_condition = get_first_open_bracket(content) - 1

    # count the whitespace between
    whitespace = 0
    i = end_of_condition
    while content[i] != "{":
        whitespace += 1
        i += 1

    start_of_true_part = end_of_condition + whitespace
    end_of_true_part = start_of_true_part + get_body_size(content[start_of_true_part:]) + 1

    boolean = content[:end_of_condition].strip()
    true_statement = content[end_of_condition:end_of_true_part].strip()[1:-1]
    false_statement = content[end_of_true_part:].strip()[1:-1]

    return (boolean, true_statement, false_statement)

def split_while(content):
    end_of_condition = get_first_open_bracket(content) - 1

    boolean = content[:end_of_condition].strip()
    body = content[end_of_condition:].strip()[1:-1]

    return (boolean, body)
    



def split_parse_body(string: str) -> List[Command]:
    return parsing.parse.parse_body(split_body(string))

