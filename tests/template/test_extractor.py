from pymetatree.template.models import (
    RDChiralTemplateExtractorInput,
    RDChiralTemplateExtractorOutput,
)
from pymetatree.template.extractor import extract_rdchiral_template


def test_build_rdchiral_input_from_smiles_without_id():
    mapped_smiles = "[CH3:1][CH2:2][NH:3][CH3:4]>>[CH3:1][CH2:2][NH2+1:3][CH3:4]"
    rdchiral_input = RDChiralTemplateExtractorInput.from_smiles(
        rxn_smiles=mapped_smiles
    )
    assert isinstance(rdchiral_input, RDChiralTemplateExtractorInput)
    assert rdchiral_input._id == "na"


def test_build_rdchiral_input_from_smiles_with_id():
    mapped_smiles = "[CH3:1][CH2:2][NH:3][CH3:4]>>[CH3:1][CH2:2][NH2+1:3][CH3:4]"
    rdchiral_input = RDChiralTemplateExtractorInput.from_smiles(
        rxn_smiles=mapped_smiles, _id="RXN_001"
    )
    assert isinstance(rdchiral_input, RDChiralTemplateExtractorInput)
    assert rdchiral_input._id == "RXN_001"


def test_extract_rdchiral_template():
    mapped_smiles = "[CH3:1][CH2:2][NH:3][CH3:4]>>[CH3:1][CH2:2][NH2+1:3][CH3:4]"
    rdchiral_input = RDChiralTemplateExtractorInput.from_smiles(
        rxn_smiles=mapped_smiles, _id="RXN_001"
    )
    rdchiral_output = extract_rdchiral_template(rdchiral_input=rdchiral_input)
    assert isinstance(rdchiral_output, RDChiralTemplateExtractorOutput)
    print(rdchiral_output)
