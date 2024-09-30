"""
Module: test_reaction_writers.py
This module contains test cases for the reaction data writer classes.
"""

import pytest
from rdkit.Chem import rdChemReactions

from pymetatree.chemoinformatics.reaction_data_writer import (
    ReactionDataError,
    WriteRxn,
    WritesSmarts,
)


class TestReactionWriters:
    """Test cases for the reaction data writer classes."""

    def test_writes_smarts(self):
        """Test the write method for WritesSmarts with a valid reaction object.

        Args:
            None

        Returns:
            None
        """
        reaction = rdChemReactions.ReactionFromSmarts("[C:1]>>[C:1](Cl)")
        writer = WritesSmarts()
        result = writer.write(reaction)
        assert isinstance(result, str)
        assert result != ""

    def test_writes_rxn(self):
        """Test the write method for WriteRxn with a valid reaction object.

        Args:
            None

        Returns:
            None
        """
        reaction = rdChemReactions.ReactionFromSmarts("[C:1]>>[C:1](Cl)")
        writer = WriteRxn()
        result = writer.write(reaction)
        assert isinstance(result, str)
        assert result != ""

    def test_empty_reaction_error_smarts(self):
        """Test the behavior of WritesSmarts when writing an empty reaction.

        Args:
            None

        Returns:
            None
        """
        writer = WritesSmarts()
        with pytest.raises(ReactionDataError):
            writer.write(None)

    def test_empty_reaction_error_rxn(self):
        """Test the behavior of WriteRxn when writing an empty reaction.

        Args:
            None

        Returns:
            None
        """
        writer = WriteRxn()
        with pytest.raises(ReactionDataError):
            writer.write(None)
