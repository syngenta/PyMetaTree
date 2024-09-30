class ReactionDataError(Exception):
    """Custom exception for errors related to reaction data processing."""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
