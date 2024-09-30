import pytest
from rdkit import Chem
from pymetatree.chemoinformatics.functions import rdmol_from_string
from pymetatree.blueprint.exceptions import InvalidSmilesError, SubstructureSearchError
from pymetatree.blueprint.substructure_search import BlueprintSubstructureSearch

valid_smiles = 'c1ccccc1'
invalid_smiles = 'invalid_smiles'
blueprint_dataset = [
    {
        "components": {
            "reactants": [
                {
                    "name": "Bitertanol",
                    "chemical_classes": {
                        "name": "Bitertanol",
                        "smarts": "CC(C)(C)C(C(N1C=NC=N1)OC2=CC=C(C=C2)C3=CC=CC=C3)O",
                        "examples": ""
                    }
                }
            ],
            "products": [
                {
                    "name": "1,2,4 triazole",
                    "chemical_classes": {
                        "name": "1,2,4 triazole",
                        "smarts": "C1=NC=NN1",
                        "examples": ""
                    }
                }
            ]
        },
        "description": "no description",
        "metadata": "",
        "name": "reaction 0000000",
        "namerxn_reaction_class": "",
        "namerxn_reaction_numbers": "",
        "templates": [
            {
                "uid": "",
                "reaction_string": "CC(C)(C)C(O)C(Oc1ccc(-c2ccccc2)cc1)[N:1]1[CH:2]=[N:3][CH:4]=[N:5]1>>[NH:1]1[CH:2]=[N:3][CH:4]=[N:5]1",
                "products_template": "[#7;a:4]1:[c:5]:[nH;D2;+0:1]:[#7;a:2]:[c:3]:1",
                "reactants_template": "C-C(-C)(-C)-C(-O)-C(-O-c1:c:c:c(-c2:c:c:c:c:c:2):c:c:1)-[n;H0;D3;+0:1]1:[#7;a:2]:[c:3]:[#7;a:4]:[c:5]:1",
                "template_fwd_smarts": "C-C(-C)(-C)-C(-O)-C(-O-c1:c:c:c(-c2:c:c:c:c:c:2):c:c:1)-[n;H0;D3;+0:1]1:[#7;a:2]:[c:3]:[#7;a:4]:[c:5]:1>>[#7;a:4]1:[c:5]:[nH;D2;+0:1]:[#7;a:2]:[c:3]:1",
                "template_rwd_smarts": "[#7;a:4]1:[c:5]:[nH;D2;+0:1]:[#7;a:2]:[c:3]:1>>C-C(-C)(-C)-C(-O)-C(-O-c1:c:c:c(-c2:c:c:c:c:c:2):c:c:1)-[n;H0;D3;+0:1]1:[#7;a:2]:[c:3]:[#7;a:4]:[c:5]:1"
            }
        ],
        "version": "",
        "uid": "blueprint1"
    },
    {
        "components": {
            "reactants": [
                {
                    "name": "Bitertanol",
                    "chemical_classes": {
                        "name": "Bitertanol",
                        "smarts": "CC(C)(C)C(C(N1C=NC=N1)OC2=CC=C(C=C2)C3=CC=CC=C3)O",
                        "examples": ""
                    }
                }
            ],
            "products": [
                {
                    "name": "4-[2-hydroxy-3,3-dimethyl-1-(1H-1,2,4-triazol-1-yl)butoxyl)-benzoic acid",
                    "chemical_classes": {
                        "name": "4-[2-hydroxy-3,3-dimethyl-1-(1H-1,2,4-triazol-1-yl)butoxyl)-benzoic acid",
                        "smarts": "CC(C)(C)C(C(N1C=NC=N1)OC2=CC=C(C=C2)C(=O)O)O",
                        "examples": ""
                    }
                }
            ]
        },
        "description": "no description",
        "metadata": "",
        "name": "reaction 0000001",
        "namerxn_reaction_class": "",
        "namerxn_reaction_numbers": "",
        "templates": [
            {
                "uid": "",
                "reaction_string": "c1cc[c:13](-[c:12]2[cH:11][cH:10][c:9]([O:8][CH:7]([CH:5]([C:2]([CH3:1])([CH3:3])[CH3:4])[OH:6])[n:18]3[cH:19][n:20][cH:21][n:22]3)[cH:17][cH:16]2)cc1>>[CH3:1][C:2]([CH3:3])([CH3:4])[CH:5]([OH:6])[CH:7]([O:8][c:9]1[cH:10][cH:11][c:12]([C:13](=[O:14])[OH:15])[cH:16][cH:17]1)[n:18]1[cH:19][n:20][cH:21][n:22]1",
                "products_template": "[C;H0;D3;+0:4]-[c;H0;D3;+0:2](:[c:1]):[c:3]",
                "reactants_template": "[c:1]:[c;H0;D3;+0:2](:[c:3])-[c;H0;D3;+0:4]1:c:c:c:c:c:1",
                "template_fwd_smarts": "[c:1]:[c;H0;D3;+0:2](:[c:3])-[c;H0;D3;+0:4]1:c:c:c:c:c:1>>[C;H0;D3;+0:4]-[c;H0;D3;+0:2](:[c:1]):[c:3]",
                "template_rwd_smarts": "[C;H0;D3;+0:4]-[c;H0;D3;+0:2](:[c:1]):[c:3]>>[c:1]:[c;H0;D3;+0:2](:[c:3])-[c;H0;D3;+0:4]1:c:c:c:c:c:1"
            }
        ],
        "version": "",
        "uid": "blueprint2"
    }
]


@pytest.fixture
def blueprint_search():
    return BlueprintSubstructureSearch(blueprint_dataset)


def test_extract_smiles_from_dataset(blueprint_search):
    expected_smiles_dict = {
        'blueprint1': ['CC(C)(C)C(C(N1C=NC=N1)OC2=CC=C(C=C2)C3=CC=CC=C3)O', 'C1=NC=NN1'],
        'blueprint2': ['CC(C)(C)C(C(N1C=NC=N1)OC2=CC=C(C=C2)C3=CC=CC=C3)O',
                       'CC(C)(C)C(C(N1C=NC=N1)OC2=CC=C(C=C2)C(=O)O)O']
    }
    assert blueprint_search.smiles_dict == expected_smiles_dict


def test_search_valid_smiles(blueprint_search):
    query_smiles = 'CC(C)(C)C(C(N1C=NC=N1)OC2=CC=C(C=C2)C3=CC=CC=C3)O'
    expected_result = ['blueprint1', 'blueprint2']
    assert blueprint_search.search(query_smiles) == expected_result


def test_search_invalid_smiles(blueprint_search):
    with pytest.raises(SubstructureSearchError) as excinfo:
        blueprint_search.search(invalid_smiles)
    assert "Invalid SMILES string" in str(excinfo.value)