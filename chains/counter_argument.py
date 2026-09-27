import os
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser


def get_counter_argument_chain(llm):
    prompt_path = os.path.join(os.path.dirname(__file__), "..", "prompts", "counter_argument_prompt.txt")
    with open(prompt_path, "r", encoding="utf-8") as f:
        template_text = f.read()
    
    prompt = PromptTemplate.from_template(template_text)
    return prompt | llm | StrOutputParser()
