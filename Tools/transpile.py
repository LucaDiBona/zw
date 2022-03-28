import sys, re

"""
    Transpiles .zwt -> .zw
    Usage: transpile.py <input> <output>
"""

class InvalidTokenError(Exception):

    def __init__(self, *args: object) -> None:
        super().__init__(*args)

invalidTokens = []

CONVERSIONS = {"SHL": "​​​​","SHR": "​​​‌","BOR": "​​​‍","BAND": "​​​⁠","BNOT": "​​‌​","BXOR": "​​‌‌","EQ": "​​‌‍","PLUS": "​​‌⁠","MINUS": "​​‍​","TIMES": "​​‍‌","DIV": "​​‍‍","MOD": "​​‍⁠","LESS": "​​⁠​","GREAT": "​​⁠‌","INC": "​​⁠‍","DEC": "​​⁠⁠","DROP": "​‌​​","DROPN": "​‌​‌","PUT": "​‌​‍","IF": "​‌​⁠","ELSE": "​‌‌​","ENDIF": "​‌‌‌","WHILE": "​‌‌‍","ENDWHILE": "​‌‌⁠","PRINT": "​‌‍​","INPUT": "​‌‍‌","WRITE": "​‌‍‍","READ": "​‌‍⁠","PROC": "​‌⁠​","ENDPROC": "​‌⁠‌","VAR": "​‌⁠‍","RET": "​‌⁠⁠"}

def transpile(input:str) -> str:

    def toZw(n:int) -> str:
        if n < 0 or n > 255:
            raise ValueError("n must be between 0 and 255")
        binStr = bin(n)[2:]
        while len(binStr) < 8:
            binStr = "0" + binStr
        retStr = ""
        print(binStr)
        for i in range(4):
            binary = binStr[:2]
            if binary == "00":
                retStr += "​"
            elif binary == "01":
                retStr += "‌"
            elif binary == "10":
                retStr += "‍"
            elif binary == "11":
                retStr += "⁠"
            binStr = binStr[2:]
        return(retStr)

    words = re.split(r" |\n",input)
    outputStr = ""
    global invalidTokens
    invalidTokens = []
    for i,val in enumerate(words):
        print(val)
        if re.match(r"^'.'$",val):
            # char literal
            outputStr += toZw(ord(val[1:2])+128)
        elif re.match(r"^[0-9]+$",val):
            #int literal
            print(toZw(0) == toZw(1))
            outputStr += toZw(int(val))
        elif re.match(r"^#(.)+$",val):
            #commment
            pass
        else:
            try:
                outputStr += CONVERSIONS[val]
            except KeyError:
                invalidTokens.append(i)
    if invalidTokens == []:
        print(f"{len(outputStr)//4} commands produced")
        return(outputStr)
    else:
        raise InvalidTokenError(f"Tokens at positions {invalidTokens} invalid")

print(sys.argv)
f = open(sys.argv[1],"r")
inputText = f.read()
f.close()

f = open(sys.argv[2],"w")
try:
    f.write(transpile(inputText))
except InvalidTokenError:
    print(f"Tokens at positions {invalidTokens} invalid, did not produce an output file.")
f.close




