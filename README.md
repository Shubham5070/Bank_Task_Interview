Intelligent Account Servicing Workflow (IASW)

Solution Design and Implementation

1. Executive Summary
Problem:
• Bank account change requests still arrive as scanned paper forms, requiring
someone to manually read, enter, verify, and route each request.
• The process is slow, costly, and vulnerable to human error.
• What was needed wasn’t full automation, but a smarter workflow that keeps a
human in control.
Solution:
• I built an IASW prototype that acts as an intelligent "Maker" it reads the uploaded
document, pulls out the key details, checks them against business rules, scores
its own confidence, and hands a clean review package to a human checker.

• The stack: FastAPI backend, Tesseract OCR, an AI agent pipeline, and a browser-
based frontend.

• No update goes through until a real person explicitly approves it. That's non-
negotiable by design.

Key Benefits:
• Documents are processed in seconds instead of minutes with far fewer errors.
• Every extraction follows the same rules, every time no inconsistency, no fatigue.
• Human oversight is baked in, not bolted on.
• Deploys cleanly via Docker with a modular, easy-to-extend architecture.

2. Problem Understanding & Scope
The Real Problem:
• In banking operations, account change requests arrive as scanned images or
documents. Someone on the team reads them, manually types out the details,
verifies the data, and passes it to a checker every single day.
• It's repetitive, high-stakes, and surprisingly easy to get wrong. Skilled people are
spending their time on work that shouldn't require their skills.
What This Project Covers:

• Accepts scanned images and documents uploaded through a simple web UI.
• Runs OCR via Tesseract, extracts structured fields, validates them, and
calculates a confidence score.
• Stores requests in a pending workflow table until a human decides.
• Provides a clean checker interface to approve or reject each case.
• Enforces one hard rule: nothing gets finalized without a human sign-off.
What It Doesn't Cover:
• Live integration with a bank's core systems or enterprise document repositories.
• Complex multi-step workflows or advanced orchestration.
• KYC, fraud detection, or deep compliance checks beyond basic field validation.
• Any form of automatic final update that door stays firmly closed.
3. Solution Architecture
How the Pieces Fit Together
• A static frontend handles uploads and displays results in the browser.
• A FastAPI backend drives all the logic OCR, agents, database, and routing.
• Tesseract OCR converts uploaded images into raw text.
• A set of AI agents then take that raw text and turn it into something meaningful.
• SQLite stores pending requests simply and reliably without heavy infrastructure.
• A checker UI gives the human reviewer everything they need to make a confident
decision.
• A mock RPS system simulates what a real downstream banking system would
receive on approval.
End-to-End Flow
1. The user uploads a document through the frontend.
2. The file lands in the FastAPI backend, which saves it and kicks off OCR.
3. Tesseract reads the image and produces raw extracted text.
4. The Document Processor Agent parses that text into structured account
servicing fields.
5. The Validation Agent checks each field against business rules and flags anything
off.
6. The Confidence Scorer gives an honest assessment of how reliable the
extraction is.
7. The Summary Agent writes a clean, readable review note for the checker.
8. The pending record with all the above is saved to the database.
9. The checker opens the review UI, sees the full picture, and makes a call: approve
or reject.
10. If approved, the request routes to the mock RPS system and the record is marked
complete. If rejected, it's logged and closed nothing sneaks through.

4. Agent Design & Prompt Engineering
Validation Agent
• What it does: Checks the extracted fields against banking business rules are
they present, correctly formatted, and consistent?
• Takes in: Structured fields like account number, customer name, request type,
and effective date.
• Gives back: A pass/fail verdict, field level issue flags, and a structured JSON
result.

Prompt approach: The agent is given a clear role as a banking validation expert, told
exactly what to check, and instructed never to alter field values only report on them.
Document Processor Agent
• What it does: Turns messy, raw OCR text into a clean, structured request object.
• Takes in: The raw OCR output and any available upload metadata.
• Gives back: A JSON object with the key fields account number, request type,
customer name, requested change, and effective date.
Prompt approach: The agent is framed as a document extraction specialist. It's told to
map text to specific field names, return JSON only, and use null for anything it can't find
no guessing.
Confidence Scorer
• What it does: Honestly assesses how much to trust the extraction and flags
when something looks shaky.
• Takes in: Raw OCR text, extracted fields, validation results, and similarity
measures.
• Gives back: A score between 0 and 1, with a plain-English reason for anything
that pulled the score down.
Prompt approach: The agent is asked to evaluate not just score providing a rationale
that helps the checker understand where to look twice.
Summary Agent
• What it does: Writes the human facing review note that the checker actually
reads.

• Takes in: Extracted fields, validation findings, and the confidence score.
• Gives back: A concise summary and a clear recommended next step.
Prompt approach: Brevity is the priority here. The agent is instructed to keep it short,
include only what the checker needs, and always end with a clear action
recommendation.
5. Assumptions, Constraints & Limitations
What I Assumed
• Documents are text based and reasonably legible the system isn't designed for
handwritten scrawl.
• The workflow focuses on one type of account servicing change request.
• Human approval isn't optional it's the whole point.
Known Constraints
• OCR quality depends entirely on the quality of the uploaded image.
• The system uses a local SQLite table rather than an enterprise-grade workflow
database.
• The mock RPS is a simulation, not a live integration.
• There's only one approval stage no multi-step chains.
Honest Limitations
• Tesseract can struggle with handwriting, low contrast scans, or unusual
document layouts.
• A bad upload will produce a bad extraction garbage in, garbage out.
• Real banking systems like RPS or FileNet are not connected they're represented
as stubs.
• There's no escalation path or multi-checker approval flow in this version.
6. Why This Stack?
• FastAPI: lightweight, fast to build with, and perfect for a prototype that needs
clean REST endpoints without the overhead of a larger framework.
• Tesseract OCR: open-source, reliable for scanned text, and integrates smoothly
via pytesseract and Pillow.
• SQLAlchemy + SQLite : keeps persistent storage simple and portable, no
database server required.
• Ollama + RapidFuzz: enables local, containerized AI-driven parsing, validation,
and similarity analysis without external API dependencies.

• Docker: makes the whole thing deployable anywhere, system dependencies and
all, with a single command.
