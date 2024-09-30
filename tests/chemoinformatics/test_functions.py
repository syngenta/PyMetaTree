import pytest

from rdkit.Chem import rdChemReactions

from pymetatree.chemoinformatics.exceptions import (
    ExceptionRxnStringFormatInvalid,
    ExceptionMolStringFormatInvalid,
    ExceptionRdrxnStringFormatInvalid
)
from pymetatree.chemoinformatics.functions import (
    rdrxn_from_string,
    rdmol_from_string,
    rdrxn_to_string,
    hash_string
)


def test_rdrxn_from_string_smiles_format():
    input_string = "C.C>>CC"
    result = rdrxn_from_string(input_string, input_format="smiles")
    assert result is not None


def test_rdrxn_from_string_smarts_format():
    input_string = "[CH3:1][CH2:2][OH:3]>>[CH3:1][CH2:2][O:3][CH3]"
    result = rdrxn_from_string(input_string, input_format="smarts")
    assert result is not None


def test_rdrxn_from_string_invalid_format():
    input_string = "C.C>>CC"
    with pytest.raises(ExceptionRxnStringFormatInvalid):
        rdrxn_from_string(input_string, input_format="invalid_format")


def test_rdmol_from_string_smiles_format():
    input_string = "C1NCN1"
    result = rdmol_from_string(input_string, input_format="smiles")
    assert result is not None


def test_rdmol_from_strings_smarts_format():
    input_string = "[CX3](=[OX1])C"
    result = rdmol_from_string(input_string, input_format="smarts")
    assert result is not None


def test_rdmol_from_string_invalid_format():
    input_string = "C1NCN1"
    with pytest.raises(ExceptionMolStringFormatInvalid):
        rdmol_from_string(input_string, input_format="invalid_format")


def test_rdrxn_to_string_smiles_format():
    reaction = rdChemReactions.ReactionFromSmarts('[C:1](=[O:2])-[OD1].[N!H0:3]>>[C:1](=[O:2])[N:3]')
    result = rdrxn_to_string(reaction, out_fmt="smiles")
    assert result is not None


def test_rdrxn_to_string_smarts_format():
    reaction = rdChemReactions.ReactionFromSmarts('[C:1](=[O:2])-[OD1].[N!H0:3]>>[C:1](=[O:2])[N:3]')
    result = rdrxn_to_string(reaction, out_fmt="smarts")
    assert result is not None


def test_rdrxn_to_string_rxn_format():
    reaction = rdChemReactions.ReactionFromSmarts('[C:1](=[O:2])-[OD1].[N!H0:3]>>[C:1](=[O:2])[N:3]')
    result = rdrxn_to_string(reaction, out_fmt="rxn")
    assert result is not None


def test_rdrxn_to_string_rxn_blockV2K_format():
    reaction = rdChemReactions.ReactionFromSmarts('[C:1](=[O:2])-[OD1].[N!H0:3]>>[C:1](=[O:2])[N:3]')
    result = rdrxn_to_string(reaction, out_fmt="rxn_blockV2K")
    assert result is not None


def test_rdrxn_to_string_rxn_blockV3K_format():
    reaction = rdChemReactions.ReactionFromSmarts('[C:1](=[O:2])-[OD1].[N!H0:3]>>[C:1](=[O:2])[N:3]')
    result = rdrxn_to_string(reaction, out_fmt="rxn_blockV2K")
    assert result is not None


def test_rdrxn_to_string_invalid_forma():
    reaction = rdChemReactions.ReactionFromSmarts('[C:1](=[O:2])-[OD1].[N!H0:3]>>[C:1](=[O:2])[N:3]')
    with pytest.raises(ExceptionRdrxnStringFormatInvalid):
        rdrxn_to_string(reaction, out_fmt="invalid_format")


def test_rdrxn_to_string_use_atom_mapping():
    reaction = rdChemReactions.ReactionFromSmarts('[C:1](=[O:2])-[OD1].[N!H0:3]>>[C:1](=[O:2])[N:3]')
    result = rdrxn_to_string(reaction, out_fmt="smiles", use_atom_mapping=True)
    assert result is not None


def test_hash_smiles_empty_input():
    with pytest.raises(ValueError):
        hash_string("")


def test_hash_smiles_non_string_input():
    with pytest.raises(TypeError):
        hash_string(123)


def test_hash_smiles_none_input():
    reaction_string = None
    with pytest.raises(TypeError):
        hash_string(reaction_string)


