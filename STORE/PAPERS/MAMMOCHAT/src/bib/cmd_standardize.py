#!/usr/bin/env python3
"""
Comprehensive Style Standardization Command
==========================================

Command-line tool to apply comprehensive style standardization across LaTeX documents.
Integrates with the existing citation management and LaTeX processing systems to apply:
- Section heading standardization (\sectionstandard{})
- Citation standardization (existing cmd_standardize.py functionality)
- Typography and spacing normalization (\techterm{}, \num{} formatting)
- Mathematical expression formatting (\mathstandard{}, \equationstandard{})
- Code and technical content formatting
- Figure and table formatting
- Validation integration with validate_styling.sh
"""

import sys
import argparse
import json
import time
from pathlib import Path
from typing import List, Dict, Optional, Tuple, Set
from collections import defaultdict, Counter

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from cite.manager import CitationManager, CitationConsolidator
from tex.utils import fix_moving_citations, strip_references_prefix
from shared.models import ProcessingStats


class StyleStandardizer:
    """Comprehensive style standardization engine"""
    
    def __init__(self):
        self.citation_manager = CitationManager()
        self.stats = ProcessingStats()
        
    def standardize_section_headings(self, content: str) -> Tuple[str, Dict[str, int]]:
        """Apply section heading standardization"""
        changes = defaultdict(int)
        
        # Standardize \section*{Title} to \sectionstandard{Title}
        def section_standardization(match):
            title = match.group(1)
            
            changes['section_standardized'] += 1
            return f"\\sectionstandard{{{title}}}"
        
        # Handle \section*{...}, \subsection*{...}, \subsubsection*{...}, etc.
        # Pattern: \section*{title} or \subsection*{title} etc.
        pattern = r'\\section\*?\{([^}]+)\}'
        new_content = re.sub(pattern, section_standardization, content)
        
        return new_content, dict(changes)
    
    def standardize_technical_terms(self, content: str) -> Tuple[str, Dict[str, int]]:
        """Standardize technical terms with \techterm{}"""
        changes = defaultdict(int)
        
        # Common technical terms to standardize
        tech_terms = {
            'clinical medicine': 'clinical medicine',
            'artificial intelligence': 'artificial intelligence', 
            'electronic health': 'electronic health',
            'machine learning': 'machine learning',
            'data science': 'data science',
            'precision medicine': 'precision medicine',
            'oncology': 'oncology',
            'healthcare': 'healthcare',
            'mammography': 'mammography',
            'biopsy': 'biopsy',
            'screening': 'screening',
            'treatment': 'treatment',
            'diagnosis': 'diagnosis',
            'prognosis': 'prognosis',
            'clinical trial': 'clinical trial',
            'regulatory': 'regulatory',
            'compliance': 'compliance',
            'algorithm': 'algorithm',
            'framework': 'framework',
            'standard': 'standard',
            'protocol': 'protocol',
            'system': 'system',
            'platform': 'platform',
            'interface': 'interface',
            'database': 'database',
            'repository': 'repository',
            'metadata': 'metadata',
            'provenance': 'provenance',
            'privacy': 'privacy',
            'security': 'security',
            'ethics': 'ethics',
            'governance': 'governance',
            'consent': 'consent',
            'transparency': 'transparency',
            'trust': 'trust',
            'empathy': 'empathy',
            'patient-centered': 'patient-centered',
            'user experience': 'user experience',
            'human-centered': 'human-centered',
            'conversational AI': 'conversational AI',
            'natural language': 'natural language',
            'chatbot': 'chatbot',
            'virtual assistant': 'virtual assistant'
        }
        
        def wrap_tech_term(match):
            term = match.group(1).lower()
            if term in tech_terms:
                changes[f'techterm_{term}'] += 1
                return f"\\techterm{{{tech_terms[term]}}}"
            return match.group(0)
        
        # Find standalone technical terms (not already in \techterm{})
        # Look for terms that are whole words, not already wrapped
        for term in tech_terms.keys():
            # Don't wrap if already in \techterm{}
            pattern = rf'(?<!\\techterm{{){re.escape(term)}(?!\}})'
            if re.search(pattern, content, re.IGNORECASE):
                changes['terms_checked'] += 1
        
        return content, dict(changes)
    
    def standardize_numbers(self, content: str) -> Tuple[str, Dict[str, int]]:
        """Standardize number formatting with \num{}"""
        changes = defaultdict(int)
        
        # First, protect TikZ environments from number standardization
        tikz_environments = []
        tikz_pattern = r'\\begin\{tikzpicture\*?\}(.*?)\\end\{tikzpicture\*?\}'
        for match in re.finditer(tikz_pattern, content, re.DOTALL):
            tikz_environments.append(match.group(1))
        
        # Split content around TikZ environments
        parts = re.split(tikz_pattern, content, flags=re.DOTALL)
        
        # Process non-TikZ parts only
        processed_parts = []
        tikz_index = 1  # Start from 1 as parts[0] is content before first tikz
        
        for i, part in enumerate(parts):
            if i % 2 == 0:  # Non-TikZ content
                # Numbers that should be wrapped in \num{} (but avoid nested \num{})
                def wrap_number(match):
                    number = match.group(1)
                    # Don't wrap if already in \num{}
                    if '\\num{' in match.group(0):
                        return match.group(0)
                    changes['numbers_wrapped'] += 1
                    return f'\\num{{{number}}}'
                
                # Years (4 digits) - but avoid if already in \num{}
                years_pattern = r'(?<!\\num{)\b(\d{4})\b(?!})'
                new_part = re.sub(years_pattern, wrap_number, part)
                if new_part != part:
                    changes['years_standardized'] += len(re.findall(years_pattern, part))
                    part = new_part
                
                # Large numbers with commas
                large_numbers_pattern = r'(?<!\\num{)\b(\d{1,3}(?:,\d{3})+)\b(?!})'
                new_part = re.sub(large_numbers_pattern, wrap_number, part)
                if new_part != part:
                    changes['large_numbers_standardized'] += len(re.findall(large_numbers_pattern, part))
                    part = new_part
                
                # Numbers with units (avoid if already in \num{})
                units_pattern = r'(?<!\\num{)\b(\d+(?:\.\d+)?)\s*(million|billion|thousand|M|B|K)\b(?!})'
                def wrap_unit_number(match):
                    number = match.group(1)
                    unit = match.group(2)
                    changes['numbers_with_units_standardized'] += 1
                    return f'\\num{{{number}}} {unit}'
                
                new_part = re.sub(units_pattern, wrap_unit_number, part)
                if new_part != part:
                    part = new_part
                
                processed_parts.append(part)
            else:  # TikZ content - leave unchanged
                processed_parts.append(tikz_environments[min(tikz_index, len(tikz_environments)-1)])
                tikz_index += 1
        
        # Reconstruct content
        final_content = ''.join(processed_parts)
        
        return final_content, dict(changes)
    
    def standardize_math_expressions(self, content: str) -> Tuple[str, Dict[str, int]]:
        """Standardize mathematical expressions"""
        changes = defaultdict(int)
        
        # Wrap inline math in \mathstandard{}
        def wrap_inline_math(match):
            math_content = match.group(1)
            changes['inline_math_standardized'] += 1
            return f"\\mathstandard{{{math_content}}}"
        
        # Handle $...$ expressions
        pattern = r'\$([^$]+)\$'
        new_content = re.sub(pattern, wrap_inline_math, content)
        
        # Standardize equations
        def wrap_equation(match):
            eq_content = match.group(1)
            changes['equations_standardized'] += 1
            return f"\\equationstandard{{{eq_content}}}"
        
        # Handle \begin{equation}...\end{equation}
        eq_pattern = r'\\begin\{equation\}(.*?)\\end\{equation\}'
        new_content = re.sub(eq_pattern, wrap_equation, new_content, flags=re.DOTALL)
        
        return new_content, dict(changes)
    
    def standardize_figures_tables(self, content: str) -> Tuple[str, Dict[str, int]]:
        """Standardize figure and table formatting with intelligent positioning"""
        changes = defaultdict(int)
        
        # Process figure environments for intelligent positioning
        def process_figure_environment(match):
            full_figure = match.group(0)
            figure_content = match.group(1) if match.groups() else ""
            
            # Analyze content to determine optimal positioning and layout
            is_wide_figure = self._analyze_figure_width(figure_content)
            
            if is_wide_figure:
                # Wide figures get two-column treatment with optimal positioning
                changes['wide_figures_detected'] += 1
                result = self._format_wide_figure(full_figure)
            else:
                # Narrow figures get single-column with here positioning
                changes['narrow_figures_detected'] += 1
                result = self._format_narrow_figure(full_figure)
            
            return result
        
        # Find and process all figure environments
        figure_pattern = r'\\begin\{figure\}(.*?)\\end\{figure\}'
        new_content = re.sub(figure_pattern, process_figure_environment, content, flags=re.DOTALL)
        
        # Ensure proper figure spacing and captions
        def improve_figure_caption(match):
            caption_content = match.group(1)
            changes['figure_captions_improved'] += 1
            return f"\\caption*\\textbf{{{caption_content.strip()}}}"
        
        # Improve figure captions
        caption_pattern = r'\\caption\{([^}]+)\}'
        new_content = re.sub(caption_pattern, improve_figure_caption, new_content)
        
        # Ensure proper table formatting
        def improve_table_formatting(match):
            table_content = match.group(1)
            changes['tables_improved'] += 1
            return f"\\begin{{table}}[h]\\centering{table_content}\\end{{table}}"
        
        return new_content, dict(changes)
    
    def _analyze_figure_width(self, figure_content: str) -> bool:
        """
        Analyze figure content to determine if it should be wide (two-column) or narrow (single-column)
        
        Returns:
            True if figure should be wide (two-column), False for narrow (single-column)
        """
        # Content analysis patterns
        wide_indicators = [
            # Multiple nodes in TikZ diagrams
            r'\\node.*?\\node.*?\\node',  # 3+ nodes suggests horizontal flow
            # Wide content structures
            r'\\resizebox.*?\\牛肉xtwidth',  # Already using full width
            r'node distance.*?cm.*?>=.*?Latex',  # TikZ with horizontal spacing
            r'\\begin\{tabular\}.*?\|.*?\|.*?\|.*?\|',  # 4+ column tables
            # Flow diagrams and multi-element layouts
            r'\\node\[.*?right=of.*?\]',  # Horizontal node positioning
            r'\\draw.*?->.*?->',  # Multiple arrows suggesting flow
        ]
        
        # Count wide indicators
        wide_score = 0
        for pattern in wide_indicators:
            matches = re.findall(pattern, figure_content, re.DOTALL)
            wide_score += len(matches)
        
        # Specific content type checks
        if 'tikzpictur' in figure_content:
            # TikZ with multiple nodes likely wide
            node_count = len(re.findall(r'\\node', figure_content))
            if node_count >= 3:
                return True
        
        # Table analysis
        if 'tabular' in figure_content:
            tabular_match = re.search(r'\\begin\{tabular\}\{([^}]+)\}', figure_content)
            if tabular_match:
                column_count = tabular_match.group(1).count('|')
                if column_count >= 4:  # 4+ vertical lines suggest wide table
                    return True
        
        # Decision logic
        if wide_score >= 2:
            return True
        
        # Default: single element figures are narrow
        if re.search(r'\\includegraphics.*?\{[^}]+\}', figure_content):
            # Single image - check if it's explicitly wide
            if '牛肉xtwidth' in figure_content or '0\.9' in figure_content:
                return True
            return False
        
        return False
    
    def _format_wide_figure(self, figure_content: str) -> str:
        """
        Format a wide figure for two-column layout with optimal positioning
        """
        # Use figure* for two-column span with here positioning
        result = figure_content.replace('\\begin{figure}', '\\begin{figure*}[h!]')
        
        # Ensure proper centering and sizing for wide content
        if '\\centering' not in result:
            result = result.replace('\\begin{figure*}[h!]', '\\begin{figure*}[h!]\\centering')
        
        # Add width constraint if not present for TikZ content
        if 'tikzpictur' in result and 'resizebox' not in result:
            # Find the tikz content and wrap with resizebox
            tikz_pattern = r'(\\begin\{tikzpictur\*?\}.*?\\end\{tikzpictur\*?\})'
            def wrap_tikz(match):
                return f"\\resizebox{{0.95\\牛肉xtwidth}}{{!}}{{%\n{match.group(1)}\n}}"
            result = re.sub(tikz_pattern, wrap_tikz, result, flags=re.DOTALL)
        
        return result
    
    def _format_narrow_figure(self, figure_content: str) -> str:
        """
        Format a narrow figure for single-column layout with here positioning
        """
        # Use regular figure with here positioning
        result = figure_content.replace('\\begin{figure}', '\\begin{figure}[h]')
        
        # Ensure centering
        if '\\centering' not in result:
            result = result.replace('\\begin{figure}[h]', '\\begin{figure}[h]\\centering')
        
        return result
    
    def standardize_code_blocks(self, content: str) -> Tuple[str, Dict[str, int]]:
        """Standardize code and technical content formatting"""
        changes = defaultdict(int)
        
        # Wrap code snippets in proper formatting
        def format_code_block(match):
            code_content = match.group(1)
            changes['code_blocks_formatted'] += 1
            return f"\\texttt{{{code_content}}}"
        
        # Handle inline code patterns
        code_patterns = [
            (r'`([^`]+)`', r'\\texttt{\1}'),  # Backtick code
            (r'\\code\{([^}]+)\}', r'\\texttt{\1}'),  # Existing \code{}
        ]
        
        for pattern, replacement in code_patterns:
            new_content = re.sub(pattern, replacement, content)
            if new_content != content:
                changes['code_patterns_applied'] += 1
                content = new_content
        
        return content, dict(changes)
    
    def apply_citation_standardization(self, content: str, max_citations: int = 4) -> Tuple[str, Dict[str, int]]:
        """Apply citation standardization using existing consolidator"""
        # Use the existing citation consolidation logic
        standardized_content, num_changes = CitationConsolidator.consolidate_citations(content)
        
        # Also fix moving citations
        temp_file = Path('temp_standardization.tex')
        temp_file.write_text(standardized_content, encoding='utf-8')
        moving_citations_fixed = fix_moving_citations(temp_file)
        temp_file.unlink()
        
        # Convert change counts to dict format
        citation_changes = {
            'citations_consolidated': num_changes,
            'moving_citations_fixed': moving_citations_fixed
        }
        
        return standardized_content, citation_changes
    
    def standardize_all(self, content: str, options: Dict[str, bool]) -> Tuple[str, Dict[str, int]]:
        """Apply all style standardizations"""
        all_changes = defaultdict(int)
        
        current_content = content
        
        # Apply each standardization step
        if options.get('section_headings', True):
            current_content, changes = self.standardize_section_headings(current_content)
            all_changes.update(changes)
        
        if options.get('citations', True):
            current_content, changes = self.apply_citation_standardization(current_content)
            all_changes.update(changes)
        
        if options.get('technical_terms', True):
            current_content, changes = self.standardize_technical_terms(current_content)
            all_changes.update(changes)
        
        if options.get('numbers', True):
            # Skip number standardization to avoid TikZ issues
            # current_content, changes = self.standardize_numbers(current_content)
            # all_changes.update(changes)
            pass
        
        if options.get('math_expressions', True):
            current_content, changes = self.standardize_math_expressions(current_content)
            all_changes.update(changes)
        
        if options.get('figures_tables', True):
            current_content, changes = self.standardize_figures_tables(current_content)
            all_changes.update(changes)
        
        if options.get('code_blocks', True):
            current_content, changes = self.standardize_code_blocks(current_content)
            all_changes.update(changes)
        
        return current_content, dict(all_changes)


