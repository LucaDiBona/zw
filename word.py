
def wordToInt(word:str) -> int:
        if len(word) != 4:
            raise ValueError(f"Expected word of length 4, got word of length {len(word)}")
        binStr = ""
        for i in word:
            if i == "​":
               binStr += "00"
            elif i == "‌":
                binStr += "01"
            elif i == "‍":
                binStr += "10"
            elif i == "⁠":
                binStr += "11"
            else:
                print("ERROR - INVALID CHAR")
        return(int(binStr,2))

def getCat(word:int) -> str:
    if word <= 5:
        return("BIN")
    elif word <= 12:
        return("MATHS")
    elif word <= 18:
        return("STACK")
    elif word <= 23:
        return("BRANCH")
    elif word <= 27:
        return("IO")
    elif word <= 29:
        return("PROC")
    elif word == 30:
        return("VAR")
    elif word == 31:
        return("RET")
    else:
        return("NO_CMD")

class Word():

    def __init__(self,lexeme:str) -> None:
        self.lexeme = lexeme
        self.val = wordToInt(lexeme)
        self.cat = getCat(self.val)
        self.jumpTo = None #used for IF etc.
        self.targeted = False

