# PyScript

## Table of Contents

1. [Introduction](#introduction)
2. [About The Project](#about-the-project)
    * [Parser](#parser)
    * [Interpreter](#interpreter)
    * [Assembler](#assembler)
    * [Compiler](#compiler)
    * [Computer](#computer)
3. [How to Use](#how-to-use)
3. [Syntax Overview](#syntax-overview)
    * [Declarations](#declarations)
    * [Functions](#functions)
    * [Body](#body)
    * [Commands](#commands)
    * [Values](#values)
4. [Examples](#examples)
    * [Echo](#echo)
    * [Factorial](#factorial)
    * [Palindromic Prime](#palindromic-prime)
5. [Formal Syntax](#formal-syntax)
6. [Formal Semantics](@formal-semantics)

## Introduction

A Sandbox is availible in repl.it: [sandbox](https://replit.com/@TansonL/PyScript#program.ps).

PyScript is a scripting language implemented in Python which can be both interpreted and compiled.
The syntax is easy to learn and has the core features of any programming language.
There are variables, functions, loops, conditionals, I/O, and comments.

## About the Project

This project is composed of several parts:

* **Parser**: parses the PyScript code and creates an AST (abstract syntax tree)
* **Interpreter**: interprets PyScript code
* **Assembler**: turns PyScript code into assembly
* **Compiler**: compiles assembly code into machine code
* **Computer**: simulates a computer by executing compiled code

### Parser

The parser takes the PyScript program and translates it into it's corresponding AST (abstract syntax tree).
This step is crucial in making the interpreter and assembler more simple.

### Interpreter

The interpreter takes the parsed PyScript program and runs it without any additional translation.

### Assembler

The assembler takes the parsed PyScript program and creates assembly code which represents the program.
This assembly code is custom assembly representing operations for a RISC (reduced instruction set computer) computer inspired by ARM.
The instruction set contains 24 instruction.
A snippet of assembly code follows:

```
BRCH _START_BODY
DATA number 0
LABEL _FUNCTION_increment_number
MOV (0 _STACK_POINTER) _RETURN_ADDRESS
ADD _STACK_POINTER _STACK_POINTER 1
MOV _RESULT number
MOV (0 _STACK_POINTER) _RESULT
ADD _STACK_POINTER _STACK_POINTER 1
MOV _RESULT 1
ADD _RESULT (-1 _STACK_POINTER) _RESULT
...
```

### Compiler

The compiler takes the custom assembled PyScript code and reduces it to machine code.
The machine code also uses custom op codes and instruction representation.
A snippet of compiled code follows:

```
000001 (0 (30)) (29)
001000 (30) (30) 1
000001 (28) (1)
000001 (0 (30)) (28)
001000 (30) (30) 1
000001 (28) 1
001000 (28) (-1 (30)) (28)
001001 (30) (30) 1
000001 (1) (28)
000001 (29) (-1 (30))
...
```

### Computer

Since the compiled code uses custom op codes and instructions, a custom computer simulator must be created.
This computer is a stored program computer meaning the instructions and data exist in the same memory.
The CPU uses a fetch-decode-execute cycle to interpret each instruction.

## How to Use

A version can be found on repl.it here: [https://replit.com/@TansonL/PyScript#.replit](https://replit.com/@TansonL/PyScript#.replit)

**Execute the program with Python3**

Usage through the command line is as follows:

```
Usage: main.py [file] [flag]

Flags:
    -interpret
    -compile
    -get-compiled [output_file]
    -get-assembled [output_file]
    -run-assembled
    -run-compiled

All Possibilities:
    main.py
    main.py -help
    main.py input_file
    main.py input_file -interpret
    main.py input_file -compile
    main.py input_file -get-compiled
    main.py input_file -get-assembled
    main.py input_file -get-compiled [output_file]
    main.py input_file -get-assembled [output_file]
    main.py input_file -run-assembled
    main.py input_file -run-compiled
```

The default mode is `-interpret` and the default file is `test.ps`.

## Syntax Overview

Every PyScript program is structured with 3 sections: declarations, functions, and body.

```
@declarations
... put declarations here
@declarations

@functions
... put functions here
@functions

@body
... put body here
@body
```

### Declarations

The declarations look like `declare <variable name> <number>`.
This declares the variable with the corresponding value.
For example, `declare counter 0` declares the variable called `counter` to `0`.
_Note: variables can only take on numerical values_

### Functions

The functions section allows for a list of subroutines which look like:

```
function <function name> {
    <function body>
}

function increment_counter {
    change counter !counter + 1!
}
```

This links `increment_counter` to the commands within the braces.

### Body

The body is the starting point of the program which is a list of commands which are
executed from top to bottom synchronously.

### Commands

| name      | example                 | expaination                                   |
| --------- | ----------------------- | --------------------------------------------- |
| `change`  | `change counter 100`    | Changes the variable `counter` to 100.        |
| `show`    | `show counter`          | Outputs the variable `counter`.               |
| `capture` | `capture height`        | Stores user input into the variable `height`. |
| `if`      | ``if \| height > 100 \| { show `tall` } { show `short` }`` | If statement. |
| `while`   | `while \| count > 0 \| { change count !count - 1! } `     | While loop. |
| `skip`    | `skip`                  | Does nothing.                                 |
| `run`     | `run increment_counter` | Runs the function `increment_counter`         |

### Values

**Numbers**

All numbers are integers.
All variables take on a number value.

Arithmetic can be performed on numbers with `+`, `-`, `*`, `/`, `%` which returns a number value.
The operation must be surrounded by `!`.
For example, `show !5 * 10!`

Comparisons can be performed on numbers with `=`, `<`, `>` which returns a boolean value
The comparison must be surrounded by `|`.
For example, `if |10 > 5| {...} {...}`

**Booleans**

Booleans are either true, false, or a boolean operation.

The binary boolean operations are `and` and `or`. The unary boolean operation is `not`.
These operations return a boolean and must be surrounded by `|`.
For example `||5 < 10| or |5 = 10||` and `|not false|`

### Comments

Comments can be added anywhere in the program. They start with `#~` and end with `~#`.
For example `#~ a comment is here ~#`.
_Note: comments cannot be nested_

## Examples

Many examples can be found in the repository in the programs folder

### Echo

A simple program which echos the value inputted.

```
@declarations
declare number 0
@declarations

@functions
@functions

@body
show `enter a number` #~ gets user input ~#
capture number
show number
@body
```

### Factorial

A program that determines the factorial of a number using a tail recursive technique.

```
@declarations
#~ factorial function variables ~#
declare factorial_number 0 #~ argument ~#
declare factorial_result 1 #~ return value ~#

#~ main body variables ~#
declare number 0
@declarations

@functions
function factorial {
    change factorial_result 1
    run factorial_helper
}

function factorial_helper {
    if |factorial_number > 1|
    {
        change factorial_result !factorial_result * factorial_number!
        change factorial_number !factorial_number - 1!
        run factorial_helper
    } {}
}

@functions

@body
show `enter a number`
capture number
change factorial_number number
run factorial
show factorial_result
@body
```

### Palidromic Prime

A program which determines if a number is a palindrome and a prime.

```
@declarations
#~ determine_prime variables ~#
declare d_prime_number 0 #~ argument ~#
declare d_prime_result 0 #~ return value ~#
declare d_prime_current 0 #~ internal variable ~#

#~ determine_palindrome variables ~#
declare d_palindrome_number 0 #~ argument ~#
declare d_palindrome_result 0 #~ return value ~#
declare d_palindrome_backwards 0 #~ internal variable ~#
declare d_palindrome_last_digit 0 #~ internal variable ~#
declare d_palindrome_number_copy 0 #~ internal variable ~#

#~ main body variables ~#
declare number 0
@declarations


@functions
function determine_prime {
    change d_prime_result 1
    change d_prime_current 2
    if |d_prime_number < 2| {
        change d_prime_result 0
    } {}
    while |d_prime_current < d_prime_number|
    {
        if |!d_prime_number % d_prime_current! = 0| {
            change d_prime_result 0
        } {}
        change d_prime_current !d_prime_current + 1!
    }
}

function determine_palindrome {
    change d_palindrome_number_copy d_palindrome_number
    change d_palindrome_backwards 0
    change d_palindrome_last_digit 0

    while |d_palindrome_number > 0|
    {
        change d_palindrome_last_digit !d_palindrome_number % 10!
        change d_palindrome_backwards !!d_palindrome_backwards * 10! + d_palindrome_last_digit!
        change d_palindrome_number !d_palindrome_number / 10!
    }
    if |d_palindrome_backwards = d_palindrome_number_copy|
    {
        change d_palindrome_result 1
    } {
        change d_palindrome_result 0
    }  
}
@functions


@body
show `enter a number` #~ gets user input ~#
capture number

change d_prime_number number
run determine_prime

change d_palindrome_number number
run determine_palindrome

if ||d_prime_result = 1| and |d_palindrome_result = 1||
{
    show `It is both a palindrome and a prime :)`
} {
    show `It is not a palindrome and a prime :(`
}
@body
```



## Formal Syntax

each program is of the form

```
@declarations
<declarations>
@declarations

@functions
<functions>
@functions

@body
<body>
@body
```

### Declarations

`<declarations>` is a list of declare statements where each declare statement is

```
declare <variable name> <simple value>
```

### Body

`<body>` is a list of `<command>`s

`<command>` is one of

-   `change <variable name> <value>`
-   `show <value>`
-   `capture <variable name>`
-   `if <boolean> { <body> } { <body> }`
-   `while <boolean> { <body> }`
-   `skip`
-   `run <function name>`

### Functions

`<functions>` is a list of `<function>`s

`<function>` is

```
function <function name> { <body> }
```

where `<function name>` is the name of the function

### Simple Values

`<simple value>` is one of

-   `<simple number>`: an integer
-   `<simple boolean>`: `true` or `false`
-   `<simple string>`: a string surrounded with "`"

### Values

`<value>` is one of

-   `<variable name>`
-   `<boolean>`
-   `<number>`
-   `<string>`

`<string>` is one of `<simple string>`

### Variable Names

`<variable name>` is a word which cannot contain any of

`!` `<` `>` `=` `` ` `` `+` `-` `*` `/` `"` `|` ` `

### Numbers

`<number>` is an expression which evaluates to a `<simple number>` and is one of

-   `<simple number>`
-   `!<number> <aop> <number>!`

where `<aop>` is one of `+` `-` `*` `/` `%`

### Booleans

`<boolean>` is an expression which evaluates to a `<simple boolean>` and is one of

-   `<simple boolean>`
-   `|<boolean> <bbop> <boolean>|`
-   `|<ubop> <boolean>|`
-   `|<number> <cmp> <number>|`

where

-   `<bbop>` is one of `and` `or`
-   `<uop>` is one of `not`
-   `<cmp>` is one of `=` `<` `>`

## Formal Semantics

#### `declare <variable name> <simple value>`

Initializes the variable `<variable name>` to the value `<simple value>`.

#### `change <variable name> <value>`

`<variable name>` must already be declared in the `<declarations>`.
Redefines `<variable name>` to the result of evaluating `<value>`.

#### `show <value>`

Evaluates then outputs `<value>` to the user.

#### `capture <variable name>`

`<variable name>` must already be declared in the `<declarations>`.
Takes integer input from the user as and redefines `<variable name>` to this value.

#### `if <boolean> { <command> ... } { <command> ... }`

Evaluates `<boolean>` and if it's `true`, executes the first block of commands, otherwise it executes the second block of commands.

#### `while <boolean> { <command> ... }`

Evaluates `<boolean>` and executes the block of commands if it is `true`. Then it continues to re-evaluate `<boolean>` and the block of commands until `<boolean>` is `false`.

#### `skip`

Does nothing. Is a NOP.

#### `run <command name>`

Runs the command `<command name>`
