#!/usr/bin/env python3
"""
Citation Manager
================

Intelligent citation placement using:
- TF-IDF similarity matching between abstracts and paragraphs
- Context-aware sentence-level placement
- Moving-argument detection and avoidance
- Citation consolidation (merging sequential citations)
- Optional LLM enhancement for precision placement

Critical Rules (from debugging sessions):
- NEVER place citations in section/subsection titles
- NEVER place citations in figure/table captions
- NEVER place citations in TikZ node/draw commands
- NEVER place citations in abstract environment
- Always consolidate sequential citations: \\autocite{a,b,c} not \\autocite{a}\\autocite{b}
"""

import re
import logging
from typing import Dict, List, Tuple, Optional, Set
from dataclasses import dataclass
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import openai
import os
import requests

logger = logging.getLogger(__name__)


@dataclass
class CitationPlacement:
    """Container for citation placement recommendation"""
    file_path: str
    line_number: int
    paragraph_text: str
    sentence: str
    citation_key: str
    similarity_score: float
    placement_type: str  # 'inline', 'reference_line', 'paragraph_end'
    confidence: float
    warning: Optional[str] = None


class MovingArgumentDetector:
    """
    Detect LaTeX moving arguments where citations should not be placed.
    
    Moving arguments are fragile contexts where macro expansion can fail:
    - Section/subsection/subsubsection titles
    - Figure/table captions
    - TikZ node and draw commands
    - Abstract environment
    - PDF metadata (title, author)
    """
    
    # Patterns for moving arguments
    MOVING_ARG_PATTERNS = [
        # Section titles
        r'\\(section|subsection|subsubsection|paragraph|subparagraph)\*?\{[^}]*$',
        r'\\(chapter|part)\*?\{[^}]*$',
        
        # Captions
        r'\\caption\*?\{[^}]*$',
        r'\\caption\*?\[[^\]]*\]\{[^}]*$',
        
        # TikZ commands
        r'\\(node|draw)\s*\[[^\]]*\]\s*(\([^)]*\))?\s*\{[^}]*$',
        r'\\node\s+\[[^\]]*$',
        r'\\draw\s+\[[^\]]*$',
        
        # Abstract
        r'\\begin\{abstract\}[^\\]*$',
        
        # Title and author
        r'\\title\{[^}]*$',
        r'\\author\{[^}]*$',
        
        # Headings in general
        r'\\[A-Za-z]*heading\*?\{[^}]*$',
    ]
    
    # Environment tracking
    ABSTRACT_ENV = r'\\begin\{abstract\}'
    ABSTRACT_END = r'\\end\{abstract\}'
    
    def __init__(self):
        self.in_abstract = False
    
    def is_moving_argument(self, line: str, context_before: List[str] = None) -> Tuple[bool, Optional[str]]:
        """
        Check if current line is within a moving argument
        
        Args:
            line: Current line of LaTeX code
            context_before: Previous lines for context (to detect environment)
            
        Returns:
            (is_moving, reason) tuple
        """
        # Check for abstract environment
        if context_before:
            full_context = '\n'.join(context_before + [line])
            if re.search(self.ABSTRACT_ENV, full_context) and not re.search(self.ABSTRACT_END, full_context):
                self.in_abstract = True
            elif re.search(self.ABSTRACT_END, line):
                self.in_abstract = False
        
        if self.in_abstract:
            return True, "Inside abstract environment"
        
        # Check for moving argument patterns
        for pattern in self.MOVING_ARG_PATTERNS:
            if re.search(pattern, line, re.IGNORECASE):
                return True, f"Moving argument: {pattern}"
        
        return False, None
    
    def get_safe_placement_location(self, lines: List[str], target_line: int) -> Tuple[int, str]:
        """
        Find safe location near target line for citation placement
        
        If target is in moving argument, suggests alternative location:
        - After the moving argument line (for titles/captions)
        - In a "References:" line adjacent to the moving argument
        
        Args:
            lines: Full LaTeX file content as list of lines
            target_line: Intended citation line (0-indexed)
            
        Returns:
            (safe_line_number, placement_strategy) tuple
        """
        context = lines[max(0, target_line - 5):target_line]
        is_moving, reason = self.is_moving_argument(lines[target_line], context)
        
        if not is_moving:
            return target_line, "direct_inline"
        
        logger.warning(f"Line {target_line} is moving argument: {reason}")
        
        # Strategy: Add a "References:" line after the moving argument
        # Find the next non-moving line
        for offset in range(1, min(10, len(lines) - target_line)):
            next_line = target_line + offset
            is_moving_next, _ = self.is_moving_argument(lines[next_line])
            if not is_moving_next and lines[next_line].strip():
                return next_line, "reference_line_after"
        
        # Fallback: end of paragraph
        return target_line + 1, "reference_line_fallback"


