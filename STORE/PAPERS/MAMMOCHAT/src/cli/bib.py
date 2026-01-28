"""
Bibliography processing commands.

This module provides command-line interface functions for bibliography
management, including fixing problematic entries, standardization,
verification, search, and LLM-enhanced citation processing. All commands
operate on BibTeX files and integrate with the LaTeX publication pipeline.
"""

import click
import json

from src.bib.processor import BibTeXFixer
from src.bib.search import ReferenceSearcher
from src.bib.standardizer import BibliographyStandardizer
from src.bib.utils import IdentifierVerifier


@click.group()
def bib():
    """Bibliography processing commands.
    
    This command group provides access to all bibliography-related
    operations including fixing syntax issues, standardization,
    verification of identifiers, searching for references, and
    LLM-enhanced citation processing.
    """
    pass


@bib.command()
@click.option('--bib', default='refs.bib', help='Bibliography file path')
@click.option('--preamble', default='preamble.tex', help='Preamble file path')
@click.pass_context
def fix(ctx, bib, preamble):
    """Fix problematic BibTeX entries.
    
    Scans the bibliography file for common issues including:
    - Missing commas after field values
    - Incorrect entry types
    - Malformed field values
    - Encoding issues
    
    Automatically applies fixes to resolve these issues and reports
    the number of changes made to each category.
    
    Args:
        ctx: Click context object for accessing configuration
        bib: Path to the BibTeX bibliography file
        preamble: Path to the LaTeX preamble file
    """
    fixer = BibTeXFixer(bib, preamble)
    fixes = fixer.fix_all()

    if ctx.obj['verbose']:
        print("Fixes applied:")
        for fix_type, count in fixes.items():
            print(f"  {fix_type}: {count}")

    total = sum(fixes.values())
    if total == 0:
        print("No fixes needed!")
    else:
        print(f"Total fixes: {total}")


@bib.command()
@click.option('--bib', default='refs.bib', help='Bibliography file path')
@click.option('--output', help='Output file path')
@click.pass_context
def standardize(ctx, bib, output):
    """Standardize bibliography entries.
    
    Applies consistent formatting to all bibliography entries including:
    - Standard entry types (@article, @book, etc.)
    - Consistent field ordering
    - Proper capitalization
    - URL and DOI formatting
    
    Args:
        ctx: Click context object for accessing configuration
        bib: Path to the input BibTeX file
        output: Optional path for standardized output file
    """
    standardizer = BibliographyStandardizer()
    standardizer.standardize_bibliography(bib, output)

    print(f"Bibliography standardized: {output or bib}")


@bib.command()
@click.option('--bib', default='refs.bib', help='Bibliography file path')
@click.option('--fix', is_flag=True, help='Apply automatic fixes')
@click.option('--report', default='verification_report.json', help='Report output file')
@click.pass_context
def verify(ctx, bib, fix, report):
    """Verify and fix bibliography identifiers.
    
    Performs comprehensive validation of bibliography entries including:
    - DOI format validation and resolution
    - PMID/PMCID cross-verification
    - URL accessibility checks
    - Missing identifier detection
    
    Args:
        ctx: Click context object for accessing configuration
        bib: Path to the bibliography file
        fix: Apply automatic corrections when possible
        report: Output file for detailed verification report
    """
    verifier = IdentifierVerifier()
    stats = verifier.verify_bibliography(
        bib_file=bib,
        fix=fix,
        report_file=report if ctx.obj['verbose'] else None
    )

    print(f"Verification complete:")
    print(f"  Total entries: {stats['total']}")
    print(f"  OK: {stats['ok']}")
    print(f"  Warnings: {stats['warning']}")
    print(f"  Errors: {stats['error']}")

    if fix:
        print(f"  Fixed: {stats['fixed']}")
        print(f"  Corrections applied: {stats['corrections_applied']}")


@bib.command()
@click.option('--bib', default='refs.bib', help='Bibliography file path')
@click.option('--output', help='Output file path')
@click.option('--limit', type=int, default=20, help='Search limit')
@click.option('--author', help='Author to search for')
@click.option('--insert', is_flag=True, help='Insert results into bibliography')
@click.pass_context
def search(ctx, bib, output, limit, author, insert):
    """Search for references using external APIs.
    
    Searches academic databases (primarily Semantic Scholar with Crossref
    fallback) to find publications by a specific author. Results are ranked
    by citation count and can be filtered and exported.
    
    Args:
        ctx: Click context object for accessing configuration
        bib: Path to the bibliography file for insertion
        output: Optional JSON file to save search results
        limit: Maximum number of results to return
        author: Author name to search for (required)
        insert: Insert top results directly into bibliography
    """
    if not author:
        print("Error: --author is required")
        import sys
        sys.exit(1)

    searcher = ReferenceSearcher()
    results = searcher.search_by_author(author, limit=limit)

    if output:
        with open(output, 'w', encoding='utf-8') as f:
            json.dump([{
                'title': it.title,
                'year': it.year,
                'authors': it.authors,
                'journal': it.journal,
                'doi': it.doi,
                'url': it.url,
                'citation_count': it.citation_count,
                'entry_type': it.entry_type
            } for it in results], f, indent=2)

    if insert:
        searcher.append_to_bib(bib, results, top=5)


