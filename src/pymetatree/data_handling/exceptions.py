class DBConnectionError(Exception):
    """Base class for database connection errors."""
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class InvalidHostInstanceError(DBConnectionError):
    """Raised when an invalid host instance is passed."""


class InvalidPackageURLError(DBConnectionError):
    """Raised when an invalid package URL is passed."""


class NetworkError(DBConnectionError):
    """Raised when a network-related error occurs."""


class DataHandlerError(Exception):
    """Base class for DataHandler exceptions."""

    def __init__(self, message):
        self.message = message
        super().__init__(message)


class MappingError(DataHandlerError):
    """Exception raised for errors related to mapping operations."""


class DiskError(DataHandlerError):
    """Exception raised for errors related to disk operations."""


class TemplateError(DataHandlerError):
    """Exception raised for errors related to template construction."""


class InvalidDataError(Exception):
    """Raised when input data is invalid."""

    def __init__(self, message):
        self.message = message
        super().__init__(message)


class ResourceNotFoundError(Exception):
    """Raised when a required resource is not found."""

    def __init__(self, message):
        self.message = message
        super().__init__(message)


class LimitExceededError(Exception):
    """Raised when a limit is exceeded."""

    def __init__(self, message):
        self.message = message
        super().__init__(message)


class LoggingError(Exception):
    """Raised when an error occurs during logging."""

    def __init__(self, message):
        self.message = message
        super().__init__(message)
