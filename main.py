# from parsing.parse import parse
from interpreter import interpret
from parsing.parse import parse
from parsing.print_parsed import print_body

def main():
    declarations, functions, program = parse("programs/factorial.ps")
    interpret(declarations, functions, program)

if __name__ == "__main__":
    main()
