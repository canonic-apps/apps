# SCHEMA — CANON

inherits: /MED/CHAT/, /CANONIC/LANGUAGE/DIMENSIONS/STRUCTURAL/

---

## Axiom

**SCHEMA = S grounded. All data has structural definition.**

---

## Core Structures

### Session

```typescript
interface Session {
  id: string;                    // UUID
  created: string;               // ISO8601
  patient_hash: string;          // Privacy-preserving ID
  context: DomainContext;        // Domain-specific
  messages: Message[];
  opts_tokens: OPTSToken[];
  state: 'ACTIVE' | 'CLOSED';
}
```

### Message

```typescript
interface Message {
  id: string;
  timestamp: string;
  role: 'PATIENT' | 'CHAT' | 'CLINICIAN';
  content: string;
  evidence_chain: EvidenceRef[];
  flags: MessageFlag[];
  opts_token: string;            // Reference to OPTS token
}
```

### OPTSToken

```typescript
interface OPTSToken {
  type: 'OPTS-Data' | 'OPTS-Consent' | 'OPTS-Credential';
  hash: string;                  // Content-addressed hash
  metadata: object;              // Domain-specific (FHIR/mCODE)
  signature: string;             // Patient signature
  timestamp: string;             // ISO8601
}
```

### EvidenceRef

```typescript
interface EvidenceRef {
  source: string;                // Domain-specific source
  citation: string;              // Full citation
  authority: 'GOLD' | 'SILVER' | 'BRONZE';
}
```

### MessageFlag

```typescript
type MessageFlag =
  | 'EMOTIONAL'       // Empathy content, not medical advice
  | 'UNVERIFIED'      // Claim pending validation
  | 'BLOCKED'         // Failed validation
  | 'ESCALATE';       // Needs clinician review
```

---

## Constraints

1. All structures MUST be JSON-serializable.
2. All timestamps MUST be ISO8601 with timezone.
3. Patient identifiers MUST be hashed.
4. Evidence references MUST be resolvable.
5. OPTS tokens MUST be included for audit.

---

*SCHEMA | S dimension | Base structural definitions*
