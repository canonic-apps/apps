"""
LaTeX Document Counter and Statistics

This module provides comprehensive counting and statistical analysis of LaTeX documents,
including structural elements, citations, bibliography entries, and style metrics.
"""

import re
import os
import sys
from pathlib import Path
from typing import Dict, List, Set, Any, Optional
from dataclasses import dataclass


@dataclass
class LatexStatistics:
    """Comprehensive LaTeX document statistics"""
    directory: str
    structural_counts: Dict[str, int]
    citation_counts: Dict[str, Any]
    bibliography_stats: Dict[str, Any]
    style_metrics: Dict[str, Any]
    total_elements: int


class LatexCounter:
    """
    Advanced LaTeX document counter with citation and bibliography analysis
    """

    def __init__(self):
        # Structural element patterns
        self.structural_patterns = {
            'chapter': re.compile(r'\\chapter\{'),
            'section': re.compile(r'\\section\{'),
            'subsection': re.compile(r'\\subsection\{'),
            'subsubsection': re.compile(r'\\subsubsection\{'),
            'part': re.compile(r'\\part\{'),
            'paragraph': re.compile(r'\\paragraph\{'),
            'figure': re.compile(r'\\begin\{figure\}'),
            'table': re.compile(r'\\begin\{table\}|\\begin\{table\*\}'),
            'equation': re.compile(r'\\begin\{equation\}|\\begin\{align\}|\\begin\{gather\}'),
            'tcolorbox': re.compile(r'\\begin\{tcolorbox\}'),
        }

        # Citation patterns
        self.citation_patterns = {
            'autocite': re.compile(r'\\autocite\{([^}]+)\}'),
            'cite': re.compile(r'\\cite\{([^}]+)\}'),
            'citep': re.compile(r'\\citep\{([^}]+)\}'),
            'citet': re.compile(r'\\citet\{([^}]+)\}'),
        }

        # Bibliography patterns
        self.bib_patterns = {
            'entry': re.compile(r'@\w+\{([^,]+),', re.MULTILINE),
            'abstract': re.compile(r'abstract\s*=\s*\{([^}]*)\}', re.IGNORECASE | re.DOTALL),
            'author': re.compile(r'author\s*=\s*\{([^}]*)\}', re.IGNORECASE),
            'title': re.compile(r'title\s*=\s*\{([^}]*)\}', re.IGNORECASE),
            'year': re.compile(r'year\s*=\s*\{([^}]*)\}', re.IGNORECASE),
        }

        # Style patterns
        self.style_patterns = {
            'textcolor': re.compile(r'\\textcolor\{[^}]+\}\{[^}]+\}'),
            'titleformat': re.compile(r'\\titleformat'),
            'pagestyle': re.compile(r'\\pagestyle'),
            'tcbset': re.compile(r'\\tcbset'),
            'definecolor': re.compile(r'\\definecolor'),
        }

    def count_latex_elements(self, dir_path: str) -> LatexStatistics:
        """
        Count all LaTeX elements in a directory

        Args:
            dir_path: Directory path to analyze

        Returns:
            Comprehensive LatexStatistics object
        """
        dir_path_obj = Path(dir_path)

        # Count structural elements
        structural_counts = self._count_structural_elements(dir_path_obj)

        # Count citations
        citation_counts = self._count_citations(dir_path_obj)

        # Analyze bibliography
        bib_stats = self._analyze_bibliography(dir_path_obj)

        # Count style elements
        style_metrics = self._count_style_elements(dir_path_obj)

        # Calculate totals
        total_elements = sum(structural_counts.values()) + citation_counts['total_commands']

        return LatexStatistics(
            directory=str(dir_path),
            structural_counts=structural_counts,
            citation_counts=citation_counts,
            bibliography_stats=bib_stats,
            style_metrics=style_metrics,
            total_elements=total_elements
        )

    def _count_structural_elements(self, dir_path: Path) -> Dict[str, int]:
        """Count structural LaTeX elements"""
        counts = {key: 0 for key in self.structural_patterns}

        for tex_file in dir_path.rglob('*.tex'):
            if tex_file.name == 'main.tex':
                continue  # Skip main.tex as it just includes other files

            try:
                content = tex_file.read_text(encoding='utf-8')
                for key, pattern in self.structural_patterns.items():
                    counts[key] += len(pattern.findall(content))
            except (IOError, OSError) as e:
                print(f"Warning: Could not read file {tex_file}: {e}", file=sys.stderr)

        return counts

    def _count_citations(self, dir_path: Path) -> Dict[str, Any]:
        """Count citations and extract unique keys"""
        citation_commands = {key: 0 for key in self.citation_patterns}
        all_keys = set()
        citation_commands_total = 0

        for tex_file in dir_path.rglob('*.tex'):
            if tex_file.name == 'main.tex':
                continue

            try:
                content = tex_file.read_text(encoding='utf-8')
                for cite_type, pattern in self.citation_patterns.items():
                    matches = pattern.findall(content)
                    citation_commands[cite_type] += len(matches)

                    # Extract individual keys from citations
                    for match in matches:
                        keys = [k.strip() for k in match.split(',')]
                        all_keys.update(keys)

                citation_commands_total += sum(len(pattern.findall(content))
                                              for pattern in self.citation_patterns.values())

            except (IOError, OSError) as e:
                print(f"Warning: Could not read file {tex_file}: {e}", file=sys.stderr)

        return {
            'commands_by_type': citation_commands,
            'total_commands': citation_commands_total,
            'unique_keys': len(all_keys),
            'all_keys': sorted(list(all_keys))
        }

    def _analyze_bibliography(self, dir_path: Path) -> Dict[str, Any]:
        """Analyze bibliography files"""
        bib_files = list(dir_path.rglob('*.bib'))
        if not bib_files:
            return {'entries': 0, 'with_abstracts': 0, 'authors': set(), 'years': set()}

        total_entries = 0
        entries_with_abstracts = 0
        all_authors = set()
        all_years = set()

        for bib_file in bib_files:
            try:
                content = bib_file.read_text(encoding='utf-8')

                # Count entries - find all @entrytype{key, patterns
                entries = self.bib_patterns['entry'].findall(content)
                total_entries += len(entries)

                # Count abstracts - more robust pattern
                abstract_pattern = re.compile(r'abstract\s*=\s*\{([^}]*)\}', re.IGNORECASE | re.DOTALL)
                abstracts = abstract_pattern.findall(content)
                entries_with_abstracts += len(abstracts)

                # Extract authors and years - find complete entries
                entry_pattern = re.compile(r'@\w+\{([^,]+),.*?\}(?=\s*@|\s*$)', re.DOTALL)
                for entry_match in entry_pattern.finditer(content):
                    entry_content = entry_match.group(0)

                    author_match = self.bib_patterns['author'].search(entry_content)
                    if author_match:
                        all_authors.add(author_match.group(1).strip())

                    year_match = self.bib_patterns['year'].search(entry_content)
                    if year_match:
                        all_years.add(year_match.group(1).strip())

            except (IOError, OSError) as e:
                print(f"Warning: Could not read bibliography {bib_file}: {e}", file=sys.stderr)

        return {
            'entries': total_entries,
            'with_abstracts': entries_with_abstracts,
            'unique_authors': len(all_authors),
            'year_range': sorted(list(all_years)) if all_years else [],
            'abstract_percentage': round((entries_with_abstracts / total_entries * 100), 1) if total_entries > 0 else 0
        }

    def _count_style_elements(self, dir_path: Path) -> Dict[str, int]:
        """Count style-related elements"""
        style_counts = {key: 0 for key in self.style_patterns}

        for tex_file in dir_path.rglob('*.tex'):
            try:
                content = tex_file.read_text(encoding='utf-8')
                for key, pattern in self.style_patterns.items():
                    style_counts[key] += len(pattern.findall(content))
            except (IOError, OSError) as e:
                print(f"Warning: Could not read file {tex_file}: {e}", file=sys.stderr)

        return style_counts

    def print_statistics(self, stats: LatexStatistics) -> None:
        """Print comprehensive statistics"""
        print("=" * 80)
        print("LaTeX DOCUMENT STATISTICS")
        print("=" * 80)
        print(f"Directory: {stats.directory}")
        print()

        # Document Citations
        cite_stats = stats.citation_counts
        bib_stats = stats.bibliography_stats

        print("CITATIONS IN DOCUMENT:")
        for cite_type, count in cite_stats['commands_by_type'].items():
            if count > 0:
                print("20")
        print(f"Total citation groups: {cite_stats['total_commands']} (each \\autocite{...} call)")
        print(f"Unique citation keys used: {cite_stats['unique_keys']} (distinct bibliography references)")

        # Calculate average keys per citation
        if cite_stats['total_commands'] > 0:
            avg_keys = cite_stats['unique_keys'] / cite_stats['total_commands']
            print(f"Average keys per citation group: {avg_keys:.2f}")
        print()

        # Bibliography Coverage
        print("BIBLIOGRAPHY COVERAGE:")
        print(f"Total bibliography entries available: {bib_stats['entries']}")
        print(f"Entries with abstracts: {bib_stats['with_abstracts']} ({bib_stats['abstract_percentage']:.1f}%)")
        print(f"Unique authors: {bib_stats['unique_authors']}")

        # Calculate coverage
        if bib_stats['entries'] > 0:
            coverage_pct = (cite_stats['unique_keys'] / bib_stats['entries']) * 100
            print(f"Citation coverage: {cite_stats['unique_keys']}/{bib_stats['entries']} entries used ({coverage_pct:.1f}%)")

        # Calculate abstract coverage for citations used in document
        # We need to load the bibliography to check which cited keys have abstracts
        try:
            from bib.processor import BibTeXProcessor
            processor = BibTeXProcessor(f"{stats.directory}/refs.bib")
            processor.load()

            abstract_keys = set()
            for entry in processor.database.entries:
                if entry.get('abstract', '').strip():
                    abstract_keys.add(entry['ID'])

            cited_abstract_keys = set(cite_stats['all_keys']) & abstract_keys
            if cite_stats['unique_keys'] > 0:
                abstract_coverage_pct = (len(cited_abstract_keys) / cite_stats['unique_keys']) * 100
                print(f"Cited keys with abstracts: {len(cited_abstract_keys)}/{cite_stats['unique_keys']} keys ({abstract_coverage_pct:.1f}%)")
        except Exception as e:
            print(f"Could not analyze citation abstracts: {e}")

        if bib_stats['year_range']:
            print(f"Publication years: {bib_stats['year_range'][0]} - {bib_stats['year_range'][-1]}")
        print()

        # Structural elements
        print("DOCUMENT STRUCTURE:")
        for element, count in stats.structural_counts.items():
            if count > 0:
                print(f"  {element}: {count}")
        print(f"Total structural elements: {sum(stats.structural_counts.values())}")
        print()

        # Style metrics
        print("STYLE ELEMENTS:")
        for style_type, count in stats.style_metrics.items():
            if count > 0:
                print(f"  {style_type}: {count}")
        print()

        print(f"GRAND TOTAL ELEMENTS: {stats.total_elements}")


def count_latex_elements(dir_path: str) -> Dict[str, Any]:
    """
    Legacy function for backward compatibility
    """
    counter = LatexCounter()
    stats = counter.count_latex_elements(dir_path)

    return {
        'directory': stats.directory,
        'counts': stats.structural_counts,
        'total': stats.total_elements,
        'citations': stats.citation_counts,
        'bibliography': stats.bibliography_stats,
        'styles': stats.style_metrics
    }


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='LaTeX Document Counter and Statistics')
    parser.add_argument('directory', help='Directory to analyze')
    parser.add_argument('--detailed', action='store_true', help='Show detailed statistics')

    args = parser.parse_args()

    counter = LatexCounter()
    stats = counter.count_latex_elements(args.directory)

    if args.detailed:
        counter.print_statistics(stats)
    else:
        print(f"Directory: {stats.directory}")
        print(f"Total elements: {stats.total_elements}")
        print(f"Citation commands: {stats.citation_counts['total_commands']}")
        print(f"Unique citation keys: {stats.citation_counts['unique_keys']}")
        print(f"Bibliography entries: {stats.bibliography_stats['entries']}")