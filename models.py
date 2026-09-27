from typing import List, Optional
from pydantic import BaseModel, Field


class TopicAnalysis(BaseModel):
    main_issue: str = Field(description="Core question or subject of the debate")
    scope: str = Field(description="Boundaries and context of the debate topic")
    key_terms: List[str] = Field(description="Essential terms and definitions")
    stakeholders: List[str] = Field(description="Key parties or groups affected")
    major_areas_of_disagreement: List[str] = Field(description="Primary points of contention")
    assumptions: List[str] = Field(description="Underlying assumptions requiring clarification")


class ClaimSet(BaseModel):
    supporting_claims: List[str] = Field(description="Distinct claims supporting the proposition")
    opposing_claims: List[str] = Field(description="Distinct claims opposing the proposition")


class EvidenceItem(BaseModel):
    claim: str = Field(description="The claim being supported")
    support_type: str = Field(description="Must be 'Verified Evidence' or 'Reasoning / Example'")
    content: str = Field(description="Supporting evidence or logical reasoning")
    limitation: Optional[str] = Field(default="", description="Potential boundary or limitation of this support")


class DebateArgument(BaseModel):
    claim: str = Field(description="Original claim statement")
    support_type: str = Field(description="Must be 'Verified Evidence' or 'Reasoning / Example'")
    support: str = Field(description="Supporting evidence or logical reasoning")
    counter_argument: str = Field(description="Direct counter-argument addressing the claim")
    rebuttal: str = Field(description="Specific rebuttal responding to the counter-argument")


class NeutralAnalysis(BaseModel):
    strengths_summary: str = Field(description="Core strengths of both supporting and opposing positions")
    trade_offs: List[str] = Field(description="Key compromises and trade-offs between positions")
    areas_of_agreement: List[str] = Field(description="Shared goals, consensus points, or common ground")
    key_uncertainties: List[str] = Field(description="Unknown factors, empirical gaps, or unmeasured impacts")
    pivotal_factors: List[str] = Field(description="Conditions or future developments that could shift the balance")


class DebateSummary(BaseModel):
    topic: str = Field(description="Debate topic proposition")
    strongest_supporting_argument: str = Field(description="Strongest supporting argument with rationale")
    strongest_opposing_argument: str = Field(description="Strongest opposing argument with rationale")
    weakest_supporting_argument: str = Field(description="Weakest supporting argument with rationale")
    weakest_opposing_argument: str = Field(description="Weakest opposing argument with rationale")
    key_counter_arguments: List[str] = Field(description="Primary counter-arguments raised across both sides")
    key_rebuttals: List[str] = Field(description="Key rebuttals offered in response to counter-arguments")
    better_supported_position: Optional[str] = Field(default=None, description="Evaluation of which position is better supported (or null if partisan/political/balanced)")
    conclusion: str = Field(description="Balanced, neutral synthesis of trade-offs")


class ConversationalResponse(BaseModel):
    response_text: str = Field(description="Detailed response to the user query")
    identified_intent: str = Field(description="Recognized user intent (e.g. challenge, request rebuttal, ambiguous)")
    referenced_argument: Optional[str] = Field(default=None, description="Argument claim referenced if determined")
    clarification_needed: bool = Field(default=False, description="True if prompt is ambiguous and requires user clarification")

