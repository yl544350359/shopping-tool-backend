class TimeoutError(RuntimeError):
    def __init__(self,arg):
        self.arg=arg