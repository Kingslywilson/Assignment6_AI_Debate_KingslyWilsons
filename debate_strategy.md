# Technical Strategy Documentation - AI Debate Generator

## 1. Pipeline Design

The system implements a multi-stage sequential reasoning pipeline using LangChain Expression Language (LCEL). Rather than asking a single LLM prompt to generate an entire debate, the task is decomposed into dedicated, modular stages where each stage's output feeds directly into the next.

```
Debate Topic
      │
      ▼
Topic Analysis (Issue breakdown, scope, key terms, stakeholders, disagreement areas)
      │
      ▼
Claim Generation (Dual-perspective distinct claims for supporting & opposing sides)
      │
      ▼
Evidence / Reasoning Generation (Structured support, enforcing verified evidence vs logical reasoning)
      │
      ▼
Counter-Argument Generation (Targeted counters addressing specific claim & support)
      │
      ▼
Rebuttal Generation (Specific rebuttals resolving counter-arguments)
      │
      ▼
Structured Debate Summary (Evaluation of strongest/weakest arguments, position analysis & conclusion)
```

### Why Multiple Stages Are Used
- **Decomposition**: Complex reasoning tasks suffer from quality degradation when forced into a single monolithic generation step.
- **Targeted Prompting**: Each stage enforces strict domain rules (e.g. evidence integrity in stage 2, direct relevance in stage 3 and 4).
- **Schema Validation**: Pydantic structured output validation occurs at key checkpoints to guarantee data integrity across stages.

---

## 2. Prompt Engineering & Design

Prompts are stored as clean template files in the `prompts/` directory:

1. **`topic_analysis_prompt.txt`**: Instructs the LLM to perform neutral pre-debate analysis without taking a side.
2. **`claim_generation_prompt.txt`**: Enforces dual-side fairness and prevents duplicate/repetitive claims.
3. **`evidence_prompt.txt`**: Mandates strict classification into `Verified Evidence` or `Reasoning / Example`. Strictly forbids inventing fake studies, dates, or citations.
4. **`counter_argument_prompt.txt`**: Requires counter-arguments to address the exact core logic of the claim rather than using generic opposing statements.
5. **`rebuttal_prompt.txt`**: Requires rebuttals to address the counter-argument directly with procedural or policy mitigations.
6. **`debate_summary_prompt.txt`**: Synthesizes the debate, evaluates argument strengths neutrally, and determines if one side is better supported by generated evidence.

---

## 3. Structured Output & Validation

Pydantic models in `models.py` define strict schemas for all workflow outputs:
- **`TopicAnalysis`**: Validates issue structure, scope, stakeholders, and assumptions.
- **`ClaimSet`**: Enforces dual list structure for supporting and opposing claims.
- **`EvidenceItem`**: Enforces `support_type` taxonomy.
- **`DebateArgument`**: Links `claim`, `support`, `counter_argument`, and `rebuttal`.
- **`DebateSummary`**: Enforces structured JSON output saved to `outputs/debate_summary.json`.

---

## 4. Conversation Memory & Multi-Turn Context

The `DebateMemory` class manages turn history and debate state:
- Maintains topic, active arguments, active side, and turn history.
- **Ambiguous Query Handling**: Identifies queries like *"Why is that wrong?"* when target argument context is absent, prompting the user for clarification rather than guessing.
- **User Challenge Resolution**: Matches user challenges against active claims and uses contextual prompt templates to formulate fair, robust responses.

---

## 5. Evidence Handling & Hallucination Prevention

To prevent AI hallucination:
- The system explicitly forbids inventing fake empirical studies, statistics, papers, quotes, or organizations.
- If verified empirical data is absent from context/pre-training, the model MUST select `"Reasoning / Example"` as its support type.
- User requests asking to fabricate fake evidence are explicitly flagged and rejected with a safety warning.
