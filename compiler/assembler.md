Assembly language

[x] ADD <destination> <source 1> <source 2>
[x] SUB <destination> <source 1> <source 2>
[x] MUL <destination> <source 1> <source 2>
[x] DIV <destination> <source 1> <source 2>
[x] MOD <destination> <source 1> <source 2>

[x] EQ <destination> <source 1> <source 2>
[x] NE <destination> <source 1> <source 2>
[x] GT <destination> <source 1> <source 2>
[x] LT <destination> <source 1> <source 2>

[x] AND <destination> <source 1> <source 2>
[x] ORR <destination> <source 1> <source 2>
[x] NOT <destination> <source 1> <source 2>

[x] BRCH <location>
[x] CBZR <source> <location>
[x] CBNZ <source> <location>
[x] BLNK <destination> <location>

[x] READ <source>
[x] PVAL <source>
[x] PSTR <string>

[x] MOV <destination> <source>
[x] HALT

[x] LABEL <name>
[ ] CONST <name> <number> // <name> is replacable by <number> anywhere
[x] DATA <name> <source>  // <name> is replacable by its address and this line compiles to the value of <source>

```
6: ...
7: DATA var 99
8: ...

(-9 var) # references the number var holds minus 9: 90
var      # references the address of var: 7

```
(0 var): references the value that 

Assembled Program Structure:

```
BRCH _START_BODY        # begin at _START_BODY
...assembled_declarations
...assembled_functions
LABEL _START_BODY
...assembled_body
LABEL _HALT_LABEL       # branch here to halt
HALT
DATA _RESULT            # store intermediate and final results
DATA _RETURN_ADDR
DATA _STACK_PTR         # pointer to the top of the stack
LABEL _STACK            # start of stack
```


Assembled Declarations:

each declaration `Declare(var1, val1)`, `Declare(height, 180)` becomes

```
DATA var1 val1
DATA height 180
```

Assembled Functions:

each function `Function(name, body)` `Function(add1, add1_body)` becomes

```
LABEL _FUNCTION_name
...assembled body
BRCH some return address

LABEL _FUNCTION_add1
...assembled add1_body
BRCH some return address
```

Assembled Body:

[x] Change
[x] Show
[x] Capture
[x] If
[x] While
[x] Skip
[x] Run

`Change(var, val)`

```
...assembled compute val (stored at _RESULT)
MOV var _RESULT
```

`Show(val)`

where val is a non-string value
```
...assembled compute val (stored at _RESULT)
PVAL _RESULT
```
where val is a string
```
PSTR val
```

`Capture(var)`

```
READ var
```

`If(cond, true_body, false_body)`

```
...assembled compute cond (stored at _RESULT)
CBNZ _RESULT <true label>
BRCH <false label>
LABEL <true label>
...assembled true_body
BRCH <end label>
LABEL <false label>
...assembled false_body
BRCH <end label>
LABEL <end label>
```


`While(cond, body)`

```
LABEL <top label>
...assembled compute cond (stored at _RESULT)
CBNZ _RESULT <body label>
BRCH <end label>
LABEL <body label>
...assembled body
BRCH <top label>
LABEL <end label>
```

`Skip`

```
<nothing>
```

`Run(function)`

```
BLNK _RETURN_ADDR _FUNCTION_function
```

