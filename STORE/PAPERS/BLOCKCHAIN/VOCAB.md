# VOCAB (/papers/BLOCKCHAIN/)

inherits: /CANONIC/language/

---

## Security Layers

### Layer 1 (Cryptography)

The foundational layer comprising hash functions (SHA-256, Keccak-256) and digital signature algorithms (ECDSA, EdDSA). No known breaks exist at this layer.

### Layer 2 (Consensus)

The protocol layer where nodes agree on transaction ordering and validity. Includes Proof of Work, Proof of Stake, and BFT variants. Subject to 51% attacks if economic security is insufficient.

### Layer 3 (Bridges)

Cross-chain communication systems and external data oracles. Architectural weak points that have suffered billions in exploits.

### Layer 4 (Smart Contracts)

Programmable business logic deployed on-chain. Subject to bugs including reentrancy, integer overflow, and access control failures.

### Layer 5 (Applications)

User-facing systems including wallets, exchanges, and DApps. Most vulnerable layer due to human factors and centralization.

---

## Cryptographic Terms

### hash function

A one-way function that maps arbitrary input to fixed-size output. Properties: pre-image resistance, second pre-image resistance, collision resistance.

### SHA-256

Secure Hash Algorithm producing 256-bit output. Used by Bitcoin. No known cryptographic breaks.

### ECDSA

Elliptic Curve Digital Signature Algorithm. Used for transaction signing. Quantum-vulnerable but currently secure.

### private key

Secret value that controls blockchain assets. Security is user responsibility—not a blockchain property.

---

## Consensus Terms

### 51% attack

Attack where majority hashrate (PoW) or stake (PoS) enables double-spending, censorship, or chain reorganization.

### finality

The point after which a transaction cannot be reversed. Probabilistic in PoW, economic in PoS, absolute in BFT.

### probabilistic finality

Finality that increases with confirmations but never reaches 100%. Bitcoin model.

### economic finality

Finality guaranteed by economic penalties (slashing) for validators who attempt reversal. Ethereum PoS model.

---

## Attack Terms

### reentrancy

Smart contract vulnerability where external calls allow recursive fund extraction before state updates.

### flash loan attack

Exploit using uncollateralized loans within a single transaction to manipulate prices or governance.

### oracle manipulation

Attack corrupting external data feeds to cause smart contracts to execute on false information.

### bridge exploit

Attack targeting cross-chain systems, often via validator key compromise or verification bugs.

### rug pull

Malicious project exit where developers drain user funds. Not a hack—a fraud.

---

## Security Properties

### tamper-evident

Property that modification is detectable. The hash chain provides tamper-evidence.

### tamper-proof

Property that modification is impossible. Blockchain is NOT tamper-proof (51% attacks exist).

### immutable

Often misused. Blockchain provides economic immutability (expensive to change) not absolute immutability.

### transparency

Property that all transactions are publicly visible. Blockchain provides transparency by design.

### pseudonymity

Property that identities are addresses, not names. NOT anonymity—chain analysis can de-anonymize.

---

## Historical Incidents

### The DAO

June 2016 exploit of Ethereum smart contract. $60M extracted via reentrancy. Led to Ethereum/Ethereum Classic fork.

### Mt. Gox

2014 exchange collapse. 850,000 BTC lost. Centralized custody failure, not blockchain failure.

### Ronin Bridge

March 2022 exploit. $625M stolen via compromised validator keys. Attributed to Lazarus Group.

---

## Inherited Concepts

See parent scopes for: scope, triad, inheritance, introspection, axiom, LEDGER, CANONIC.

---
