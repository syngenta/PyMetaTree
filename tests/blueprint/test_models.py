import pytest
from pydantic import ValidationError
from pymetatree.blueprint.models import ChemicalClass, ReactionComponent, Blueprint
from pymetatree.template.models import Template

@pytest.fixture
def sample_chemical_class():
    return ChemicalClass(name="Test", smarts="C=C", examples=["CC", "CCC"])

@pytest.fixture
def sample_reaction_component(sample_chemical_class):
    return ReactionComponent(name="Component", chemical_classes=sample_chemical_class)

@pytest.fixture
def sample_template():
    return Template(
        reaction_string="CC>>C",
        products_template="C",
        reactants_template="CC",
        template_fwd_smarts="CC>>C",
        template_rwd_smarts="C>>CC"
    )

@pytest.fixture
def sample_blueprint(sample_reaction_component, sample_template):
    components = {
        "reactants": [sample_reaction_component],
        "products": [ReactionComponent(name="Product")]
    }
    return Blueprint(
        components=components,
        description="Test Blueprint",
        name="Test",
        templates=[sample_template]
    )

class TestChemicalClass:
    def test_valid_creation(self, sample_chemical_class):
        assert sample_chemical_class.name == "Test"
        assert sample_chemical_class.smarts == "C=C"
        assert sample_chemical_class.examples == ["CC", "CCC"]

    def test_optional_fields(self):
        chemical_class = ChemicalClass()
        assert chemical_class.name is None
        assert chemical_class.smarts is None
        assert chemical_class.examples is None

class TestReactionComponent:
    def test_valid_creation(self, sample_reaction_component, sample_chemical_class):
        assert sample_reaction_component.name == "Component"
        assert sample_reaction_component.chemical_classes == sample_chemical_class

    def test_optional_fields(self):
        reaction_component = ReactionComponent()
        assert reaction_component.name is None
        assert reaction_component.chemical_classes is None

class TestBlueprint:
    def test_valid_creation(self, sample_blueprint, sample_template):
        assert isinstance(sample_blueprint.components, dict)
        assert sample_blueprint.description == "Test Blueprint"
        assert sample_blueprint.name == "Test"
        assert sample_blueprint.templates == [sample_template]

    def test_uid_computation(self, sample_blueprint):
        assert isinstance(sample_blueprint.uid, str)
        assert len(sample_blueprint.uid) > 0

    def test_optional_fields(self, sample_reaction_component):
        components = {"reactants": [sample_reaction_component], "products": []}
        blueprint = Blueprint(components=components)
        assert blueprint.description is None
        assert blueprint.metadata is None
        assert blueprint.name is None
        assert blueprint.namerxn_reaction_class is None
        assert blueprint.namerxn_reaction_numbers is None
        assert blueprint.templates is None
        assert blueprint.version is None

    def test_validation_error(self):
        with pytest.raises(ValidationError):
            Blueprint()

    def test_uid_consistency(self, sample_template):
        components = {"reactants": [], "products": []}
        template2 = Template(
            reaction_string="CCC>>CC",
            products_template="CC",
            reactants_template="CCC",
            template_fwd_smarts="CCC>>CC",
            template_rwd_smarts="CC>>CCC"
        )

        blueprint1 = Blueprint(components=components, templates=[sample_template, template2])
        blueprint2 = Blueprint(components=components, templates=[template2, sample_template])

        assert blueprint1.uid == blueprint2.uid

    def test_uid_different(self, sample_template):
        components = {"reactants": [], "products": []}
        template2 = Template(
            reaction_string="CCC>>CC",
            products_template="CC",
            reactants_template="CCC",
            template_fwd_smarts="CCC>>CC",
            template_rwd_smarts="CC>>CCC"
        )

        blueprint1 = Blueprint(components=components, templates=[sample_template])
        blueprint2 = Blueprint(components=components, templates=[template2])

        assert blueprint1.uid != blueprint2.uid
