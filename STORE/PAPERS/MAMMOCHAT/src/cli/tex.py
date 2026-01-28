"""
LaTeX processing commands
"""

import click
import glob
import json
import os
import subprocess
import sys
from pathlib import Path

from src.tex.compiler import compile_latex_document
from src.tex.counter import LatexCounter, count_latex_elements
from src.tex.unicode import UnicodeCleaner


@click.group()
def tex():
    """LaTeX processing commands"""
    pass


@tex.command()
@click.argument('directory', type=click.Path(exists=True, file_okay=False, dir_okay=True), default='tex')
@click.pass_context
def clean(ctx, directory):
    """Clean LaTeX build files from a directory."""
    build_extensions = ['.aux', '.log', '.bbl', '.blg', '.out', '.toc', '.lof', '.lot', '.fls', '.fdb_latexmk', '.synctex.gz']
    
    cleaned_files_count = 0
    for ext in build_extensions:
        for build_file in Path(directory).glob(f'*{ext}'):
            try:
                build_file.unlink()
                if ctx.obj['verbose']:
                    print(f"Removed: {build_file}")
                cleaned_files_count += 1
            except OSError as e:
                print(f"Error removing file {build_file}: {e}", file=sys.stderr)

    if cleaned_files_count > 0:
        print(f"Cleaned {cleaned_files_count} build files from '{directory}'.")
    else:
        print(f"No build files found to clean in '{directory}'.")


@tex.command()
@click.option('--tex-files', help='LaTeX files to process (glob pattern)')
@click.pass_context
def clean_unicode(ctx, tex_files):
    """Clean Unicode characters in LaTeX files"""
    if tex_files:
        files = glob.glob(tex_files)
    else:
        files = [f for f in Path('.').glob('*.tex') if f.name not in ('main.tex', 'preamble.tex')]

    if not files:
        print("No LaTeX files found to process")
        return

    cleaner = UnicodeCleaner()
    for tex_file in files:
        result = cleaner.clean_file(str(tex_file))
        if ctx.obj['verbose']:
            print(f"Cleaned {tex_file}: {result.num_changes} changes")


@tex.command()
@click.option('--file', default='main.tex', help='LaTeX file to compile')
@click.pass_context
def compile(ctx, file):
    """Compile LaTeX document to PDF"""
    try:
        compile_latex_document(file)
        print(f"Successfully compiled {file}")
    except Exception as e:
        print(f"Compilation failed: {e}")
        import sys
        sys.exit(1)


@tex.command()
@click.option('--mode', type=click.Choice(['auto', 'full', 'custom']), default='auto', help='Stripping mode')
@click.option('--no-backup', is_flag=True, help='Do not create backup files')
@click.option('--tex-files', help='Specific LaTeX files to strip (glob pattern)')
@click.option('--verbose', is_flag=True, help='Verbose output')
@click.pass_context
def strip(ctx, mode, no_backup, tex_files, verbose):
    """Strip LaTeX environments and formatting that may cause compilation issues"""
    from tex.stripper import LatexStripper

    if verbose and ctx.obj.get('verbose'):
        print(f"Stripping LaTeX files with mode: {mode}")

    # Determine files to process
    if tex_files:
        files = glob.glob(tex_files)
    else:
        # Get all .tex files except main files
        files = [f for f in Path('.').glob('*.tex') if f.name not in ('main.tex', 'preamble.tex')]
        files = [str(f) for f in files]

    if not files:
        print("No LaTeX files found to process")
        return

    # Create stripper
    stripper = LatexStripper(strip_mode=mode)

    # Strip files
    total_stripped = 0
    files_changed = 0

    for file_path in files:
        try:
            result = stripper.strip_file(file_path, backup=not no_backup)
            if result.total_stripped > 0:
                total_stripped += result.total_stripped
                files_changed += 1
                if verbose or ctx.obj.get('verbose'):
                    print(f"Stripped {result.total_stripped} constructs from {file_path}")
                    for rule_name, count in result.rules_applied.items():
                        print(f"  - {rule_name}: {count} removed")
        except Exception as e:
            print(f"Warning: Could not strip {file_path}: {e}")
            continue

    print(f"Total constructs stripped: {total_stripped}")
    print(f"Files changed: {files_changed}/{len(files)}")


@tex.command()
@click.argument('directories', nargs=-1, required=True)
@click.pass_context
def count_latex(ctx, directories):
    """Count LaTeX elements in one or more directories"""
    results = []
    for dir_path in directories:
        path = Path(dir_path)
        if not path.is_dir():
            print(f"Error: Directory '{dir_path}' does not exist or is not a directory", file=sys.stderr)
            sys.exit(1)
        try:
            result = count_latex_elements(path)
            results.append(result)
        except Exception as e:
            print(f"Error: Failed to count LaTeX elements in '{dir_path}': {e}", file=sys.stderr)
            sys.exit(1)

    print(json.dumps(results, indent=2))


@tex.command()
@click.argument('directory', type=click.Path(exists=True, file_okay=False, dir_okay=True), default='tex')
@click.option('--detailed/--summary', default=False, help='Show detailed statistics vs summary')
@click.option('--output', help='Output file for JSON report')
@click.pass_context
def stats(ctx, directory, detailed, output):
    """Generate comprehensive LaTeX document statistics"""
    counter = LatexCounter()
    stats = counter.count_latex_elements(directory)

    if detailed:
        counter.print_statistics(stats)
    else:
        print(f"LaTeX Document Statistics for: {directory}")
        print(f"Structural elements: {sum(stats.structural_counts.values())}")
        print(f"Citation commands: {stats.citation_counts['total_commands']}")
        print(f"Unique citation keys: {stats.citation_counts['unique_keys']}")
        print(f"Bibliography entries: {stats.bibliography_stats['entries']}")
        print(f"Entries with abstracts: {stats.bibliography_stats['with_abstracts']} ({stats.bibliography_stats['abstract_percentage']:.1f}%)")
        print(f"Style elements: {sum(stats.style_metrics.values())}")
        print(f"Total elements: {stats.total_elements}")

    if output:
        import json
        report = {
            'directory': stats.directory,
            'structural_counts': stats.structural_counts,
            'citation_counts': stats.citation_counts,
            'bibliography_stats': stats.bibliography_stats,
            'style_metrics': stats.style_metrics,
            'total_elements': stats.total_elements
        }
        with open(output, 'w') as f:
            json.dump(report, f, indent=2)
        print(f"\nReport saved to: {output}")