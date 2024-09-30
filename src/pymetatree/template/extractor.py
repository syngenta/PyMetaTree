from pymetatree.template.models import RDChiralTemplateExtractorOutput, RDChiralTemplateExtractorInput
from pymetatree.template.exceptions import RDChiralExtractionError
from rdchiral import template_extractor


def extract_rdchiral_template(
    rdchiral_input: RDChiralTemplateExtractorInput,
) -> RDChiralTemplateExtractorOutput:
    try:
        rdchiral_output_dictionary = template_extractor.extract_from_reaction(
            reaction=rdchiral_input.to_dict()
        )
        rdchiral_output = RDChiralTemplateExtractorOutput(**rdchiral_output_dictionary)
        return rdchiral_output
    except Exception as e:
        raise RDChiralExtractionError(f"Error while extracting templates: {e}")
