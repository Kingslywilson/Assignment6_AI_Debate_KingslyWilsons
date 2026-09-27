# Assignment 6 — AI Debate & Counter-Argument Generator

## Overview

An AI-powered multi-stage debate system built using Python, LangChain, Groq, and Pydantic.

The system analyzes a debate topic, generates supporting and opposing arguments, produces reasoning, counter-arguments and rebuttals, maintains conversational context, and generates a structured debate summary.

## Features

* Debate topic validation
* Topic analysis
* Supporting arguments
* Opposing arguments
* Claim generation
* Evidence / reasoning generation
* Counter-argument generation
* Rebuttal generation
* Neutral analysis
* Conversational debate mode
* Conversation memory
* Ambiguous query handling
* Pydantic structured output
* Evidence integrity and hallucination prevention
* Structured debate summary
* JSON output generation

## Technologies

* Python
* LangChain
* LangChain Groq
* Groq LLM
* Pydantic
* python-dotenv

## Python Version

Python 3.11+

## Project Structure

```text
Assignment6_AI_Debate/
│
├── app.py
├── debate_pipeline.py
├── memory.py
├── models.py
├── requirements.txt
├── .env.example
├── README.md
├── debate_strategy.md
├── test_log.md
│
├── chains/
│   ├── topic_analysis.py
│   ├── claim_generation.py
│   ├── evidence_generation.py
│   ├── counter_argument.py
│   ├── rebuttal.py
│   ├── neutral_analysis.py
│   └── debate_summary.py
│
├── prompts/
│   ├── topic_analysis_prompt.txt
│   ├── claim_generation_prompt.txt
│   ├── evidence_prompt.txt
│   ├── counter_argument_prompt.txt
│   ├── rebuttal_prompt.txt
│   ├── neutral_analysis_prompt.txt
│   └── debate_summary_prompt.txt
│
└── outputs/
    └── debate_summary.json
```

## Debate Workflow

The application uses a multi-stage LangChain workflow:

```text
Debate Topic
     ↓
Topic Analysis
     ↓
Claim Generation
     ↓
Evidence / Reasoning
     ↓
Counter-Argument
     ↓
Rebuttal
     ↓
Neutral Analysis
     ↓
Structured Debate Summary
     ↓
Conversational Debate
```

Each stage performs a specific task and passes its result to the next stage.

## LangChain Concepts Used

* `PromptTemplate`
* LangChain chains
* Multi-stage LLM workflow
* Pydantic structured output
* `PydanticOutputParser`
* Conversation memory/context
* LangChain Groq integration
* `StrOutputParser`

## LLM Configuration

This project uses Groq through LangChain.

The configured model is:

```text
openai/gpt-oss-120b
```

The API key is loaded from an environment variable.

## Environment Configuration

Create a `.env` file in the project directory:

```text
GROQ_API_KEY=your_groq_api_key
```

Do not include the actual `.env` file or API key in the submission.

A `.env.example` file is included for reference.

## Installation

Create and activate a Python virtual environment, then install the dependencies:

```text
pip install -r requirements.txt
```

## Run the Application

Start the application with:

```text
python app.py
```

Enter a debate topic when prompted.

Example:

```text
Should remote work become the default working model?
```

The application then runs the complete multi-stage debate pipeline.

## Example Debate Topics

```text
Should remote work become the default working model?

Should AI tools be allowed in education?

Is cloud computing better than on-premise infrastructure for startups?

Should companies adopt a four-day work week?

Is online learning as effective as classroom learning?
```

## Conversational Debate

After the main pipeline completes, the application enters conversational debate mode.

Example:

```text
User > Give me the strongest counter-argument against the supporting position.

User > Now rebut that counter-argument.

User > Compare the strongest supporting and opposing arguments.
```

The application maintains the current debate topic, arguments, previous discussion, and relevant conversational context.

It also asks for clarification when a follow-up question is ambiguous.

## Structured Output

Pydantic models are used to validate structured results such as:

* Topic analysis
* Debate arguments
* Evidence
* Debate summary

The final summary includes:

* Strongest supporting argument
* Strongest opposing argument
* Weakest supporting argument
* Weakest opposing argument
* Key counter-arguments
* Key rebuttals
* Better-supported position
* Neutral conclusion

For political or partisan topics, the system keeps the comparison neutral instead of selecting a winning side.

## Evidence Integrity

The system is designed not to fabricate evidence.

It does not intentionally invent:

* Research studies
* Statistics
* Academic papers
* Surveys
* Quotes
* Organizations
* Researchers
* Dates
* Citations

When verified evidence is unavailable, the system uses:

```text
Reasoning / Example
```

instead of presenting an invented source as factual evidence.

## Output

The generated debate result is saved to:

```text
outputs/debate_summary.json
```

## Error Handling

The application handles:

* Empty topics
* Whitespace-only topics
* Very broad topics
* Ambiguous conversational queries
* Unsupported evidence requests
* Missing Groq API key

## Testing

Testing results are documented in:

```text
test_log.md
```

The application has been tested for:

* Topic analysis
* Supporting arguments
* Opposing arguments
* Evidence/reasoning
* Counter-arguments
* Rebuttals
* Neutral analysis
* Conversation memory
* Follow-up questions
* Argument comparison
* Evidence integrity
* Structured summary
* JSON output
* Interactive session handling

## Strategy Documentation

The implementation approach is documented in:

```text
debate_strategy.md
```

It explains the multi-stage pipeline, prompt design, structured output, conversation memory, and evidence-handling strategy.

## Known Limitations

* The system does not perform independent web research.
* Evidence quality depends on the information available to the LLM.
* When verified evidence is unavailable, the system uses reasoning/examples instead.
* Long conversations may require context reduction to stay within the LLM token limits.
* The generated arguments should be treated as AI-generated reasoning rather than authoritative research.

## Submission

The submission ZIP should contain the complete project, including:

* Python source files
* Chain files
* Prompt files
* `README.md`
* `test_log.md`
* `debate_strategy.md`
* `requirements.txt`
* `.env.example`
* Generated `outputs/debate_summary.json`

Do not include:

* `.env`
* API keys
* `venv/`
* `.venv/`
* `__pycache__/`
* IDE configuration
* Temporary/cache files
