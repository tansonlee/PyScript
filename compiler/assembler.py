

from typing import List
from interpreter import get_functions_table

from tokenization.commands import Capture, Change, Declaration, Function, Command, If, Run, Show, Skip, While
from tokenization.value import BBinary, BCompare, BLiteral, BUnary, Boolean, NBinary, NLiteral, NVariable, Number, String, Value

from tokenization.enums import PLUS, MINUS, DIVIDE, MULTIPLY, MOD
from tokenization.enums import AND, OR, NOT
from tokenization.enums import EQUAL, NOTEQUAL, LESSTHAN, GREATERTHAN

SP = "_STACK_POINTER"
RA = "_RETURN_ADDRESS"
RES = "_RESULT"

# ----------------------------------------------------------------
# main assemble function
# ----------------------------------------------------------------
def assemble(declarations: List[Declaration], functions: List[Function], body: List[Command]):
    assembled_declarations = assemble_declarations(declarations)
    assembled_functions = assemble_functions(functions)
    assembled_body = assemble_body(body)

    result = []
    result.append("BRCH _START_BODY") # begin at _START_BODY
    result.extend(assembled_declarations)
    result.extend(assembled_functions)
    result.append("LABEL _START_BODY")
    result.extend(assembled_body)
    result.append("BRCH _HALT_LABEL")
    result.append("LABEL _HALT_LABEL") # branch here to halt
    result.append("HALT")
    result.append(f"DATA {RES} 0") # store intermediate and final results
    result.append(f"DATA {RA} 0")
    result.append(f"DATA {SP} _STACK") # pointer to the top of the stack
    result.append("LABEL _STACK") # start of stack
    return result

# assemble the declarations
# from [Declaration(var1, val1), Declaration(var2, val2), ...]
# to   ["DATA var1 val1", "DATA var2, val2", ...]
# the value is guarenteed to be a number literal
def assemble_declarations(declarations: List[Declaration]) -> List[str]:
    result = []
    for declaration in declarations:
        assembled = f"DATA {declaration.variable} {get_number_from_value(declaration.value)}"
        result.append(assembled)
    return result

# assemble the functions
def assemble_functions(functions: List[Function]) -> List[str]:
    result = []
    for function in functions:
        assembled_function = assemble_function(function)
        result.extend(assembled_function)
    return result

def assemble_function(function: Function) -> List[str]:
    name = function.name
    body = function.body
    assembled_body = assemble_body(body)

    result = []
    result.append(f"LABEL {get_function_label(name)}")
    result.append(f"MOV (0 {SP}) {RA}")
    result.append(f"ADD {SP} {SP} 1")
    result.extend(assembled_body)
    result.append(f"MOV {RA} (-1 {SP})")
    result.extend(pop)
    result.append(f"BRCH (0 {RA})")
    return result

# assemble the body
def assemble_body(body: List[Command]) -> List[str]:
    result = []
    for command in body:
        assembled_command = assemble_command(command)
        result.extend(assembled_command)
    return result

# ----------------------------------------------------------------
# assemble commands
# ----------------------------------------------------------------
def assemble_command(command: Command) -> List[str]:
    type = command.type
    if type == Capture:
        return assemble_capture(command.content)
    elif type == Change:
        return assemble_change(command.content)
    elif type == If:
        return assemble_if(command.content)
    elif type == Run:
        return assemble_run(command.content)
    elif type == Show:
        return assemble_show(command.content)
    elif type == Skip:
        return assemble_skip(command.content)
    elif type == While:
        return assemble_while(command.content)
    else:
        print(f"unreachable in assemble_command bad type: {type}")

def assemble_change(content: Change) -> List[str]:
    result = []
    assembled_value = assemble_value(content.value)
    result.extend(assembled_value)
    result.append(f"MOV {content.variable} {RES}")
    return result

def assemble_show(content: Show) -> List[str]:
    if content.value.type == String:
        return [f'PSTR "{content.value.content.content}"']
    
    result = []
    assembled_value = assemble_value(content.value)
    result.extend(assembled_value)
    result.append(f"PVAL {RES}")
    return result

def assemble_capture(content: Capture) -> List[str]:
    return [f"READ {content.variable}"]

def assemble_if(content: If) -> List[str]:
    assembled_cond = assemble_boolean(content.condition)
    assembled_true_body = assemble_body(content.true_part)
    assembled_false_body = assemble_body(content.false_part)

    true_label = get_label()
    false_label = get_label()
    end_label = get_label()

    result = []
    result.extend(assembled_cond)
    result.append(f"CBNZ {RES} {true_label}")
    result.append(f"BRCH {false_label}")
    result.append(f"LABEL {true_label}")
    result.extend(assembled_true_body)
    result.append(f"BRCH {end_label}")
    result.append(f"LABEL {false_label}")
    result.extend(assembled_false_body)
    result.append(f"BRCH {end_label}")
    result.append(f"LABEL {end_label}")
    return result

