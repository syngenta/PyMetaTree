import copy
import hashlib
from functools import partial
from typing import Optional, List, Dict

from rdkit import Chem
from rdkit.Chem import rdChemReactions

from pymetatree.chemoinformatics.exceptions import (
    ExceptionRxnStringFormatInvalid,
    ExceptionMolStringFormatInvalid,
    ExceptionRdrxnStringFormatInvalid,
    ExceptionHashing,
)

HashValue = Optional[str]


def rdmol_from_string(input_string: str, input_format: str) -> Chem.Mol:
    """
    Generate an RDKit Mol object from a molecular string.

    Args:
        input_string (str): The molecular string.
        input_format (str): The format of the input string (e.g., 'smiles', 'smarts', 'molblock').

    Returns:
        Chem.Mol: The RDKit Mol object.

    Raises:
        ExceptionMolStringFormatInvalid: If the input format is not supported.
    """
    converter_factory = {
        "smiles": Chem.MolFromSmiles,
        "smarts": Chem.MolFromSmarts,
        "molblock": Chem.MolFromMolBlock,
    }
    if input_format not in converter_factory:
        raise ExceptionMolStringFormatInvalid(
            f"The molecule input format {input_format} is not available: "
            f"please use one of {list(converter_factory.keys())}"
        )
    convert_func = converter_factory[input_format]
    return convert_func(input_string)


def rdrxn_from_string(
    input_string: str, input_format: str
) -> rdChemReactions.ChemicalReaction:
    """
    Build an RDKit Chemical Reaction object from a reaction string.

    Args:
        input_string (str): The reaction string.
        input_format (str): The format of the input string (e.g., 'smiles', 'smarts', 'molblock').

    Returns:
        rdChemReactions.ChemicalReaction: The RDKit Chemical Reaction object.

    Raises:
        ExceptionRxnStringFormatInvalid: If the input format is not supported.
    """
    converter_factory = {
        "smiles": partial(Chem.rdChemReactions.ReactionFromSmarts, useSmiles=True),
        "smarts": partial(Chem.rdChemReactions.ReactionFromSmarts, useSmiles=False),
        "rxn_block": Chem.rdChemReactions.ReactionFromRxnBlock,
    }
    if input_format not in converter_factory:
        raise ExceptionRxnStringFormatInvalid(
            f"The reaction input format {input_format} is not available: "
            f"please use one of {list(converter_factory.keys())}"
        )
    converter_func = converter_factory[input_format]
    return converter_func(input_string)


def rdrxn_to_string(
    rdrxn: rdChemReactions.ChemicalReaction,
    out_fmt: str,
    use_atom_mapping: bool = False,
) -> str:
    """
    Build a reaction string from an RDKit Chemical Reaction object.

    Args:
        rdrxn (rdChemReactions.ChemicalReaction): The RDKit Chemical Reaction object.
        out_fmt (str): The output format of the RDKit Chemical Reaction object.
        use_atom_mapping (bool, optional): Whether to use atom mapping or not. Defaults to False.

    Returns:
        str: The RDKit Chemical Reaction string.

    Raises:
        ExceptionMolStringFormatInvalid: If the input format is not supported.
    """
    if not use_atom_mapping:
        rdrxn_copy = copy.deepcopy(rdrxn)
        Chem.rdChemReactions.RemoveMappingNumbersFromReactions(rdrxn_copy)
    else:
        rdrxn_copy = rdrxn

    function_map = {
        "smiles": partial(Chem.rdChemReactions.ReactionToSmiles, canonical=True),
        "smarts": Chem.rdChemReactions.ReactionToSmarts,
        "rxn": partial(
            Chem.rdChemReactions.ReactionToRxnBlock,
            forceV3000=True,
            separateAgents=True,
        ),
        "rxn_blockV2K": Chem.rdChemReactions.ReactionToRxnBlock,
        "rxn_blockV3K": partial(
            Chem.rdChemReactions.ReactionToV3KRxnBlock, separateAgents=True
        ),
    }
    if out_fmt not in function_map:
        raise ExceptionRdrxnStringFormatInvalid(
            f"The reaction input format {out_fmt} is not available: "
            f"please use one of {list(function_map.keys())}"
        )
    converter_func = function_map[out_fmt]
    return converter_func(rdrxn_copy)


def hash_string(input_string: str) -> HashValue:
    """
    Calculate the SHA-256 hash value of a string.

    Args:
        input_string (str): The string.

    Returns:
        HashValue: The SHA-256 hash value.

    Raises:
        TypeError: If the input is not a string.
        ValueError: If the input string is empty.
        ExceptionHashing: If an error occurred during hashing.
    """
    if not isinstance(input_string, str):
        raise TypeError("Input reaction_string must be a string.")
    if not input_string.strip():
        raise ValueError("Input reaction_string cannot be empty.")
    try:
        smiles_bytes = input_string.encode('utf-8')
        sha256 = hashlib.sha256()
        sha256.update(smiles_bytes)
        hash_value = sha256.hexdigest()
        return hash_value
    except Exception as e:
        raise ExceptionHashing(f"An error occurred: {e}")


def split_reaction_string(reaction_string: str) -> Dict[str, str]:
    reactants, products = reaction_string.split(">>")
    reactants_list = reactants.split(".")
    products_list = products.split(".")
    return {
        'reactants': reactants_list,
        'products': products_list
    }


def join_molecule_strings(molecules: Dict[str, List[str]]) -> str:
    reactants = ".".join(reactant for reactant in molecules['reactants'])
    products = ".".join(product for product in molecules['products'])
    return reactants + ">>" + products


def canonicalize_molecule_string(molecules_string: str) -> str:
    rdkit_molecule = rdmol_from_string(molecules_string, 'smiles')
    return Chem.MolToSmiles(rdkit_molecule)


def canonicalize_reaction_string(reaction_string: str) -> str:
    molecules = split_reaction_string(reaction_string)
    canonicalized_reactants = [canonicalize_molecule_string(reactant) for reactant in molecules['reactants']]
    canonicalized_products = [canonicalize_molecule_string(product) for product in molecules['products']]
    canonicalized_molecules = {
        'reactants': canonicalized_reactants,
        'products': canonicalized_products
    }
    return join_molecule_strings(canonicalized_molecules)