@bib.command()
@click.option('--bib', default='refs.bib', help='Bibliography file path')
@click.option('--tex-files', multiple=True, help='LaTeX files to process')
@click.option('--openai-key', help='OpenAI API key (legacy)')
@click.option('--deepseek-key', help='DeepSeek API key')
@click.option('--llm-provider', type=click.Choice(['deepseek', 'openai']),
              help='LLM provider to use (default: deepseek)')
@click.option('--use-llm', is_flag=True, help='Use LLM for placement')
@click.option('--author-bias', is_flag=True, help='Apply author bias from config')
@click.option('--threshold', type=float, default=0.12, help='Similarity threshold')
@click.option('--strip-abstracts', is_flag=True, help='Strip citations of abstract entries first')
@click.option('--dry-run', is_flag=True, help='Show what would be done')
@click.pass_context
def enhance(ctx, bib, tex_files, openai_key, deepseek_key, llm_provider,
            use_llm, author_bias, threshold, strip_abstracts, dry_run):
    """LLM Abstract-Based Citation Enhancement with Author Bias.
    
    Uses LLM models to enhance citation placement based on abstract content
    similarity. Can apply author bias to prioritize citations from featured
    authors defined in the configuration. Supports optional abstract citation
    stripping and LLM-enhanced similarity matching.
    
    Args:
        ctx: Click context object for accessing configuration
        bib: Path to bibliography file
        tex_files: LaTeX files to process (auto-detected if not specified)
        openai_key: Legacy OpenAI API key
        deepseek_key: DeepSeek API key
        llm_provider: LLM provider to use (deepseek or openai)
        use_llm: Enable LLM-enhanced similarity matching
        author_bias: Apply author bias from configuration
        threshold: Similarity threshold for citation matching
        strip_abstracts: Strip abstract-based citations first
        dry_run: Preview changes without applying them
    """
    import glob
    from src.bib.llm_enhancer import LLMAuthorBiasEnhancer

    if not tex_files:
        # Auto-detect .tex files if not specified
        tex_files = glob.glob('*.tex')
        tex_files = [f for f in tex_files if f not in ('main.tex', 'preamble.tex')]

    if not tex_files:
        print("No LaTeX files found to process")
        return

    # Initialize the LLM enhancer
    enhancer = LLMAuthorBiasEnhancer(
        bib_path=bib,
        similarity_threshold=threshold,
        openai_api_key=openai_key,
        deepseek_api_key=deepseek_key,
        use_llm=use_llm,
        llm_provider=llm_provider
    )

    print("LLM Abstract-Based Citation Enhancement")
    print("=" * 50)

    # Show featured authors from config
    if enhancer.featured_authors:
        print("Featured authors from configuration:")
        for author in enhancer.featured_authors:
            print(f"  - {author}")
        print(f"Found {len(enhancer.featured_author_keys)} entries by featured authors")

    # Strip abstract citations if requested
    if strip_abstracts:
        print("Stripping citations of abstract entries...")
        strip_results = enhancer.strip_abstract_citations(tex_files)

        total_changes = 0
        for file_path, result in strip_results.items():
            if result['changes']:
                print(f"Modified {file_path}: {len(result['changes'])} changes")
                total_changes += len(result['changes'])

        print(f"Total citations stripped: {total_changes}")

    # Apply enhanced citations
    if author_bias:
        print("Applying author-biased citations...")
        results = enhancer.apply_all_with_author_bias(tex_files)
    else:
        print("Applying standard citations...")
        results = enhancer.apply_all(tex_files)

    # Report results
    total_applied = sum(r.applied for r in results if r)
    total_priority_applied = sum(
        len(r.priority_keys) for r in results if hasattr(r, 'priority_keys')
    )

    print(f"Applied {total_applied} citations")
    if author_bias and total_priority_applied > 0:
        print(f"Prioritized {total_priority_applied} featured author citations")

    print("Enhancement completed")