def assemble_while(content: While) -> List[str]:
    assembled_cond = assemble_boolean(content.condition)
    assembled_body = assemble_body(content.body)

    top_label = get_label()
    body_label = get_label()
    end_label = get_label()

    result = []
    result.append(f"LABEL {top_label}")
    result.extend(assembled_cond)
    result.append(f"CBNZ {RES} {body_label}")
    result.append(f"BRCH {end_label}")
    result.append(f"LABEL {body_label}")
    result.extend(assembled_body)
    result.append(f"BRCH {top_label}")
    result.append(f"LABEL {end_label}")
    return result

def assemble_skip(content: Skip) -> List[str]:
    return []

def assemble_run(content: Run) -> List[str]:
    return [f"BLNK {RA} {get_function_label(content.function)}"]



# ----------------------------------------------------------------
# assemble values
# ----------------------------------------------------------------
def assemble_value(value: Value) -> List[str]:
    type = value.type
    if type == String:
        return assemble_string(value.content)
    elif type == Number:
        return assemble_number(value.content)
    elif type == Boolean:
        return assemble_boolean(value.content)
    else:
        assert False, f"Unreachable in assemble_value bad type {type}"

# generates the assembly which puts the value on the stack
def assemble_number(num: Number) -> List[str]:
    type = num.type
    if type == NBinary:
        return assemble_nbinary(num.content)
    elif type == NLiteral:
        return assemble_nliteral(num.content)
    elif type == NVariable:
        return assemble_nvariable(num.content)
    else:
        assert False, f"Unreachable in assemble_number, bad type {type}"

def assemble_nbinary(num: NBinary) -> List[str]:
    assembled_left = assemble_number(num.left)
    assembled_right = assemble_number(num.right)
    operation = get_operation(num.operation)

    result = []
    result.extend(assembled_left)
    result.extend(push)
    result.extend(assembled_right)
    result.append(f"{operation} {RES} (-1 {SP}) {RES}")
    result.extend(pop)
    return result

def assemble_nliteral(num: NLiteral) -> List[str]:
    return [f"MOV {RES} {num.value}"]

def assemble_nvariable(num: NVariable) -> List[str]:
    return [f"MOV {RES} {num.variable}"]


def assemble_boolean(boolean: Boolean) -> List[str]:
    type = boolean.type
    if type == BCompare:
        return assemble_bcompare(boolean.content)
    elif type == BUnary:
        return assemble_bunary(boolean.content)
    elif type == BBinary:
        return assemble_bbinary(boolean.content)
    elif type == BLiteral:
        return assemble_bliteral(boolean.content)
    else:
        assert False, f"Unreachable in assemble_boolean, bad type: {type}"

def assemble_bcompare(boolean: BCompare) -> List[str]:
    operation = get_operation(boolean.operation)
    assembled_left = assemble_number(boolean.left)
    assembled_right = assemble_number(boolean.right)

    result = []
    result.extend(assembled_left)
    result.extend(push)
    result.extend(assembled_right)
    result.append(f"{operation} {RES} (-1 {SP}) {RES}")
    result.extend(pop)
    return result

def assemble_bunary(boolean: BUnary) -> List[str]:
    operation = get_operation(boolean.operation)
    assembled_value = assemble_boolean(boolean.body)

    result = []
    result.extend(assembled_value)
    result.append(f"{operation} {RES} {RES}")
    return result

def assemble_bbinary(boolean: BBinary) -> List[str]:
    operation = get_operation(boolean.operation)
    assembled_left = assemble_boolean(boolean.left)
    assembled_right = assemble_boolean(boolean.right)

    result = []
    result.extend(assembled_left)
    result.extend(push)
    result.extend(assembled_right)
    result.append(f"{operation} {RES} (-1 {SP}) {RES}")
    result.extend(pop)
    return result

def assemble_bliteral(boolean: BLiteral) -> List[str]:
    if boolean.value:
        return [f"MOV {RES} 1"]
    else:
        return [f"MOV {RES} 0"]

def assemble_string(string: String) -> List[str]:
    assert False, f"Unreachable in assemble_string, strings cannot be assembled: {string}"



# ----------------------------------------------------------------
# helper functions
# ----------------------------------------------------------------
push = [f"MOV (0 {SP}) {RES}", f"ADD {SP} {SP} 1"]
pop = [f"SUB {SP} {SP} 1"]

def get_operation(operation):
    op_table = {
        PLUS: "ADD",
        MINUS: "SUB",
        MULTIPLY: "MUL",
        DIVIDE: "DIV",
        MOD: "MOD",
        EQUAL: "EQ",
        LESSTHAN: "LT",
        GREATERTHAN: "GT",
        AND: "AND",
        OR: "ORR",
        NOT: "NOT"
    }
    if operation not in op_table:
        assert False, f"Unreachable in get_operation, bad operation {operation}"
    return op_table[operation]


def get_number_from_value(value: Value):
    return value.content.content.value

def get_function_name(function: Function):
    return function.name

# from add1 -> _FUNCTION_add1
def get_function_label(name: str) -> str:
    return f"_FUNCTION_{name}"

# generate labels
class Label:
    def __init__(self):
        self.count = 0
    def get_label(self):
        self.count += 1
        return self.count

label_maker = Label()
def get_label():
    return f"_LABEL_{label_maker.get_label()}"