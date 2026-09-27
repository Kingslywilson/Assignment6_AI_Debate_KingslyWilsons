import os
import sys
import json
from typing import Dict, Any

from dotenv import load_dotenv

if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

from debate_pipeline import DebatePipeline, get_llm
from memory import DebateMemory
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()


class AIDebateApp:
    def __init__(self):
        self.llm = get_llm()
        self.pipeline = DebatePipeline(llm=self.llm)
        self.memory = DebateMemory()
        self.pipeline_result: Dict[str, Any] = {}

    def validate_topic(self, topic: str) -> tuple[bool, str]:
        if not topic or not topic.strip():
            return False, "Error: Topic cannot be empty or whitespace-only. Please provide a valid debate topic."

        topic_clean = topic.strip()
        broad_keywords = ["good or bad", "is good", "is bad", "stuff", "things"]

        if len(topic_clean.split()) <= 3 and any(
            k in topic_clean.lower() for k in broad_keywords
        ):
            return False, (
                f"The topic '{topic_clean}' is very broad. "
                "Could you please narrow down the scope or specify a domain "
                "(e.g., in education, healthcare, or startup infrastructure)?"
            )

        return True, ""

    def start_debate(self, topic: str) -> Dict[str, Any]:
        valid, msg = self.validate_topic(topic)

        if not valid:
            print(msg)
            return {"error": msg}

        print("\n==================================================")
        print("       AI DEBATE GENERATOR & ANALYZER           ")
        print("==================================================")
        print(f"Topic: {topic}\n")

        print("[Phase 1 & 2] Executing Multi-Stage Reasoning Pipeline...")

        self.pipeline_result = self.pipeline.run_full_pipeline(topic)
        self.memory.set_topic(topic)

        all_args = (
            self.pipeline_result["supporting_arguments"]
            + self.pipeline_result["opposing_arguments"]
        )

        self.memory.set_claims(all_args)

        os.makedirs("outputs", exist_ok=True)

        summary_path = os.path.join(
            "outputs",
            "debate_summary.json"
        )

        full_export = {
            "topic": topic,
            "topic_analysis": self.pipeline_result["topic_analysis"],
            "supporting_arguments": self.pipeline_result["supporting_arguments"],
            "opposing_arguments": self.pipeline_result["opposing_arguments"],
            "neutral_analysis": self.pipeline_result.get(
                "neutral_analysis",
                {}
            ),
            "summary": self.pipeline_result["summary"]
        }

        with open(summary_path, "w", encoding="utf-8") as f:
            json.dump(
                full_export,
                f,
                indent=2,
                ensure_ascii=False
            )

        self._display_pipeline_results()

        return self.pipeline_result

    def _display_pipeline_results(self):
        analysis = self.pipeline_result["topic_analysis"]

        print("\n--- PHASE 1: TOPIC ANALYSIS ---")
        print(f"Main Issue: {analysis.get('main_issue')}")
        print(f"Scope: {analysis.get('scope')}")
        print(
            f"Key Terms: "
            f"{', '.join(analysis.get('key_terms', []))}"
        )
        print(
            f"Stakeholders: "
            f"{', '.join(analysis.get('stakeholders', []))}"
        )
        print(
            f"Major Disagreements: "
            f"{', '.join(analysis.get('major_areas_of_disagreement', []))}"
        )

        print("\n--- PHASE 2: SUPPORTING ARGUMENTS ---")

        for idx, arg in enumerate(
            self.pipeline_result["supporting_arguments"],
            1
        ):
            print(f"\nArgument {idx}:")
            print(f"  Claim: {arg['claim']}")
            print(f"  Support Type: {arg['support_type']}")
            print(f"  Support: {arg['support']}")
            print(
                f"  Counter-Argument: "
                f"{arg['counter_argument']}"
            )
            print(f"  Rebuttal: {arg['rebuttal']}")

        print("\n--- PHASE 2: OPPOSING ARGUMENTS ---")

        for idx, arg in enumerate(
            self.pipeline_result["opposing_arguments"],
            1
        ):
            print(f"\nArgument {idx}:")
            print(f"  Claim: {arg['claim']}")
            print(f"  Support Type: {arg['support_type']}")
            print(f"  Support: {arg['support']}")
            print(
                f"  Counter-Argument: "
                f"{arg['counter_argument']}"
            )
            print(f"  Rebuttal: {arg['rebuttal']}")

        neutral = self.pipeline_result.get(
            "neutral_analysis",
            {}
        )

        if neutral:
            print(
                "\n--- PHASE 3: "
                "DEDICATED NEUTRAL ANALYSIS ---"
            )

            print(
                f"Strengths Summary: "
                f"{neutral.get('strengths_summary')}"
            )

            print(
                f"Key Trade-offs: "
                f"{', '.join(neutral.get('trade_offs', []))}"
            )

            print(
                f"Areas of Agreement: "
                f"{', '.join(neutral.get('areas_of_agreement', []))}"
            )

            print(
                f"Key Uncertainties: "
                f"{', '.join(neutral.get('key_uncertainties', []))}"
            )

            print(
                f"Pivotal Factors: "
                f"{', '.join(neutral.get('pivotal_factors', []))}"
            )

        summary = self.pipeline_result["summary"]

        print("\n--- PHASE 4: STRUCTURED DEBATE SUMMARY ---")

        print(
            f"Strongest Supporting Argument: "
            f"{summary.get('strongest_supporting_argument')}"
        )

        print(
            f"Strongest Opposing Argument: "
            f"{summary.get('strongest_opposing_argument')}"
        )

        print(
            f"Weakest Supporting Argument: "
            f"{summary.get('weakest_supporting_argument')}"
        )

        print(
            f"Weakest Opposing Argument: "
            f"{summary.get('weakest_opposing_argument')}"
        )

        print(
            f"Key Counter-Arguments: "
            f"{', '.join(summary.get('key_counter_arguments', []))}"
        )

        print(
            f"Key Rebuttals: "
            f"{', '.join(summary.get('key_rebuttals', []))}"
        )

        print(
            f"Better-Supported Position: "
            f"{summary.get('better_supported_position')}"
        )

        print(
            f"Neutral Conclusion: "
            f"{summary.get('conclusion')}"
        )

    def _compact_argument(self, argument: Dict[str, Any]) -> Dict[str, Any]:
        """
        Keep only the most useful fields for conversational debate.
        This prevents the interactive prompt from exceeding Groq's TPM limit.
        """

        return {
            "claim": argument.get("claim", ""),
            "support_type": argument.get("support_type", ""),
            "support": str(argument.get("support", ""))[:500],
            "counter_argument": str(
                argument.get("counter_argument", "")
            )[:600],
            "rebuttal": str(
                argument.get("rebuttal", "")
            )[:600]
        }

    def _get_compact_arguments_summary(self) -> str:
        """
        Build a compact debate context instead of sending the
        complete JSON representation of every argument.
        """

        supporting = [
            self._compact_argument(arg)
            for arg in self.pipeline_result.get(
                "supporting_arguments",
                []
            )
        ]

        opposing = [
            self._compact_argument(arg)
            for arg in self.pipeline_result.get(
                "opposing_arguments",
                []
            )
        ]

        compact_context = {
            "supporting_arguments": supporting,
            "opposing_arguments": opposing
        }

        return json.dumps(
            compact_context,
            ensure_ascii=False
        )

    def _get_compact_history(self, max_messages: int = 4) -> str:
        """
        Keep only the most recent conversation messages.
        """

        history = self.memory.get_history_as_string()

        if not history:
            return "No previous conversation."

        lines = history.splitlines()

        # Keep only recent history.
        lines = lines[-max_messages * 2:]

        history = "\n".join(lines)

        # Additional character protection.
        if len(history) > 2500:
            history = history[-2500:]

        return history

    def handle_user_query(self, user_query: str) -> str:
        if not user_query or not user_query.strip():
            return "Please enter a valid question or comment."

        query = user_query.strip()

        self.memory.add_user_message(query)

        if (
            "make them up" in query.lower()
            or "fabricate" in query.lower()
            or "fake studies" in query.lower()
        ):
            response = (
                "Evidence Integrity Violation Warning: "
                "As per system safety and truthfulness rules, "
                "I cannot fabricate research studies, statistics, "
                "surveys, or citations. "
                "I can, however, provide logical reasoning, "
                "principles, or real-world examples to support "
                "the argument."
            )

            self.memory.add_ai_message(response)

            return response

        matched_arg = self.memory.find_matching_argument(query)

        if matched_arg:
            self.memory.set_last_discussed(matched_arg)

        if self.memory.is_ambiguous_query(query):
            response = self.memory.get_claims_clarification_prompt()

            self.memory.add_ai_message(response)

            return response

        referenced_arg_str = (
            json.dumps(
                self._compact_argument(matched_arg),
                ensure_ascii=False
            )
            if matched_arg
            else "None specifically matched "
                 "(general topic question)"
        )

        prompt = PromptTemplate.from_template(
            "You are a neutral AI Debate Assistant.\n\n"

            "Debate Topic:\n"
            "{topic}\n\n"

            "Currently Referenced Argument:\n"
            "{referenced_argument}\n\n"

            "Relevant Debate Context:\n"
            "{arguments_summary}\n\n"

            "Recent Conversation:\n"
            "{history}\n\n"

            "User Input:\n"
            "{user_input}\n\n"

            "Rules:\n"
            "1. Respond directly to the user's request.\n"
            "2. Use only the debate context and conversation provided.\n"
            "3. Do not invent studies, statistics, surveys, "
            "citations, organizations, researchers, dates, "
            "or other unsupported facts.\n"
            "4. If asked for a counter-argument, give a targeted "
            "counter-argument.\n"
            "5. If asked for a rebuttal, respond to the argument "
            "actually presented.\n"
            "6. If asked to compare positions, compare them fairly "
            "without inventing evidence.\n"
            "7. For political or partisan topics, remain neutral "
            "and do not select a winning side.\n"
            "8. Keep the response concise and focused.\n\n"

            "Response:"
        )

        chain = prompt | self.llm | StrOutputParser()

        args_summary = self._get_compact_arguments_summary()
        history = self._get_compact_history(max_messages=4)

        import time
        time.sleep(3)

        response = chain.invoke(
            {
                "topic": self.memory.topic,
                "referenced_argument": referenced_arg_str,
                "arguments_summary": args_summary,
                "history": history,
                "user_input": query
            }
        )

        self.memory.add_ai_message(response)

        return response

    def run_interactive_session(self):
        print("\n=== STARTING INTERACTIVE DEBATE SESSION ===")

        topic = input(
            "Enter debate topic "
            "(or press Enter for default "
            "'Should remote work become the default working model?'): "
        ).strip()

        if not topic:
            topic = (
                "Should remote work become the default "
                "working model?"
            )

        self.start_debate(topic)

        print("\n--- CONVERSATIONAL DEBATE MODE ACTIVE ---")
        print(
            "You can challenge arguments, ask for "
            "counter-arguments, request rebuttals, "
            "or compare positions."
        )
        print("Type 'exit' or 'quit' to end session.\n")

        while True:
            try:
                user_input = input("\nUser > ").strip()

                if user_input.lower() in ["exit", "quit"]:
                    print(
                        "Ending debate session. "
                        "Debate summary saved to "
                        "outputs/debate_summary.json."
                    )
                    break

                if not user_input:
                    continue

                response = self.handle_user_query(
                    user_input
                )

                print(f"\nAI > {response}")

            except KeyboardInterrupt:
                print(
                    "\nSession interrupted. Exiting."
                )
                break


if __name__ == "__main__":
    app = AIDebateApp()

    if len(sys.argv) > 1:
        topic_arg = " ".join(sys.argv[1:])
        app.start_debate(topic_arg)
    else:
        app.run_interactive_session()