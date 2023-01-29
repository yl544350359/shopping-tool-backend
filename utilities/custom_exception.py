class TimeoutError(RuntimeError):
    def __init__(self,arg):
        self.arg=arg

class NoSupportError(RuntimeError):
    def __init__(self,arg):
        self.arg=arg

class InvalidUrlError(RuntimeError):
    def __init__(self,arg):
        self.arg=arg