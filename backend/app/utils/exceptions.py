class UserNotFoundException(Exception):
    pass


class DuplicateException(Exception):
    pass


class DatabaseOperationException(Exception):
    pass


class InvalidCredentialsException(Exception):
    pass


class ValidationException(Exception):
    pass


class NotAuthorisedException(Exception):
    pass
