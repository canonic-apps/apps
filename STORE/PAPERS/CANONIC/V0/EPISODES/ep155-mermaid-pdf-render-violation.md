# EPISODE - ep155

Mermaid PDF render violation

---

## Metadata

- Date: 2026-01-14
- Episode ID: ep155
- Type: Violation
- Participants: Dexter Hadley, Codex (GPT-5)
- Agent: Codex
- Model identity: gpt-5 (Codex CLI)
- Channel: IDE
- Source: ~/.codex/sessions/
- Status: Resolved

---

## Context

The PDF build failed to render Mermaid diagrams, causing figures to appear as
code blocks in the manuscript output.

---

## Session narrative

We added Mermaid support to the PDF build by installing a Mermaid filter and
CLI, routing the build through a quiet wrapper, and updating Mermaid labels to
avoid parser errors. The build now renders diagrams in the PDF.

---

## Violations encountered

- Mermaid diagrams did not render in the PDF output.

---

## Corrections applied

- Added Mermaid filter support to the PDF build script.
- Installed Mermaid CLI and filter.
- Replaced Mermaid line breaks with `<br/>` in Figure 5.
- Adjusted build output to keep Mermaid artifacts in `paper/output/`.

---

## Evidence references (LEDGER)

- paper: working tree (manuscript and build script updates)
- writing: working tree (episode creation)

---

## Notes

This keeps PDF output consistent with manuscript figures and supporting
materials.

---

**This file is a non-authoritative template.**  
**It defines structure only and confers no governance, enforcement, or interpretive meaning.**
