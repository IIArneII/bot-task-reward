class ServiceError(Exception):
    ...

class NotFoundError(ServiceError):
    ...

class ForbiddenError(ServiceError):
    ...

class BadRequestError(ServiceError):
    ...

class AlreadyExistsError(BadRequestError):
    ...

class AlreadyDoneError(BadRequestError):
    ...


NOT_FOUND_ERR = NotFoundError('Not found')
FORBIDDEN_ERR = ForbiddenError('Forbidden')
ALREADY_EXISTS = AlreadyExistsError('Already exists')
ALREADY_DONE = AlreadyDoneError('Already done')
