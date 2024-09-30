import logging
from abc import ABC, abstractmethod

from rdkit.Chem import AllChem, rdChemReactions

from pymetatree.chemoinformatics.reaction_data_error import ReactionDataError


class ReactionReader(ABC):
    """Abstract base class for reaction data readers."""

    @abstractmethod
    def read(self, reaction: str) -> rdChemReactions:
        """Reads the reaction data and returns an rdChemReactions object.

        Args:
            reaction (str): The input reaction data.

        Returns:
            rdChemReactions: The parsed reaction data as an rdChemReactions object.
        """
        pass


class ReadSmarts(ReactionReader):
    """A reaction data reader for SMARTS format."""

    def read(self, reaction: str) -> rdChemReactions:
        """Reads the reaction data in SMARTS format and returns an rdChemReactions object.

        Args:
            reaction (str): The input reaction data in SMARTS format.

        Returns:
            rdChemReactions: The parsed reaction data as an rdChemReactions object.

        Raises:
            ReactionDataError: If an error occurs while reading the reaction data.
        """
        try:
            if not reaction:
                raise ReactionDataError("Empty SMARTS string")
            return AllChem.ReactionFromSmarts(reaction)
        except Exception as e:
            logging.error(f"Error while reading SMARTS data: {e}")
            raise ReactionDataError(f"Error while reading SMARTS data: {e}")


class ReadRxn(ReactionReader):
    """A reaction data reader for RXN file format."""

    def read(self, reaction: str) -> rdChemReactions:
        """Reads the reaction data in RXN file format and returns an rdChemReactions object.

        Args:
            reaction (str): The input reaction data in RXN file format.

        Returns:
            rdChemReactions: The parsed reaction data as an rdChemReactions object.

        Raises:
            ReactionDataError: If an error occurs while reading the reaction data.
        """
        try:
            if not reaction:
                raise ReactionDataError("Empty RXN string")
            return AllChem.ReactionFromRxnFile(reaction)
        except Exception as e:
            logging.error(f"Error while reading RXN data: {e}")
            raise ReactionDataError(f"Error while reading RXN data: {e}")
