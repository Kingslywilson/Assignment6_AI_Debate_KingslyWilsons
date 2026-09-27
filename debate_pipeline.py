import os
import json
import time
from typing import List

from dotenv import load_dotenv
from langchain_groq import ChatGroq

from models import (
    TopicAnalysis,
    DebateArgument,
    NeutralAnalysis,
    DebateSummary
)

from chains.topic_analysis import get_topic_analysis_chain
from chains.claim_generation import get_claim_generation_chain
from chains.evidence_generation import get_evidence_generation_chain
from chains.counter_argument import get_counter_argument_chain
from chains.rebuttal import get_rebuttal_chain
from chains.neutral_analysis import get_neutral_analysis_chain
from chains.debate_summary import get_debate_summary_chain


load_dotenv()


# ============================================================
# GROQ LLM
# ============================================================

def get_llm():
    """
    Create and return the Groq LLM.
    """

    groq_api_key = os.getenv("GROQ_API_KEY")

    if not groq_api_key:
        raise ValueError(
            "GROQ_API_KEY is not set in the environment."
        )

    return ChatGroq(
        model="openai/gpt-oss-120b",
        temperature=0.2,
        api_key=groq_api_key
    )


# ============================================================
# POLITICAL TOPIC DETECTION
# ============================================================

def _is_political_or_partisan_topic(topic: str) -> bool:
    """
    Detect potentially political or partisan topics.

    Political topics must remain neutral and should not receive
    a better-supported-position selection.
    """

    political_terms = [
        "election",
        "elections",
        "president",
        "prime minister",
        "politician",
        "politics",
        "political",
        "government",
        "parliament",
        "congress",
        "senate",
        "democrat",
        "republican",
        "labour",
        "conservative",
        "liberal party",
        "political party",
        "candidate",
        "campaign",
        "vote",
        "voting",
        "ballot",
        "policy",
        "legislation",
        "law",
        "bill",
        "minister",
        "governor",
        "chief minister",
        "mp",
        "mla",
        "ideology",
        "partisan"
    ]

    topic_lower = topic.lower()

    return any(
        term in topic_lower
        for term in political_terms
    )


# ============================================================
# TEXT SIZE CONTROL
# ============================================================

def _shorten_text(text: str, max_chars: int) -> str:
    """
    Shorten long generated text before sending it to another
    LLM stage.

    This helps keep Groq requests below the TPM limit.
    """

    if not text:
        return ""

    text = str(text).strip()

    if len(text) <= max_chars:
        return text

    return text[:max_chars] + "... [truncated]"


# ============================================================
# DEBATE PIPELINE
# ============================================================

