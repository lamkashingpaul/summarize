from fastapi import HTTPException


class CustomHttpException(HTTPException):
    def __init__(self, status_code: int, detail: str):
        super().__init__(status_code=status_code, detail=detail)


class CustomDatabaseException(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class CustomDatabaseBadRequestException(CustomDatabaseException):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class CustomDatabaseNotFoundException(CustomDatabaseException):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)
