## Syntax

each program is of the form

```
@declarations
<declaration>
...
@declarations

@functions
<function>
...
@functions

@body
<body>
...
@body
```

### Declarations

`declare <variable name> <simple value>` gets parsed into

```
declaration {
    "name": <variable name>,
    "type": typeof(<simple value>),
    "value": <simple value>
}
```

### Body

```
command {
    "command": <command>
    "content": <command content>
}
```

`change <variable name> <value>` gets parsed into

```
change {
    "variable": <variable name>,
    "value": parse_value(<value>)
}
```

`show <value>` gets parsed into

```
show {
    "value": parse_value(<value>)
}
```

`capture <variable name>` gets parsed into

```
capture {
    "variable": <variable name>
}
```

`if <boolean> { <command> ... } { <command> ... }`

```
if {
    "condition": <boolean>,
    "true_part": <true commands>,
    "false_part": <false commands>
}
```

`while <boolean> { <command> ... }`

```
while {
    "condition": <boolean>,
    "body": <commands>
}
```

`skip`

```
skip {}
```

### Functions

### Simple Values

`<simple value>` is one of

-   `<simple number>`: an integer
-   `<simple boolean>`: `true` or `false`
-   `<simple string>`: a string surrounded with "`"

### Values

`<value>`

```
value {
    "type": <a type of value (1 of 4)>,
    "value": <values struct>
}
```

-   `<variable name>`

```
variable {
    "name": <variable name>
}
```

-   `<boolean>`

```
boolean {
    "type": <boolean type>,
    ...
    "operation",
    "compare",
    "left",
    "right",
    "content":
}
```

-   `<number>`
-   `<string>`

`<string>` is one of `<simple string>`

### Variable Names

`<variable name>` is a word which cannot contain any of

`!` `<` `>` `=` ``\` `+` `-` `*` `/` `"` `|` ` `

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
