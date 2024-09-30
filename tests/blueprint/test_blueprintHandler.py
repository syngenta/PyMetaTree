import pytest
from rdkit import Chem
from pymetatree.chemoinformatics.functions import rdmol_from_string
from pymetatree.blueprint.models import Blueprint, ReactionComponent, ChemicalClass
from pymetatree.data_handling.models import ChemicalReaction, Molecule
from pymetatree.template.models import Template
from pymetatree.blueprint.blueprint_handler import BlueprintHandler

reaction_dict = {'dataset': 'EAWAG_SOIL',
 'description': 'no description',
 'enzyme_classes': [],
 'mapped_smiles': 'CC(C)(C)C(O)C(Oc1ccc(-c2ccccc2)cc1)[N:1]1[CH:2]=[N:3][CH:4]=[N:5]1>>[NH:1]1[CH:2]=[N:3][CH:4]=[N:5]1',
 'multistep_flag': False,
 'name': 'reaction 0000000',
 'namerxn_reaction_class': None,
 'namerxn_reaction_numbers': None,
 'pathways': [{'uid': None}],
 'products': [{'name': '1,2,4 triazole',
   'smiles': 'C1=NC=NN1',
   'uid': 'e424cb24c7ebec8a4410bec6433bafbe658e2ad57fedafeb539cc88745e9bf4a'}],
 'reactants': [{'name': 'Bitertanol',
   'smiles': 'CC(C)(C)C(C(N1C=NC=N1)OC2=CC=C(C=C2)C3=CC=CC=C3)O',
   'uid': '6d5f58846f00b8d185d5c1ed8b048933ee437185cc99bb2f1aa84875474efe9c'}],
 'scenarios': [],
 'template': {'reaction_string': 'CC(C)(C)C(O)C(Oc1ccc(-c2ccccc2)cc1)[N:1]1[CH:2]=[N:3][CH:4]=[N:5]1>>[NH:1]1[CH:2]=[N:3][CH:4]=[N:5]1',
  'products_template': '[#7;a:4]1:[c:5]:[nH;D2;+0:1]:[#7;a:2]:[c:3]:1',
  'reactants_template': 'C-C(-C)(-C)-C(-O)-C(-O-c1:c:c:c(-c2:c:c:c:c:c:2):c:c:1)-[n;H0;D3;+0:1]1:[#7;a:2]:[c:3]:[#7;a:4]:[c:5]:1',
  'template_fwd_smarts': 'C-C(-C)(-C)-C(-O)-C(-O-c1:c:c:c(-c2:c:c:c:c:c:2):c:c:1)-[n;H0;D3;+0:1]1:[#7;a:2]:[c:3]:[#7;a:4]:[c:5]:1>>[#7;a:4]1:[c:5]:[nH;D2;+0:1]:[#7;a:2]:[c:3]:1',
  'template_rwd_smarts': '[#7;a:4]1:[c:5]:[nH;D2;+0:1]:[#7;a:2]:[c:3]:1>>C-C(-C)(-C)-C(-O)-C(-O-c1:c:c:c(-c2:c:c:c:c:c:2):c:c:1)-[n;H0;D3;+0:1]1:[#7;a:2]:[c:3]:[#7;a:4]:[c:5]:1',
  'uid': '03c92b57aecf61227ad1efc3aba9a75e4edc4ecab7791544ead296e25d6ee13d'},
 'uid': 'ef7bca056aff8220e4b4918a24ab585f1bf11bfdde54c001582f736ded85ab58',
 'unmapped_smiles': 'CC(C)(C)C(C(N1C=NC=N1)OC2=CC=C(C=C2)C3=CC=CC=C3)O>>C1=NC=NN1',
 'unmapped_smiles_canonicalized': 'CC(C)(C)C(O)C(Oc1ccc(-c2ccccc2)cc1)n1cncn1>>c1nc[nH]n1'}

