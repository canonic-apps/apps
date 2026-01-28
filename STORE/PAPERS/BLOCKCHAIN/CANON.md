# BLOCKCHAIN PAPER (/papers/BLOCKCHAIN/)

inherits: /CANONIC/
series: *.md

---

## Axioms

### 1. Layer Separation

Claims about blockchain security MUST specify the layer:

| Layer | Name | Examples |
|-------|------|----------|
| Layer 1 | CRYPTOGRAPHY | hashes, signatures |
| Layer 2 | CONSENSUS | PoW, PoS, BFT |
| Layer 3 | BRIDGES | cross-chain, oracles |
| Layer 4 | CONTRACTS | smart contract logic |
| Layer 5 | APPLICATIONS | wallets, exchanges, DApps |

Claims about "blockchain" without layer specification are INVALID.

---

### 2. Evidence Requirement

Security claims MUST cite:
- Historical exploits with dates and amounts
- Cryptographic proofs or references
- Attack cost calculations where applicable

Unsupported claims are INVALID.

---

### 3. Precision of Terms

The following terms MUST NOT be used without qualification:

| Term | Requires |
|------|----------|
| "unhackable" | Layer specification |
| "immutable" | Finality type (probabilistic/absolute) |
| "secure" | Attack vector and cost |
| "decentralized" | Node count and distribution |

---

### 4. Attack Documentation

Each documented attack MUST include:
- Date
- Amount lost
- Attack vector
- Layer affected
- Source/reference

---

### 5. Balanced Analysis

Papers MUST acknowledge:
- What blockchain DOES guarantee (with caveats)
- What blockchain does NOT guarantee
- Layer-specific security properties

One-sided claims (pure maximalist or pure skeptic) are INVALID.

---

### 6. Evidence Window

This paper covers documented exploits from 2014-2024.
Claims about events outside this window require separate evidence.

---
