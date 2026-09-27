import os
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from models import DebateSummary


def get_debate_summary_chain(llm):
    prompt_path = os.path.join(os.path.dirname(__file__), "..", "prompts", "debate_summary_prompt.txt")
    with open(prompt_path, "r", encoding="utf-8") as f:
        template_text = f.read()
    
    parser = PydanticOutputParser(pydantic_object=DebateSummary)
    prompt = PromptTemplate(
        template=template_text,
        input_variables=["topic", "supporting_summary", "opposing_summary"],
        partial_variables={"format_instructions": parser.get_format_instructions()}
    )
    return prompt | llm | parser
