import sys, re

"""
    Transpiles .zwt -> .zw
    Usage: transpile.py <input> <output>
"""

CONVERSIONS = {"SHL": "​​​​","SHR": "​​​‌","BOR": "​​​‍","BAND": "​​​⁠","BNOT": "​​‌​","BXOR": "​​‌‌","EQ": "​​‌‍","PLUS": "​​‌⁠","MINUS": "​​‍​","TIMES": "​​‍‌","DIV": "​​‍‍","MOD": "​​‍⁠","LESS": "​​⁠​","GREAT": "​​⁠‌","INC": "​​⁠‍","DEC": "​​⁠⁠","DROP": "​‌​​","DROPN": "​‌​‌","PUT": "​‌​‍","IF": "​‌​⁠","ELSE": "​‌‌​","ENDIF": "​‌‌‌","WHILE": "​‌‌‍","ENDWHILE": "​‌‌⁠","PRINT": "​‌‍​","INPUT": "​‌‍‌","WRITE": "​‌‍‍","READ": "​‌‍⁠","PROC": "​‌⁠​","ENDPROC": "​‌⁠‌","VAR": "​‌⁠‍","RET": "​‌⁠⁠"}

def transpile(input:str) -> str:
    words = re.split(r" |\n",input)
    outputStr = ""
    for i in words:
        outputStr += CONVERSIONS[i]
    print(len(outputStr))
    return(outputStr)

print(sys.argv)
f = open(sys.argv[1],"r")
inputText = f.read()
f.close()

f = open(sys.argv[2],"w")
f.write(transpile(inputText))
f.close




