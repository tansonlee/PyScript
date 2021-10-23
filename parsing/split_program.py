from typing import List, Tuple
from parsing.utility import get_body_size, get_first_open_bracket

from tokenization.enums import STRINGQUOTE

"""
@declarations
...
@declarations

@functions
...
@functions

@body
...
@body
"""

def split_program(program: str) -> Tuple[List[Tuple[str, str]], List[Tuple[str, str]]]:
    declarations, functions, body = split_declarations_function_body(program)
    declarations_split = split_declarations(declarations)
    functions_split = split_functions(functions)
    body_split = split_body(body)
    return (declarations_split, functions_split, body_split)

# finds the index that key starts in string with starting point as start
def my_find(string, key, start):
    string = string[start:]
    ignore = False
    for i in range(len(string)):
        if string[i] == "`":
            ignore = not ignore

        if ignore:
            continue

        if string[i:i + len(key)] == key:
            return start + i

    return len(string) - 1


def split_declarations_function_body(program: str) -> Tuple[str, str, str]:
    declarations_seperator = "@declarations"
    functions_seperator = "@functions"
    body_seperator = "@body"
    program.strip()

    start_declare = my_find(program, declarations_seperator, 0)
    end_declare = my_find(program, declarations_seperator, start_declare + 1)

    start_functions = my_find(program, functions_seperator, end_declare + 1)
    end_functions = my_find(program, functions_seperator, start_functions + 1)

    start_body = my_find(program, body_seperator, end_functions + 1)
    end_body = my_find(program, body_seperator, start_body + 1)

    declarations = program[start_declare + len(declarations_seperator):end_declare].strip()
    functions = program[start_functions + len(functions_seperator): end_functions].strip()
    body = program[start_body + len(body_seperator): end_body].strip()

    return (declarations, functions, body)

# # returns a tuple of (declarations, functions, body)
# def split_declarations_function_body(program: str) -> Tuple[str, str, str]:
#     ignore = False
#     seperator_indexes = []
#     for i in range(len(program) - 2):
#         # ignore everything inside a string
#         if program[i:i + len(STRINGQUOTE)] == STRINGQUOTE:
#             ignore = not ignore
#         if ignore:
#             continue
#         if program[i:i+len(DECLARATIONSEPERATOR)] == DECLARATIONSEPERATOR:
#             seperator_indexes.append(i)
#             if len(seperator_indexes) == 2:
#                 break

#     declarations_start = seperator_indexes[0] + len(DECLARATIONSEPERATOR)
#     declarations_end = seperator_indexes[1]
#     body_start = seperator_indexes[1] + len(DECLARATIONSEPERATOR)
#     body_end = len(program)
#     return (program[declarations_start:declarations_end], program[body_start:body_end])

# takes a string of the declarations and returns a list of
# [(var1, val1), (var2, val2), ...]
def split_declarations(declarations: str) -> List[Tuple[str, str]]:
    declarations = declarations.strip()
    result = []
    split_declarations = declarations.split("\n")

    for d in split_declarations:
        d = d.strip()
        if d == "" or d[0:7] != "declare":
            continue
        # remove the "declare at the start"
        d = d[7:].strip()
        space = d.find(" ")

        variable_name = d[0:space].strip()
        value = d[space:].strip()
        result.append((variable_name, value))

    return result

# returns the next command from the string if there is one
# otherwise returns ""
def get_command_from(string: str) -> str:
    commands = ["change", "show", "capture", "if", "while", "skip", "run"]
    for command in commands:
        if string[:len(command)] == command:
            return command
    return ""

# takes the function string and returns a list of
# [(name1, [(command1, content1), ...]), (name2, [(command2, content2)...]]
def split_functions(functions: str) -> List[Tuple[str, List[Tuple[str, str]]]]:
    functions = functions.strip()
    result = []
    while len(functions) > 0:
        # consume the word "function"
        functions = functions[8:].strip()

        # get the function name
        first_space = functions.find(" ")
        name = functions[:first_space].strip()
        functions = functions[first_space:].strip()

        # get the function body
        end_of_body = get_body_size(functions) - 1
        body = functions[1:end_of_body + 1]
        functions = functions[end_of_body + 2:].strip()
        body_split = split_body(body)
        result.append((name, body_split))

        functions = functions.strip()
    return result

# takes the body string and returns a list of
# [(command1, content1), (command2, content2), ...]
def split_body(body: str) -> List[Tuple[str, str]]:
    body = body.strip()
    result = []
    ignore = False

    while len(body) > 0:
        # ignore everything inside a string
        if body[0:len(STRINGQUOTE)] == STRINGQUOTE:
            ignore = not ignore
        if ignore:
            continue

        command = get_command_from(body)

        end_of_command = -1

        if command == "if":
            end_of_command = get_end_of_if(body[len(command):])
        elif command == "while":
            end_of_command = get_end_of_while(body[len(command):])
        elif command == "change":
            end_of_command = get_end_of_change(body[len(command):])
        elif command == "show":
            end_of_command = get_end_of_show(body[len(command):])
        elif command == "capture":
            end_of_command = get_end_of_capture(body[len(command):])
        elif command == "skip":
            end_of_command = get_end_of_skip(body[len(command):])
        elif command == "run":
            end_of_command = get_end_of_run(body[len(command):])
        else:
            print(f"unreachable in split_body bad command: {command}")

        result.append((command, body[len(command): len(command) + end_of_command].strip()))

        body = body[len(command) + end_of_command:].strip()


    return result

# |...| {...} {...}
def get_end_of_if(string: str) -> int:
    current_index = 0

    # first consume the condition
    current_index += get_first_open_bracket(string)

    # consume the true body
    current_index += get_body_size(string[current_index:])

    # consume white space between
    while string[current_index] != "{":
        current_index += 1

    # consume the false body
    current_index += get_body_size(string[current_index:])

    return current_index + 1

# |...| {...}
def get_end_of_while(string: str) -> int:
    current_index = 0

    # first consume the condition
    current_index += get_first_open_bracket(string)
    #consume the body
    current_index += get_body_size(string[current_index:])

    return current_index + 1

def get_until_next_command(string: str) -> int:
    ignore = False
    for i in range(len(string)):
        # ignore everything inside a string
        if string[i] == STRINGQUOTE:
            ignore = not ignore
        if ignore:
            continue 

        command = get_command_from(string[i:])
        if command:
            return i - 1
    return len(string)

get_end_of_change = get_until_next_command
get_end_of_show = get_until_next_command
get_end_of_capture = get_until_next_command
get_end_of_skip = get_until_next_command
get_end_of_run = get_until_next_command


