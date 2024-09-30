"""
This module provides a class BlueprintHandler to handle chemical reactions and their corresponding blueprints.

The BlueprintHandler class is designed to manage the creation, modification, and execution of chemical reactions
based on a Blueprint object. It provides methods to build a Blueprint from a ChemicalReaction instance, add or remove
reactions, activate templates, and run reactions on molecules.

Usage:
1. Create an instance of BlueprintHandler with a ChemicalReaction object or a Blueprint object.
2. Use the provided methods to manipulate the Blueprint and execute reactions.
"""
import logging
from typing import Optional, List
from rdkit import Chem
from pymetatree.chemoinformatics.functions import rdrxn_from_string, rdmol_from_string
from pymetatree.blueprint.models import Blueprint, ReactionComponent, ChemicalClass
from pymetatree.data_handling.models import ChemicalReaction, Molecule

logger = logging.getLogger(__name__)


class BlueprintHandler:
    """
    A class to handle chemical reactions and their corresponding blueprints.

    Attributes:
        chemical_reaction (ChemicalReaction): The chemical reaction object.
        blueprint (Blueprint): The blueprint object associated with the chemical reaction.
        _rdrxn (rdkit.Chem.rdChemReaction): The RDKit chemical reaction object.
    """
    def __init__(self, chemical_reaction: Optional[ChemicalReaction] = None,
                 blueprint: Optional[Blueprint] = None) -> None:
        """
        Initialize the BlueprintHandler with a ChemicalReaction or a Blueprint object.

        Args:
            chemical_reaction (ChemicalReaction, optional): The chemical reaction object.
            blueprint (Blueprint, optional): The blueprint object built from a ChemicalReaction object.

        Raises:
            ValueError: If neither chemical_reaction nor blueprint is provided.
       """
        if chemical_reaction is None and blueprint is None:
            raise ValueError("Either chemical_reaction or blueprint must be provided.")
        if chemical_reaction and not isinstance(chemical_reaction, ChemicalReaction):
            raise ValueError("chemical_reaction must be an instance of ChemicalReaction.")
        if blueprint and not isinstance(blueprint, Blueprint):
            raise ValueError("blueprint must be an instance of Blueprint.")
        self.chemical_reaction = chemical_reaction
        self.blueprint = blueprint or self._build_blueprint()
        self._rdrxn = None

    @staticmethod
    def _build_components(components: List[Molecule]) -> List[ReactionComponent]:
        """
        Build a list of ReactionComponent objects from a list of Molecule objects.

        Args:
            components (List[Molecule]): A list of Molecule objects.

        Returns:
            List[ReactionComponent]: A list of ReactionComponent objects.
        """
        return [
            ReactionComponent(
                name=component.name,
                chemical_classes=ChemicalClass(
                    name=component.name,
                    smarts=component.smiles,
                )
            )
            for component in components
        ]

    def _build_blueprint(self) -> Blueprint:
        """
        Build a Blueprint object from the ChemicalReaction object.

        Returns:
            Blueprint: The Blueprint object.

        Raises:
            ValueError: If the ChemicalReaction object is not present.
        """
        if self.chemical_reaction is None:
            raise ValueError("ChemicalReaction object must be provided to build the blueprint.")
        reactants = self._build_components(self.chemical_reaction.reactants)
        products = self._build_components(self.chemical_reaction.products)
        components = {
            "reactants": reactants,
            "products": products
        }
        return Blueprint(
            components=components,
            description=self.chemical_reaction.description,
            name=self.chemical_reaction.name,
            namerxn_reaction_class=self.chemical_reaction.namerxn_reaction_class,
            namerxn_reaction_numbers=self.chemical_reaction.namerxn_reaction_numbers,
            templates=[self.chemical_reaction.template]
        )

    def add_new_reaction(self, new_reaction: ChemicalReaction) -> None:
        """
        Add a new chemical reaction to the blueprint.

        Args:
            new_reaction (ChemicalReaction): The new chemical reaction to be added.

        Raises:
            ValueError: If the provided new_reaction is not an instance of ChemicalReaction.
        """
        if not isinstance(new_reaction, ChemicalReaction):
            raise ValueError("new_reaction must be an instance of ChemicalReaction.")
        pass

    def remove_reaction(self, reaction_index: int) -> None:
        """
        Remove a chemical reaction from the blueprint.

        Args:
            reaction_index (int): The index of the reaction to be removed.

        Raises:
            IndexError: If the reaction_index is out of range.
        """
        if reaction_index < 0 or reaction_index >= len(self.blueprint.templates):
            raise IndexError("Reaction index out of range.")
        pass

    def activate_template(self, template_index: int, reaction_direction: str) -> None:
        """
        Activate a template for the chemical reaction.

        Args:
            template_index (int): The index of the template to be activated.
            reaction_direction (str): The direction of the reaction ("forward" or "backward").

        Raises:
            ValueError: If the reaction_direction is not "forward" or "backward".
            IndexError: If the template_index is out of range.
        """
        if reaction_direction not in ["forward", "backward"]:
            raise ValueError("Reaction direction must be 'forward' or 'backward'.")
        if template_index < 0 or template_index >= len(self.blueprint.templates):
            raise IndexError("Template index out of range.")
        template = self.blueprint.templates[template_index]
        if reaction_direction == "forward":
            self._rdrxn = rdrxn_from_string(template.template_fwd_smarts, "smarts")
        elif reaction_direction == "backward":
            self._rdrxn = rdrxn_from_string(template.template_rwd_smarts, "smarts")

    def run_reaction(self, template_index: int, reaction_direction: str, molecules: List[str]) -> Chem.Mol:
        """
        Run the chemical reaction on a list of molecules.

        Args:
            template_index (int): The index of the template to be used.
            reaction_direction (str): The direction of the reaction ("forward" or "backward").
            molecules (List[Chem.Mol]): A list of RDKit molecule objects.

        Returns:
            List[Chem.Mol]: A list of resulting molecules after the reaction.

        Raises:
            ValueError: If no molecules are provided.
        """
        if molecules is None or not molecules:
            raise ValueError("Molecules must be provided to run the reaction.")
        activated_molecules = [self.activate_molecule(molecule) for molecule in molecules]
        molecules_tuple = tuple(activated_molecules)
        self.activate_template(template_index, reaction_direction)
        try:
            result = self._rdrxn.RunReactants(molecules_tuple)[0][0]
            return result
        except Exception as e:
            logger.error(f"Error running the reaction: {e}")
            raise RuntimeError(f"Error running the reaction: {e}")

    @staticmethod
    def activate_molecule(molecule: str) -> Chem.Mol:
        """
        Convert a SMILES string to an RDKit molecule object.

        Args:
            molecule (str): The SMILES string representing the molecule.

        Returns:
            Chem.Mol: The RDKit molecule object.
        """
        if isinstance(molecule, str):
            return rdmol_from_string(molecule, 'smiles')
        else:
            raise ValueError("Molecule must be an instance of str.")
