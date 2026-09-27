import os
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from models import EvidenceItem


def get_evidence_generation_chain(llm):
    prompt_path = os.path.join(
        os.path.dirname(__file__),
        "..",
        "prompts",
        "evidence_prompt.txt"
    )

    with open(prompt_path, "r", encoding="utf-8") as f:
        template_text = f.read()

    parser = PydanticOutputParser(pydantic_object=EvidenceItem)

    template_with_format = (
        template_text
        + "\n\nFormat Instructions:\n{format_instructions}"
    )

    prompt = PromptTemplate(
        template=template_with_format,
        input_variables=["topic", "claim"],
        partial_variables={
            "format_instructions": parser.get_format_instructions()
        }
    )

    return prompt | llm | parser