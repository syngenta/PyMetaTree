from pymetatree.template.models import Template, RDChiralTemplateExtractorInput
from pymetatree.template.extractor import extract_rdchiral_template
from pymetatree.data_handling.models import ChemicalReaction


class TemplateConstructor:
    def __init__(self) -> None:
        pass

    @staticmethod
    def extract_from_string(reaction_string: str) -> Template:
        template = Template(reaction_string=reaction_string)
        rdchiral_input = RDChiralTemplateExtractorInput.from_smiles(template.reaction_string)
        rdchiral_output = extract_rdchiral_template(rdchiral_input)
        rdchiral_output_dict = rdchiral_output.to_dict()
        template.products_template = rdchiral_output_dict["products"]
        template.reactants_template = rdchiral_output_dict["reactants"]
        template.template_rwd_smarts = rdchiral_output_dict["reaction_smarts"]
        template.template_fwd_smarts = ">".join(template.template_rwd_smarts.split(">")[::-1])
        return template

    @staticmethod
    def extract_from_chemical_reaction_object(chemical_reaction: ChemicalReaction) -> ChemicalReaction:
        template = TemplateConstructor.extract_from_string(chemical_reaction.mapped_smiles)
        chemical_reaction.template = template
        return chemical_reaction
