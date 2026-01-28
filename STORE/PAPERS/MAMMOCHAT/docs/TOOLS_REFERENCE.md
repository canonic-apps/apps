# White Paper Tools Reference

Complete reference for all CLI tools and core modules in the `src/`
directory.

## Core Modules (`src/core/`)

Reusable libraries for bibliography and citation management.

### `metadata_fetcher.py`
**Purpose:** Unified metadata fetching from PubMed, CrossRef, and Semantic Scholar with file-based caching.

**Features:**
- API caching in `.metadata_cache/` directory (MD5 keys)
- Fetches: DOI, PMID, PMC, URLs, abstracts, authors, publication info
- Supports PubMed, CrossRef, Semantic Scholar APIs
- Rate limiting and error handling

**Usage:**
```python
from src.core.metadata_fetcher import MetadataFetcher

fetcher = MetadataFetcher(email="your@email.com")
metadata = fetcher.fetch_metadata(pmid="12345678")
# Returns: {doi, pmid, pmc, url, abstract, title, authors, journal, ...}
```

### `bibtex_processor.py`
**Purpose:** Process and manage BibTeX bibliography files.

**Features:**
- Parse and validate BibTeX syntax
- Add/update metadata fields
- Remove unused entries
- Fix formatting issues
- Validate cross-references

**Usage:**
```python
from src.core.bibtex_processor import BibTeXProcessor

processor = BibTeXProcessor('refs.bib')
processor.load()
# Access entries: processor.database.entries
processor.save(backup=True)
```

### `inline_citation_applier.py`
**Purpose:** Intelligent citation placement using TF-IDF sentence similarity.

**Features:**
- Convert trailing "References:" lines to inline citations
- **Refine existing inline citations** for more precise placement
- TF-IDF similarity matching between abstracts and sentences
- Citation consolidation (merge adjacent citations)
- Configurable similarity threshold (default: 0.12)

**Usage:**
```python
from src.core.inline_citation_applier import InlineCitationApplier

applier = InlineCitationApplier(bib_path='refs.bib', similarity_threshold=0.12)

# Apply to new reference lines
results = applier.apply_all(['01_intro.tex', '02_methods.tex'])

# Refine existing inline citations
results = applier.refine_all(['01_intro.tex', '02_methods.tex'])
```

### `citation_manager.py`
**Purpose:** Consolidate and merge adjacent/duplicate citations.

**Features:**
- Merge `\autocite{a}\autocite{b}` → `\autocite{a,b}`
- Remove duplicate keys within citations
- Preserve citation order

**Usage:**
```python
from src.core.citation_manager import CitationConsolidator

consolidator = CitationConsolidator()
clean_text, count = consolidator.consolidate_citations(text)
```

### Other Core Modules
- `bibtex_fixer.py` - BibTeX syntax repair utilities
- `unicode_cleaner.py` - Unicode normalization and LaTeX escaping
- `counter.py` - Enhanced LaTeX document statistics and counting

### `counter.py` ⭐
**Purpose:** Comprehensive LaTeX document analysis and statistics.

**Features:**
- Count structural elements (sections, figures, tables, equations)
- Analyze citations (commands by type, unique keys, bibliography stats)
- Bibliography analysis (entries, abstracts, authors, publication years)
- Style metrics (colors, formatting, headers/footers)
- JSON report generation

**Usage:**
```python
from src.tex.counter import LatexCounter

counter = LatexCounter()
stats = counter.count_latex_elements('tex/')

# Access comprehensive statistics
print(f"Citations: {stats.citation_counts['total_commands']}")
print(f"Unique keys: {stats.citation_counts['unique_keys']}")
print(f"Bibliography entries: {stats.bibliography_stats['entries']}")
print(f"Abstracts: {stats.bibliography_stats['with_abstracts']}")
```

**CLI Usage:**
```bash
# Summary statistics
python3 main.py tex stats tex

# Detailed statistics
python3 main.py tex stats tex --detailed

# Save JSON report
python3 main.py tex stats tex --output stats.json
```

---

## CLI Tools (`src/tools/`)

### Pipelines (`src/tools/pipelines/`)

#### `comprehensive_pipeline.py` ⭐
**Purpose:** Complete bibliography enhancement pipeline.

**Usage:**
```bash
python3 src/tools/pipelines/comprehensive_pipeline.py [OPTIONS]

Options:
  --bib BIB             Bibliography file (default: refs.bib)
  --dry-run             Preview only
  --email EMAIL         Email for APIs
  --skip-citations      Skip citation cleanup step
```