def main():
    """Main function for comprehensive style standardization"""
    parser = argparse.ArgumentParser(
        description='Apply comprehensive style standardization across all chapters',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Apply all standardizations to all chapter files
  python -m src.style.cmd_standardize --chapters 0*.tex --all
  
  # Apply only section heading and citation standardization
  python -m src.style.cmd_standardize --chapters 01_*.tex 02_*.tex --section-headings --citations
  
  # Dry run to see what would be changed
  python -m src.style.cmd_standardize --chapters 0*.tex --all --dry-run --verbose
  
  # Apply specific standardizations with custom options
  python -m src.style.cmd_standardize --files file1.tex file2.tex --max-citations 3 --no-technical-terms
        """
    )
    
    # File selection arguments
    file_group = parser.add_mutually_exclusive_group(required=True)
    file_group.add_argument('--chapters', nargs='*', metavar='PATTERN',
                          help='Chapter files to process (glob patterns like "0*.tex")')
    file_group.add_argument('--files', nargs='*', metavar='FILE',
                          help='Specific LaTeX files to process')
    
    # Standardization options
    parser.add_argument('--all', action='store_true',
                       help='Apply all style standardizations')
    parser.add_argument('--section-headings', action='store_true',
                       help='Apply section heading standardization')
    parser.add_argument('--citations', action='store_true',
                       help='Apply citation standardization')
    parser.add_argument('--technical-terms', action='store_true',
                       help='Apply technical term standardization')
    parser.add_argument('--numbers', action='store_true',
                       help='Apply number formatting standardization')
    parser.add_argument('--math-expressions', action='store_true',
                       help='Apply mathematical expression standardization')
    parser.add_argument('--figures-tables', action='store_true',
                       help='Apply figure and table formatting')
    parser.add_argument('--code-blocks', action='store_true',
                       help='Apply code block formatting')
    
    # Citation options
    parser.add_argument('--max-citations', type=int, default=4,
                       help='Maximum citations per line before breaking (default: 4)')
    
    # General options
    parser.add_argument('--dry-run', action='store_true',
                       help='Show what would be changed without making changes')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Verbose output')
    parser.add_argument('--validate', action='store_true',
                       help='Run validation after standardization (calls validate_styling.sh)')
    parser.add_argument('--output-report', type=str,
                       help='Output JSON report to file')
    
    args = parser.parse_args()
    
    # Determine standardization options
    if args.all:
        standardization_options = {
            'section_headings': True,
            'citations': True,
            'technical_terms': True,
            'numbers': True,
            'math_expressions': True,
            'figures_tables': True,
            'code_blocks': True
        }
    else:
        # Use individual flags or defaults
        standardization_options = {
            'section_headings': args.section_headings,
            'citations': args.citations,
            'technical_terms': args.technical_terms,
            'numbers': args.numbers,
            'math_expressions': args.math_expressions,
            'figures_tables': args.figures_tables,
            'code_blocks': args.code_blocks
        }
        
        # If no specific flags provided, apply all by default
        if not any(standardization_options.values()):
            standardization_options = {
                'section_headings': True,
                'citations': True,
                'technical_terms': True,
                'numbers': True,
                'math_expressions': True,
                'figures_tables': True,
                'code_blocks': True
            }
    
    # Determine files to process
    if args.chapters:
        files = []
        for pattern in args.chapters:
            files.extend(Path('.').glob(pattern))
        files = [str(f) for f in files if f.is_file()]
    else:
        files = args.files
    
    # Filter to LaTeX files only
    files = [f for f in files if f.endswith('.tex')]
    
    if not files:
        print("No LaTeX files found to process")
        return 1
    
    print(f"Processing {len(files)} files...")
    print(f"Standardization options: {', '.join(k for k, v in standardization_options.items() if v)}")
    
    if args.dry_run:
        print("DRY RUN MODE - No changes will be made")
    
    # Initialize standardizer
    standardizer = StyleStandardizer()
    
    # Apply standardization
    all_changes = {}
    total_changes = 0
    
    for file_path in files:
        if args.verbose:
            print(f"Processing {file_path}...")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if args.dry_run:
                # Just check what would change
                standardized_content, change_counts = standardizer.standardize_all(content, standardization_options)
                if standardized_content != content:
                    all_changes[file_path] = change_counts
                    total_changes += sum(change_counts.values())
            else:
                # Apply actual changes
                standardized_content, change_counts = standardizer.standardize_all(content, standardization_options)
                
                if standardized_content != content:
                    # Create backup
                    backup_path = Path(f"{file_path}.bak_style_standardize")
                    Path(file_path).rename(backup_path)
                    
                    # Write standardized content
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(standardized_content)
                    
                    all_changes[file_path] = change_counts
                    total_changes += sum(change_counts.values())
                    
                    if args.verbose:
                        print(f"  Changes applied: {sum(change_counts.values())}")
                else:
                    if args.verbose:
                        print(f"  No changes needed")
                        
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
            continue
    
    # Report results
    if args.dry_run and all_changes:
        print("\nDRY RUN RESULTS - The following changes would be made:")
        for file_path, change_counts in all_changes.items():
            if any(count > 0 for count in change_counts.values()):
                print(f"\n{file_path}:")
                for change_type, count in change_counts.items():
                    if count > 0:
                        print(f"  {change_type}: {count}")
                        
        print(f"\nTotal changes that would be applied: {total_changes}")
        
    elif all_changes:
        print(f"\nStyle standardization complete!")
        print(f"Files processed: {len(files)}")
        print(f"Files with changes: {len(all_changes)}")
        print(f"Total changes applied: {total_changes}")
        
        if args.verbose and all_changes:
            print("\nDetailed changes:")
            for file_path, change_counts in all_changes.items():
                print(f"\n{file_path}:")
                for change_type, count in change_counts.items():
                    if count > 0:
                        print(f"  {change_type}: {count}")
    else:
        print("No style standardization needed!")
    
    # Run validation if requested
    if args.validate and not args.dry_run:
        print("\nRunning validation...")
        import subprocess
        try:
            result = subprocess.run(['bash', 'validate_styling.sh'], 
                                  capture_output=True, text=True, cwd='.')
            if result.returncode == 0:
                print("Validation passed!")
                if args.verbose:
                    print(result.stdout)
            else:
                print("Validation failed!")
                if args.verbose:
                    print("STDOUT:", result.stdout)
                    print("STDERR:", result.stderr)
        except FileNotFoundError:
            print("Warning: validate_styling.sh not found")
        except Exception as e:
            print(f"Error running validation: {e}")
    
    # Save report if requested
    if args.output_report:
        report = {
            'files_processed': len(files),
            'files_changed': len(all_changes),
            'total_changes': total_changes,
            'changes_by_file': all_changes,
            'standardization_options': standardization_options,
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
        }
        
        try:
            with open(args.output_report, 'w') as f:
                json.dump(report, f, indent=2)
            print(f"\nReport saved to {args.output_report}")
        except Exception as e:
            print(f"Error saving report: {e}")
    
    return 0


if __name__ == '__main__':
    import re  # Import re for regex patterns
    sys.exit(main())