from typing import Dict, List


def compile(program: List[str]) -> List[str]:
    state = {}
    program = handle_label(program, state)
    program = handle_data(program, state)
    state = process_state(state)
    program = replace_vars(program, state)
    program = replace_commands(program)

    return program


def replace_commands(program: List[str]) -> List[str]:
    result = []
    for command in program:
        split_command = my_split(command)
        op_code = get_op_code(split_command[0])
        split_command[0] = op_code
        result.append(" ".join(split_command))
    return result

def get_op_code(operation):
    op_code_table = {
        "HALT": "000000",
        "MOV": "000001",
        "ADD": "001000",
        "SUB": "001001",
        "MUL": "001010",
        "DIV": "001011",
        "MOD": "001100",
        "EQ": "010000",
        "NE": "010001",
        "GT": "010010",
        "LT": "010011",
        "AND": "011000",
        "ORR": "011001",
        "NOT": "011010",
        "BRCH": "100000",
        "CBZR": "100001",
        "CBNZ": "100010",
        "BLNK": "100011",
        "READ": "101000",
        "PVAL": "101001",
        "PSTR": "101010",
        "LABEL": "110000",
        "CONST": "110001",
        "DATA": "110010"
    }
    if operation not in op_code_table:
        return operation
    return op_code_table[operation]


# removes LABELs from the program and adds them to the state
def handle_label(program: List[str], state: Dict) -> List[str]:
    line_count = 0
    result = []

    for command in program:
        operation = command.split()[0].strip()
        if operation == "LABEL":
            label_name = command.split()[1].strip()
            state[label_name] = line_count
        else:
            line_count += 1
            result.append(command)
    return result

# replaces DATAs from the program with their value and adds them to the state
# labels must first be removed to call this function
def handle_data(program: List[str], state: Dict) -> List[str]:
    result = []
    for i, command in enumerate(program):
        operation = command.split()[0].strip()
        if operation == "DATA":
            data_name = command.split()[1].strip()
            data_value = command.split()[2].strip()
            result.append(data_value)
            state[data_name] = i
        else:
            result.append(command)
    return result

# gets determine and replaces all values in the hash with their final values
# { "a": "b", "b": 10 } => { "a": 10, "b": 10 }
def process_state(state: Dict):
    def get_final_value(key: str, state):
        if key not in state:
            assert False, f"Unreachable in process_state, bad key {key}"
        if isinstance(state[key], int):
            return state[key]
        else:
            return get_final_value(state[key], state)
    for key in state.keys():
        state[key] = get_final_value(key, state)
    return state


def replace_vars(program: List[str], state: Dict) -> List[str]:
    result = []
    for command in program:
        split_command = my_split(command)
        op = split_command[0]
        if op == "MOV":
            result.append(replace_vars_mov(split_command, state))
        elif op in ["ADD", "SUB", "MUL", "DIV", "MOD", "EQ", "NE", "GT", "LT", "AND", "ORR"]:
            result.append(replace_vars_binary_op(split_command, state))
        elif op in ["NOT"]:
            result.append(replace_vars_unary_op(split_command, state))
        elif op in ["CBZR", "CBNZ"]:
            result.append(replace_vars_cond_branch(split_command, state))
        elif op == "PVAL":
            result.append(replace_vars_pval(split_command, state))    
        elif op == "BRCH":
            result.append(replace_vars_brch(split_command, state))
        elif op == "BLNK":
            result.append(replace_vars_blnk(split_command, state))
        else:
            for i, word in enumerate(split_command):
                if word in state:
                    split_command[i] = str(state[word])
            result.append(" ".join(split_command))

    return result

def is_int(string):
    try:
        int(string)
        return True
    except:
        return False

def replace_vars_mov(command, state):
    destination = command[1]
    source = command[2]
    command[1] = get_address(destination, state)
    if not is_int(source):
        command[2] = get_address(source, state)
    return " ".join(command)

def replace_vars_binary_op(command, state):
    command[1] = get_address(command[1], state)
    command[2] = get_address(command[2], state)
    command[3] = get_address(command[3], state)
    return " ".join(command)

def replace_vars_unary_op(command, state):
    command[1] = get_address(command[1], state)
    command[2] = get_address(command[2], state)
    return " ".join(command)

def replace_vars_pval(command, state):
    command[1] = get_address(command[1], state)
    return " ".join(command)

def replace_vars_cond_branch(command, state):
    command[1] = get_address(command[1], state)
    if command[2] in state:
        command[2] = str(state[command[2]])
    return " ".join(command)

def replace_vars_brch(command, state):
    command[1] = get_brch_address(command[1], state)
    return " ".join(command)

def replace_vars_blnk(command, state):
    command[1] = get_address(command[1], state)
    command[2] = str(state[command[2]])
    return " ".join(command)

def my_split(string):
    curr_index = 0
    result = []
    while curr_index < len(string):
        if string[curr_index] == " ":
            curr_index += 1
            continue
        end_of_word = get_end_of_word(string, curr_index)
        result.append(string[curr_index:end_of_word + 1])
        curr_index = end_of_word + 1
    return result

def get_end_of_word(string, index):
    if string[index] == "(":
        return end_of_bracket(string, index)
    elif string[index] == '"':
        return end_of_string(string, index)
    else:
        return end_of_number(string, index)
        
def end_of_bracket(string, index):
    open_bracket = 0
    close_bracket = 0
    for i in range(index, len(string)):
        if string[i] == "(":
            open_bracket += 1
        if string[i] == ")":
            close_bracket +=1
        if close_bracket == open_bracket:
            return i
    assert False, "Unreachable in end_of_bracket"

def end_of_string(string, index):
    found = string.find('"', index + 1)
    if found == -1:
        return len(string) - 1
    return found

def end_of_number(string, index):
    found = string.find(" ", index)
    if found == -1:
        return len(string) - 1
    return found - 1

# 10 -> 10 and _RESULT -> state["_RESULT"]
def get_destination_address(address, state):
    if is_int(address):
        return address
    return str(state[address])

# (8 10) -> 18 and (-1 SP) -> (-1 (state["SP"])) and _RESULT -> (state["_RESULT"])
def get_address(address, state):
    address = address.strip()
    if address[0] == "(" and address[-1] == ")":
        offset, addr = address[1:-1].split()
        if not is_int(addr):
            addr = state[addr]
        return f"({int(offset)} ({int(addr)}))"
    if not is_int(address):
        return f"({state[address]})"
    return address

def get_brch_address(address, state):
    address = address.strip()
    if address[0] == "(" and address[-1] == ")":
        offset, addr = address[1:-1].split()
        if not is_int(addr):
            addr = state[addr]
        return f"({int(offset)} ({int(addr)}))"
    if not is_int(address):
        return f"{state[address]}"
    return address