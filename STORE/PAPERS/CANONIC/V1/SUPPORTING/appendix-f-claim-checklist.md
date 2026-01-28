# Appendix F - Claim Admissibility Checklist

Use this checklist to verify that a claim is admissible under PAPER CANON.

---

## Checklist

- Claim has a cited ledger reference (commit or tag).
- Claim is bounded by recorded episodes.
- Claim uses only defined terms (VOCAB closure).
- Claim is stated as an observation, not a new rule.
- Evidence exists within the freeze window when required.
- Transcript references (if any) are hash-only and privacy-preserving.

---

## Claim-to-evidence map - freeze window

\begingroup\small
\noindent\begin{tabularx}{\columnwidth}{>{\raggedright\arraybackslash}p{0.4\columnwidth} >{\raggedright\arraybackslash}p{0.6\columnwidth}}
\hline
\textbf{Claim} & \textbf{Evidence reference} \\
\hline
"129 episode artifacts" & \path{writing/episodes/} file count at tag \path{stack-freeze-2026-01-12} \\
"33 violation-labeled episodes" & \path{writing/episodes/*violation*} file count at tag \path{stack-freeze-2026-01-12} \\
"12 triad scopes across 9 repos" & \path{writing/episodes/ep136-stack-compliance-reports.md} (Report A) \\
"First CANON timestamp" & \path{writing/CANON.md} initial commit \path{writing:bca9ec0} \\
"Freeze timestamp" & tag \path{stack-freeze-2026-01-12} (tag timestamp \path{2026-01-12T18:34:47-05:00}, commit \path{writing:f8acf128}) \\
"OS is minimal substrate (frozen) for downstream work" & \path{writing/episodes/ep100-os-initiation-and-refactor.md}, \path{writing/episodes/ep101-canonic-os-minimality-report.md} \\
"Claude Code co-authored early CANONIC foundation commits" & \path{canonic:49d6b65} \\
"Agent-model correlation and violation ranking" & \path{writing/episodes/ep130-agent-model-correlation.md} \\
"Model identity gap (understanding violation)" & \path{writing/episodes/ep135-model-identity-gap.md} \\
"AI work product without SPEC boundary (post-freeze)" & \path{writing/episodes/ep145-ai-work-product-missing-spec.md} \\
"Cloud discovery to CANON drift hypothesis" & \path{writing/episodes/ep146-cloud-discovery-canon-drift-hypothesis.md} \\
"Positive control discovery lexicon" & \path{writing/episodes/ep147-positive-control-lexicon.md} \\
"LFG signal enforcement gap" & \path{writing/episodes/ep148-lfg-enforcement-gap.md} \\
"LFG timeline annotation gap" & \path{writing/episodes/ep149-lfg-timeline-annotation-gap.md} \\
"Ledger-signal verification via session transcripts" & \path{writing/episodes/ep133-ledger-signal-violation-patterns.md} \\
\hline
\end{tabularx}
\endgroup

---

## Notes

This checklist is descriptive and does not define governance.
