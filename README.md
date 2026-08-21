# AI-Powered Finance Decision Support Assistant- Team 1



## Table of Contents

- [Overview](#overview)
- [Problem Statement](#problem-statement)
- [Target Users](#target-users)
- [Key Features](#key-features)
- [Primary Use Case](#primary-use-case)
- [Tech Stack](#tech-stack)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [User Stories & Acceptance Criteria](#user-stories--acceptance-criteria)
- [Scope](#scope)
- [3-Sprint Roadmap](#3-sprint-roadmap)
- [Success Criteria](#success-criteria)
- [Assumptions & Constraints](#assumptions--constraints)
- [Team](#team)


---

## Overview

An AI-powered conversational assistant that streamlines financial data analysis and decision-making. It consolidates data from multiple sources, understands user questions in natural language, and delivers clear, easy-to-understand answers along with an explanation of how each result was derived. When a response involves a financial calculation, the assistant outlines the calculation method and the steps followed, provides supporting sources, and links the results to relevant policies and market context. This enables financial analysts to better understand the data and make more accurate, well-informed financial decisions — with full traceability back to the source of every figure and result.

## Problem Statement

Financial analysts currently spend a significant portion of their time manually gathering and consolidating financial data from multiple sources before it can be converted into usable, actionable insights. This manual, time-intensive process creates bottlenecks that delay downstream decision-making.

## Target Users

| User | Type | Relationship to Tool |
|---|---|---|
| Financial Analysts | Direct user | Uses the tool directly to gather, consolidate, and analyse financial data |
| CFOs | Indirect user | Consumes generated insights and reports to inform decisions, without using the tool directly |

## Key Features

- **Core financial calculations** — Dollar Variance, Percentage Variance, Gross Margin, Period-over-Period Growth, Year-over-Year (YoY) Growth, and Variance Contribution by Category.
- **Traceability** — every key figure shows its source (e.g. `financial_report2.csv`).
- **Policy & market linking** — financial results are connected to relevant policy or market context with citations.
- **Analysis summaries** — short, clear summaries generated to support human review.
- **Conversational, natural-language interface** — Analysts can ask the assistant financial questions using natural language..
- **Synthetic data by design** — all test data is fictional but realistic; no real or confidential data is used.

## Primary Use Case

**Use Case Name:** Financial Performance Analysis and Decision Support

**Primary Actor:** Financial Analyst

**Goal:** Ask questions using natural language about financial performance and receive accurate, traceable analysis to support financial analysts' decision-making.

**Basic Flow:**
1. Financial Analyst asks a finance-related question(e.g. "What is the variance between actual and budgeted revenue for Q2?")
2. Assistant identifies the required financial data and calculation.
3. Assistant retrieves the required data from the available sources.
4. Assistant validates the data.
5. Assistant performs the appropriate financial calculation.
6. Assistant provides the result, calculation steps, and source traceability and links the results to relevant policies and market context. .
7. Assistant provides a short analysis summary where applicable.

**Alternative / Exception Flow:**
If required data is missing, invalid, ambiguous, or zero where division by zero would occur, the assistant does not perform the calculation. Instead, it explains the issue and identifies the missing or invalid value or source.


## Tech Stack
## Getting Started
### Prerequisites
### Installation
### Running Locally
## Usage
## Project Structure
## User Stories & Acceptance Criteria



### Epic 1: Data Ingestion & Traceability

**US-1.1** — As a financial analyst, I want the assistant to ingest CSV/SQL financial data, so that I don't have to manually consolidate it from multiple sources.
- **AC1:** The system  successfully ingests at least one CSV file and one SQL data source without requiring manual pre-processing by the user.
- **AC2:** Ingested data is validated for structural integrity correct/expected columns present, no corrupted or unreadable rows before it is used in any downstream calculation.
- **AC3:** If ingestion fails, the system returns a clear, human-readable error identifying the  affected file/source and the reason for failure (not a silent failure or generic error)

**US-1.2** — As a financial analyst, I want every key figure in a response to show its data source, so that I can trust and verify the result.
- **AC1:** Every material figure in an assistant response is tagged with its source file (e.g financial_report2.csv).
- **AC2:** The source reference includes reporting period and, where applicable, row/field identifiers.
- **AC3:** If required source data is missing or unavailable, the assistant clearly informs the user that the analysis cannot be completed and identifies the missing source or data.
- **AC4:** The assistant must not generate, assume, or fabricate missing financial data or present an unsupported result as fact.

### Implementation Notes:
- Define a standard source citation format for every figure, including details such as {file, sheet/table, row_id, period}, and apply it consistently across Epics 1, 2, 3, and 4.
- AC4 should be enforced at the prompt/response layer (e.g., grounding checks, refusal to answer without matching source data) flag this as a core guardrail to test explicitly, including adversarial test cases ("just estimate it for me")

### Epic 2: Financial Calculations

**US-2.1** — As a financial analyst, I want the assistant to calculate Dollar Variance, Percentage Variance, Gross Margin, Period-over-Period Growth, YoY Growth, and Variance Contribution by Category, so that I get accurate results without manual computation.
- **AC1:** The system correctly calculates each supported financial metric using its predefined formula and required input values.
- **AC2:** The assistant displays the calculated result together with the input values used and the source of each input.
- **AC3:** The assistant displays the calculation formula and the steps used to derive the result.
- **AC4:** The system validates that all required input values are available and valid before performing the calculation.
- **AC5:** If any required input is missing or invalid, the system does not perform the calculation or assume a value, and displays a clear error message identifying the missing or invalid input.
- **AC6:** Calculation results and their supporting inputs are traceable to their original data sources, including the relevant reporting period and, where applicable, the row or field identifier.
- **AC7:** Edge cases that would cause a mathematically undefined or misleading result (e.g., division by zero when calculating Percentage Variance or Gross Margin) are detected and return a clear explanatory message instead of an error, NaN, or Infinity.

### Implementation Notes:
- Document the exact formula for each of the six financial metrics in a shared reference file (e.g., calculations/formulas.md) so the development team uses consistent definitions for implementation and testing.
- Define standard numeric formatting and rounding rules, including decimal precision, currency formatting, and percentage display.
- For AC7, document all known mathematically undefined or invalid-result scenarios for each formula, along with the expected explanatory message for each case.
- Define what constitutes an "invalid input" for AC5, including examples such as non-numeric values, invalid negative values where not permitted, and unsupported or out-of-range reporting periods.


**US-2.2** — As a CFO, I want a short, clear analysis summary accompanying each calculation, so that I can quickly understand the result without reading raw data.
- **AC1:** The system generates a concise plain-language summary for each completed financial calculation.
- **AC2:** The generated summary is based on the calculated result and validated input values.
- **AC3:** The summary identifies the key calculated metric and its corresponding result, such as variance, growth rate, margin, or contribution.
- **AC4:** The system does not generate unsupported claims, assumptions, or conclusions that cannot be derived from the available input data and calculated results.
- **AC5:** If the required calculation cannot be completed due to missing or invalid inputs, the system does not generate an analytical summary and instead returns the relevant error message

### Implementation Notes:
- Define a standard format and maximum length for summaries (e.g., 2–3 sentences) and prevent speculative statements such as “this suggests future growth will…”.
- AC4 should be treated as a grounding constraint. Consider adding a validation step to ensure the summary only references values and conclusions supported by the calculation output before it is shown to the user.


### Epic 3: Policy & Market Context

**US-3.1** — As a financial analyst, I want financial results linked to relevant policy or market context, so that I can interpret numbers within the right framework.
- **AC1:** The system identifies and retrieves relevant company policies and market context based on the financial query and calculated result.
- **AC2:**Each company policy or market reference used in the response includes a valid source citation or link.
- **AC3:**The referenced company policy or market context must be directly relevant to the financial result and query.
- **AC4:**The assistant clearly distinguishes between the calculated financial result, company policy, and market context.
- **AC5:**If no relevant policy or market context is available, the assistant explicitly states that no relevant reference was found and does not fabricate or infer a reference.


### Implementation Notes:
- Resolve the retrieval source before estimation: Determine whether the assistant will use a document store with RAG/embedding search, a static curated reference set, or an external API. This decision will significantly affect the project scope and should be confirmed first.
- Define a measurable relevance method for AC3, such as a similarity-score threshold or required keyword/category match, so that “directly relevant” can be tested objectively.
- Confirm which policy and market documents are within the project scope and whether they are synthetic and approved under Epic 5.

### Epic 4: Conversational Interface

**US-4.1** — As a financial analyst, I want to ask finance questions in natural language, so that I don't need to learn a query syntax.
- **AC1:** The assistant correctly answers at least one finance-related question end-to-end by the end of Sprint 2.
- **AC2:** The assistant correctly answers at least five finance-related questions using synthetic data by project completion.
- **AC3:** The assistant identifies questions outside the defined use cases and returns a clear response explaining the supported use cases instead of attempting to answer them.

### Implementation Notes:
- Move sprint-specific targets and question counts (e.g., “1 question by Sprint 2” or “5 questions by project completion”) to the release plan or Definition of Done. Acceptance Criteria should focus on system behaviour and functionality, not project timelines.
- Define the out-of-scope detection mechanism for AC3, such as an intent classifier, predefined intent-to-use-case mapping, confidence threshold, or keyword/topic matching. Prepare a test dataset containing both in-scope and out-of-scope questions to validate the detection logic.
- Maintain a centralised list of supported use cases/intents as the single source of truth. The same list should be used by the intent detection logic and the user-facing response, ensuring that the system consistently identifies and communicates its supported capabilities.

**US-4.2** — As a financial analyst, I want to download an analysis artifact from the web interface, so that I can share results outside the tool.
- **AC1:** The web interface provides a download option for at least one analysis artifact for each completed analysis.
- **AC2:** The downloaded artifact contains the relevant analysis results and maintains the source citations and traceability information provided in the assistant response.
- **AC3:**The downloaded artifact can be successfully generated and opened outside the web application.

### Implementation Notes:
- Confirm the supported downloadable artifact format(s), such as PDF, XLSX, or CSV, and determine whether the user can select the preferred format.
- For AC3, define a clear compatibility test matrix specifying the supported applications or environments where the artifact must open successfully (e.g., Adobe Reader for PDF, Microsoft Excel or Google Sheets for XLSX/CSV).

### Epic 5: Data Privacy & Synthetic Data

**US-5.1** — As a project team member, I want the assistant to use only synthetic data, so that no real company or personal data is exposed.
- **AC1:** The system accepts and processes only datasets identified as synthetic and approved for project use.
- **AC2:** Synthetic data remains realistic, with plausible revenue and expense values, as defined by the project's synthetic data policy.
- **AC3:**The system blocks or flags any dataset identified as containing non-synthetic, personal, or confidential data.
- **AC4:** The assistant does not expose non-synthetic, personal, or confidential data through responses, calculations, reports, or downloadable artifacts.
- **AC5:** All blocking, flagging, or quarantine actions are logged (timestamp, dataset identifier, triggering rule, action taken) and retrievable for compliance review.

### Implementation Notes:
- Dependency note: this epic's validation logically must run before Epic 1 ingestion completes- sequence accordingly in the backlog/board.
- Define how the system will identify approved synthetic datasets, such as through dataset metadata, an approved dataset list, or a manual approval process.
- Define the actual synthetic data policy document referenced in AC2 (thresholds, ranges, formats) — confirm it exists; if not, this is a dependency to raise now.
- Define how the system will identify non-synthetic, personal, or confidential data in AC3 and specify which data types need to be checked, such as names, email addresses, tax IDs, and real company names.
- AC4 should be broken into per-surface test cases during QA planning (chat output, calculation output, report generation, file export) since each is implemented differently.
- Confirm "block" vs. "flag" behavior is it configurable, or fixed per data type/severity?

### Epic 6: Reliability & Evaluation

**US-6.1** — As a project team member, I want the assistant to be evaluated against defined accuracy and reliability criteria, so that its performance and limitations can be assessed before wider use.

- **AC1:** The system produces an evaluation report covering four measured dimensions: numerical accuracy, source/citation quality, response usefulness, and identified limitations - each dimension scored/recorded separately.
- **AC2:** The evaluation runs against the full defined question set (see Implementation Notes), with a pass/fail or scored result recorded for every question in the set — no question is skipped or left unrecorded.
- **AC3:** For each question with a numerical answer, the result is compared against a predefined expected value within a defined tolerance, and the comparison outcome (pass/fail, delta) is recorded. 
- **AC4:** For each response, source/citation quality is checked against the traceability rules defined in Epic 1 (US-1.2) and Epic 3 (US-3.1) — confirming a citation exists, is relevant, and is resolvable to real source data.
- **AC5:**  All failed test cases, identified limitations, and unsupported/out-of-scope use cases encountered during evaluation are documented in the report with enough detail to reproduce the failure (question asked, actual vs. expected output).


### Implementation Notes:
- Define and version the evaluation question set as a separate project artifact (e.g., eval/question_set_v1.md). The set should be based on the supported use cases from Epic 4 and include relevant edge cases such as missing data, invalid inputs, and out-of-scope questions
- Define the numerical accuracy tolerance for AC3, such as an exact match for currency values or an allowed tolerance for percentage calculations. Confirm the required accuracy threshold with the project stakeholders.
- Define a measurable method for evaluating response usefulness. This could use a reviewer scoring rubric (e.g., 1–5) or a fixed checklist covering criteria such as answering the question, providing sources, and avoiding unsupported claims. Select one method and document the evaluation criteria.
- Define when the evaluation should be performed: once before release or repeated after significant prompt, model, or system changes as part of regression testing. This decision will determine whether the evaluation process should be automated.
- AC4 should use the existing source and traceability requirements defined in Epic 1 and Epic 3 rather than creating separate rules. Any changes to those requirements should be reflected in the evaluation criteria.
- Define the overall pass/fail threshold for the Epic, such as requiring at least 95% of the defined question set to pass before the system is considered ready for wider use.

**US-6.2** — As a financial analyst, I want the assistant to surface missing, ambiguous, or conflicting information rather than guessing, so that I don't act on incorrect data
- **AC1:** When required data is missing, the assistant explicitly states this rather than returning a fabricated or assumed figure (consistent with the no-fabrication rule defined in US-1.2 AC4 and US-2.1 AC5).
- **AC2:** When a user's question is ambiguous (e.g., could reasonably refer to more than one time period, metric, or entity), the assistant asks a clarifying question rather than guessing which interpretation was intended.
- **AC3:**When source data conflicts (e.g., two sources report different values for the same figure/period), the assistant flags the conflict and displays both values with their respective sources, rather than silently picking one.
- **AC4:**Missing-data, ambiguity, and conflict flags are visually/structurally distinguishable from a normal successful response, consistent with how errors are surfaced elsewhere in the assistant (e.g., US-1.1 AC3).


### Implementation Notes:

- Define what qualifies as "ambiguous" for AC2 — e.g., a fixed list of ambiguity triggers (missing period reference, metric name matches multiple definitions, entity name matches multiple records) rather than leaving it to model judgment alone. This needs a test set of ambiguous vs. unambiguous sample questions, similar to Epic 4's in-scope/out-of-scope set.
- Define conflict detection logic for AC3 — this depends on Epic 1's ingestion allowing multiple sources for the same figure to coexist rather than being deduplicated/overwritten on ingest. Confirm this is supported upstream.
- AC1 is a restatement of an existing system-wide rule for this story's context — reuse the same test cases from US-1.2/US-2.1 rather than duplicating test logic.
---

## Scope

### In Scope (this term)
- Support for 5+ core financial calculations (Dollar Variance, Percentage Variance, Gross Margin, Period-over-Period Growth, YoY Growth, Variance Contribution by Category)
- Source traceability for every key figure
- Linking results to relevant policy/market context
- Short, clear analysis summaries
- Reduced manual data collection time
- Synthetic (self-generated) test data under a defined synthetic data policy

### Out of Scope (this term)
- Processing real or confidential data
- Autonomous or multi-agent systems
- Integration with internal IBM tools beyond the provided brief
- Mobile application
- Browser support beyond Chrome and Safari
- Completing financial transactions
- Finance questions outside defined use cases

## 3-Sprint Roadmap

| Sprint | Focus | Deliverables |
|---|---|---|
| **Sprint 1 — Design & Bootstrap** | Environment setup | CSV/SQL ingestion and Watsonx Orchestrate environment live; synthetic data policy defined; calculation functions and conversational workflow exist as paper prototype only |
| **Sprint 2 — Raw MVP** | Core functionality | First transparent calculation functions working end-to-end, validated via expected-results tests; conversational workflow answers at least one finance question with linked policy/market documents |
| **Sprint 3 — Refine MVP** | Hardening | Traceability, evaluation measures, and risk documentation added; testing covers numerical accuracy, citations, privacy, and failure handling across the full question set |

## Success Criteria

- Assistant accurately answers at least 5 finance questions using synthetic data
- Core calculation functions match an independently prepared expected-results dataset
- Each material answer identifies data source, reporting period, assumptions, and calculation method
- All policy/market statements include a usable citation or source link
- Missing, ambiguous, or conflicting information is surfaced, not invented
- Working web interface supports natural-language questions with at least one downloadable artifact
- Evaluation report measures numerical accuracy, source quality, response usefulness, and known limitations

## Assumptions & Constraints

**Assumptions**
- English-only product and language support
- Testing limited to Chrome and Safari
- Synthetic and publicly licensed data will be sufficient for testing
- Client-provided financial calculations are assumed correct and approved
- watsonx Developer Edition and ADK remain available throughout the project
- Client provides feedback at agreed milestones
- AI may assist with refining work (with acknowledgement); final product reviewed by the PM

**Constraints**
- Only synthetic or publicly licensed data may be used
- Application must be web-based
- Must use IBM Cloud
- Must use the IBM product stack
- Project must be completed within 9 weeks

## Team

| Role | Assigned To |
|---|---|
| Project Manager | Jack Robinson-Fletcher |
| Business Analyst | Raghdah Al-Gahdari |
| UX Designer | Monika Swiergon |
| Developer | Donovan Ong |
| Developer | Mike Jayilian |

**Client / Organization:** Aaron / IBM
