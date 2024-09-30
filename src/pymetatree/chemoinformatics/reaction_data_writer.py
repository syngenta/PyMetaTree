import logging
from abc import ABC, abstractmethod

from rdkit.Chem import AllChem, rdChemReactions

from pymetatree.chemoinformatics.reaction_data_error import ReactionDataError


class ReactionWriter(ABC):
    """Abstract base class for reaction data writers."""

    @abstractmethod
    def write(self, reaction: rdChemReactions) -> str:
        """Writes the RDKit reaction object to a string in a specific format.
        Args:
            reaction (rdChemReactions): The RDKit reaction object to be written.
        Returns:
            str: The reaction data in the specified format as a string.
        """
        pass


class WritesSmarts(ReactionWriter):
    """A reaction data writer for SMARTS format."""

    def write(self, reaction: rdChemReactions) -> str:
        """Writes the RDKit reaction object to a string in SMARTS format.
        Args:
            reaction (rdChemReactions): The RDKit reaction object to be written.
        Returns:
            str: The reaction data in SMARTS format as a string.
        Raises:
            ReactionDataError: If an error occurs while writing the reaction data.
        """
        try:
            if not reaction:
                raise ReactionDataError("Empty reaction object")
            return AllChem.ReactionToSmarts(reaction)
        except Exception as e:
            logging.error(f"Error while writing SMARTS data: {e}")
            raise ReactionDataError(f"Error while writing SMARTS data: {e}")


class WriteRxn(ReactionWriter):
    """A reaction data writer for RXN file format."""

    def write(self, reaction: rdChemReactions) -> str:
        """Writes the RDKit reaction object to a string in RXN file format.
        Args:
            reaction (rdChemReactions): The RDKit reaction object to be written.
        Returns:
            str: The reaction data in RXN file format as a string.
        Raises:
            ReactionDataError: If an error occurs while writing the reaction data.
        """
        try:
            if not reaction:
                raise ReactionDataError("Empty reaction object")
            return AllChem.ReactionToRxnBlock(reaction)
        except Exception as e:
            logging.error(f"Error while writing RXN data: {e}")
            raise ReactionDataError(f"Error while writing RXN data: {e}")
