# Appendix E - Reproducibility Methods

This appendix summarizes steps to reproduce key checks in the frozen evidence
window. It is descriptive and does not define governance.

---

## E1. Evidence window checkout

1. Clone the repo
2. Checkout the freeze tag
3. Confirm commit IDs

Example:

```
git clone https://github.com/canonic-machine/writing.git
cd writing
git checkout stack-freeze-2026-01-12
```

---

## E2. Triad compliance checks

1. Verify `CANON.md`, `VOCAB.md`, `README.md` exist for each scope
2. Verify `LICENSE` and `NOTICE` at repo roots

---

## E3. Claim traceability

1. Locate claim in manuscript
2. Follow cited episode or ledger reference
3. Confirm evidence exists in frozen ledger

---

## E4. Stream indexing

1. Open `writing/streams/README.md`
2. Navigate to the referenced stream
3. Verify episode membership and metadata

---

## E5. Transcript record validation (optional)

1. Use `validators/transcript/validate_transcript_records.py`
2. Confirm required metadata fields are present

---

## E6. Learned episode checks

1. Confirm transcript record IDs are present
2. Confirm inception mapping cites earliest record and stream reference

---

## E7. PDF render (optional)

1. Run `paper/scripts/build_pdf.sh`
2. Confirm output at `paper/output/manuscript.pdf`

---

## E8. PDF output validation (optional)

1. Run `validators/paper/validate_pdf_output.py`
2. Confirm it reports the output file

---

## E9. Figure rendering (optional)

1. Render Mermaid sources from `paper/figures/*.mmd` to SVG and PDF using `mermaid-cli`.
2. Confirm the corresponding `paper/figures/*.svg` and `paper/figures/*.pdf` assets exist.
