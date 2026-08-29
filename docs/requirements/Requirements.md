# Requirements Specification
## AI-Powered Finance Decision Support Assistant — Team A

| | |
|---|---|
| **Document Status** | Draft — v1 |
| **Owner** | Business Analyst (Raghdah Al-Gahdari) |
| **Client / Organization** | Aaron / IBM |


## Table of Contents

- [1. Overview](#1-overview)
- [2. Problem Statement](#2-problem-statement)
- [3. Target Users](#3-target-users)
- [4. Functional Requirements](#4-functional-requirements)
- [5. Non-Functional Requirements](#5-non-functional-requirements)
- [6. Primary Use Case](#6-primary-use-case)
- [7. Scope](#7-scope)
- [8. Success Criteria](#8-success-criteria)
- [9. Assumptions & Constraints](#9-assumptions--constraints)

---

## 1. Overview

An AI-powered conversational assistant that streamlines financial data analysis and decision-making. It consolidates data from multiple sources, understands user questions in natural language, and delivers clear, easy-to-understand answers along with an explanation of how each result was derived. When a response involves a financial calculation, the assistant outlines the calculation method and steps followed, provides supporting sources, and links results to relevant policies and market context — giving financial analysts full traceability back to the source of every figure and result.

## 2. Problem Statement

Financial analysts currently spend a significant portion of their time manually gathering and consolidating financial data from multiple sources before it can be converted into usable, actionable insights. This manual, time-intensive process creates bottlenecks that delay downstream decision-making.

## 3. Target Users

| User | Type | Relationship to Tool |
|---|---|---|
| Financial Analysts | Direct user | Uses the tool directly to gather, consolidate, and analyse financial data |
| CFOs | Indirect user | Consumes generated insights and reports to inform decisions, without using the tool directly |

---

## 4. Functional Requirements

### 4.1 Data Ingestion

| ID | Requirement |
|---|---|
| FR-01 | The system shall ingest structured financial data supplied as CSV files and shall handle common file-format variations, including delimiters and text encoding, without requiring the user to manually clean or reformat the file. |
| FR-02 | The system shall ingest structured financial data from a relational database source (IBM Db2). |
| FR-03 | The system shall use parameterized queries or prepared statements for all database queries and shall not directly insert user-supplied input into query text, to prevent injection vulnerabilities. |
| FR-04 | The system shall validate every ingested record against a defined set of required fields (see the project data dictionary) before the record is used in any calculation, and shall reject or flag records that fail validation. |
| FR-05 | The system shall retrieve financial values using exact lookups rather than approximate or similarity-based search, so that each value used in a calculation can be traced to a specific source record.|

### 4.2 Calculations & Traceability

| ID | Requirement |
|---|---|
| FR-06 | The system shall provide source traceability for every key figure presented in a response, including the source file or database table, record or row, and column. Where a comparison uses data from two separate reporting periods, the system shall provide source traceability for each period.|
| FR-07 | The system shall calculate six core financial metrics: Dollar Variance, Percentage Variance, Gross Margin, Period-over-Period Growth, Year-over-Year Growth, and Variance Contribution by Category.(Exact formulas and business definitions are maintained in the *Financial_Calculation_Formulas.md*).|
| FR-08 | The system shall display, for every calculation, the result, the formula applied, the calculation steps, and full source traceability (per FR-06). |
| FR-09 | The system shall generate a short plain-language summary (target: 3–6 sentences) **in addition to** — not instead of — the full result/formula/steps/sources breakdown (FR-08). The summary states only the metric and result in plain language, with no repeated steps and no unsupported or forward-looking claims. |

### 4.3 Edge Cases

| ID | Requirement |
|---|---|
| FR-10 | The system shall handle all calculation edge cases (division by zero, missing/non-numeric values, negative results, mismatched or non-adjacent reporting periods) exactly as defined in the *Financial_Calculation_Formulas.md*, including: never silently substituting a missing value with zero; never displaying an unreadable result (e.g. NaN, Infinity, raw error code); always identifying the specific value/source causing the issue; and always showing negative results as-is with an explanatory note. |
| FR-11 | The system shall surface missing, ambiguous, or conflicting information explicitly — asking for clarification or stating the conflict — rather than guessing or fabricating a result. |

### 4.4 Policy & Market Context

| ID | Requirement |
|---|---|
| FR-12 | The system shall retrieve and link relevant company policy or market context to financial results, drawn from an approved, team-maintained reference source, with a source citation. |
| FR-13 | The system shall clearly distinguish, in its response, between the calculated financial result, cited company policy, and cited market context. |

### 4.5 Conversational Interface

| ID | Requirement |
|---|---|
| FR-14 | The system shall accept and answer finance-related questions posed in natural language. |
| FR-15 | The system shall identify questions that fall outside its scope (as defined in Section 7) and respond by clarifying the use cases it supports, rather than attempting to answer them. |
| FR-16 | The system shall provide a downloadable analysis artifact containing the financial results, calculation details, source citations, and source traceability defined in FR-06 and FR-08. |

### 4.6 Data Privacy

| ID | Requirement |
|---|---|
| FR-17 | The system shall accept only datasets identified as synthetic and approved for project use. |
| FR-18 | The system shall block or flag any dataset or value containing non-synthetic, personal, or confidential data. |
| FR-19 | The system shall log all data blocking/flagging actions (timestamp, dataset identifier, triggering rule, action taken), retrievable for compliance review. |

## 5. Non-Functional Requirements

| ID | Category | Requirement |
|---|---|---|
| NFR-01 | Formatting | Currency displayed as `$#,###.##` (2 decimal places); percentages displayed to 1 decimal place. Full precision retained internally; rounding applied at display only. |
| NFR-02 | Reliability | The system must never present a fabricated, assumed, or unsupported figure as fact. |
| NFR-03 | Reliability | The system shall provide a clear, human-readable error message when a calculation fails, identifying the affected source and the reason for the failure (e.g., a missing required value). |
| NFR-04 | Security & Privacy | Only synthetic or publicly licensed data may be processed; no real, personal, or confidential data permitted at any stage (see FR-17/FR-18). |
| NFR-05 | Security | Database credentials must never be hard-coded or stored in the project's source repository. |
| NFR-06 | Usability | Summaries (FR-09) must avoid forward-looking or speculative claims (e.g. "this suggests future growth will..."). |
| NFR-07 | Maintainability | Financial calculation formulas shall be maintained in Financial_Calculation_Formulas.md. Any formula change shall first be reflected in this document and then consistently implemented in the system and associated tests. |
| NFR-08 | Compatibility | The application must run as a web-based tool, supporting Chrome and Safari only. |
| NFR-09 | Language Support | The product supports English only. |

---

## 6. Primary Use Case

**Use Case Name:** Financial Performance Analysis and Decision Support.

**Primary Actor:** Financial Analyst.

**Goal:** Ask questions using natural language about financial performance and receive accurate, traceable analysis to support decision-making.

**Basic Flow:**
1. Financial Analyst asks a finance-related question (e.g. "What is the variance between actual and budgeted revenue for Q2?").
2. Assistant identifies the required financial data and calculation.
3. Assistant retrieves the required data from the available sources.
4. Assistant validates the data.
5. Assistant performs the appropriate financial calculation.
6. Assistant provides the result, calculation steps, and source traceability, and links the results to relevant policies and market context.
7. Assistant provides a short analysis summary where applicable.

**Alternative / Exception Flow:**
If required data is missing, invalid, ambiguous, or zero where division by zero would occur, the assistant does not perform the calculation. Instead, it explains the issue and identifies the missing or invalid value or source.

---

## 7. Scope

### In Scope (this term)
The following activities are included within this project's Scope:
1. Support for at least 5 core financial calculations (minimum project requirement); the team has selected 6 to implement: Dollar Variance, Percentage Variance, Gross Margin, Period-over-Period Growth, Year-over-Year (YoY) Growth, and Variance Contribution by Category.
2. Show the source of each key figure (Traceability) — e.g., financial_report2.csv.
3. Link financial results to relevant policies and/or market context.
4. Generate a short, clear analysis summary to support human review and decision-making.
5. Reduce time spent collecting and organizing financial data.
6. Help analysts focus on decision-making instead of manual data gathering.
7. Use synthetic (self-generated) financial data for testing, since real data isn't available.
8. Define our own synthetic data policy, ensuring that no real company or personal data is used. All data will be fictional but realistic, using plausible values for items such as revenue and expenses.

### Out of Scope (this term)
The following items are excluded from the project's scope:
1. Processing real or confidential data: synthetic data will be used instead, since real financial data isn't available or appropriate for this project.
2. Support for autonomous or multi-agent systems is out of scope: The assistant will operate as a single tool that requires user input and guidance.
3. Integration with other internal IBM tools not listed in the provided brief: to stay within the agreed scope.
4. A mobile application: development will focus on a single platform this term.
5. Browser testing will be limited to Chrome and Safari: due to the project's timeline.
6. Completing financial transactions: The assistant will support financial analysis only and will not execute financial actions.
7. Financial questions outside of defined use cases are out of scope to keep the assistant focused and reliable within its intended purpose.

## 8. Success Criteria

- Assistant accurately answers at least 5 finance questions using synthetic data.
- Core calculation functions match an independently prepared expected-results dataset.
- Each material answer identifies data source, reporting period, assumptions, and calculation method.
- All policy/market statements include a usable citation or source link.
- Missing, ambiguous, or conflicting information is surfaced, not invented.
- Working web interface supports natural-language questions with at least one downloadable artifact.
- Evaluation report measures numerical accuracy, source quality, response usefulness, and known limitations.

## 9. Assumptions & Constraints

**Assumptions**
- The product and supported language will be English only.
- Testing will be limited to Chrome and Safari.
- Synthetic data and publicly licensed data will be sufficient for testing the proposed solution.
- The financial calculations provided by the client are assumed to be correct and approved.
- The watsonx Developer Edition and ADK will remain available throughout the project.
- The client will provide feedback at agreed project milestones.
- AI may be used to help refine work, with acknowledgement, but the final product will be reviewed by the PM.

**Constraints**
- Only synthetic or publicly licensed data may be used.
- Application must be web-based.
- Must use IBM Cloud and the IBM product stack.
- Project must be completed within 9 weeks.

