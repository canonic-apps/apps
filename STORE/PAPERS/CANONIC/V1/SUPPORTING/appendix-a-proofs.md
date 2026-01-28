# Appendix A - Mathematical Appendix (Proof Sketches)

These are proof sketches that formalize why AI slop is structurally inadmissible
under CANONIC governance. They are descriptive and bounded to this system.

---

## Notation

Let:

- $\mathcal{C}$ be the set of claims in PAPER.
- $\mathcal{E}$ be the set of episodes.
- $\mathcal{L}$ be the set of ledger evidence (commits and tags).
- $\mathcal{V}$ be the vocabulary (defined terms in VOCAB).
- $\mathrm{Terms}(c)$ be the set of terms used by claim $c$.
- $T(c,\ell)$ be the traceability predicate ("$c$ traces to ledger item $\ell$").
- $B(c,e)$ be the bounding predicate ("$c$ is bounded by episode $e$").
- $V(c)$ be vocabulary closure for $c$.
- $A(c)$ be admissibility of $c$.
- $S(c)$ be AI slop for $c$.
- $U(t)$ be undefinedness of term $t$.
- $\mathrm{Invalid}(\mathrm{scope})$ indicate a scope fails validity constraints.

---

## Definitions

**D1. Vocabulary closure**
$$
V(c) \iff \mathrm{Terms}(c) \subseteq \mathcal{V}
$$

**D2. Admissible claim**
A claim is admissible if and only if it is traceable to ledger evidence, bounded
by episodes, and vocabulary-closed.
$$
A(c) \iff \exists \ell \in \mathcal{L}, \exists e \in \mathcal{E} :
T(c,\ell) \land B(c,e) \land V(c)
$$

**D3. Undefined term**
Let $\mathcal{R}$ be the set of terms appearing in CANON/README.
$$
U(t) \iff t \in \mathcal{R} \land t \notin \mathcal{V}
$$

**D4. AI slop**
AI slop is any claim that fails admissibility or uses undefined terms:
$$
S(c) \iff \neg A(c) \lor \exists t \in \mathrm{Terms}(c) : U(t)
$$

---

## Lemma 1 - Unsupported claims are inadmissible

If a claim lacks ledger evidence, it is not admissible.
$$
\neg \exists \ell \in \mathcal{L} : T(c,\ell) \Rightarrow \neg A(c)
$$

**Sketch.** Direct from D2.

---

## Lemma 2 - Vocabulary violations invalidate admissibility

If a claim uses an undefined term, it is inadmissible.
$$
\exists t \in \mathrm{Terms}(c) : U(t) \Rightarrow \neg A(c)
$$

**Sketch.** By D1 and D2, $V(c)$ is required for $A(c)$. If $U(t)$ appears in
$\mathrm{Terms}(c)$, then $V(c)$ fails and so does $A(c)$.

---

## Proposition 1 - AI slop is structurally rejected

AI slop cannot be admitted as a claim in CANONIC PAPER.
$$
S(c) \Rightarrow \neg A(c)
$$

**Sketch.** D4 implies either $\neg A(c)$ directly or a vocabulary violation,
which by Lemma 2 implies $\neg A(c)$.

---

## Proposition 2 - Undefined governance terms invalidate scope

If a governing term is undefined, the scope is invalid.
$$
U(t) \Rightarrow \mathrm{Invalid}(\mathrm{scope})
$$

**Sketch.** By introspection, every term in CANON/README must be in $\mathcal{V}$.
If not, the scope fails validity and cannot yield admissible claims.

---

## Proposition 3 - Ledger immutability preserves traceability

Let $L_t$ be the ledger state at time $t$. Immutability implies:
$$
L_t \subseteq L_{t+1}
$$

**Sketch.** Corrections add new records instead of overwriting old ones. Thus
evidence chains are monotonic and fully reconstructable.

---

## Corollary - Non-erasure of evidence

For any correction chain $x \to x'$,
$$
x \in L_t \land x' \in L_{t+1}
$$
so both the original and correction remain visible for forensic reconstruction.
