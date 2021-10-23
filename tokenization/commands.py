from typing import List, Union

import tokenization.value
Value = tokenization.value.Value
Boolean = tokenization.value.Boolean

CommandTypes = Union["Change", "Show", "Capture", "If", "While", "Skip", "Run"]

class Declaration:
    def __init__(self, variable: str, value: Value):
        self.variable = variable
        self.value = value

# where type is one of CHANGE SHOW CAPTURE IF WHILE SKIP
# where content is one of Change Show Capture If While Skip
class Command:
    def __init__(self, type: CommandTypes, content: CommandTypes):
        self.type = type
        self.content = content
    
class Function:
    def __init__(self, name: str, body: List[Command]):
        self.name = name
        self.body = body

# where value is a Value
class Change:
    def __init__(self, variable: str, value: Value):
        self.variable = variable
        self.value = value

# where value is a Value
class Show:
    def __init__(self, value: Value):
        self.value = value

# where variable is a string
class Capture:
    def __init__(self, variable: str):
        self.variable = variable

# where condition is a Boolean
# where true_part and false_part are lists of Commands
class If:
    def __init__(self, condition: Boolean, true_part: List[Command], false_part: List[Command]):
        self.condition = condition
        self.true_part = true_part
        self.false_part = false_part

# where condition is a Boolean
# where body is a list of Commands
class While:
    def __init__(self, condition: Boolean, body: List[Command]):
        self.condition = condition
        self.body = body

# empty - contains no information
class Skip:
    def __init__(self):
        pass

class Run:
    def __init__(self, function: Function):
        self.function = function
