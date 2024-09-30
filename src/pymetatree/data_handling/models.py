"""
This module defines Pydantic models for representing chemical reactions, molecules, enzyme classes, and pathways.

The main model is `ChemicalReaction`, which includes fields for various properties of a chemical reaction,
such as reactants, products, enzyme classes, pathways, and reaction templates. It also includes methods
for validating and canonicalizing SMILES strings, as well as setting unique identifiers (UIDs) for the
reaction, reactants, and products.

The `Molecule` model represents a single molecule, with fields for its name, SMILES string, and UID.
The `EnzymeClass` model represents an enzyme class, with fields for its name and class number.
The `Pathway` model represents a pathway, with a field for its UID.
"""

import logging
from pydantic import BaseModel, Field, model_validator, computed_field, AliasChoices, field_validator
from typing import List, Optional
from pymetatree.chemoinformatics.functions import hash_string, canonicalize_reaction_string, rdmol_from_string
from pymetatree.template.models import Template

logging.basicConfig(level=logging.INFO)


class Molecule(BaseModel):
    """
    A model representing a molecule.
    """
    name: Optional[str] = Field(None, validation_alias=AliasChoices('compoundName', 'name'),
                                description="Name of the molecule")
    smiles: Optional[str] = Field(None, description="SMILES of the molecule")
    uid: Optional[str] = Field(None, description="UID of the molecule")

    @field_validator('smiles')
    @classmethod
    def check_smiles_validity(cls, value: str) -> str:
        try:
            molecule = rdmol_from_string(value, 'smiles')
            if molecule is None:
                raise ValueError("Invalid SMILES string")
        except Exception as e:
            raise ValueError(f"Error validating SMILES string: {e}")
        return value


class EnzymeClass(BaseModel):
    """
    A model representing an enzyme class.
    """
    enzyme_class_name: Optional[str] = Field(None,
                                             validation_alias='ecName',
                                             description="Name of the enzyme class")
    enzyme_class_number: Optional[str] = Field(None,
                                               validation_alias='ecNumber',
                                               description="Enzyme class number")


class Pathway(BaseModel):
    """
    A model representing a pathway.
    """
    uid: Optional[str] = Field(None, description="UID of the pathway")


class ChemicalReaction(BaseModel):
    """
    A Pydantic model representing a chemical reaction.
    """
    dataset: Optional[str] = Field(None, description="Origin dataset of the reaction")
    description: Optional[str] = Field(None, description="Description of the reaction")
    enzyme_classes: Optional[List[EnzymeClass]] = Field(None,
                                                        validation_alias=AliasChoices('ecNumbers',
                                                                                      'enzyme_classes'),
                                                        description="List of enzyme classes")
    mapped_smiles: Optional[str] = Field(None, description="Mapped SMILES of the reaction")
    multistep_flag: Optional[bool] = Field(None,
                                           validation_alias=AliasChoices('multistep',
                                                                         'multistep_flag'),
                                           description="Flag indicating if the reaction is multistep")
    name: Optional[str] = Field(None, description="Name of the reaction")
    namerxn_reaction_class: Optional[str] = Field(None)
    namerxn_reaction_numbers: Optional[List[str]] = Field(None)
    pathways: Optional[List[Pathway]] = Field(None, description="List of pathways")
    products: Optional[List[Molecule]] = Field(None, description="List of product molecules")
    reactants: Optional[List[Molecule]] = Field(None,
                                                validation_alias=AliasChoices('educts', 'reactants'),
                                                description="List of reactant molecules")
    scenarios: Optional[List[str]] = Field(None, description="Reaction scenarios")
    template: Optional[Template] = Field(None,
                                         validation_alias='template',
                                         description="Reaction template extracted with RDChiral")
    uid: Optional[str] = Field(None, description="Unique identifier for the reaction")
    unmapped_smiles: str = Field(validation_alias=AliasChoices('smirks', 'unmapped_smiles'),
                                 description="SMILES string of the reaction")

    @computed_field
    @property
    def unmapped_smiles_canonicalized(self) -> str:
        """
        Compute the canonicalized version of the unmapped SMILES string.
        """
        try:
            return canonicalize_reaction_string(self.unmapped_smiles)
        except Exception as e:
            logging.error(f"Error canonicalizing reaction string: {e}")
            return ""

    @model_validator(mode='after')
    def set_uid(self) -> None:
        """
        Set UIDs for the reaction, reactants, and products if not provided.
        """
        if self.uid is None:
            self.uid = hash_string(self.unmapped_smiles_canonicalized)
        for reactant in self.reactants:
            if reactant.uid is None:
                reactant.uid = hash_string(reactant.smiles)
        for product in self.products:
            if product.uid is None:
                product.uid = hash_string(product.smiles)
