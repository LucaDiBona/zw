"""
    prints a dict that matches words to their zero-width equivalent
"""

WORDS = ["SHL","SHR","BOR","BAND","BNOT","BXOR","EQ","PLUS","MINUS","TIMES","DIV","MOD","LESS","GREAT","INC","DEC","DROP","DROPN","PUT","IF","ELSE","ENDIF","WHILE","ENDWHILE","PRINT","INPUT","WRITE","READ","PROC","ENDPROC","VAR","RET"]
print(len(WORDS))
outputStr = "{"

def toZw(num:int) -> str:
    binStr = f"{num:b}"
    binStr = binStr.rjust(8,"0")
    outputStr = ""
    print(binStr)
    for i in range(4):
        letter = binStr[(2*i)] + binStr[(2*i)+1]
        if letter == "00":
            outputStr += "​"
            #outputStr += "A"
        elif letter == "01":
            outputStr += "‌"
            #outputStr += "B"
        elif letter == "10":
            outputStr += "‍"
            #outputStr += "C"
        elif letter == "11":
            outputStr += "⁠"
            #outputStr += "D"
    return(outputStr)


for i,val in enumerate(WORDS):
    outputStr += f'"{val}": "{toZw(i)}",'

outputStr = outputStr[:-1] + "}"

print(outputStr)