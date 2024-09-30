import pytest
from pymetatree.template.constructors import TemplateConstructor
from pymetatree.template.models import Template
from pymetatree.data_handling.models import ChemicalReaction, Molecule, EnzymeClass, Pathway


@pytest.fixture
def template_constructor():
    return TemplateConstructor()


@pytest.fixture
def sample_chemical_reaction():
    return ChemicalReaction(
        dataset="test_dataset",
        description="Test reaction",
        enzyme_classes=[EnzymeClass(enzyme_class_name="Test Enzyme", enzyme_class_number="1.1.1.1")],
        mapped_smiles="[CH3:1][C:2]([OH:3])=[O:4].[CH3:6][NH2:5]>>[CH3:6][NH:5][C:2]([CH3:1])=[O:4].[OH2:3]",
        multistep_flag=False,
        name="Test Reaction",
        pathways=[Pathway(uid="P001")],
        products=[Molecule(name="Product", smiles="CC(=O)NC")],
        reactants=[Molecule(name="Reactant 1", smiles="CC(=O)O"), Molecule(name="Reactant 2", smiles="CN")],
        scenarios=["test_scenario"],
        unmapped_smiles="CC(=O)O.CN>>CC(=O)NC.O"
    )


def test_extract_from_string(template_constructor):
    reaction_string = "[CH3:1][C:2]([OH:3])=[O:4].[CH3:6][NH2:5]>>[CH3:6][NH:5][C:2]([CH3:1])=[O:4].[OH2:3]"
    template = template_constructor.extract_from_string(reaction_string=reaction_string)

    assert isinstance(template, Template)
    assert template.reaction_string == reaction_string
    assert template.products_template is not None
    assert template.reactants_template is not None
    assert template.template_rwd_smarts is not None
    assert template.template_fwd_smarts is not None
    assert template.template_fwd_smarts == ">".join(template.template_rwd_smarts.split(">")[::-1])


def test_extract_from_chemical_reaction_object(template_constructor, sample_chemical_reaction):
    updated_reaction = template_constructor.extract_from_chemical_reaction_object(sample_chemical_reaction)

    assert isinstance(updated_reaction, ChemicalReaction)
    assert updated_reaction.template is not None
    assert isinstance(updated_reaction.template, Template)
    assert updated_reaction.template.reaction_string == sample_chemical_reaction.mapped_smiles


def test_invalid_reaction_string(template_constructor):
    with pytest.raises(Exception):  # Replace with specific exception if known
        template_constructor.extract_from_string("invalid_reaction_string")


def test_empty_reaction_string(template_constructor):
    with pytest.raises(Exception):  # Replace with specific exception if known
        template_constructor.extract_from_string("")


def test_template_properties(template_constructor):
    reaction_string = "[CH3:1][C:2]([OH:3])=[O:4].[CH3:6][NH2:5]>>[CH3:6][NH:5][C:2]([CH3:1])=[O:4].[OH2:3]"
    template = template_constructor.extract_from_string(reaction_string)

    assert template.uid is not None
    assert isinstance(template.uid, str)
    assert len(template.uid) > 0


def test_extract_and_set_template(template_constructor, sample_chemical_reaction):
    updated_reaction = template_constructor.extract_from_chemical_reaction_object(sample_chemical_reaction)
    assert updated_reaction.template is not None
    assert isinstance(updated_reaction.template, Template)
    assert updated_reaction.template.reaction_string == sample_chemical_reaction.mapped_smiles
    assert updated_reaction.template.products_template is not None
    assert updated_reaction.template.reactants_template is not None
    assert updated_reaction.template.template_rwd_smarts is not None
    assert updated_reaction.template.template_fwd_smarts is not None
