from typing import Union
from tokenization.enums import NumberOperations, BooleanComparisons, BooleanUnaryOperations, BooleanBinaryOperations



DataTypes = Union["String", "Number", "Boolean"]
NumberTypes = Union["NBinary", "NLiteral", "NVariable"]
BooleanTypes = Union["BCompare", "BUnary", "BBinary", "BLiteral"]


# where type is one of STRING NUMBER BOOLEAN
# where content is one of String Number Boolean
class Value:
    def __init__(self, type: DataTypes, content: DataTypes):
        self.type = type
        self.content = content

class String:
    def __init__(self, content: str):
        self.content = content

# where type is one of NBINARY NLITERAL NVARIABLE
# where content is one of NBinary NLiteral NVariable
class Number:
    def __init__(self, type: NumberTypes, content: NumberTypes):
        self.type = type
        self.content = content

# where operation is one of PLUS MINUS MULTIPLY DIVIDE
class NBinary:
    def __init__(self, operation: NumberOperations, left: Number, right: Number):
        self.operation = operation
        self.left = left
        self.right = right

class NLiteral:
    def __init__(self, value: int):
        self.value = value

class NVariable:
    def __init__(self, variable: str):
        self.variable = variable

# where type is one of BCOMPARE BUNARY BBINARY BLITERAL
# where content is one of BCompare BUnary BBinary BLiteral 
class Boolean:
    def __init__(self, type: BooleanTypes, content: BooleanTypes):
        self.type = type
        self.content = content

# where operation is one of EQUAL NOTEQUAL LESSTHAN GREATERTHAN
class BCompare:
    def __init__(self, operation: BooleanComparisons, left: Number, right: Number):
        self.operation = operation
        self.left = left
        self.right = right

# where operation is one of NOT
class BUnary:
    def __init__(self, operation: BooleanUnaryOperations, body: Boolean):
        self.operation = operation
        self.body = body

# where operation is one of AND OR
class BBinary:
    def __init__(self, operation: BooleanBinaryOperations, left: Boolean, right: Boolean):
        self.operation = operation
        self.left = left
        self.right = right 

class BLiteral:
    def __init__(self, value: bool):
        self.value = value
