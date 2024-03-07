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

class UnknownSocialNetworkError(BadRequestError):
    ...

class AuthorizationFailureError(BadRequestError):
    ...


NOT_FOUND_ERR = NotFoundError('Not found')
FORBIDDEN_ERR = ForbiddenError('Forbidden')
ALREADY_EXISTS = AlreadyExistsError('Already exists')
ALREADY_DONE = AlreadyDoneError('Already done')
UNKNOWN_SOCIAL_NETWORK = UnknownSocialNetworkError('Unknown social network')
AUTHORIZATION_FAILURE = AuthorizationFailureError('Authorization failure')
