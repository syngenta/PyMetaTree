class ExceptionRxnStringFormatInvalid(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message


class ExceptionMolStringFormatInvalid(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message


class ExceptionRdrxnStringFormatInvalid(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message


class ExceptionHashing(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message
