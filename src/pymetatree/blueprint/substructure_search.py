from typing import List, Dict
from rdkit import Chem

from pymetatree.chemoinformatics.functions import rdmol_from_string
from pymetatree.blueprint.exceptions import InvalidSmilesError, SubstructureSearchError


class BlueprintSubstructureSearch:
    """
    A class to search for blueprints that contain a given substructure.
    """
    def __init__(self, blueprint_dataset: List[Dict]):
        self.blueprint_dataset = blueprint_dataset
        self.smiles_dict = self._extract_smiles_from_dataset()

    def _extract_smiles_from_dataset(self) -> Dict[str, List[str]]:
        """
        Extract SMILES strings from the blueprint dataset and store them in a dictionary.

        Returns:
            Dict[str, List[str]]: A dictionary where the keys are blueprint UIDs,
                                  and the values are lists of SMILES strings.
        """
        smiles_with_uids = {}
        for blueprint in self.blueprint_dataset:
            blueprint_uid = blueprint['uid']
            smiles_list = [
                reactant['chemical_classes']['smarts'] for reactant in blueprint['components']['reactants']
            ] + [
                product['chemical_classes']['smarts'] for product in blueprint['components']['products']
            ]
            smiles_with_uids[blueprint_uid] = smiles_list
        return smiles_with_uids

    def search(self, query_smiles: str) -> List[str]:
        """
        Search for blueprints that contain the given substructure.

        Args:
            query_smiles (str): The SMILES string representing the substructure.

        Returns:
            List[str]: A list of blueprint UIDs that contain the substructure.

        Raises:
            InvalidSmilesError: If the input `query_smiles` is not a valid SMILES string.
            SubstructureSearchError: If any other error occurs during the substructure search process.
        """
        try:
            query_mol = rdmol_from_string(query_smiles, 'smiles')
            if query_mol is None:
                raise InvalidSmilesError(f"Invalid SMILES string: {query_smiles}")
            matched_blueprints = [
                blueprint_uid
                for blueprint_uid, smiles_list in self.smiles_dict.items()
                if any(self._has_substructure(smile, query_mol) for smile in smiles_list)
            ]
            return matched_blueprints
        except Exception as e:
            raise SubstructureSearchError(f"An error occurred during the substructure search: {str(e)}") from e

    @staticmethod
    def _has_substructure(smiles: str, query_mol: Chem.Mol) -> bool:
        """
        Check if a given SMILES string contains the substructure represented by the query molecule.

        Args:
            smiles (str): The SMILES string to check.
            query_mol (Chem.Mol): The query molecule representing the substructure.

        Returns:
            bool: True if the SMILES string contains the substructure, False otherwise.

        Raises:
            SubstructureSearchError: If any error occurs during the substructure check.
        """
        try:
            mol = rdmol_from_string(smiles, 'smiles')
            return mol.HasSubstructMatch(query_mol)
        except Exception as e:
            raise SubstructureSearchError(f"An error occurred while checking substructure for SMILES: {smiles}") from e
