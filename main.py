from execeptions import *
from word import Word
from buffer import Buffer
import sys

WORDS = ["SHL","SHR","BOR","BAND","BNOT","BXOR","EQ","PLUS","MINUS","TIMES","DIV","MOD","LESS","GREAT","INC","DEC","DROP","DROPN","PUT","IF","ELSE","ENDIF","WHILE","ENDWHILE","PRINT","INPUT","WRITE","READ","PROC","ENDPROC","VAR","RET"]

RESERVED_VARS = {"IOMODE" : 32,"WRITEMODE": 33}

DEFAULT_RESERVED_VARS = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

DEBUG = False # prints the stack at every step

buffer = Buffer()
#TODO flag

def parse(text:str) -> list:

    def seek(target:str,pos:int) -> int:

        i = len(comList) - 1

        while i > pos  and (WORDS[comList[i].val] != target or comList[i].targeted):
            i -= 1

        if i <= pos:
            raise TargetNotFoundErr()
        return(i)

    def target(target:int) -> int:
        comList[target].targeted = True
        return(target)

    comList = []
    if len(text) % 4 != 0:
        print("ERROR")
    for i in range(int(len(text)/4)):
        comList.append(Word(text[i*4:i*4+4]))

    for i,val in enumerate(comList):
        if val.cat in ["BRANCH","RET"]:
            if WORDS[val.val] == "IF":
                try:
                    val.jumpTo = target(seek("ELSE",i))
                except TargetNotFoundErr:
                    val.jumpTo = target(seek("ENDIF",i))
            elif WORDS[val.val] == "ELSE":
                val.jumpTo = target(seek("ENDIF",i))
            elif WORDS[val.val] == "WHILE":
                val.jumpTo = target(seek("ENDWHILE",i))
                comList[target].jumpTo = i
            elif WORDS[val.val] == "RET":
                try:
                    val.jumpTo = target(seek("ENDPROC",i))
                except TargetNotFoundErr:
                    val.jumpTo = -1 #end execution

    return(comList)


