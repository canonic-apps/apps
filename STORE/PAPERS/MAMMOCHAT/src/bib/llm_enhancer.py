#!/usr/bin/env python3
"""
LLM Abstract-Based Citation Enhancement Tool

This module extends the existing citation applier to:
1. Strip citations of entries with abstracts from LaTeX files
2. Use LLM to enhance abstract-based citation placement
3. Implement configurable author bias for prioritized publications
"""

import re
import json
import time
from typing import Dict, List, Set, Optional, Tuple, Any
from pathlib import Path
from dataclasses import dataclass

# Import the existing citation applier and related modules
import sys
from pathlib import Path

# Add the src directory to Python path for imports
current_dir = Path(__file__).parent.parent
sys.path.insert(0, str(current_dir))

from cite.applier import InlineCitationApplier, InlineResult, is_generic_abstract
from cite.manager import CitationManager
from shared.config import get_config


@dataclass
class AuthorBiasedResult(InlineResult):
    """Extended result with author bias information"""
    priority_keys: List[str]
    featured_authors: List[str]


class LLMAuthorBiasEnhancer(InlineCitationApplier):
    """
    Enhanced citation applier with LLM support and author bias
    Extends the existing InlineCitationApplier to add new features
    """
    
    def __init__(self,
                 bib_path: str = 'refs.bib',
                 similarity_threshold: float = 0.12,
                 openai_api_key: Optional[str] = None,
                 deepseek_api_key: Optional[str] = None,
                 use_llm: bool = False,
                 llm_provider: str = "deepseek"):
        """
        Initialize the LLM Author Bias Enhancer
        
        Args:
            bib_path: Bibliography file path
            similarity_threshold: TF-IDF similarity threshold
            openai_api_key: OpenAI API key for LLM enhancement (legacy)
            deepseek_api_key: DeepSeek API key for LLM enhancement
            use_llm: Whether to use LLM for precision placement
            llm_provider: LLM provider to use ('deepseek' or 'openai')
        """
        # Initialize parent class
        super().__init__(
            bib_path=bib_path,
            similarity_threshold=similarity_threshold
        )
        
        # Load configuration for author bias and LLM settings
        self.config = get_config()
        
        # Get LLM configuration from config, with env var fallback
        config_deepseek_key = self.config.api.deepseek_api_key
        config_openai_key = self.config.api.openai_api_key
        
        # Use provided keys, config keys, or environment variables
        final_deepseek_key = deepseek_api_key or config_deepseek_key
        final_openai_key = openai_api_key or config_openai_key
        
        # Add LLM capability with multi-provider support
        self.citation_manager = CitationManager(
            openai_api_key=final_openai_key,
            deepseek_api_key=final_deepseek_key,
            deepseek_base_url=self.config.api.deepseek_base_url,
            deepseek_model=self.config.api.deepseek_model,
            use_llm=use_llm,
            llm_provider=llm_provider or self.config.api.llm_provider
        )
        
        self.use_llm = use_llm and bool(final_deepseek_key or final_openai_key)
        self.featured_authors = self._get_featured_authors()
        
        # Get featured author keys from bibliography
        self.featured_author_keys = self._get_featured_author_keys()
    
    def _get_featured_authors(self) -> List[str]:
        """
        Get list of featured authors from configuration
        
        Returns:
            List of author names to prioritize
        """
        # Try to get from citation.featured_authors first
        if hasattr(self.config, 'citation') and hasattr(self.config.citation, 'featured_authors'):
            return self.config.citation.featured_authors or []
        
        # Fallback to authors.primary from config.json
        if hasattr(self.config, 'authors') and hasattr(self.config.authors, 'primary'):
            primary_authors = []
            for author in self.config.authors.primary:
                if isinstance(author, dict):
                    primary_authors.append(author.get('name', ''))
                else:
                    primary_authors.append(str(author))
            return primary_authors
        
        return []
    
    def _get_featured_author_keys(self) -> Set[str]:
        """
        Get bibliography keys for featured authors
        
        Returns:
            Set of bibliography entry keys authored by featured authors
        """
        if not self.featured_authors:
            return set()
        
        featured_keys = set()
        
        for entry in self.processor.database.entries:
            authors = entry.get('author', '').lower()
            if any(author.lower() in authors for author in self.featured_authors):
                featured_keys.add(entry['ID'])
        
        return featured_keys
    
    def _is_featured_author_entry(self, key: str) -> bool:
        """Check if a bibliography key belongs to a featured author"""
        return key in self.featured_author_keys
    
    def strip_abstract_citations(self, tex_files: List[str]) -> Dict[str, str]:
        """
        Strip citations of entries with abstracts from LaTeX files
        
        Args:
            tex_files: List of LaTeX file paths
            
        Returns:
            Dictionary mapping file paths to backup content and changes made
        """
        # Get keys of entries that have abstracts
        abstract_keys = set()
        for entry in self.processor.database.entries:
            if entry.get('abstract', '').strip():
                abstract_keys.add(entry['ID'])
        
        results = {}
        
        # Citation patterns to match - simplified to match any citation containing abstract keys
        cite_patterns = [
            r'\\cite\{([^}]+)\}',
            r'\\autocite\{([^}]+)\}',
            r'\\citep?\{([^}]+)\}',
        ]
        
        for tex_file in tex_files:
            if not Path(tex_file).exists():
                continue
                
            with open(tex_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            changes_made = []
            
            # Find and remove citations of abstract entries
            for pattern in cite_patterns:
                matches = list(re.finditer(pattern, content))

                for match in reversed(matches):  # Process in reverse to maintain indices
                    citation_content = match.group(1)

                    # Parse individual keys in the citation
                    keys = [k.strip() for k in citation_content.split(',')]
                    abstract_citation_keys = [k for k in keys if k in abstract_keys]

                    if abstract_citation_keys:
                        # Remove entire citation if it contains ANY abstract keys
                        content = content[:match.start()] + content[match.end():]
                        changes_made.append(f"Removed citation with abstract keys: \\cite{{{citation_content}}}")
            
            # Track results
            if content != original_content:
                # Create backup
                backup_path = f"{tex_file}.backup_abstract_strip_{int(time.time())}"
                with open(backup_path, 'w', encoding='utf-8') as f:
                    f.write(original_content)
                
                # Write modified content
                with open(tex_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                results[tex_file] = {
                    'backup': backup_path,
                    'changes': changes_made,
                    'content': content
                }
            else:
                results[tex_file] = {
                    'backup': None,
                    'changes': [],
                    'content': original_content
                }
        
        return results
    
    def _enhanced_best_sentence_for_key(self, paragraph: str, abstract: str, key: str) -> Optional[int]:
        """
        Enhanced sentence selection with author bias and LLM support
        
        Args:
            paragraph: Paragraph text to search
            abstract: Abstract text for the citation
            key: Bibliography key for the entry
            
        Returns:
            Best sentence index or None
        """
        # First try the standard TF-IDF method
        sentence_idx = self._best_sentence_for_key(paragraph, abstract)
        
        if sentence_idx is None:
            return None
        
        # If using LLM and this is a featured author, enhance the placement
        if self.use_llm and self._is_featured_author_entry(key):
            try:
                # Use LLM to find a better sentence for featured authors
                enhanced_idx = self._llm_enhanced_placement(paragraph, abstract, key)
                if enhanced_idx is not None:
                    return enhanced_idx
            except Exception as e:
                print(f"Warning: LLM enhancement failed for {key}: {e}")
                # Fall back to TF-IDF result
        
        return sentence_idx
    
    def _llm_enhanced_placement(self, paragraph: str, abstract: str, key: str) -> Optional[int]:
        """
        Use LLM to find better sentence placement for abstract citations

        Args:
            paragraph: Paragraph text
            abstract: Abstract text
            key: Bibliography key

        Returns:
            Enhanced sentence index or None
        """
        if not self.use_llm:
            return None

        # Get the entry title for better context
        entry_title = ""
        for entry in self.processor.database.entries:
            if entry['ID'] == key:
                entry_title = entry.get('title', '')
                break

        # Use the citation manager's LLM functionality
        llm_result = self.citation_manager.get_llm_sentence_placement(
            abstract=abstract,
            title=entry_title,
            paragraph=paragraph,
            citation_key=key
        )

        if llm_result and llm_result != "NO_MATCH":
            # Find which sentence in the paragraph matches the LLM result
            from cite.applier import split_sentences
            sentences = split_sentences(paragraph)

            # Look for the sentence that contains the citation
            for i, sentence in enumerate(sentences):
                if f'\\autocite{{{key}}}' in sentence:
                    return i

        return None
    
    def apply_with_author_bias(self, tex_file: str) -> Optional[AuthorBiasedResult]:
        """
        Apply citations with author bias prioritization
        
        Args:
            tex_file: Path to LaTeX file
            
        Returns:
            AuthorBiasedResult with applied citations
        """
        result = self.apply_file(tex_file)
        
        if result is None:
            return None
        
        # Get priority keys (featured authors)
        priority_keys = [key for key in result.keys if self._is_featured_author_entry(key)]
        
        return AuthorBiasedResult(
            file=result.file,
            para_start=result.para_start,
            para_end=result.para_end,
            keys=result.keys,
            applied=result.applied,
            fallback=result.fallback,
            priority_keys=priority_keys,
            featured_authors=self.featured_authors
        )
    
    def apply_all_with_author_bias(self, tex_files: List[str]) -> List[AuthorBiasedResult]:
        """
        Apply citations with author bias to multiple files
        
        Args:
            tex_files: List of LaTeX file paths
            
        Returns:
            List of AuthorBiasedResult objects
        """
        results = []
        for fp in tex_files:
            res = self.apply_with_author_bias(fp)
            if res:
                results.append(res)
        return results


def main():
    """Command line interface for LLM Author Bias Enhancement"""
    import argparse
    
    parser = argparse.ArgumentParser(description='LLM Author-Bias Citation Enhancement')
    parser.add_argument('--bib', default='refs.bib', help='Bibliography file path')
    parser.add_argument('--tex-files', nargs='+', help='LaTeX files to process')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be done')
    parser.add_argument('--openai-key', help='OpenAI API key (legacy)')
    parser.add_argument('--deepseek-key', help='DeepSeek API key')
    parser.add_argument('--llm-provider', choices=['deepseek', 'openai'], default='deepseek',
                       help='LLM provider to use (default: deepseek)')
    parser.add_argument('--use-llm', action='store_true', help='Use LLM for placement')
    parser.add_argument('--author-bias', action='store_true', help='Apply author bias from config')
    parser.add_argument('--threshold', type=float, default=0.12, help='Similarity threshold')
    parser.add_argument('--strip-abstracts', action='store_true', help='Strip citations of abstract entries first')
    
    args = parser.parse_args()
    
    # Initialize enhancer
    enhancer = LLMAuthorBiasEnhancer(
        bib_path=args.bib,
        similarity_threshold=args.threshold,
        openai_api_key=args.openai_key,
        deepseek_api_key=args.deepseek_key,
        use_llm=args.use_llm,
        llm_provider=args.llm_provider
    )
    
    # Get files to process
    if not args.tex_files:
        args.tex_files = list(Path('.').glob('*.tex'))
        args.tex_files = [str(f) for f in args.tex_files if f.name not in ('main.tex', 'preamble.tex')]
    
    print("LLM Author-Bias Citation Enhancement")
    print("=" * 50)
    
    # Show featured authors from config
    if enhancer.featured_authors:
        print("Featured authors from configuration:")
        for author in enhancer.featured_authors:
            print(f"  - {author}")
        print(f"Found {len(enhancer.featured_author_keys)} entries by featured authors")
    
    # Strip abstract citations if requested
    if args.strip_abstracts:
        print("Stripping citations of abstract entries...")
        strip_results = enhancer.strip_abstract_citations(args.tex_files)
        
        total_changes = 0
        for file_path, result in strip_results.items():
            if result['changes']:
                print(f"Modified {file_path}: {len(result['changes'])} changes")
                total_changes += len(result['changes'])
        
        print(f"Total citations stripped: {total_changes}")
    
    # Apply enhanced citations
    if args.author_bias:
        print("Applying author-biased citations...")
        results = enhancer.apply_all_with_author_bias(args.tex_files)
    else:
        print("Applying standard citations...")
        results = enhancer.apply_all(args.tex_files)
    
    # Report results
    total_applied = sum(r.applied for r in results if r)
    total_priority_applied = sum(
        len(r.priority_keys) for r in results if isinstance(r, AuthorBiasedResult)
    )
    
    print(f"Applied {total_applied} citations")
    if args.author_bias and total_priority_applied > 0:
        print(f"Prioritized {total_priority_applied} featured author citations")
    
    print("Enhancement completed")


if __name__ == '__main__':
    main()