class BufferError(Exception):

    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class Buffer():

    def __init__(self) -> None:
        self.contents = ""
        self.mode = ("r","t")
        self.isOpen = False

    def open(self,mode:str):
        if len(mode) != 2 or mode[0] not in "rawx" or mode[1] not in "tb":
            raise BufferError("Invalid mode")
        elif mode[0] == "x":
            raise BufferError("Create mode not supported for buffer")

        self.mode = (mode[0], mode[1])
        self.isOpen = True

    def close(self):
        self.isOpen = False

    def write(self,text:str):
        if not self.isOpen:
            raise BufferError("Buffer closed")
        if self.mode[0] == "r":
            raise BufferError("File opened as read only")
        elif self.mode[0] == "a":
            self.contents += text
        elif self.mode[0] == "w":
            self.contents = text

    def read(self):
        if not self.isOpen:
            raise BufferError("Buffer closed")
        return(self.contents)

