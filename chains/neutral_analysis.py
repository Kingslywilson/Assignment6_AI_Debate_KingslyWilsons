import os
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from models import NeutralAnalysis


def get_neutral_analysis_chain(llm):
    prompt_path = os.path.join("prompts", "neutral_analysis_prompt.txt")
    with open(prompt_path, "r", encoding="utf-8") as f:
        prompt_template_text = f.read()

    parser = PydanticOutputParser(pydantic_object=NeutralAnalysis)

    prompt = PromptTemplate(
        template=prompt_template_text,
        input_variables=["topic", "supporting_summary", "opposing_summary"],
        partial_variables={"format_instructions": parser.get_format_instructions()}
    )

    return prompt | llm | parser
