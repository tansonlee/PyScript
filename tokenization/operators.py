from tokenization.enums import PLUS, MINUS, MULTIPLY, DIVIDE, MOD
from tokenization.enums import EQUAL, LESSTHAN, GREATERTHAN
from tokenization.enums import AND, OR, NOT


number_operators = ["+", "-", "*", "/", "%"]
boolean_binary_operators = ["and", "or"]
boolean_unary_operators = ["not"]
boolean_comparison_operators = ["=", ">", "<"]

def get_operation_type(op):
    operation_name_table = {
        "+": PLUS,
        "-": MINUS,
        "*": MULTIPLY,
        "/": DIVIDE,
        "%": MOD,
        "=": EQUAL,
        "<": LESSTHAN,
        ">": GREATERTHAN,
        "and": AND,
        "or": OR,
        "not": NOT
    }
    return operation_name_table[op]

def get_operation_symbol(op):
    operation_name_table = {
        PLUS: "+",
        MINUS: "-",
        MULTIPLY: "*",
        DIVIDE: "/",
        MOD: "%",
        EQUAL: "=",
        LESSTHAN: "<",
        GREATERTHAN: ">",
        AND: "and",
        OR: "or",
        NOT: "not" 
    }
    return operation_name_table[op]