class InvalidSmilesError(Exception):
    """
    Custom exception raised when an invalid SMILES string is encountered.
    """
    pass


class SubstructureSearchError(Exception):
    """
    Custom exception raised when an error occurs during the substructure search process.
    """
    pass
