from typing import List, Dict, Any, Optional
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage


class DebateMemory:
    def __init__(self, topic: str = ""):
        self.topic: str = topic
        self.messages: List[BaseMessage] = []
        self.claims: List[Dict[str, Any]] = []
        self.active_side: str = "general"
        self.last_discussed_argument: Optional[Dict[str, Any]] = None

    def set_topic(self, topic: str):
        self.topic = topic
        self.messages.clear()
        self.claims.clear()
        self.last_discussed_argument = None

    def set_claims(self, arguments: List[Dict[str, Any]]):
        self.claims = arguments

    def add_user_message(self, text: str):
        self.messages.append(HumanMessage(content=text))

    def add_ai_message(self, text: str):
        self.messages.append(AIMessage(content=text))

    def get_history_as_string(self) -> str:
        history_str = []
        for msg in self.messages[-10:]:
            prefix = "User: " if isinstance(msg, HumanMessage) else "AI: "
            history_str.append(f"{prefix}{msg.content}")
        return "\n".join(history_str)

    def set_last_discussed(self, argument: Dict[str, Any], side: str = "general"):
        self.last_discussed_argument = argument
        self.active_side = side

    def find_matching_argument(self, query: str) -> Optional[Dict[str, Any]]:
        lower_q = query.strip().lower()
        for arg in self.claims:
            claim_text = arg.get("claim", "").lower()
            words = [w.strip("?,.!") for w in claim_text.split() if len(w) > 4]
            if any(w in lower_q for w in words):
                self.set_last_discussed(arg)
                return arg
        return self.last_discussed_argument

    def is_ambiguous_query(self, query: str) -> bool:
        lower_q = query.strip().lower()
        ambiguous_phrases = [
            "why is that wrong", "why is that wrong?",
            "what is wrong with that", "what is wrong with that?",
            "explain that", "explain that?",
            "why", "how so", "elaborate", "what about that"
        ]
        if any(p == lower_q for p in ambiguous_phrases) and not self.last_discussed_argument:
            return True
        return False

    def get_claims_clarification_prompt(self) -> str:
        if not self.claims:
            return "Which specific argument or perspective are you referring to? Please specify your question."
        claim_bullets = "\n".join([f"- {c.get('claim')}" for c in self.claims])
        return (f"Your query is ambiguous as to which point you are referring to. "
                f"Which of the following arguments would you like to discuss?\n{claim_bullets}")