def interpret(comList:list) -> str:

    # get command line arguments to put on the stack
    stack = sys.argv

    stack.pop(0)
    stack.pop(0)

    for i,val in enumerate(stack):
        stack[i] = int(val) #TODO convert ascii input automatically?

    if DEBUG:
        print(stack)

    procs = []
    for i in range(128):
        procs.append([])

    def getProc(n:int) -> list:
        if n < 64 or n > 191:
            print("ERROR - PROC OUT OF RANGE")
        return(procs[n-64])

    def setProc(n:int,val:list) -> None:
        if n < 64 or n > 191:
            print("ERROR - PROC OUT OF RANGE")
        procs[n-64] = val

    reservedVars = DEFAULT_RESERVED_VARS
    vars_ = []
    for i in range(64):
        vars_.append(0)


    def getVar(n:int) -> int:
        if n >= 192:
            if n > 255:
                print("ERROR - VAR OUT OF RANGE")
            return(vars_[n-128])
        elif n > 31 and n < 64:
            return(reservedVars[n-32])
        else:
            print("ERROR - VAR OUT OF RANGE")

    def setVar(n:int,val:int) -> None:
        if DEBUG:
            print((n,val))
        if n >= 128:
            if n > 255:
                print("ERROR - VAR OUT OF RANGE")
            vars_[n-128] = val
        elif n > 31 and n < 64:
            reservedVars[n-32] = val
        else:
            print("ERROR - VAR OUT OF RANGE")

    bufferFile = 0

    def toAsciiStr(n:int) -> str:
        size = 1
        while n > 2**(8*size):
            size += 1

        outputStr = ""


        for i in range(size):
            letter = n >> (8*((size-i)-1))
            if DEBUG:
                print(letter - 128)
                print(chr(letter - 128))
            outputStr += chr(letter - 128)
            n = n - (letter * (2**(8*((size-i)-1))))

        return(outputStr)

    def fromAsciiStr(str:str) -> int:

        acc = 0

        for i,val in enumerate(str):
            acc += (ord(val)+128)
            acc = acc*256

        return(acc >> 8)

    def evalWord(i:int,wordObj) -> None:

        try:
            word = WORDS[wordObj.val]
        except IndexError:
            raise ValueError("Expected instruction token")

        if word == "SHL":
            b = stack.pop()
            a = stack.pop()
            stack.append(a<<b)

        elif word == "SHR":
            b = stack.pop()
            a = stack.pop()
            stack.append(a>>b)

        elif word == "BOR":
            b = stack.pop()
            a = stack.pop()
            stack.append(a|b)

        elif word == "BAND":
            b = stack.pop()
            a = stack.pop()
            stack.append(a&b)

        elif word == "BNOT":
            a = stack.pop()
            stack.append(~a)

        elif word == "BXOR":
            b = stack.pop()
            a = stack.pop()
            stack.append(a^b)

        elif word == "EQ":
            b = stack.pop()
            a = stack.pop ()
            if a == b:
                stack.append(1)
            else:
                stack.append(0)

        elif word == "PLUS":
            b = stack.pop()
            a = stack.pop()
            stack.append(a+b)

        elif word == "MINUS":
            b = stack.pop()
            a = stack.pop()
            stack.append(a-b)

        elif word == "TIMES":
            b = stack.pop()
            a = stack.pop()
            stack.append(a*b)

        elif word == "DIV":
            b = stack.pop()
            a = stack.pop()
            stack.append(int(a/b))

        elif word == "MOD":
            b = stack.pop()
            a = stack.pop()
            stack.append(a%b)

        elif word == "LESS":
            b = stack.pop()
            a = stack.pop()
            stack.append(int(a<b))

        elif word == "GREAT":
            b = stack.pop()
            a = stack.pop()
            stack.append(int(a>b))

        elif word == "INC":
            a = stack.pop()
            stack.append(a+1)

        elif word == "DEC":
            a = stack.pop()
            stack.append(a-1)

        elif word == "DROP":
            stack.pop()

        elif word == "DROPN":
            n = stack.pop()
            while n > 0:
                stack.pop()
                n -= 1

        elif word == "PUT":
            if DEBUG:
                print(comList[i+1].val)
            stack.append(comList[i+1].val)
            return(i+2)

        elif word == "IF":
            condition = stack.pop()
            if condition != 0:
                return(None)
            else:
                return(comList[i].jumpTo + 1)

        elif word == "ELSE":
            return(comList[i].jumpTo + 1)

        elif word == "ENDIF":
            pass

        elif word == "WHILE":
            condition = stack.pop()
            if condition != 0:
                return(comList.jumpTo + 1)
            else:
                return(None)

        elif word == "PRINT":
            if DEBUG:
                print("print")
                print(getVar(32))

            a = stack.pop()

            if getVar(RESERVED_VARS["IOMODE"]) == 0:
                pass

            else:
                if DEBUG:
                    print(f"PRINTING {a}")
                print(toAsciiStr(a))

        elif word == "INPUT":
            a = input()

            if reservedVars[RESERVED_VARS["IOMODE"]] == 0:
                stack.append(fromAsciiStr(a))

        elif word == "WRITE":

            fileName = toAsciiStr(stack.pop())
            contents = toAsciiStr(stack.pop())

            writeMode = getVar(RESERVED_VARS["WRITEMODE"])
            ioMode = getVar(RESERVED_VARS["IOMODE"])

            if writeMode == 0:
                mode = "a"
            elif writeMode > 0:
                mode = "w"
            else:
                mode = "x"
            if ioMode == 0:
                mode += "b"
            else:
                mode += "t"

            if fileName == 0:
                f = buffer
                f.open(mode)
            else:
                f = open(fileName,mode)

            f.write(contents)
            f.close()


        elif word == "READ":

            fileName = toAsciiStr(stack.pop())

            if getVar(RESERVED_VARS["IOMODE"]) == 0:
                mode = "rb"
            else:
                mode = "rt"

            if fileName == 0:
                f = buffer
                f.open(mode)
            else:
                f = open(fileName,mode)

            stack.append(fromAsciiStr(f.read()))
            f.close()


        elif word == "PROC":
            pass

        elif word == "ENDPROC":
            pass

        elif word == "VAR":
            if DEBUG:
                print(stack)
            a = stack.pop()
            setVar(comList[i+1].val,a)
            if DEBUG:
                print(vars_)
                print(reservedVars)
            return(i+2)

        elif word == "RET":
            pass

        if DEBUG:
            print(stack)


    i = 0
    while i < len(comList):
        try:
            target = evalWord(i,comList[i])
        except ValueError:
            print(f"Expected instruction token at {i}")
            break
        if target == None:
            i+= 1
        else:
            i = target


f = open(sys.argv[1],"r")
code = f.read()
f.close()

interpret(parse(code))
