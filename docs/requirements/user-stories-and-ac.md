# AI Finance Decision Support — User Stories & Acceptance Criteria

**Project:** AI Finance Decision Support — Team 1, built for IBM
**Document type:** Product Requirements — User Stories & Acceptance Criteria
**Status:** Draft — pending open items with tech team. Will update once confirmed
**Last updated:** 2026-09-04

---

## Epic 1: Data Ingestion & Traceability

### US-1.1 — Data Ingestion
As a financial analyst, I want the assistant to ingest CSV/SQL financial data, so that I don't have to manually consolidate it from multiple sources.

> *Scope note: the project's calculations currently run on two generated CSV files (financial data for 2025 and 2026). The technical team has confirmed a SQL data source will also be supported — the specific database type (e.g. PostgreSQL, MySQL, SQL Server) is still to be confirmed with the technical team.*

- **AC1:** The system successfully ingests financial data from at least one CSV file and one SQL data source without requiring the user to manually reformat or pre-clean the data first. Given the project's CSV data is small (monthly financial data per year, well under 1,000 rows per file), no special handling for large files is required for this phase.
- **AC2:** Before any data is used in a calculation or shown to the user, the system checks that it is structurally valid — all expected columns are present, values are in a usable format, and no rows are corrupted or unreadable.
- **AC3:** When a source contains some invalid or unreadable rows, the system ingests all structurally valid rows normally and does **not** reject the entire file. For each excluded row, the user is told which row and column caused the issue and why — the system never silently drops rows or silently includes them anyway.
- **AC4:** If ingestion fails entirely, the system tells the user exactly which file or source failed and the reason, in plain language — never a silent failure or a generic error message.

### US-1.2 — Source Traceability
As a financial analyst, I want every key figure in a response to show its data source, so that I can trust and verify the result.

- **AC1:** Every figure in an assistant response that is pulled from or calculated using source data is tagged with the file or source it came from.
- **AC2:** The source reference tells the user enough to find the original data themselves — at minimum, the reporting period and, where relevant, the specific row or field it came from.
- **AC3:** When a figure is calculated from more than one source (e.g. a total combining two files), the response shows all contributing sources, not just one.
- **AC4:** If a calculation cannot be completed because required data is missing, the assistant clearly states it cannot complete the analysis and identifies exactly which file, row, and column the missing value belongs to — not a general "data unavailable" message.
- **AC5:** The assistant never generates, estimates, or assumes a financial figure that isn't backed by actual source data, even if the user asks it to "just estimate" or "give a rough number."

### US-1.3 — Business Rule Flagging
As a financial analyst, I want the assistant to explain why a result was flagged, so that I understand whether it reflects a real issue or just normal variation.

- **AC1:** When a calculated result breaches a defined business rule threshold (e.g. revenue variance above 8%), the assistant flags the result and states which business rule triggered the flag.
- **AC2:** The explanation names the specific rule and threshold that was breached (e.g. "flagged because revenue variance exceeds the 8% threshold defined in [rule name]"), not just that "something looks unusual." The citation includes the version number of `business-rules.md` in effect at the time, so the analyst knows exactly which version of the rules was applied.
- **AC3:** The flag and its explanation are shown together with the result — the user never sees a flagged figure without also seeing why it was flagged, and the flag is presented as **"this result requires review"** rather than as a conclusion that something is wrong.
- **AC4:** The assistant does not make or imply a judgment call on the flagged result (e.g. it does not say "this is an error" or recommend an action) — it only presents the figure, the rule breached, and the fact that it needs review. The decision on how to interpret or act on the flag remains with the financial analyst.

---

## Epic 2: Financial Calculations

### US-2.1 — Core Calculations
As a financial analyst, I want the assistant to calculate Dollar Variance, Percentage Variance, Gross Margin, Period-over-Period Growth, YoY Growth, and Variance Contribution by Category, so that I get accurate results without manual computation.

