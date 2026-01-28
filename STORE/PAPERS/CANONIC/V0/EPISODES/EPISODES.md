# EPISODES

## 1. Purpose

Define EPISODES as the execution-time recording unit of the WRITING scope.

EPISODES capture bounded human–AI interaction sessions and their evidence for later reconstruction, without defining governance, enforcement, or interpretation.

---

## 2. Scope

- Applies to `/canonic/machine/os/writing/episodes/`.
- Inherits from `/canonic/machine/os/writing/`.
- Records execution-time interaction and outcomes as evidence.

---

## 3. Normative language

The key words **MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT**, and **MAY** are to be interpreted as described in RFC 2119.

Statements using these key words are normative. Narrative guidance and examples are non-normative unless explicitly stated otherwise.

---

## 4. Principles

### 4.1 Execution-time evidence

EPISODES exist to record what occurred during execution under CANONIC governance.

EPISODES do not interpret, judge, or canonify outcomes.

---

### 4.2 Immutability

Once recorded, an episode is immutable.

Corrections and changes occur only through the creation of new episodes.

---

### 4.3 Traceability

Each episode is traceable to authoritative LEDGER history.

Evidence without ledger traceability has no standing.

---

## 5. Constraints

- EPISODES **MUST** be recorded as discrete, bounded sessions.
- Each episode **MUST** disclose participating humans and model identities.
- Each episode **MUST** reference relevant LEDGER entries.
- EPISODES **MUST NOT** define governance, enforcement, or interpretation.
- EPISODES **MUST NOT** contain finalized paper prose.

---

## 6. Structure (recommended)

### 6.1 Required metadata

Each episode **MUST** include, at minimum:

- Date or timestamp
- Episode identifier
- Participants
- Model identity
- Status (single-line outcome)

---

### 6.2 Recommended sections

Episodes typically include:

- Session summary
- Actions taken
- Evidence references (LEDGER)
- Violations encountered (if any)
- Corrections applied (if any)

This structure is recommended but not authoritative.

---

## 7. Templates

Canonical episode templates define suggested structure only and live in `episodes/templates/`.

Templates:
- apply to new episodes only,
- do not alter existing episodes, and
- have no authoritative or executable effect.

---

## 8. Validation

An EPISODES scope is valid if and only if:

- the triad (`CANON.md`, `VOCAB.md`, `README.md`) is present,
- episodes are immutable once recorded,
- episodes reference authoritative LEDGER history, and
- no governance or interpretation is introduced.

---

## 9. Consumption notes

- PAPER reconstructs claims by referencing episode identifiers and ledger evidence.
- Episodes serve as primary execution evidence.
- Canonification of insights requires explicit human action in an upstream CANON.

---

**This SPEC is descriptive and non-authoritative.**  
**Governance is defined exclusively by CANON.**

---