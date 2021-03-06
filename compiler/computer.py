

from os import link
from typing import Dict, List
from compiler.compiler import my_split

arithmetic_ops = ["001000", "001001", "001010", "001011", "001100"]
comparison_ops = ["010000", "010001", "010010", "010011"]
binary_boolean_ops = ["011000", "011001"]
unary_boolean_ops = ["011010"]
branching_ops = ["100000", "100001", "100010", "100011"]
io_ops = ["101000", "101001", "101010"]
other_ops = ["000001"]

def ram_fetch(ram: Dict, addr: int) -> int:
    return ram[addr]

def ram_store(ram: Dict, addr: int, val: int):
    ram[addr] = val

def execute_machine_code(code: List[str]):
    ram = {}
    pc = 0
    ram = load_program(code, ram)

    while True:
        command = ram[pc]
        if isinstance(command, int) or command == "000000":
            # print("CORE DUMPED")
            # for i in ram.keys():
            #     print(f"{i}: {ram[i]}")
            break
        split_command = my_split(command)
        operation = split_command[0]
        if operation in arithmetic_ops:
            execute_arithmetic_op(split_command, ram)
            pc += 1

        elif operation in comparison_ops:
            execute_comparison_op(split_command, ram)
            pc += 1

        elif operation in binary_boolean_ops:
            execute_binary_boolean_op(split_command, ram)
            pc += 1

        elif operation in unary_boolean_ops:
            execute_unary_boolean_op(split_command, ram)
            pc += 1

        elif operation in branching_ops:
            pc = execute_branching_op(split_command, ram, pc)

        elif operation in io_ops:
            execute_io_op(split_command, ram)
            pc += 1

        elif operation in other_ops:
            execute_other_ops(split_command, ram)
            pc += 1
        
        # print("CORE DUMPED")
        # for i in ram.keys():
        #     print(f"{i}: {ram[i]}")

def is_int(string):
    try:
        int(string)
        return True
    except:
        return False

def load_program(code, ram):
    for i, line in enumerate(code):
        if is_int(line):
            ram[i] = int(line)
        else:
            ram[i] = line
    return ram


def execute_arithmetic_op(command, ram):
    # ADD 10 5 6
    op = command[0]
    destination = get_destination(command[1], ram)
    left = get_value(command[2], ram)
    right = get_value(command[3], ram)
    result = 0
    if op == "001000":
        result = left + right
    elif op == "001001":
        result = left - right
    elif op == "001010":
        result = left * right
    elif op == "001011":
        result = left // right
    elif op == "001100":
        result = left % right
    else:
        assert False, f"Unreachable in execute_arithmetic_op, bad command {command}"

    ram[destination] = result


def execute_comparison_op(command, ram):
    op = command[0]
    destination = get_destination(command[1], ram)
    left = get_value(command[2], ram)
    right = get_value(command[3], ram)
    result = 0
    if op == "010000":
        result = bool_to_int(left == right)
    elif op == "010001":
        result = bool_to_int(left != right)
    elif op == "010010":
        result = bool_to_int(left > right)
    elif op == "010011":
        result = bool_to_int(left < right)
    else:
        assert False, f"Unreachable in execute_comparison_op, bad command {command}"

    ram[destination] = result

def execute_binary_boolean_op(command, ram):
    op = command[0]
    destination = get_destination(command[1], ram)
    left = int_to_bool(get_value(command[2], ram))
    right = int_to_bool(get_value(command[3], ram))
    result = 0
    if op == "011000":
        result = left and right
    elif op == "011001":
        result = left or right
    else:
        assert False, f"Unreachable in execute_binary_boolean_op, bad command {command}"

    ram[destination] = bool_to_int(result)

def execute_unary_boolean_op(command, ram):
    op = command[0]
    destination = get_destination(command[1], ram)
    body = int_to_bool(get_value(command[2], ram))
    if op == "011010":
        ram[destination] = bool_to_int(not body)
    else:
        assert False, f"Unreachable in execute_unary_boolean_op, bad command {command}"

def execute_branching_op(command, ram, pc):
    op = command[0]
    if op == "100000":
        target = get_value2(command[1], ram)
        return target
    elif op == "100010":
        condition = ram[get_destination(command[1], ram)]
        if condition == 1:
            return int(command[2])
        elif condition == 0:
            return pc + 1
        else:
            assert False, f"Unreachable in execute_branching_op > CBNZ, bad condition {condition}"
    elif op == "100001":
        condition = ram[get_destination(command[1], ram)]
        if condition == 0:
            return int(command[2])
        elif condition == 1:
            return pc + 1
        else:
            assert False, f"Unreachable in execute_branching_op > CBZR, bad condition {condition}"
    elif op == "100011":
        link_address = get_destination(command[1], ram)
        ram[link_address] = pc + 1
        return int(command[2])

    else:
        assert False, f"Unreachable in execute_branching_op, bad op {op}"


def execute_io_op(command, ram):
    op = command[0]
    if op == "101010":
        print(command[1][1:-1]) # strip the quotes ""
    elif op == "101001":
        value_address = get_destination(command[1], ram)
        print(ram[value_address])
    elif op == "101000":
        user_input = int(input())
        destination = int(command[1])
        ram[destination] = user_input
    else:
        assert False, f"Unreachable in execute_io_op, bad command {command}"

def execute_other_ops(command, ram):
    op = command[0]

    if op == "000001":
        destination = get_destination(command[1], ram)
        value = get_value(command[2], ram)
        ram[destination] = value
    else:
        assert False, f"Unreachable in execute_other_ops, bad command {command}"


    # MOV

# (5) -> 5 and (-1 (12)) -> ram[12] + -1
def get_destination(string, ram) -> int:
    string = string[1:-1]
    if len(string.split()) > 1:
        offset, address2 = string.split()
        return int(ram[int(address2[1:-1])]) + int(offset)
    else:
        return int(string)



# (5) -> ram[5] or 5 -> 5 or (-1 (12)) -> ram[ram[12] + -1]
def get_value(address, ram) -> int:
    address = address.strip()
    if address[0] == "(" and address[-1] == ")":
        if len(address.split()) > 1:
            offset, address2 = address[1:-1].split()
            return ram[int(ram[int(address2[1:-1])]) + int(offset)]
        else:
            return int(ram[int(address[1:-1])])
    return int(address)

# (5) -> ram[5] or 5 -> 5 or (-1 (12)) -> ram[12] + -1
def get_value2(address, ram) -> int:
    address = address.strip()
    if address[0] == "(" and address[-1] == ")":
        if len(address.split()) > 1:
            offset, address2 = address[1:-1].split()
            return int(ram[int(address2[1:-1])]) + int(offset)
        else:
            return int(ram[int(address[1:-1])])
    return int(address)

def int_to_bool(num):
    if num == 1:
        return True
    if num == 0:
        return False
    else:
        assert False, f"Unreachable in int_to_bool, bad num {num}"
    
def bool_to_int(b):
    return 1 if b else 0