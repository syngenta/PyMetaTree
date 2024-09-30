from typing import Optional
from pydantic import BaseModel, Field, model_validator, computed_field
from dataclasses import dataclass, field

from pymetatree.chemoinformatics.functions import hash_string
from pymetatree.template.exceptions import RDChiralInputError


@dataclass
class RDChiralTemplateExtractorInput:
    _id: str = field(default_factory=str)
    products: str = field(default_factory=str)
    agents: str = field(default_factory=str)
    reactants: str = field(default_factory=str)

    @classmethod
    def from_smiles(cls, rxn_smiles: str, _id: str = None):
        if _id is None:
            _id = "na"
        try:
            reactants, reagents, products = rxn_smiles.split(">")
        except ValueError as e:
            raise RDChiralInputError(f"Invalid SMILES string format: {e}")
        if not reactants or not products:
            raise RDChiralInputError("Invalid SMILES string: missing reactants or products")
        return cls(
            _id=_id,
            products=products,
            agents=reagents,
            reactants=reactants,
        )

    def to_dict(self):
        return {
            "_id": self._id,
            "products": self.products,
            "agents": self.agents,
            "reactants": self.reactants,
        }


@dataclass
class RDChiralTemplateExtractorOutput:
    products: str = field(default_factory=str)
    reactants: str = field(default_factory=str)
    reaction_smarts: str = field(default_factory=str)
    intra_only: bool = field(default_factory=bool)
    dimer_only: bool = field(default_factory=bool)
    reaction_id: str = field(default_factory=str)
    necessary_reagent: str = field(default_factory=str)

    def to_dict(self):
        return {
            "products": self.products,
            "reactants": self.reactants,
            "reaction_smarts": self.reaction_smarts,
            "intra_only": self.intra_only,
            "dimer_only": self.dimer_only,
            "reaction_id": self.reaction_id,
            "necessary_reagent": self.necessary_reagent,
        }


class Template(BaseModel):
    reaction_string: str = Field(description="Reaction string as mapped SMARTS")
    products_template: Optional[str] = Field(None, description="Product template resulting from RDChiral")
    reactants_template: Optional[str] = Field(None, description="Reactants template resulting from RDChiral")
    template_fwd_smarts: Optional[str] = Field(None,
                                               description="Forward reaction template resulting from RDChiral")
    template_rwd_smarts: Optional[str] = Field(None,
                                               description="Backward reaction template resulting from RDChiral")

    @computed_field
    @property
    def uid(self) -> str:
        return hash_string(self.reaction_string)
