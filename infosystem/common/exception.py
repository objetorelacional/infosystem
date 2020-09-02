
class InfoSystemException(Exception):

    status = 500
    message = ''

    def __init__(self, message=None):
        if message is not None:
            self.message = message


class NotFound(InfoSystemException):

    status = 404
    message = 'Entity not found'


class DuplicatedEntity(InfoSystemException):

    status = 404
    message = 'Entity already exists'


class BadRequest(InfoSystemException):

    status = 400
    message = 'Provided body does not represent a valid entity'


class OperationBadRequest(InfoSystemException):

    status = 400
    message = 'Provided body does not provide ' + \
        'valid info for performing operation'


class BadRequestContentType(BadRequest):

    message = 'Content-Type header must be application/json'


class PreconditionFailed(BadRequest):

    message = 'One or more preconditions failed'


class FatalError(InfoSystemException):

    message = 'FATAL ERROR'
