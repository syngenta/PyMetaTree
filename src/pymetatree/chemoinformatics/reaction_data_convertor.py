from abc import ABC, abstractmethod

from pymetatree.chemoinformatics.reaction_data_reader import ReadRxn, ReadSmarts
from pymetatree.chemoinformatics.reaction_data_writer import WriteRxn, WritesSmarts


class ReactionDataConvertor(ABC):
    """Abstract base class for reaction data converters."""

    @abstractmethod
    def convert(self, reaction: str) -> str:
        """Converts the input reaction data to a different format.

        Args:
            reaction (str): The input reaction data to be converted.

        Returns:
            str: The converted reaction data in the new format.
        """
        pass


class ConvertRxnToSmarts(ReactionDataConvertor):
    """Converts reaction data from RXN format to SMARTS format."""

    def convert(self, reaction: str) -> str:
        """Converts the input reaction data from RXN format to SMARTS format.

        Args:
            reaction (str): The input reaction data in RXN format.

        Returns:
            str: The converted reaction data in SMARTS format.
        """
        rxn_reader = ReadRxn()
        smarts_writer = WritesSmarts()
        rxn = rxn_reader.read(reaction)
        return smarts_writer.write(rxn)


class ConvertSmartsToRxn(ReactionDataConvertor):
    """Converts reaction data from SMARTS format to RXN format."""

    def convert(self, reaction: str) -> str:
        """Converts the input reaction data from SMARTS format to RXN format.

        Args:
            reaction (str): The input reaction data in SMARTS format.

        Returns:
            str: The converted reaction data in RXN format.
        """
        smart_reader = ReadSmarts()
        rxn_writer = WriteRxn()
        smarts = smart_reader.read(reaction)
        return rxn_writer.write(smarts)
