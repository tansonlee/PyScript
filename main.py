import sys
from compiler.computer import execute_machine_code

from interpreter.interpreter import interpret
from parsing.parse import parse
from compiler.assembler import assemble
from compiler.compiler import compile

"""
[file] is a file name
[mode] is either -interpret for "interpret" or -compile for "compile"

python3 main.py
python3 main.py [file]
python3 main.py [file] [mode]

python3 main.py [file] -get-compiled
python3 main.py [file] -get-assembled

python3 main.py [file] -get-compiled [file]
python3 main.py [file] -get-assembled [file]

python3 main.py -run-assembled [file]
python3 main.py -run-compiled [file]

python3 main.py [file] [flag]

flags:
* -interpret [file]
* -compile [file]
* -get-compiled [file]
* -get-assembled [file]
* -run-assembled file
* -run-compiled file

"""

def usage(program):
    print(f"""
For more information, visit:
    https://github.com/tansonlee/PyScript

Usage: {program} [file] [flag]

Flags:
    -interpret             
    -compile
    -get-compiled [output_file]
    -get-assembled [output_file]
    -run-assembled
    -run-compiled

All Possibilities:
    {program}
    {program} -help
    {program} input_file
    {program} input_file -interpret
    {program} input_file -compile
    {program} input_file -get-compiled
    {program} input_file -get-assembled
    {program} input_file -get-compiled [output_file]
    {program} input_file -get-assembled [output_file]
    {program} input_file -run-assembled
    {program} input_file -run-compiled
    """)


def main():
    inputFile = "test.ps"
    outputFile = ""
    mode = "-interpret" # interpret or compile or run assembled or run compiled

    if len(sys.argv) == 2:
        if sys.argv[1] == "-help":
            usage(sys.argv[0])
            return
        inputFile = sys.argv[1]
    if len(sys.argv) == 3:
        inputFile = sys.argv[1]
        mode = sys.argv[2]
    if len(sys.argv) == 4:
        inputFile = sys.argv[1]
        mode = sys.argv[2]
        outputFile = sys.argv[3]
    
    if mode == "-run-assembled":
        f = open(inputFile, "r")
        compiled = compile(f.read().split("\n"))
        execute_machine_code(compiled)
        f.close()
        return
    elif mode == "-run-compiled":
        f = open(inputFile, "r")
        execute_machine_code(f.read().split("\n"))
        f.close()
        return
    
    declarations, functions, program = parse(inputFile)
    if mode == "-interpret":
        interpret(declarations, functions, program)
    elif mode == "-compile":
        assembled = assemble(declarations, functions, program)
        compiled = compile(assembled)
        execute_machine_code(compiled)
    elif mode == "-get-assembled":
        assembled = "\n".join(assemble(declarations, functions, program))
        if outputFile == "":
            print(assembled)
        else:
            f = open(outputFile, "w")
            f.write(assembled)
            f.close()
    elif mode == "-get-compiled":
        assembled = assemble(declarations, functions, program)
        compiled = "\n".join(compile(assembled))
        if outputFile == "":
            print(compiled)
        else:
            f = open(outputFile, "w")
            f.write(compiled)
            f.close()
    else:
        print("Invalid flag: " + mode)

if __name__ == "__main__":
    main()

