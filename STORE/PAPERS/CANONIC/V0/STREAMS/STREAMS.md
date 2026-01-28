# STREAMS

## 1. Purpose

Define STREAMS as typed indexes over EPISODES for navigation and analysis within WRITING.

STREAMS organize episode references without defining governance, enforcement, or interpretation.

---

## 2. Scope

- Applies to `/canonic/machine/os/writing/streams/`.
- Inherits from `/canonic/machine/os/writing/`.
- Indexes episodes stored in `/writing/episodes/`.

---

## 3. Normative language

The key words **MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT**, and **MAY** are to be interpreted as described in RFC 2119.

Statements using these key words are normative. Examples are non-normative unless explicitly marked otherwise.

---

## 4. Principles

### 4.1 Index-only

STREAMS provide pointers to episodes, not new evidence.

---

### 4.2 Criteria transparency

STREAMS document the criteria used to form each index.

---

### 4.3 Non-authority

STREAMS do not define governance, enforcement, or interpretation.

---

### 4.4 Channel and source

When channel and source are recorded, they should be derived from transcript store evidence or remote transcript identifiers.

---

### 4.5 Coverage for reconstruction

Streams should index episodes that support claims or disclosures so evidence can be reconstructed without publishing transcripts.

---

## 5. Constraints

- The STREAMS scope **MUST** contain the triad:
  - `CANON.md`
  - `VOCAB.md`
  - `README.md`
- Stream indexes **MUST** reference episodes stored in `/writing/episodes/`.
- Stream indexes **MUST NOT** duplicate episode content beyond minimal reference metadata.
- Stream criteria **MUST** be documented in `streams/README.md` and/or the stream `README.md`.
- Channel and source labels **MUST** be based on available transcript store evidence when present.
- STREAMS **MUST NOT** introduce governance, enforcement, or interpretive claims.

---

## 6. Validation

A STREAMS scope is valid if and only if:

- the triad is present,
- every referenced episode exists in `/writing/episodes/`,
- criteria are documented for each stream, and
- entries remain reference-only.

---

## 7. Consumption notes

- STREAMS are derivative navigation aids for EPISODES.
- Reindexing STREAMS does not alter episode evidence.
- PAPER may cite stream membership only as a pointer to episodes, not as evidence.
- Claims and disclosures should cite episodes that are indexed in the relevant streams.

---

**This SPEC is descriptive and non-authoritative.**  
**Governance is defined exclusively by CANON.**

---
