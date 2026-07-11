class AppException(Exception):
    pass


class BadRequestException(AppException):
    pass


class NotFoundException(AppException):
    pass


class UnauthorizedException(AppException):
    pass


class ConflictException(AppException):
    pass