class DebatePipeline:

    def __init__(self, llm=None):
        """
        Initialize the debate pipeline.

        If an LLM is not provided, the Groq LLM is created
        automatically.
        """

        self.llm = llm or get_llm()

    # ========================================================
    # FULL PIPELINE
    # ========================================================

    def run_full_pipeline(self, topic: str):

        if not topic or not topic.strip():
            raise ValueError(
                "Debate topic cannot be empty."
            )

        topic = topic.strip()

        # ====================================================
        # PHASE 1: TOPIC ANALYSIS
        # ====================================================

        print("\n" + "=" * 60)
        print("PHASE 1: TOPIC ANALYSIS")
        print("=" * 60)

        topic_analysis_chain = get_topic_analysis_chain(
            self.llm
        )

        topic_analysis: TopicAnalysis = (
            topic_analysis_chain.invoke(
                {
                    "topic": topic
                }
            )
        )

        print("\nTopic Analysis:")
        print(topic_analysis)

        time.sleep(1)

        # ====================================================
        # PHASE 2: CLAIM GENERATION
        # ====================================================

        print("\n" + "=" * 60)
        print("PHASE 2: CLAIM GENERATION")
        print("=" * 60)

        claim_chain = get_claim_generation_chain(
            self.llm
        )

        # IMPORTANT:
        # Claim generation requires both topic and main_issue.
        # main_issue comes from Phase 1.

        claim_result = claim_chain.invoke(
            {
                "topic": topic,
                "main_issue": topic_analysis.main_issue
            }
        )

        supporting_claims = (
            claim_result.supporting_claims
        )

        opposing_claims = (
            claim_result.opposing_claims
        )

        print("\nSupporting Claims:")

        for claim in supporting_claims:
            print("-", claim)

        print("\nOpposing Claims:")

        for claim in opposing_claims:
            print("-", claim)

        time.sleep(1)

        # ====================================================
        # PHASE 3: EVIDENCE + COUNTER + REBUTTAL
        # ====================================================

        print("\n" + "=" * 60)
        print(
            "PHASE 3: EVIDENCE, COUNTER-ARGUMENT & REBUTTAL"
        )
        print("=" * 60)

        evidence_chain = (
            get_evidence_generation_chain(
                self.llm
            )
        )

        counter_chain = (
            get_counter_argument_chain(
                self.llm
            )
        )

        rebuttal_chain = (
            get_rebuttal_chain(
                self.llm
            )
        )

        supporting_args: List[DebateArgument] = []

        opposing_args: List[DebateArgument] = []

        # ====================================================
        # SUPPORTING ARGUMENTS
        # ====================================================

        for index, claim in enumerate(
            supporting_claims[:2],
            start=1
        ):

            print(
                f"\nSupporting Argument {index}"
            )

            # ------------------------------------------------
            # Evidence / Reasoning
            # ------------------------------------------------

            evidence = evidence_chain.invoke(
                {
                    "topic": topic,
                    "claim": claim
                }
            )

            print("\nSupport Type:")
            print(evidence.support_type)

            print("\nSupport:")
            print(evidence.content)

            # ------------------------------------------------
            # Counter Argument
            # ------------------------------------------------

            counter_argument = counter_chain.invoke(
                {
                    "topic": topic,
                    "claim": claim,
                    "support": evidence.content
                }
            )

            print("\nCounter-Argument:")
            print(counter_argument)

            # ------------------------------------------------
            # Rebuttal
            # ------------------------------------------------

            rebuttal = rebuttal_chain.invoke(
                {
                    "topic": topic,
                    "claim": claim,
                    "counter_argument": counter_argument
                }
            )

            print("\nRebuttal:")
            print(rebuttal)

            # ------------------------------------------------
            # Store Argument
            # ------------------------------------------------

            supporting_args.append(
                DebateArgument(
                    claim=claim,
                    support_type=evidence.support_type,
                    support=evidence.content,
                    limitation=evidence.limitation,
                    counter_argument=counter_argument,
                    rebuttal=rebuttal
                )
            )

            time.sleep(1)

        # ====================================================
        # OPPOSING ARGUMENTS
        # ====================================================

        for index, claim in enumerate(
            opposing_claims[:2],
            start=1
        ):

            print(
                f"\nOpposing Argument {index}"
            )

            # ------------------------------------------------
            # Evidence / Reasoning
            # ------------------------------------------------

            evidence = evidence_chain.invoke(
                {
                    "topic": topic,
                    "claim": claim
                }
            )

            print("\nSupport Type:")
            print(evidence.support_type)

            print("\nSupport:")
            print(evidence.content)

            # ------------------------------------------------
            # Counter Argument
            # ------------------------------------------------

            counter_argument = counter_chain.invoke(
                {
                    "topic": topic,
                    "claim": claim,
                    "support": evidence.content
                }
            )

            print("\nCounter-Argument:")
            print(counter_argument)

            # ------------------------------------------------
            # Rebuttal
            # ------------------------------------------------

            rebuttal = rebuttal_chain.invoke(
                {
                    "topic": topic,
                    "claim": claim,
                    "counter_argument": counter_argument
                }
            )

            print("\nRebuttal:")
            print(rebuttal)

            # ------------------------------------------------
            # Store Argument
            # ------------------------------------------------

            opposing_args.append(
                DebateArgument(
                    claim=claim,
                    support_type=evidence.support_type,
                    support=evidence.content,
                    limitation=evidence.limitation,
                    counter_argument=counter_argument,
                    rebuttal=rebuttal
                )
            )

            time.sleep(1)

        # ====================================================
        # PHASE 4: COMPACT SUMMARY INPUT
        # ====================================================

        print("\n" + "=" * 60)
        print("PREPARING COMPACT DEBATE SUMMARY INPUT")
        print("=" * 60)

        """
        Phase 3 can produce a large amount of text.

        Groq has a token-per-minute limit, so the final
        summary stage receives shortened versions of the
        generated arguments.
        """

        supporting_summary_parts = []

        for argument in supporting_args:

            supporting_summary_parts.append(
                f"""
Claim:
{_shorten_text(argument.claim, 250)}

Support ({argument.support_type}):
{_shorten_text(argument.support, 340)}

Counter-Argument:
{_shorten_text(argument.counter_argument, 400)}

Rebuttal:
{_shorten_text(argument.rebuttal, 400)}
""".strip()
            )

        opposing_summary_parts = []

        for argument in opposing_args:

            opposing_summary_parts.append(
                f"""
Claim:
{_shorten_text(argument.claim, 250)}

Support ({argument.support_type}):
{_shorten_text(argument.support, 340)}

Counter-Argument:
{_shorten_text(argument.counter_argument, 400)}

Rebuttal:
{_shorten_text(argument.rebuttal, 400)}
""".strip()
            )

        supporting_summary = "\n\n".join(
            supporting_summary_parts
        )

        opposing_summary = "\n\n".join(
            opposing_summary_parts
        )

        # ====================================================
        # PHASE 4A: NEUTRAL ANALYSIS
        # ====================================================

        print("\n" + "=" * 60)
        print("PHASE 4A: NEUTRAL ANALYSIS")
        print("=" * 60)

        neutral_analysis_chain = (
            get_neutral_analysis_chain(
                self.llm
            )
        )

        neutral_analysis: NeutralAnalysis = (
            neutral_analysis_chain.invoke(
                {
                    "topic": topic,
                    "supporting_summary": supporting_summary,
                    "opposing_summary": opposing_summary
                }
            )
        )

        print("\nNeutral Analysis:")
        print(neutral_analysis)

        time.sleep(1)

        # ====================================================
        # PHASE 4B: STRUCTURED DEBATE SUMMARY
        # ====================================================

        print("\n" + "=" * 60)
        print("PHASE 4B: STRUCTURED DEBATE SUMMARY")
        print("=" * 60)

        summary_chain = (
            get_debate_summary_chain(
                self.llm
            )
        )

        summary: DebateSummary = (
            summary_chain.invoke(
                {
                    "topic": topic,
                    "supporting_summary": supporting_summary,
                    "opposing_summary": opposing_summary
                }
            )
        )

        # ====================================================
        # POLITICAL / PARTISAN SAFETY
        # ====================================================

        if _is_political_or_partisan_topic(topic):

            summary.better_supported_position = None

        print("\nStructured Summary:")
        print(summary)

        # ====================================================
        # FINAL RESULT
        # ====================================================

        result = {
            "topic": topic,

            "topic_analysis":
                topic_analysis.model_dump(),

            "supporting_arguments": [
                argument.model_dump()
                for argument in supporting_args
            ],

            "opposing_arguments": [
                argument.model_dump()
                for argument in opposing_args
            ],

            "neutral_analysis":
                neutral_analysis.model_dump(),

            "summary":
                summary.model_dump()
        }

        print("\n" + "=" * 60)
        print("DEBATE PIPELINE COMPLETED")
        print("=" * 60)

        return result


# ============================================================
# DIRECT FILE TEST
# ============================================================

if __name__ == "__main__":

    pipeline = DebatePipeline()

    topic = input(
        "\nEnter a debate topic: "
    ).strip()

    if not topic:

        print(
            "\nError: Debate topic cannot be empty."
        )

    else:

        result = pipeline.run_full_pipeline(
            topic
        )

        print("\n" + "=" * 60)
        print("FINAL JSON RESULT")
        print("=" * 60)

        print(
            json.dumps(
                result,
                indent=2,
                ensure_ascii=False
            )
        )
