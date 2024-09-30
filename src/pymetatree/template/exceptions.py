class RDChiralInputError(Exception):
    """Exception raised for errors in the input to RDChiralTemplateExtractorInput."""
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class RDChiralExtractionError(Exception):
    """Exception raised for errors during the extraction process."""
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class RDChiralDataCreationError(Exception):
    """Exception raised for errors in creating RDChiral data."""
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class TemplateConstructionError(Exception):
    """Exception raised for errors in creating Template."""
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class TemplateFormatError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class BluePrintPatternError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
