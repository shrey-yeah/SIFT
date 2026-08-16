Mission Description
What this mission is about
Companies deal with large volumes of internal documents — HR policies, product manuals, onboarding guides, SOPs — and employees waste time hunting for answers buried in PDFs. Build an AI assistant that lets users ask questions in plain English and get accurate, cited answers from a document library.

Instructions
Follow these steps to complete the mission
Use these tech stacks according to your track.
Python / GenAI : FastAPI + LangChain ,ChromaDB / FAISS, Streamlit



Deliverables
What you must hand in to complete this mission

Parse and chunk 5+ PDFs into clean text

Generate and store embeddings in a vector DB

Build the RAG pipeline - query → retrieve →

answer

Streamlit UI with source citation on every answer

Demo to mentor with 3 test documents


How You'll Be Evaluated
Your mentor scores you on these dimensions during the demo — click any category to see the parameters
M6A
AI Concept and Understanding
21%
▲
M6A1
Explains the core AI concept in plain English — no code, no slides
Ask: "Explain RAG / prompt engineering / JSON schema to me like I'm a Product Manager"
M6A2
Knows why their technical approach was chosen
Ask: "Why ChromaDB and not a simple keyword search?" / "Why few-shot vs zero-shot?"
M6A3
Understands what the model is doing between input and output
Ask: "Walk me through what happens after I submit the query until the answer appears"
M6A4
Can identify where the AI is most likely to fail or be unreliable
Ask: "Where is your system most likely to give a wrong answer?"
M6A5
Connects the AI technique to a real business outcome
Ask: "Who would use this and what specific problem does it solve for them?"


M6B1
AI output is consistent — same input produces equivalent output
Run identical input twice, 5 minutes apart. Compare outputs.
M6B2
Edge cases are handled gracefully — empty input, very long input, wrong language
Test each: blank input → does it error or respond meaningfully?
M6B3
API failure is handled without crashing the system
Use an invalid API key or disconnect. Does it crash or show a useful error?
M6B4
Output is in a usable, readable format for the end user
Is the output human-readable? Structured where structure is needed?
M6B5
No hardcoded secrets — API keys in .env or secrets manager
Ask them to show the repo root and config files.


M6C1
The output actually solves the stated business problem
Run the real use case: upload a real doc / paste real feedback / route a real ticket
M6C2
A non-technical user could operate it without explanation
Ask a colleague unfamiliar with the project to use it unassisted
M6C3
Interface / output format is appropriate for the context
CLI for DevOps, dashboard for analytics, chat for doc Q&A — does the format fit?
M6C4
Scope is complete — not a demo that promises more than it delivers
Does it work end-to-end? Are there obvious missing pieces?


M6D1
Can articulate what was hardest and why
Ask: "What took you the longest? What broke that surprised you?"
M6D2
Has a clear "what I'd do differently" answer
Ask: "If you started today, what would you change in your approach?"
M6D3
Commit history shows consistent progress over the 2-week sprint
Check GitHub: 2-week commit spread vs. a single dump the night before
M6D4
Knows what they don't know yet — honest self-awareness
Ask: "What aspect of this are you least confident about?"
M6D5
Researched beyond the brief — encountered a problem and solved it independently
Ask: "What did you figure out that wasn't in the instructions?"


M6E1
Code is readable — naming, structure, comments make intent clear
Scan the main file: can you understand each section in < 2 minutes?
M6E2
README or documentation allows another developer to run it
Try to follow the README cold — does it work?
M6E3
No obvious security issues — validated inputs, no secrets in code
Check for raw API keys, unvalidated user input, SQL-injection patterns
M6E4
Follows conventions for their own stack (evaluated within track only)
Python → PEP8; Java → Spring conventions; JS → ESLint; DevOps → containerised, idempotent