**Pipeline Steps:**
1. Clean duplicate citations in .tex files
2. Enhance metadata from PubMed/CrossRef (with caching)
3. Fix BibTeX syntax issues

---

### Bibliography Tools (`src/tools/bibliography/`)

#### `verify_identifiers.py`
**Purpose:** Comprehensive identifier verification and correction.

**Usage:**
```bash
python3 src/tools/bibliography/verify_identifiers.py refs.bib [OPTIONS]

Options:
  --fix                 Auto-correct issues
  --report REPORT       Report output file
  --email EMAIL         Email for API requests
  --rate-limit N        Rate limit (default: 3 requests/sec)
```

**Checks:**
- DOI format and validity
- PMID/PMC linkage
- URL accessibility
- Missing identifiers

#### `search_references.py`
**Purpose:** Search for missing references in bibliography.

**Usage:**
```bash
python3 src/tools/bibliography/search_references.py [OPTIONS]

Options:
  --bib BIB             Bibliography file
  --query QUERY         Search query
```

#### `reorder_citations.py`
**Purpose:** Reorder bibliography entries by citation order in document.

**Usage:**
```bash
python3 src/tools/bibliography/reorder_citations.py
```

Scans all .tex files, extracts citation order, and reorders refs.bib accordingly.

#### `redistribute_citations.py`
**Purpose:** Balance citations across chapters.

**Usage:**
```bash
python3 src/tools/bibliography/redistribute_citations.py
```

#### `standardize_pmc.py`
**Purpose:** Migrate PMC IDs to usera field format.

**Usage:**
```bash
python3 src/tools/bibliography/standardize_pmc.py [refs.bib]
```

**Changes:** `pmc = {PMC12345}` → `usera = {PMC12345}`

#### `fix_org_authors.py`
**Purpose:** Fix organizational author formatting.

**Usage:**
```bash
python3 src/tools/bibliography/fix_org_authors.py refs.bib
```

Wraps organizational authors in double braces: `{{Organization Name}}`

#### `bibliography_standardizer.py`
**Purpose:** Standardize entry types and metadata.

**Usage:**
```bash
python3 src/tools/bibliography/bibliography_standardizer.py [refs.bib]
```

**Features:**
- Standardize entry types (@article, @online, @misc, etc.)
- Fetch missing metadata from PubMed
- Clean formatting

---

### BibTeX Tools (`src/tools/bibtex/`)

#### `fix_missing_commas.py`
**Purpose:** Add missing commas after BibTeX fields.

**Usage:**
```bash
python3 src/tools/bibtex/fix_missing_commas.py
```

Adds commas where fields are missing them (common BibTeX syntax error).

#### `fix_standards.py`
**Purpose:** Fix standard/database entries with proper names.

**Usage:**
```bash
python3 src/tools/bibtex/fix_standards.py [refs.bib]
```

Updates standard entries (LOINC, RxNorm, UMLS, SNOMED CT, W3C specs, etc.) with correct author and title fields.

---

### Citation Tools (`src/tools/citations/`)

#### `apply_inline_citations.py` ⭐
**Purpose:** Apply or refine inline citations using abstract similarity.

**Usage:**
```bash
python3 src/tools/citations/apply_inline_citations.py [FILES] [OPTIONS]

Options:
  --bib BIB             Bibliography file (default: refs.bib)
  --threshold FLOAT     Similarity threshold 0.08-0.20 (default: 0.12)
  --refine              Refine existing inline citations
  --dry-run             Preview only (not yet implemented)

Examples:
  # Refine all citations in all .tex files
  python3 src/tools/citations/apply_inline_citations.py --refine

  # Refine specific files
  python3 src/tools/citations/apply_inline_citations.py --refine 01_intro.tex

  # Use higher threshold for stricter matching
  python3 src/tools/citations/apply_inline_citations.py --refine --threshold 0.15
```

**How it works:**
- Extracts citations from paragraphs
- Fetches abstracts from refs.bib
- Computes TF-IDF similarity between abstract and each sentence
- Repositions citation at most semantically similar sentence
- Consolidates adjacent citations

#### `fix_duplicate_citations.py`
**Purpose:** Fix duplicate and adjacent citations.

**Usage:**
```bash
python3 src/tools/citations/fix_duplicate_citations.py
```