- **AC1:** The system correctly calculates each of the six supported metrics using its standard, agreed-upon formula.
- **AC2:** The assistant displays the calculated result together with the input values used and the source of each input value.
- **AC3:** The assistant shows the formula and the step-by-step logic used to reach the result — not just the final number.
- **AC4:** Before performing a calculation, the system checks that all required inputs are present and valid (e.g. numeric where a number is expected, no negative values where negatives aren't valid, reporting period is one the system supports).
- **AC5:** If any required input is missing or invalid, the system does not perform the calculation and does not assume or substitute a value — it displays a clear message identifying exactly which input is missing or invalid and why.
- **AC6:** Calculation results and their inputs are traceable to their original data sources, including reporting period and, where applicable, row/field identifiers (consistent with US-1.2).
- **AC7:** The system correctly distinguishes between two different result scenarios:
  - **AC7a — Negative results:** When a calculation produces a mathematically valid negative result (e.g. negative variance, negative growth), the result is displayed normally along with a clear label/explanation that it represents a decrease or negative change — never worded in a way that could be mistaken for a positive/growth result.
  - **AC7b — Undefined results (e.g. division by zero):** When a calculation cannot be performed because a required input value is zero, the system does not return an error code, "NaN," or "Infinity." Instead, it returns a clear message stating the calculation cannot be completed, and traces the cause to its exact source — naming the specific file, column, and row where the zero (or invalid) value came from. This traceability must never be generic or approximate.
- **AC8:** If a calculated result triggers a business rule flag (per US-1.3), that flag and its explanation are shown alongside the result — the calculation output and the flag are never presented separately.

### US-2.2 — Analysis Summary
As a financial analyst, I want a short, clear analysis summary accompanying each calculation, so that I can quickly understand the result and prepare accurate reporting for stakeholders like the CFO.

- **AC1:** Every completed calculation is accompanied by a short, plain-language summary (2–3 sentences).
- **AC2:** The summary is based only on the calculated result and the validated input values used to produce it — nothing outside that scope.
- **AC3:** The summary names the specific metric and its result (e.g. "Gross Margin for Q2 2026 is 34%"), not a vague statement.
- **AC4:** The summary states facts derived directly from the calculation only. It does not include predictions, interpretations, or claims about causes/future outcomes that aren't directly supported by the input data.
- **AC5:** If the calculation could not be completed due to missing or invalid inputs, no summary is generated — the user sees the relevant error message instead (per US-2.1 AC5).
- **AC6:** When a result is flagged under a business rule (per US-1.3), the flag and its explanation are shown to the financial analyst together with the summary, so the analyst can review and decide how to reflect it (if at all) in whatever report they later share with the CFO or other stakeholders.

---

## Epic 3: Market Context

> *Scope note: the project has no separate "company policy" document. Threshold/classification rules are covered by `business-rules.md` (see US-1.3), and dataset-generation rules are covered by `synthetic-data-policy.md` (see Epic 5). This epic covers only external market context, sourced from the internal `market-context.md` file maintained for the project.*

### US-3.1 — Contextualizing Results with Market Conditions
As a financial analyst, I want financial results linked to relevant external market context, so that I can understand not just *what* happened, but whether something in the market could explain *why*.

- **AC1:** When a financial result is calculated, the system checks the internal `market-context.md` file for external market context (economic or industry conditions/events) that could plausibly relate to that specific result, and retrieves it if found.
- **AC2:** Every market context reference shown to the user includes a valid source citation (document/source name, the `market-context.md` version number in effect at the time, and, where applicable, date or section).
- **AC3:** The market context referenced is directly relevant to the financial result and query — relevance is determined by matching the calculation's category (e.g. Revenue, COGS, Marketing Expense) to a related market driver, not a general or loosely-associated reference.
- **AC4:** The assistant clearly separates and labels two things in its response: the calculated financial result, and the market context reference. The market context is always stated in **probabilistic/possibility language** (e.g. "this may be related to...") and is explicitly flagged as requiring the financial analyst's own evaluation — it is never presented with the same certainty as the calculated result.
- **AC5:** If no relevant market context exists for a given result, the assistant explicitly states that no relevant external context was found. It does not fabricate, infer, or loosely associate an unrelated market event just to provide an answer.

---

## Epic 4: Conversational Interface

> *Scope note: the assistant is accessed by a single user role — the financial analyst. No tiered permissions or role-based access levels are required for this phase.*
>
> *Open item — pending team confirmation: does the assistant need to support follow-up questions that rely on earlier conversation context (e.g. "and what about the previous quarter?" without repeating the metric), or is every question treated independently for this phase? US-4.1 below assumes each question is answered independently until this is confirmed.*

### US-4.1 — Natural Language Q&A
As a financial analyst, I want to ask finance questions in natural language, so that I don't need to learn a query syntax.

- **AC1:** The assistant correctly interprets and answers finance-related questions in natural language, without requiring the user to use a specific query syntax or format.
- **AC2:** The assistant accurately answers questions covering the six financial calculations defined in US-2.1 (Dollar Variance, Percentage Variance, Gross Margin, Period-over-Period Growth, YoY Growth, and Variance Contribution by Category), as documented in `Financial_Calculation_Formulas.md` — this is the definitive list of in-scope use cases.
- **AC3:** When a question falls outside these six defined use cases, the assistant identifies this and returns a clear response explaining the use cases it does support, instead of attempting to answer or guessing.
- **AC4:** The list of supported use cases the assistant refers to when explaining its limits (AC3) always matches the six calculations defined in AC2 — the two must never fall out of sync.

> *Note: Sprint-level delivery targets belong in the release plan / Definition of Done, not in Acceptance Criteria, since ACs describe system behavior, not delivery timing.*

### US-4.2 — Downloadable Artifacts
As a financial analyst, I want to download an analysis artifact from the web interface, so that I can share results outside the tool.

- **AC1:** The web interface provides a PDF download option for every completed analysis.
- **AC2:** The downloaded artifact contains the relevant analysis results and preserves the source citations and traceability information provided in the assistant's response (per US-1.2, US-2.1).
- **AC3:** The downloaded artifact opens correctly outside the web application, in the tools relevant users would normally use to open it.

---

## Epic 5: Data Privacy & Synthetic Data

### US-5.1 — Synthetic Data Only
As a project team member, I want the assistant to use only synthetic data, so that no real company or personal data is exposed.

- **AC1:** The system accepts and processes only the two approved project datasets (financial data for 2025 and 2026). Any file that is not one of these two approved datasets is rejected before it is used in any calculation or response.
- **AC2:** Synthetic data remains realistic — plausible revenue and expense values, consistent with the project's synthetic data policy — and is never randomly generated in a way that produces implausible results.
- **AC3:** The system checks for indicators of real, personal, or confidential data — including but not limited to real people's names, email addresses, tax/ID numbers, and real company names. If any are detected, the system does **not** use that data in any calculation, response, or output, and tells the user the data was identified as sensitive/real and is prohibited from use under the project's synthetic data policy (`synthetic-data-policy.md`).
- **AC4:** The assistant does not expose non-synthetic, personal, or confidential data through responses, calculations, reports, or downloadable artifacts, under any circumstance.

---

## Epic 6: Reliability & Evaluation

### US-6.1 — Evaluation Against Defined Criteria
As a project team member, I want the assistant to be evaluated against defined accuracy and reliability criteria, so that its performance and limitations can be assessed before wider use.

- **AC1:** The system produces an evaluation report covering four dimensions, each scored/recorded separately: numerical accuracy, source/citation quality, response usefulness (scored against a defined checklist — e.g. did it answer the question, cite sources, avoid unsupported claims), and identified limitations.
- **AC2:** The evaluation runs against the defined set of 5 test questions (the same set used for the project demo), with a pass/fail result recorded for every question. The assistant is considered ready for wider use only if all 5 questions pass correctly (5/5) — no question is skipped or left unrecorded.
- **AC3:** For each question with a numerical answer, the evaluator independently computes the expected result by applying the formula, decimal precision, and rounding rules defined in `Financial_Calculation_Formulas.md`, and compares it to the assistant's output. The outcome (pass/fail, and the delta if it fails) is recorded for each question.
- **AC4:** For each response, source/citation quality is checked against the traceability rules defined in US-1.2 and US-3.1 — confirming a citation exists, is relevant, and is resolvable to real source data.
- **AC5:** All failed test cases, identified limitations, and unsupported/out-of-scope use cases encountered during evaluation are documented in the report with enough detail to reproduce the failure (question asked, actual vs. expected output).

### US-6.2 — Surfacing Uncertainty
As a financial analyst, I want the assistant to surface missing, ambiguous, or conflicting information rather than guessing, so that I don't act on incorrect data.

- **AC1:** When required data is missing, the assistant explicitly states this rather than returning a fabricated or assumed figure (consistent with US-1.2 AC5 and US-2.1 AC5).
- **AC2:** When a user's question is ambiguous (e.g. could reasonably refer to more than one time period, metric, or entity), the assistant asks a clarifying question rather than guessing which interpretation was intended.
- **AC3:** When source data conflicts (e.g. two sources report different values for the same figure/period), the assistant flags the conflict and displays both values with their respective sources, rather than silently picking one.
- **AC4:** Missing-data, ambiguity, and conflict flags are visually/structurally distinguishable from a normal successful response, consistent with how errors are surfaced elsewhere in the assistant (e.g. US-1.1 AC4).

---

## Epic 7: Performance & Availability (Non-Functional)

### US-7.1 — Responsive and Available Assistant
As a financial analyst, I want the assistant to respond quickly and be available when I need it, so that I can rely on it during my daily work and the project demo.

- **AC1:** The assistant responds to a standard question (a single calculation with source citation) within an agreed maximum response time. *(Target response time: to be confirmed with the technical team.)*
- **AC2:** The assistant is available and functioning during normal usage hours and, critically, during the project demo session. Any planned downtime (e.g. for maintenance or updates) is communicated in advance.
- **AC3:** If the assistant is temporarily unavailable or a request times out, the user sees a clear message explaining this — never a blank response or a silent failure.

> *Open item — pending confirmation: exact target response time (e.g. under 5 seconds, under 10 seconds) and required availability window (e.g. business hours only, or 24/7) need to be set with the technical team.*

---

*End of document.*
