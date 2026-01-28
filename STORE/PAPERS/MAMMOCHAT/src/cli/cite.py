"""
Citation processing commands.

This module provides command-line interface functions for citation management,
including consolidating duplicate citations and applying inline citations using
TF-IDF similarity matching. All commands operate on LaTeX files and integrate
with the publication pipeline.
"""

import click
import glob
from pathlib import Path

from src.cite.consolidator import consolidate_all_tex_files, fix_citations_in_file
from src.cite.applier import InlineCitationApplier


@click.group()
def cite():
    """Citation processing commands.
    
    This command group provides access to citation management operations
    including consolidation of duplicate citations and automated inline
    citation placement using semantic similarity matching.
    """
    pass


@cite.command()
@click.option('--tex-files', help='LaTeX files to process (glob pattern)')
@click.pass_context
def consolidate(ctx, tex_files):
    """Consolidate duplicate citations in LaTeX files.
    
    Scans LaTeX files for duplicate and adjacent citation commands and
    consolidates them into single commands. For example:
    \autocite{key1}\autocite{key2} → \autocite{key1,key2}
    
    Args:
        ctx: Click context object for accessing configuration
        tex_files: Optional glob pattern to specify which files to process.
                   If not provided, processes all .tex files in current directory.
    """
    if tex_files:
        # Process specific files
        results = {
            'files_processed': 0,
            'files_changed': 0,
            'total_merges': 0
        }

        for tex_file in glob.glob(tex_files):
            p = Path(tex_file)
            if p.exists():
                results['files_processed'] += 1
                changed, merge_count, changes = fix_citations_in_file(p)
                if changed:
                    results['files_changed'] += 1
                    results['total_merges'] += merge_count
    else:
        # Process all files
        results = consolidate_all_tex_files()

    print(f"Citation consolidation complete:")
    print(f"  Files processed: {results['files_processed']}")
    print(f"  Files changed: {results['files_changed']}")
    print(f"  Total merges: {results['total_merges']}")


@cite.command()
@click.option('--bib', default='refs.bib', help='Bibliography file path')
@click.option('--tex-files', help='LaTeX files to process (glob pattern)')
@click.option('--threshold', type=float, default=0.12, help='Similarity threshold')
@click.pass_context
def apply(ctx, bib, tex_files, threshold):
    """Apply inline citations using similarity matching.
    
    Uses TF-IDF similarity analysis to automatically place citations
    at semantically relevant locations in the document. Analyzes
    citation abstracts and document sentences to find optimal placement.
    
    Args:
        ctx: Click context object for accessing configuration
        bib: Path to bibliography file containing citation information
        tex_files: Optional glob pattern to specify which files to process
        threshold: Similarity threshold for citation placement (0.0-1.0)
    """
    if tex_files:
        files = glob.glob(tex_files)
    else:
        files = sorted(Path('.').glob('*.tex'))
        files = [str(f) for f in files if f.name not in ('main.tex', 'preamble.tex')]

    if not files:
        print("No LaTeX files found to process")
        return

    applier = InlineCitationApplier(bib_path=bib, similarity_threshold=threshold)
    results = applier.apply_all(files)
    total_applied = sum(r.applied for r in results if r)

    print(f"Inline citations applied: {total_applied} citations in {len([r for r in results if r])} files")