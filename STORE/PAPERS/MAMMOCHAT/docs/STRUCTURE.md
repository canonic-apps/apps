# Project Structure Documentation

## Directory Organization

```
white_paper/
├── src/                                    # Source code (all Python modules)
│   ├── __init__.py
│   ├── pipeline.py                         # Main CLI orchestrator
│   │
│   ├── core/                               # Core processing modules
│   │   ├── __init__.py
│   │   ├── bibtex_processor.py            # BibTeX parsing, loading, saving
│   │   ├── citation_manager.py            # Citation placement, TF-IDF matching
│   │   ├── metadata_fetcher.py            # Multi-API metadata fetching
│   │   └── unicode_cleaner.py             # Unicode normalization & escaping
│   │
│   ├── utils/                              # Utility scripts and helpers
│   │   ├── __init__.py
│   │   ├── bibliography_standardizer.py   # Entry format standardization
│   │   ├── enhance_bibliography.py        # Bibliography enhancement utilities
│   │   ├── fix_org_authors.py            # Organization author formatting
│   │   ├── fix_standards.py              # Standards & guidelines formatting
│   │   ├── redistribute_citations.py     # Citation density redistribution
│   │   ├── search_references.py          # Author-based reference search (Semantic Scholar)
│   │   ├── standardize_pmc.py            # PMC ID normalization to usera field
│   │   └── verify_identifiers.py         # DOI/PMID/PMCID verification & cross-check
│   │
│   └── validators/                        # Document validation modules
│       ├── __init__.py
│       └── latex_validator.py            # Moving args, typography, Nature style checks
│
├── outputs/                               # Generated outputs (gitignored)
│   ├── reports/                          # JSON/MD reports
│   │   ├── verification_*.json
│   │   ├── citation_placement_report.json
│   │   └── validation_report.json
│   ├── search_results/                   # Search query results
│   │   └── search_*.json
│   ├── backups/                          # BibTeX backups
│   │   └── refs.bib.backup_*
│   └── pipeline.log                      # Execution log
│
├── archive/                              # Historical scripts (reference only)
│   └── [old standalone scripts]
│
├── *.tex                                 # LaTeX source files
├── refs.bib                              # Main bibliography database
├── main.tex                              # Main LaTeX document
├── preamble.tex                          # LaTeX preamble (Nature style config)
├── pipeline_config.yaml                  # Pipeline configuration
├── requirements.txt                      # Python dependencies
├── run_pipeline.sh                       # Quick run script
├── README.md                             # Main documentation
└── .gitignore                           # Git ignore rules

```

## Module Responsibilities

### Core Modules (`src/core/`)

**bibtex_processor.py**
- Load, parse, and save BibTeX files
- Entry validation and normalization
- Backup creation
- Key extraction and management

**citation_manager.py**
- TF-IDF similarity matching
- Citation placement suggestions
- Context-aware placement (avoids moving arguments)
- Paragraph extraction from LaTeX

**metadata_fetcher.py**
- PubMed API integration
- CrossRef API integration
- Semantic Scholar API integration
- ClinicalTrials.gov API integration
- Open Library API integration
- Quality scoring and source prioritization
- Rate limiting and retry logic

**unicode_cleaner.py**
- Smart Unicode normalization
- Typography preservation (en/em dashes)
- LaTeX character escaping
- BibTeX field sanitization

### Utility Modules (`src/utils/`)

**search_references.py**
- Author-based publication search
- Citation count ranking (Semantic Scholar)
- Coauthor filtering
- Year range filtering
- Minimum citations threshold
- DOI-based deduplication
- Direct insertion into refs.bib
- Hadley-first sorting preference

**verify_identifiers.py**
- DOI format validation
- PMID/PMCID cross-verification
- NCT ID extraction
- Identifier reconciliation
- Title/author similarity checks
- Auto-fix capabilities

**redistribute_citations.py**
- Citation density analysis
- Cluster identification (5+ citations)
- Sparse section detection
- Abstract-based matching
- Hadley-first prioritization
- Move suggestion generation

**standardize_pmc.py**
- PMC ID normalization
- usera field standardization
- Format validation (PMC + digits)

**bibliography_standardizer.py**
- Entry type standardization
- Required field enforcement
- Format normalization

**enhance_bibliography.py**
- Batch metadata enrichment
- Abstract fetching
- Field completion

**fix_org_authors.py**
- Organization author detection
- Proper formatting for institutions

**fix_standards.py**
- Standards document formatting
- Guidelines and specifications

### Validators (`src/validators/`)

**latex_validator.py**
- Moving argument detection
  - Section/subsection titles
  - Captions (figure, table)
  - TikZ commands
  - Abstract environment
- Citation consolidation verification
- Typography checks (ranges, numbers)
- Nature style compliance
- PDF string compatibility

### Main Orchestrator (`src/pipeline.py`)

Central CLI that coordinates all modules:

