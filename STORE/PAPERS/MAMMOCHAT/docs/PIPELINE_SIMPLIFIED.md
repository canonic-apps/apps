# LaTeX Publication Pipeline - Simplified

## Overview
The LaTeX Publication Pipeline is a lean, efficient system for processing
academic publications with automated citations, bibliography management,
style validation, and document compilation.

## Core Features
- **BibTeX Processing**: Fix problematic bibliography entries
- **Citation Management**: Consolidate duplicate citations and apply inline citations
- **LLM Enhancement**: Use AI to enhance citations with author bias
- **Style Validation**: Comprehensive style checking and standardization
- **Document Compilation**: Automated LaTeX compilation with error handling
- **Fast Mode**: Quick compilation for development workflows

## Main Pipeline Command

### Comprehensive Pipeline
The single, streamlined pipeline command that orchestrates all processing steps:

```bash
# Basic usage
python -m src.main comprehensive

# Fast mode (latexmk only)
python -m src.main comprehensive --fast

# With LLM enhancement
python -m src.main comprehensive --llm-enhance --author-bias

# With specific configuration
python -m src.main comprehensive --bib custom.bib --email user@domain.com --dry-run

# Skip citation processing
python -m src.main comprehensive --skip-citations
```

**Pipeline Steps (when not in fast mode):**
1. Fix BibTeX entries
2. Clean Unicode characters
3. Strip problematic LaTeX constructs
4. Consolidate duplicate citations (if not skipped)
5. Apply inline citations (if not skipped)
6. Validate document
7. Compile document

**LLM Enhancement (when enabled):**
1. Strip abstract citations
2. Apply citations with or without author bias
3. Use configured LLM provider (DeepSeek or OpenAI)

## Individual Commands

### BibTeX Processing
```bash
# Fix bibliography entries
python -m src.main bib fix --bib refs.bib

# Standardize bibliography
python -m src.main bib standardize --bib refs.bib --output refs_standardized.bib

# Verify bibliography identifiers
python -m src.main bib verify --bib refs.bib --fix

# Search for references
python -m src.main bib search --author "Smith" --limit 20

# LLM enhancement
python -m src.main bib enhance --bib refs.bib --llm-enhance --author-bias
```

### Citation Processing
```bash
# Consolidate citations
python -m src.main cite consolidate

# Apply inline citations
python -m src.main cite apply --threshold 0.15
```

### LaTeX Processing
```bash
# Clean build files
python -m src.main tex clean

# Clean Unicode
python -m src.main tex clean-unicode

# Compile document
python -m src.main tex compile --file main.tex
```

### Style Processing
```bash
# Validate style
python -m src.main style validate

# Standardize style
python -m src.main style standardize --chapters "0*.tex" --all
```

### Configuration Management
```bash
# Create default config
python -m src.main config --create-config config.yaml

# Apply preset
python -m src.main config --preset development
```

## Configuration
The pipeline uses YAML configuration files for settings. Key configuration options:
- API keys for LLM providers
- Similarity thresholds
- Featured authors for author bias
- Processing options

## Architecture
The pipeline follows a domain-driven design with minimal redundancy:
- **bib/**: Bibliography processing
- **cite/**: Citation management  
- **tex/**: LaTeX processing
- **style/**: Style validation and standardization
- **doc/**: Document processing orchestration
- **shared/**: Shared utilities and configuration

## Error Handling
The pipeline follows lean coding standards:
- Fail-fast: Invalid inputs cause immediate failures
- No defensive programming or fallbacks
- Clear error messages for debugging
- Dry-run mode for testing changes
- No try-catch blocks for unrecoverable errors

## Recent Cleanup
- Removed redundant `full_pipeline` and `doc pipeline` commands
- Merged fast-mode functionality into comprehensive command
- Cleaned up unused imports and dependencies
- Removed deprecated backup files and stale scripts
- Simplified to single, efficient pipeline option