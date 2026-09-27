import os
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from models import TopicAnalysis


def get_topic_analysis_chain(llm):
    prompt_path = os.path.join(os.path.dirname(__file__), "..", "prompts", "topic_analysis_prompt.txt")
    with open(prompt_path, "r", encoding="utf-8") as f:
        template_text = f.read()
    
    parser = PydanticOutputParser(pydantic_object=TopicAnalysis)
    template_with_format = template_text + "\n\nFormat Instructions:\n{format_instructions}"
    prompt = PromptTemplate(
        template=template_with_format,
        input_variables=["topic"],
        partial_variables={"format_instructions": parser.get_format_instructions()}
    )
    return prompt | llm | parser
