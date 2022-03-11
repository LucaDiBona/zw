class InvalidWordErr(Exception):

    def __init__(self,message="Invalid Word"):
        self.message = message
        super().__init__(self.message)

class TargetNotFoundErr(Exception):

    def __init__(self,message="Target not found"):
        self.message = message
        super().__init__(self.message)