**Fixes:**
- `\autocite{a}\autocite{b}` → `\autocite{a,b}`
- `\autocite{a,a,b}` → `\autocite{a,b}`
- Creates .bak_citations backups

---

## Directory Structure

```
src/
├── core/                          # Reusable libraries
│   ├── metadata_fetcher.py        # API fetching with caching
│   ├── bibtex_processor.py        # BibTeX management
│   ├── inline_citation_applier.py # Smart citation placement
│   ├── citation_manager.py        # Citation consolidation
│   ├── bibtex_fixer.py
│   └── unicode_cleaner.py
│
├── tools/                         # CLI executables
│   ├── pipelines/
│   │   └── comprehensive_pipeline.py    ⭐ Main pipeline
│   │
│   ├── bibliography/
│   │   ├── verify_identifiers.py        Check IDs
│   │   ├── search_references.py         Search refs
│   │   ├── reorder_citations.py         Reorder by usage
│   │   ├── redistribute_citations.py    Balance citations
│   │   ├── standardize_pmc.py           PMC → usera
│   │   ├── fix_org_authors.py           Org author format
│   │   └── bibliography_standardizer.py Entry types
│   │
│   ├── bibtex/
│   │   ├── fix_missing_commas.py        Add commas
│   │   └── fix_standards.py             Fix standards
│   │
│   └── citations/
│       ├── apply_inline_citations.py    ⭐ Smart placement
│       └── fix_duplicate_citations.py   Merge duplicates
│
└── utils/                         # DEPRECATED
    └── README_DEPRECATED.md
```

---

## Common Workflows

### 1. Complete Bibliography Enhancement
```bash
# Run full pipeline with metadata fetching and caching
python3 src/tools/pipelines/comprehensive_pipeline.py --email your@email.com

# Result: Enhanced refs.bib with DOIs, PMIDs, abstracts, etc.
```

### 2. Refine Citation Placement
```bash
# After adding abstracts, refine citation positions
python3 src/tools/citations/apply_inline_citations.py --refine

# Result: 798 citations repositioned based on abstract similarity
```

### 3. Verify and Fix Bibliography
```bash
# Check all identifiers
python3 src/tools/bibliography/verify_identifiers.py refs.bib --report report.txt

# Fix issues automatically
python3 src/tools/bibliography/verify_identifiers.py refs.bib --fix

# Fix syntax issues
python3 src/tools/bibtex/fix_missing_commas.py
```

### 4. Clean Up Citations
```bash
# Remove duplicates
python3 src/tools/citations/fix_duplicate_citations.py

# Reorder by document usage
python3 src/tools/bibliography/reorder_citations.py
```

---

## API Caching

The metadata fetcher uses file-based caching in `.metadata_cache/`:
- Cache key: MD5 hash of service + identifier
- Format: JSON files
- Dramatically speeds up repeated runs
- Currently 112 cached responses

To clear cache:
```bash
rm -rf .metadata_cache/
```

---

## Testing Tools

All tools can be tested for basic functionality:

```bash
# Tools with --help
python3 src/tools/pipelines/comprehensive_pipeline.py --help
python3 src/tools/bibliography/verify_identifiers.py --help
python3 src/tools/citations/apply_inline_citations.py --help

# Tools without argparse (run directly)
python3 src/tools/citations/fix_duplicate_citations.py
python3 src/tools/bibtex/fix_missing_commas.py

# Test core imports
python3 -c "from src.core.metadata_fetcher import MetadataFetcher; print('✓')"
python3 -c "from src.core.inline_citation_applier import InlineCitationApplier; print('✓')"
```

---

## Recent Enhancements (Nov 2024)

1. **Refactored structure**: Separated core libraries from CLI tools (eliminated 769 lines of duplicate code)
2. **API caching**: Added file-based caching to metadata_fetcher (112 cache files)
3. **Enhanced 10 entries**: Added abstracts via comprehensive_pipeline
4. **Refined 798 citations**: Used apply_inline_citations.py --refine for precise placement
5. **Smart citation placement**: TF-IDF similarity matching between abstracts and sentences

---

## Notes

- All tools with shebang (`#!/usr/bin/env python3`) can be run directly
- Tools create backups (`.bak`, `.backup_*` extensions) before modifications
- Use `--dry-run` where available to preview changes
- Email parameter needed for PubMed/CrossRef APIs (rate limiting)
- Threshold 0.12 is optimal for citation placement (tested range: 0.08-0.20)
