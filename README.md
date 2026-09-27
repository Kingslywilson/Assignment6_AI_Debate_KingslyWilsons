# AI Debate System

## Overview

An AI-powered multi-stage debate system built using Python, LangChain, Groq, and Pydantic.

The system analyzes a debate topic, generates arguments for both sides, produces evidence/reasoning, creates counter-arguments and rebuttals, and generates a structured debate summary.

## Features

* Topic analysis
* Supporting and opposing claim generation
* Evidence and reasoning generation
* Counter-argument generation
* Rebuttal generation
* Neutral analysis
* Structured debate summary
* Conversational debate mode
* Conversation memory
* Pydantic structured outputs
* Evidence integrity protection
* JSON debate summary export
* Groq LLM integration

## Technologies

* Python
* LangChain
* Groq
* Pydantic
* python-dotenv

## Project Structure

```text
Assignment6_AI_Debate_System/
│
├── app.py
├── debate_pipeline.py
├── memory.py
├── models.py
├── requirements.txt
├── .env
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

## Configuration

Create a `.env` file and add the Groq API key:

```text
GROQ_API_KEY=your_groq_api_key
```

## Running the Application

Run the application using:

```text
python app.py
```

Enter a debate topic when prompted.

After the main debate pipeline completes, the system enters conversational debate mode.

Example questions:

```text
Give me the strongest counter-argument against the supporting position.
Now rebut that counter-argument.
Compare the strongest supporting and opposing arguments.
```

Type `exit` or `quit` to end the session.

## Debate Pipeline

The system follows these stages:

1. Topic Analysis
2. Claim Generation
3. Evidence / Reasoning
4. Counter-Argument
5. Rebuttal
6. Neutral Analysis
7. Structured Debate Summary
8. Conversational Debate

## Evidence Integrity

The system is designed to avoid fabricated:

* Research studies
* Statistics
* Surveys
* Citations
* Organizations
* Researchers
* Dates
* Reports
* URLs

When verified evidence is not available, the system uses reasoning or clearly identified examples instead.

## Output

After a debate session, the structured result is saved as:

```text
outputs/debate_summary.json
```

## Testing

Testing results are documented in:

```text
testlog.md
```

The system was tested for the main debate pipeline, evidence integrity, counter-arguments, rebuttals, comparisons, conversation memory, and interactive session handling.
