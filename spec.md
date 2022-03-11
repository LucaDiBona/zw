# Basics

## Words

## Types

Strings are stored as ascii + 128
# Commands

## Binary Operators

SHL (0):
x y -> (x<<y)

SHR (1):
x y -> (y>>x)

BOR (2):
x y -> (x&y)

BAND (3):
x y -> (x|y)

BNOT (4):
x -> ~x

BXOR (5):

x y -> x^y

EQ (6):
x y -> 0|1
Adds 0 to the stack if and y are different, else adds 1

## Arithmetic

PLUS (7):
x y -> (x+y)

MINUS (8):
x y -> (x-y)

TIMES (9):
x y -> (x*y)

DIV (10):
x y -> (x/y)

Returns the quotient, with any remainder ignored

MOD (11):
x y -> (x%y)

Produces an error for y<1

LESS (12):
x y -> x < y

GREAT (13):
x y -> x > y

INC (14):
x -> (x++)

DEC (15):
x -> (x--)

## Stack Operations

DROP (16):
x y -> x

DROPN (17):

x y z 2 -> x

PUT (18):

Treats the following word as an 8-bit integer and add to the stack

## Conditionals and Loops

IF (19) ... ELSE (20) ... ENDIF (21)
-?->

If the top of the stack is non-zero, perform the first set of code.
Optionally if not perform the second set, then goto ENDIF

WHILE (22) ... ENDWHILE (23)
-?->

If the top of the stack is non-zero, perform code and repeat this until the top of the stack is 0

## Interaction

PRINT (24):
x ->

Prints x to the console in the current mode

INPUT (25):
-> x

Takes input from the user in the current mode


WRITE (26):
x y ->

Writes to a file in the current mode with the file always in ascii. If the filename is 0 uses a buffer "file"

READ (27):
x -> y

Reads a whole file in the current mode


## Procedures

PROC (28) <WORD>... ENDPROC (29)
->

Defines a new procedure. The code is one word and is used to call the procedure, and must be in the range 64-127

StdLib defines procs in the range 128-191, although these can be overidden

## Variables

VAR (30) <WORD>
-> x

Defines a new variable. The code is one word and is used to put the value of the variable on the stack, and must usually be in the range 192-255. Variables can be redefined (this is in fact the only way they can be changed)

### Reserved values

The variables in the range 32-63 are reserved. They are explained below, including defaults and if they can be reassigned to a new value (r) or if this gives an error (nothing):

32 IOMODE=0 (r):
If 0, use binary input and output
If nonzero, use ascii

48-63 RESERVED (r):
Reserved for stdlib procs to use although these can be overriden, stdlib procs may change them

## Return

RET (31)

If in a procedure, ends procedure.

If not in procedure, end execution and return the top of the stack as the output.