class CitationConsolidator:
    """
    Consolidate sequential citations into grouped format.
    
    Transforms: \\autocite{a}\\autocite{b}\\autocite{c}
    Into: \\autocite{a,b,c}
    
    This is essential for biblatex sortcites to work properly.
    """
    
    @staticmethod
    def remove_duplicate_keys(text: str) -> Tuple[str, int]:
        """
        Remove duplicate citation keys within single \\autocite commands
        
        Args:
            text: LaTeX text content
            
        Returns:
            (deduplicated_text, num_duplicates_removed) tuple
        """
        from collections import OrderedDict
        
        pattern = r'\\autocite\{([^}]+)\}'
        duplicates_removed = 0
        
        def deduplicator(match):
            nonlocal duplicates_removed
            keys_str = match.group(1)
            keys = [k.strip() for k in keys_str.split(',')]
            
            # Remove duplicates while preserving order
            unique_keys = list(OrderedDict.fromkeys(keys))
            
            if len(unique_keys) != len(keys):
                duplicates_removed += len(keys) - len(unique_keys)
                logger.info(f"Removed {len(keys) - len(unique_keys)} duplicate key(s) from citation")
            
            return f"\\autocite{{{','.join(unique_keys)}}}"
        
        result = re.sub(pattern, deduplicator, text)
        return result, duplicates_removed
    
    @staticmethod
    def consolidate_citations(text: str) -> Tuple[str, int]:
        """
        Consolidate sequential \\autocite commands and remove duplicate keys
        
        Args:
            text: LaTeX text content
            
        Returns:
            (consolidated_text, num_consolidations) tuple
        """
        # First remove duplicates within citations
        text, dups_removed = CitationConsolidator.remove_duplicate_keys(text)
        
        # Then consolidate adjacent citations
        pattern = r'\\autocite\{([^}]+)\}(?:\s*\\autocite\{([^}]+)\})+'
        
        consolidations = 0
        
        def replacer(match):
            nonlocal consolidations
            from collections import OrderedDict
            
            # Extract all citation keys from the match
            full_match = match.group(0)
            keys = re.findall(r'\\autocite\{([^}]+)\}', full_match)
            
            if len(keys) > 1:
                consolidations += 1
                # Split all keys, remove duplicates while preserving order
                all_keys = []
                for key_group in keys:
                    all_keys.extend([k.strip() for k in key_group.split(',')])
                
                unique_keys = list(OrderedDict.fromkeys(all_keys))
                combined = ','.join(unique_keys)
                
                return f'\\autocite{{{combined}}}'
            return full_match
        
        result = re.sub(pattern, replacer, text)
        
        total_changes = consolidations + dups_removed
        if total_changes > 0:
            logger.info(f"Consolidated {consolidations} citation groups, removed {dups_removed} duplicates")
        
        return result, total_changes

    @staticmethod
    def standardize_citations(text: str, max_citations_per_line: int = 4) -> Tuple[str, Dict[str, int]]:
        """
        Standardize citation formatting across text:
        - Break down long citations (5-10+ references)
        - Fix citations in moving arguments
        - Apply context-specific formatting
        
        Args:
            text: LaTeX text content
            max_citations_per_line: Maximum citations per line before breaking
            
        Returns:
            (standardized_text, changes_made) tuple
        """
        changes = {'long_citations': 0, 'moving_args': 0, 'context_applied': 0}
        
        # Fix long citations by breaking them into smaller groups
        long_citation_pattern = r'\\autocite\{([^}]+)\}'
        
        def break_long_citations(match):
            keys_str = match.group(1)
            keys = [k.strip() for k in keys_str.split(',')]
            
            if len(keys) > max_citations_per_line:
                changes['long_citations'] += 1
                # Split into multiple citations
                first_group = keys[:max_citations_per_line]
                remaining_keys = keys[max_citations_per_line:]
                
                if remaining_keys:
                    return f'\\autocite{{{",".join(first_group)}}} \\autocite{{{",".join(remaining_keys)}}}'
                else:
                    return match.group(0)
            return match.group(0)
        
        text = re.sub(long_citation_pattern, break_long_citations, text)
        
        # Fix citations in moving arguments (captions, section titles, etc.)
        moving_arg_patterns = [
            (r'\\caption\{([^}]*?)\\autocite\{([^}]+)\}([^}]*?)\}', r'\\caption{\1(\\cite{\2})\3}'),
            (r'\\(section|subsection|subsubsection)\*?\{([^}]*?)\\autocite\{[^}]+\}([^}]*?)\}', r'\\\1*{\2\3}'),
        ]
        
        for pattern, replacement in moving_arg_patterns:
            if re.search(pattern, text):
                changes['moving_args'] += 1
                text = re.sub(pattern, replacement, text)
        
        # Apply context-specific citation formatting
        context_patterns = [
            (r'\(Data source:\s+([^,]+),\s*([^)]+)\)', r'\\datacitation{\1}{\2}'),
            (r'see Figure\s+([^,]+)', r'\\figureref{\1}'),
            (r'see Table\s+([^,]+)', r'\\tableref{\1}'),
        ]
        
        for pattern, replacement in context_patterns:
            if re.search(pattern, text):
                changes['context_applied'] += 1
                text = re.sub(pattern, replacement, text)
        
        return text, changes