template_dict = {'reaction_string': 'CC(C)(C)C(O)C(Oc1ccc(-c2ccccc2)cc1)[N:1]1[CH:2]=[N:3][CH:4]=[N:5]1>>[NH:1]1[CH:2]=[N:3][CH:4]=[N:5]1',
  'products_template': '[#7;a:4]1:[c:5]:[nH;D2;+0:1]:[#7;a:2]:[c:3]:1',
  'reactants_template': 'C-C(-C)(-C)-C(-O)-C(-O-c1:c:c:c(-c2:c:c:c:c:c:2):c:c:1)-[n;H0;D3;+0:1]1:[#7;a:2]:[c:3]:[#7;a:4]:[c:5]:1',
  'template_fwd_smarts': 'C-C(-C)(-C)-C(-O)-C(-O-c1:c:c:c(-c2:c:c:c:c:c:2):c:c:1)-[n;H0;D3;+0:1]1:[#7;a:2]:[c:3]:[#7;a:4]:[c:5]:1>>[#7;a:4]1:[c:5]:[nH;D2;+0:1]:[#7;a:2]:[c:3]:1',
  'template_rwd_smarts': '[#7;a:4]1:[c:5]:[nH;D2;+0:1]:[#7;a:2]:[c:3]:1>>C-C(-C)(-C)-C(-O)-C(-O-c1:c:c:c(-c2:c:c:c:c:c:2):c:c:1)-[n;H0;D3;+0:1]1:[#7;a:2]:[c:3]:[#7;a:4]:[c:5]:1',
  'uid': '03c92b57aecf61227ad1efc3aba9a75e4edc4ecab7791544ead296e25d6ee13d'}

reactant_smiles = 'CC(C)(C)C(C(N1C=NC=N1)OC2=CC=C(C=C2)C3=CC=CC=C3)O'
product_smiles = 'C1=NC=NN1'
template = Template(**template_dict)
reactant_molecule = Molecule(name='Bitertanol', smiles=reactant_smiles)
product_molecule = Molecule(name='1,2,4 triazole', smiles=product_smiles)
chemical_reaction = ChemicalReaction(**reaction_dict)


def create_blueprint_handler(chemical_reaction: ChemicalReaction) -> BlueprintHandler:
    return BlueprintHandler(chemical_reaction)


def create_blueprint() -> Blueprint:
    reactant_component = ReactionComponent(
        name='reactant',
        chemical_classes=ChemicalClass(name='Bitertanol', smarts=reactant_smiles)
    )
    product_component = ReactionComponent(
        name='product',
        chemical_classes=ChemicalClass(name='1,2,4 triazole', smarts=product_smiles),
    )
    components = {
        "reactants": [reactant_component],
        "products": [product_component],
    }
    return Blueprint(
        components=components,
        templates=[template]
        )


def test_init_with_chemical_reaction():
    handler = create_blueprint_handler(chemical_reaction)
    assert handler.chemical_reaction == chemical_reaction
    assert isinstance(handler.blueprint, Blueprint)


def test_init_with_blueprint():
    blueprint = create_blueprint()
    handler = BlueprintHandler(blueprint=blueprint)
    assert handler.blueprint == blueprint
    assert handler.chemical_reaction is None


def test_init_with_none():
    with pytest.raises(ValueError):
        BlueprintHandler()


def test_build_components():
    components = BlueprintHandler._build_components([reactant_molecule, product_molecule])
    assert len(components) == 2
    assert isinstance(components[0], ReactionComponent)
    assert isinstance(components[1], ReactionComponent)


def test_build_blueprint():
    handler = create_blueprint_handler(chemical_reaction)
    blueprint = handler._build_blueprint()
    assert isinstance(blueprint, Blueprint)
    assert blueprint.templates == [template]
    assert blueprint.name == chemical_reaction.name
    assert len(blueprint.components["reactants"]) == 1
    assert len(blueprint.components["products"]) == 1


def test_activate_template():
    handler = create_blueprint_handler(chemical_reaction)
    handler.activate_template(0, "forward")
    assert handler._rdrxn is not None
    with pytest.raises(ValueError):
        handler.activate_template(0, "invalid")
    with pytest.raises(IndexError):
        handler.activate_template(1, "forward")


def test_run_reaction():
    handler = create_blueprint_handler(chemical_reaction)
    handler.activate_template(0, "forward")
    result = handler.run_reaction(0, "forward", [reactant_smiles])
    expected_product = rdmol_from_string(product_smiles, 'smiles')
    assert Chem.MolToSmiles(result) == Chem.MolToSmiles(expected_product)
    with pytest.raises(ValueError):
        handler.run_reaction(0, "forward", [])
    with pytest.raises(RuntimeError):
        handler.run_reaction(0, "forward", ["invalid_smiles"])


def test_activate_molecule():
    molecule = BlueprintHandler.activate_molecule(reactant_smiles)
    assert isinstance(molecule, Chem.Mol)