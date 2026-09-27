import os
from pydantic import BaseModel, Field
from typing import List
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from models import ClaimSet


class SupportingClaims(BaseModel):
    claims: List[str] = Field(description="List of 2 distinct claims supporting the debate proposition")


class OpposingClaims(BaseModel):
    claims: List[str] = Field(description="List of 2 distinct claims opposing the debate proposition")


class ClaimGenerationRunner:
    def __init__(self, llm):
        self.llm = llm

        p1 = PydanticOutputParser(pydantic_object=SupportingClaims)
        prompt1_text = (
            "Role: Supporting Debate Strategist\n"
            "Debate Topic: {topic}\n"
            "Main Issue: {main_issue}\n\n"
            "Task: Generate exactly 2 distinct, impactful claims supporting the proposition.\n"
            "{format_instructions}"
        )
        self.sup_chain = PromptTemplate(
            template=prompt1_text,
            input_variables=["topic", "main_issue"],
            partial_variables={"format_instructions": p1.get_format_instructions()}
        ) | llm | p1

        p2 = PydanticOutputParser(pydantic_object=OpposingClaims)
        prompt2_text = (
            "Role: Opposing Debate Strategist\n"
            "Debate Topic: {topic}\n"
            "Main Issue: {main_issue}\n\n"
            "Task: Generate exactly 2 distinct, impactful claims opposing the proposition.\n"
            "{format_instructions}"
        )
        self.opp_chain = PromptTemplate(
            template=prompt2_text,
            input_variables=["topic", "main_issue"],
            partial_variables={"format_instructions": p2.get_format_instructions()}
        ) | llm | p2

    def invoke(self, inputs: dict) -> ClaimSet:
        sup_res = self.sup_chain.invoke(inputs)
        opp_res = self.opp_chain.invoke(inputs)
        return ClaimSet(
            supporting_claims=sup_res.claims,
            opposing_claims=opp_res.claims
        )


def get_claim_generation_chain(llm):
    return ClaimGenerationRunner(llm)