class CitationManager:
    """
    Manage citation placement with context-aware intelligence
    """
    
    def __init__(self,
                 openai_api_key: Optional[str] = None,
                 deepseek_api_key: Optional[str] = None,
                 deepseek_base_url: str = "https://api.deepseek.com",
                 deepseek_model: str = "deepseek-chat",
                 use_llm: bool = False,
                 llm_provider: str = "deepseek"):
        """
        Args:
            openai_api_key: OpenAI API key for LLM-enhanced placement (legacy)
            deepseek_api_key: DeepSeek API key for LLM-enhanced placement
            deepseek_base_url: DeepSeek API base URL
            deepseek_model: DeepSeek model to use
            use_llm: Whether to use LLM for precision placement
            llm_provider: LLM provider to use ('deepseek' or 'openai')
        """
        self.llm_provider = llm_provider
        self.use_llm = use_llm
        
        # Check for API keys and determine if LLM can be used
        if self.use_llm:
            if self.llm_provider == "deepseek" and deepseek_api_key:
                self.deepseek_api_key = deepseek_api_key
                self.deepseek_base_url = deepseek_base_url
                self.deepseek_model = deepseek_model
                self.use_llm = True
            elif self.llm_provider == "openai" and openai_api_key:
                openai.api_key = openai_api_key
                self.use_llm = True
            else:
                self.use_llm = False
                if not deepseek_api_key and not openai_api_key:
                    logger.warning(f"No API key provided for LLM provider '{llm_provider}'")
        
        self.detector = MovingArgumentDetector()
        self.consolidator = CitationConsolidator()
        self.vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
    
    def find_placement_by_similarity(
        self,
        abstract: str,
        tex_paragraphs: List[Dict],
        citation_key: str,
        threshold: float = 0.1
    ) -> Optional[CitationPlacement]:
        """
        Find best paragraph for citation using TF-IDF similarity
        
        Args:
            abstract: Reference abstract text
            tex_paragraphs: List of {'content': str, 'file': str, 'start_line': int} dicts
            citation_key: BibTeX key for citation
            threshold: Minimum similarity threshold
            
        Returns:
            CitationPlacement recommendation or None
        """
        if not abstract or not abstract.strip():
            logger.warning(f"Empty abstract for {citation_key}")
            return None
        
        if not tex_paragraphs:
            logger.warning("No paragraphs provided")
            return None
        
        try:
            # Build TF-IDF matrix
            corpus = [p['content'] for p in tex_paragraphs] + [abstract]
            tfidf_matrix = self.vectorizer.fit_transform(corpus)
            
            paragraph_vectors = tfidf_matrix[:-1]
            abstract_vector = tfidf_matrix[-1]
            
            # Calculate similarities
            similarities = cosine_similarity(abstract_vector, paragraph_vectors)[0]
            
            # Find best match above threshold
            best_idx = similarities.argmax()
            best_score = similarities[best_idx]
            
            if best_score < threshold:
                logger.warning(f"Best similarity {best_score:.3f} below threshold {threshold}")
                return None
            
            best_para = tex_paragraphs[best_idx]
            
            # Check for moving arguments
            try:
                with open(best_para['file'], 'r', encoding='utf-8') as f:
                    lines = f.readlines()
            except IOError as e:
                logger.error(f"Could not read file {best_para['file']}: {e}")
                return None
            
            safe_line, strategy = self.detector.get_safe_placement_location(
                lines,
                best_para['start_line']
            )
            
            placement = CitationPlacement(
                file_path=best_para['file'],
                line_number=safe_line,
                paragraph_text=best_para['content'][:300],
                sentence="",  # Will be determined in next step
                citation_key=citation_key,
                similarity_score=best_score,
                placement_type=strategy,
                confidence=best_score
            )
            
            if strategy != "direct_inline":
                placement.warning = f"Moving argument detected, using {strategy} strategy"
            
            logger.info(
                f"Found placement for {citation_key} in {best_para['file']} "
                f"(similarity: {best_score:.3f}, strategy: {strategy})"
            )
            
            return placement
            
        except ValueError as e:
            logger.error(f"TF-IDF error: {e}")
            return None
    
    def _call_deepseek_api(self, messages: List[Dict], max_tokens: int = 200) -> Optional[str]:
        """
        Call DeepSeek API to get LLM response
        
        Args:
            messages: List of message dictionaries for the chat
            max_tokens: Maximum tokens to generate
            
        Returns:
            Response text or None if error
        """
        try:
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.deepseek_api_key}"
            }
            
            data = {
                "model": self.deepseek_model,
                "messages": messages,
                "max_tokens": max_tokens,
                "temperature": 0.0
            }
            
            response = requests.post(
                f"{self.deepseek_base_url}/v1/chat/completions",
                headers=headers,
                json=data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result["choices"][0]["message"]["content"].strip()
            else:
                logger.error(f"DeepSeek API error: {response.status_code} - {response.text}")
                return None
                
        except requests.exceptions.RequestException as e:
            logger.error(f"DeepSeek API request failed: {e}")
            return None
        except Exception as e:
            logger.error(f"An unexpected error occurred during DeepSeek API call: {e}")
            return None
    
    def get_llm_sentence_placement(
        self,
        abstract: str,
        title: str,
        paragraph: str,
        citation_key: str
    ) -> Optional[str]:
        """
        Use LLM to find precise sentence for citation placement
        
        Args:
            abstract: Reference abstract
            title: Reference title
            paragraph: Target paragraph text
            citation_key: Citation key
            
        Returns:
            Suggested sentence with citation inserted, or None
        """
        if not self.use_llm:
            return None
        
        prompt = f"""You are a LaTeX citation expert. Find the best sentence in a paragraph to insert a citation.

**Reference:**
- Key: {citation_key}
- Title: {title}
- Abstract: {abstract}

**Paragraph:**
```latex
{paragraph}
```

**Instructions:**
1. Identify the single best sentence for this citation based on semantic relevance
2. Return ONLY that sentence with `\\autocite{{{citation_key}}}` inserted at the appropriate position
3. If no good match exists, return "NO_MATCH"

**Output format:** Just the sentence with citation, nothing else."""
        
        try:
            if self.llm_provider == "deepseek":
                messages = [
                    {"role": "system", "content": "You are a helpful LaTeX citation assistant."},
                    {"role": "user", "content": prompt}
                ]
                result = self._call_deepseek_api(messages, max_tokens=200)
                
            elif self.llm_provider == "openai":
                messages = [
                    {"role": "system", "content": "You are a helpful LaTeX citation assistant."},
                    {"role": "user", "content": prompt}
                ]
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=messages,
                    max_tokens=200,
                    temperature=0.0
                )
                result = response.choices[0].message.content.strip()
            else:
                logger.error(f"Unsupported LLM provider: {self.llm_provider}")
                return None
            
            if result == "NO_MATCH":
                return None
            
            return result
            
        except openai.error.OpenAIError as e:
            logger.error(f"OpenAI API error: {e}")
            return None
        except Exception as e:
            logger.error(f"An unexpected error occurred during LLM placement: {e}")
            return None
    
    def consolidate_file_citations(self, file_path: str) -> int:
        """
        Consolidate all sequential citations in a LaTeX file
        
        Args:
            file_path: Path to .tex file
            
        Returns:
            Number of consolidations performed
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        consolidated, num_changes = self.consolidator.consolidate_citations(content)
        
        if num_changes > 0:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(consolidated)
            logger.info(f"Consolidated {num_changes} citation groups in {file_path}")
        
        return num_changes
    
    def extract_paragraphs_from_tex(self, file_path: str) -> List[Dict]:
        """
        Extract paragraphs from a LaTeX file with line number tracking
        
        Args:
            file_path: Path to .tex file
            
        Returns:
            List of paragraph dictionaries with content, file, and line info
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        paragraphs = []
        current_para = []
        para_start_line = 0
        
        for i, line in enumerate(lines):
            stripped = line.strip()
            
            # Skip comments and commands
            if stripped.startswith('%') or stripped.startswith('\\begin') or stripped.startswith('\\end'):
                if current_para:
                    paragraphs.append({
                        'content': ' '.join(current_para),
                        'file': file_path,
                        'start_line': para_start_line
                    })
                    current_para = []
                continue
            
            # Empty line = paragraph break
            if not stripped:
                if current_para:
                    paragraphs.append({
                        'content': ' '.join(current_para),
                        'file': file_path,
                        'start_line': para_start_line
                    })
                    current_para = []
            else:
                if not current_para:
                    para_start_line = i
                current_para.append(stripped)
        
        # Add final paragraph
        if current_para:
            paragraphs.append({
                'content': ' '.join(current_para),
                'file': file_path,
                'start_line': para_start_line
            })
        
        return paragraphs
from pathlib import Path