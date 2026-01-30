# SCHEMA — CANON

inherits: /CANONIC/LANGUAGE/DIMENSIONS/STRUCTURAL/

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
  context: PatientContext;
  messages: Message[];
  state: 'ACTIVE' | 'CLOSED';
}
```

### PatientContext

```typescript
interface PatientContext {
  diagnosis_type: 'DCIS' | 'INVASIVE' | 'UNKNOWN';
  treatment_phase: 'SCREENING' | 'DIAGNOSIS' | 'TREATMENT' | 'SURVIVORSHIP';
  birads_category?: 0 | 1 | 2 | 3 | 4 | 5 | 6;
  molecular_subtype?: 'ER+' | 'HER2+' | 'TNBC' | 'UNKNOWN';
}
```

### Message

```typescript
interface Message {
  id: string;
  timestamp: string;
  role: 'PATIENT' | 'MAMMOCHAT' | 'CLINICIAN';
  content: string;
  evidence_chain: EvidenceRef[];
  flags: MessageFlag[];
}
```

### EvidenceRef

```typescript
interface EvidenceRef {
  source: 'NCCN' | 'BIRADS' | 'TRIAL';
  citation: string;           // e.g., "NCCN.Breast.2024.3.2"
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

## Validation Structures

### ValidationResult

```typescript
interface ValidationResult {
  claim: string;
  status: 'VALID' | 'BLOCKED' | 'FLAGGED';
  evidence: EvidenceRef[];
  reason?: string;
  timestamp: string;
}
```

---

## Constraints

1. All structures MUST be JSON-serializable.
2. All timestamps MUST be ISO8601 with timezone.
3. Patient identifiers MUST be hashed.
4. Evidence references MUST be resolvable.

---

*SCHEMA | S dimension | Structural definitions*
