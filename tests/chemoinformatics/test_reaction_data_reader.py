"""
Module: test_reaction_data_reader.py
This module contains test cases for the reaction data reader classes.
"""

from unittest.mock import MagicMock, patch

import pytest
from rdkit.Chem import rdChemReactions

from pymetatree.chemoinformatics.reaction_data_reader import (
    ReactionDataError,
    ReadRxn,
    ReadSmarts,
)


class TestReadSmarts:
    """
    Test cases for the ReadSmarts class.
    """

    @patch("rdkit.Chem.AllChem.ReactionFromSmarts")
    def test_read_valid_smarts(self, mock_reaction_from_smarts):
        """
        Test the read method with valid SMARTS data.

        Args:
        - mock_reaction_from_smarts: MagicMock object for ReactionFromSmarts

        Returns:
        - None
        """
        smarts_data = "[C:1]>>[C:1](Cl)"
        mock_reaction = MagicMock(spec=rdChemReactions.ChemicalReaction)
        mock_reaction_from_smarts.return_value = mock_reaction
        reader = ReadSmarts()
        result = reader.read(smarts_data)
        assert result == mock_reaction

    def test_read_empty_smarts(self):
        """
        Test the read method with empty SMARTS data.

        Args:
        - None

        Returns:
        - None
        """
        smarts_data = ""
        with pytest.raises(ReactionDataError):
            reader = ReadSmarts()
            reader.read(smarts_data)


class TestReadRxn:
    """
    Test cases for the ReadRxn class.
    """

    @patch("rdkit.Chem.AllChem.ReactionFromRxnFile")
    def test_read_valid_rxn(self, mock_reaction_from_rxn):
        """
        Test the read method with valid reaction data.

        Args:
        - mock_reaction_from_rxn: MagicMock object for ReactionFromRxnFile

        Returns:
        - None
        """
        rxn_data = "A>>B"
        mock_reaction = MagicMock(spec=rdChemReactions.ChemicalReaction)
        mock_reaction_from_rxn.return_value = mock_reaction
        reader = ReadRxn()
        result = reader.read(rxn_data)
        assert result == mock_reaction

    def test_read_empty_rxn(self):
        """
        Test the read method with empty reaction data.

        Args:
        - None

        Returns:
        - None
        """
        rxn_data = ""
        with pytest.raises(ReactionDataError):
            reader = ReadRxn()
            reader.read(rxn_data)
