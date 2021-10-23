from interpreter import FALSEBOOL
from tokenization.commands import Run, Show, Capture, Change, If, While, Skip

from tokenization.enums import STRINGQUOTE, ENCLOSENUMBER, ENCLOSEBOOLEAN
from tokenization.enums import TRUEBOOL, FALSEBOOL

from tokenization.value import Boolean, DataTypes, Number, String
from tokenization.commands import CommandTypes
from tokenization.value import DataTypes


disallowed_in_variable = ["!", "<", ">", "=", "`", "+", "-", "*", "/", "%", '"', "|", " ", "@"]

def is_simple_number(val: str) -> bool:
    try:
        int(val)
        return True
    except ValueError:
        return False

def is_simple_boolean(val: str) -> bool:
    return val == TRUEBOOL or val == FALSEBOOL

def get_type(value: str) -> DataTypes:
    # basic values
    if is_simple_boolean(value):
        return Boolean
    if is_simple_number(value):
        return Number 
    if value[0] == STRINGQUOTE and value[-1] == STRINGQUOTE:
        return String

    # compound values
    if value[0] == ENCLOSEBOOLEAN and value[-1] == ENCLOSEBOOLEAN:
        return Boolean
    if value[0] == ENCLOSENUMBER and value[-1] == ENCLOSENUMBER:
        return Number

    # a variable
    return Number

def get_body_size(string: str) -> int:
    string = string.strip()
    bracket_depth = 1
    ignore = False
    for i in range(1, len(string)):
       # ignore everything inside a string
        if string[i] == STRINGQUOTE:
            ignore = not ignore
        if ignore:
            continue 

        if string[i] == "{":
            bracket_depth += 1
        if string[i] == "}":
            bracket_depth -= 1
        
        if bracket_depth == 0:
            return i
    print("unreachable in get_body_size")

def get_first_open_bracket(string: str) -> int:
    ignore = False
    for i in range(len(string)):
        # ignore everything inside a string
        if string[i] == STRINGQUOTE:
            ignore = not ignore
        if ignore:
            continue 
        
        if string[i] == "{":
            return i

def get_command_type(command:str) -> CommandTypes:
    if command == "change":
        return Change
    elif command == "show":
        return Show
    elif command == "capture":
        return Capture
    elif command == "if":
        return If
    elif command == "while":
        return While
    elif command == "skip":
        return Skip
    elif command == "run":
        return Run
    print("unreachable in get command type")
        
def is_single_word(string: str) -> bool:
    if any(char in string for char in disallowed_in_variable):
        return False
    return len(string.strip().split()) == 1

def is_single_number_token(string: str) -> bool:
    if string[0] == ENCLOSENUMBER and string[-1] == ENCLOSENUMBER:
        return True
    if is_simple_number(string):
        return True
    if is_single_word(string):
        return True
    return False

def is_single_boolean_token(string: str) -> bool:
    if string == TRUEBOOL or string == FALSEBOOL:
        return True
    if string[0] == ENCLOSEBOOLEAN and string[-1] == ENCLOSEBOOLEAN:
        return True
    return False

def is_single_string_token(string:str) -> bool:
    stripped = string.strip()
    return stripped[0] == STRINGQUOTE and stripped[-1] == STRINGQUOTE