**Commands:**
- `verify-ids` - Identifier verification
- `search-cite` - Author search & insertion
- `fetch-abstracts` - Abstract fetching
- `place-citations` - Citation placement
- `redistribute-citations` - Citation redistribution
- `clean-unicode` - Unicode cleaning
- `consolidate` - Citation consolidation
- `validate` - Comprehensive validation
- `compile` - LaTeX compilation
- `full-pipeline` - Complete workflow

## Configuration (`pipeline_config.yaml`)

```yaml
# File paths
bib_file: refs.bib
main_tex: main.tex
preamble: preamble.tex

# Metadata fetching
metadata:
  rate_limit: 0.34          # seconds between requests
  fetch_abstracts: true
  quality_threshold: 0.5

# Search settings
search:
  default_limit: 50
  sources:
    - semantic_scholar      # primary (citation counts)
    - crossref             # fallback

# Citation placement
citation:
  similarity_threshold: 0.1
  use_llm: false           # set true for GPT-4 enhancement
  min_paragraph_length: 50

# Redistribution
redistribution:
  cluster_threshold: 5     # 5+ citations = cluster
  sparse_threshold: 1      # 0-1 citations = sparse
  similarity_threshold: 0.4
  hadley_first: true       # prioritize Hadley citations

# Unicode handling
unicode:
  preserve_typography: true
  aggressive: false

# Validation
validation:
  check_moving_args: true
  check_consolidation: true
  check_typography: true
  check_nature_style: true

# Compilation
compilation:
  engine: pdflatex
  bibtex: biber
  passes: 4
```

## Output Files

### Reports (`outputs/reports/`)
- `verification_*.json` - Identifier verification results
- `citation_placement_report.json` - Citation placement suggestions
- `redistribution_report.json` - Citation move suggestions
- `validation_report.json` - Document validation issues

### Search Results (`outputs/search_results/`)
- `search_*.json` - Author search query results
- Includes full metadata for top-cited works

### Backups (`outputs/backups/`)
- `refs.bib.backup_*` - Timestamped BibTeX backups
- Created before any modification
- Format: `refs.bib.backup_YYYYMMDD_HHMMSS`

### Logs (`outputs/`)
- `pipeline.log` - Detailed execution log with timestamps

## Data Flow

```
1. Input: refs.bib + *.tex files
   ↓
2. Verification: verify_identifiers.py
   ↓ (fixes DOI/PMID/PMCID)
   ↓
3. Enhancement: metadata_fetcher.py
   ↓ (adds abstracts)
   ↓
4. Search (optional): search_references.py
   ↓ (finds new citations)
   ↓
5. Placement: citation_manager.py
   ↓ (suggests locations)
   ↓
6. Manual editing: Add citations to .tex
   ↓
7. Redistribution: redistribute_citations.py
   ↓ (rebalance density)
   ↓
8. Cleaning: unicode_cleaner.py
   ↓ (normalize text)
   ↓
9. Consolidation: pipeline.py consolidate
   ↓ (merge sequential citations)
   ↓
10. Validation: latex_validator.py
    ↓ (check for errors)
    ↓
11. Compilation: pdflatex + biber
    ↓
12. Output: main.pdf
```

## Archive Directory

The `archive/` directory contains historical standalone scripts used during development. These are kept for reference but are **not part of the active pipeline**. All functionality has been integrated into the `src/` modules.

## Best Practices

1. **Always run verification first**: `python src/pipeline.py verify-ids`
2. **Fetch abstracts before placement**: Enables TF-IDF matching
3. **Use search-cite for new references**: Ensures proper metadata
4. **Review reports before manual changes**: Check suggestions carefully
5. **Run validation before compile**: Catch errors early
6. **Keep backups**: All operations create timestamped backups

## Migration from Old Scripts

Old standalone scripts in root → New integrated modules:

| Old Script | New Location |
|------------|--------------|
| `verify_identifiers.py` | `src/utils/verify_identifiers.py` |
| `fetch_metadata.py` | `src/core/metadata_fetcher.py` |
| `place_citations.py` | `src/core/citation_manager.py` |
| `clean_unicode.py` | `src/core/unicode_cleaner.py` |
| `validate_*.py` | `src/validators/latex_validator.py` |
| Various fixers | `src/utils/fix_*.py` |

All accessed via: `python src/pipeline.py <command>`

## Environment Setup

```bash
# Create virtual environment
python -m venv bib_env
source bib_env/bin/activate  # On Windows: bib_env\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set API keys (optional)
export OPENAI_API_KEY=sk-...  # For LLM enhancement
export SEMANTIC_SCHOLAR_API_KEY=...  # For higher rate limits

# Verify setup
python src/pipeline.py --help
```

## Quick Reference

```bash
# Full pipeline
python src/pipeline.py full-pipeline

# Individual steps
python src/pipeline.py verify-ids --report outputs/reports/verification.json
python src/pipeline.py search-cite --author "Author Name" --limit 50
python src/pipeline.py fetch-abstracts
python src/pipeline.py place-citations
python src/pipeline.py redistribute-citations
python src/pipeline.py clean-unicode
python src/pipeline.py consolidate
python src/pipeline.py validate
python src/pipeline.py compile
```
