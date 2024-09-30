from pydantic import BaseModel, Field, computed_field
from typing import Dict, List, Optional
from pymetatree.template.models import Template
from pymetatree.chemoinformatics.functions import hash_string


class ChemicalClass(BaseModel):
    name: Optional[str] = Field(None)
    smarts: Optional[str] = Field(None)
    examples: Optional[List[str]] = Field(None)


class ReactionComponent(BaseModel):
    name: Optional[str] = Field(None)
    chemical_classes: Optional[ChemicalClass] = Field(None)


class Blueprint(BaseModel):
    components: Dict[str, List[ReactionComponent]]
    description: Optional[str] = Field(None)
    metadata: Optional[Dict[str, str]] = Field(None)
    name: Optional[str] = Field(None)
    namerxn_reaction_class: Optional[str] = Field(None)
    namerxn_reaction_numbers: Optional[List[str]] = Field(None)
    templates: Optional[List[Template]] = Field(None)
    version: Optional[str] = Field(None)

    @computed_field
    @property
    def uid(self) -> str:
        sorted_templates = sorted(self.templates, key=lambda t: t.uid)
        templates_uid = ""
        for template in sorted_templates:
            templates_uid += template.uid
        return hash_string(templates_uid)
