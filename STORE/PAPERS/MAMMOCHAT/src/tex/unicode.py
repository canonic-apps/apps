#!/usr/bin/env python3
"""
Unicode Cleaner
===============

Clean Unicode characters that cause LaTeX compilation issues.

Based on lessons learned:
- PRESERVE en dashes (–) for ranges: 2025–2030
- PRESERVE em dashes (—) for punctuation (with \pdfstringdefDisableCommands)
- PRESERVE smart quotes when appropriate
- REMOVE/REPLACE problematic spacing and control characters
- ESCAPE special LaTeX characters

Key insight: Not all Unicode is bad! Some improves typography.
We clean ONLY what causes compilation errors or PDF issues.
"""

import re
import logging
from typing import Dict, Tuple, Set
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class UnicodeCleaningResult:
    """Results from Unicode cleaning operation"""
    file_path: str
    original_chars: Set[str]
    replaced_chars: Dict[str, str]
    removed_chars: Set[str]
    num_changes: int
    preserved_unicode: Set[str]


class UnicodeCharacterMap:
    """
    Unicode character handling based on LaTeX compatibility
    
    Categories:
    1. PRESERVE: Unicode that enhances typography (requires \\usepackage[utf8]{inputenc})
    2. REPLACE: Unicode with LaTeX equivalents
    3. REMOVE: Problematic characters that should be deleted
    """
    
    # Preserve these - good for typography with proper LaTeX setup
    PRESERVE = {
        '–': 'EN DASH (U+2013) - for ranges',
        '—': 'EM DASH (U+2014) - for emphasis',
        ''': 'LEFT SINGLE QUOTE (U+2018)',
        ''': 'RIGHT SINGLE QUOTE (U+2019)',
        '"': 'LEFT DOUBLE QUOTE (U+201C)',
        '"': 'RIGHT DOUBLE QUOTE (U+201D)',
        '°': 'DEGREE SIGN (U+00B0)',
        '±': 'PLUS-MINUS (U+00B1)',
        '×': 'MULTIPLICATION (U+00D7)',
        '÷': 'DIVISION (U+00F7)',
        '≤': 'LESS THAN OR EQUAL (U+2264)',
        '≥': 'GREATER THAN OR EQUAL (U+2265)',
        '≠': 'NOT EQUAL (U+2260)',
        '≈': 'ALMOST EQUAL (U+2248)',
        'α': 'ALPHA (U+03B1)',
        'β': 'BETA (U+03B2)',
        'γ': 'GAMMA (U+03B3)',
        'μ': 'MU (U+03BC)',
    }
    
    # Replace with LaTeX equivalents
    REPLACE = {
        # Problematic spaces
        '\u2003': ' ',  # EM SPACE
        '\u2002': ' ',  # EN SPACE
        '\u2001': ' ',  # EM QUAD
        '\u2000': ' ',  # EN QUAD
        '\u00A0': '~',  # NON-BREAKING SPACE -> LaTeX ~
        '\u202F': '\\,',  # NARROW NO-BREAK SPACE -> thin space
        
        # Ellipsis
        '…': '\\ldots{}',  # HORIZONTAL ELLIPSIS
        
        # Bullet and dashes (if not using preserve mode)
        '•': '\\textbullet{}',  # BULLET
        '‐': '-',  # HYPHEN
        '‑': '-',  # NON-BREAKING HYPHEN
        '‒': '--',  # FIGURE DASH
        '―': '---',  # HORIZONTAL BAR
        
        # Fractions
        '½': '\\frac{1}{2}',
        '⅓': '\\frac{1}{3}',
        '¼': '\\frac{1}{4}',
        '¾': '\\frac{3}{4}',
        
        # Superscripts (convert to LaTeX)
        '¹': '$^1$',
        '²': '$^2$',
        '³': '$^3$',
        
        # Arrows
        '→': '$\\rightarrow$',
        '←': '$\\leftarrow$',
        '↔': '$\\leftrightarrow$',
        '⇒': '$\\Rightarrow$',
        '⇐': '$\\Leftarrow$',
        
        # Special punctuation
        '‹': '<',
        '›': '>',
        '«': '``',
        '»': "''",
    }
    
    # Remove completely (control characters, zero-width, CJK characters, etc.)
    REMOVE = {
        '\u200B',  # ZERO WIDTH SPACE
        '\u200C',  # ZERO WIDTH NON-JOINER
        '\u200D',  # ZERO WIDTH JOINER
        '\uFEFF',  # ZERO WIDTH NO-BREAK SPACE (BOM)
        '\u00AD',  # SOFT HYPHEN
        '\u2060',  # WORD JOINER
    }
    
    # CJK character ranges that need to be removed for LaTeX compatibility
    # These characters cause pdflatex compilation errors
    CJK_RANGES = [
        (0x4E00, 0x9FFF),  # CJK Unified Ideographs
        (0x3400, 0x4DBF),  # CJK Extension A
        (0x20000, 0x2A6DF),  # CJK Extension B
        (0x2A700, 0x2B73F),  # CJK Extension C
        (0x2B740, 0x2B81F),  # CJK Extension D
        (0x2B820, 0x2CEAF),  # CJK Extension E
        (0x2CEB0, 0x2EBEF),  # CJK Extension F
        (0x30000, 0x3134F),  # CJK Extension G
        (0x3190, 0x319F),  # Kanbun
        (0x31C0, 0x31EF),  # CJK Strokes
        (0x31F0, 0x31FF),  # Katakana Phonetic Extensions
        (0x3200, 0x32FF),  # Enclosed CJK Letters and Months
        (0x3300, 0x33FF),  # CJK Compatibility
        (0xF900, 0xFAFF),  # CJK Compatibility Ideographs
        (0x2F800, 0x2FA1F),  # CJK Compatibility Ideographs Supplement
    ]
    
    @classmethod
    def is_cjk_character(cls, char: str) -> bool:
        """
        Check if a character is a CJK character that should be removed
        """
        if not char:
            return False
            
        code_point = ord(char)
        
        # Check if character is in any CJK range
        for start, end in cls.CJK_RANGES:
            if start <= code_point <= end:
                return True
                
        return False


class SpecialCharacterEscaper:
    """
    Escape special LaTeX characters in text mode
    
    Critical for BibTeX fields like 'issue' where underscores appear.
    Example: "15_suppl" must become "15\_suppl"
    """
    
    # Characters that need escaping in LaTeX text mode
    ESCAPE_CHARS = {
        '_': '\\_',
        '%': '\\%',
        '$': '\\$',
        '&': '\\&',
        '#': '\\#',
        # Note: { } \ are more complex, handle separately if needed
    }
    
    @staticmethod
    def escape_text(text: str, exclude: Set[str] = None) -> Tuple[str, int]:
        """
        Escape special characters in LaTeX text
        
        Args:
            text: Input text
            exclude: Set of characters to NOT escape
            
        Returns:
            (escaped_text, num_escapes) tuple
        """
        if exclude is None:
            exclude = set()
        
        result = text
        escapes = 0
        
        for char, replacement in SpecialCharacterEscaper.ESCAPE_CHARS.items():
            if char in exclude:
                continue
            
            # Only escape if not already escaped
            pattern = f'(?<!\\\\){re.escape(char)}'
            matches = len(re.findall(pattern, result))
            if matches > 0:
                result = re.sub(pattern, replacement, result)
                escapes += matches
        
        return result, escapes
    
    @staticmethod
    def escape_bibtex_field(field_content: str) -> Tuple[str, int]:
        """
        Escape special characters in BibTeX field values
        
        Particularly important for:
        - issue fields (e.g., "15_suppl")
        - note fields
        - title fields with special characters
        
        Args:
            field_content: BibTeX field value
            
        Returns:
            (escaped_content, num_escapes) tuple
        """
        # For BibTeX, mainly worry about underscores in text mode
        # (DOIs and URLs should be in \url{} or protected)
        
        # Don't escape if it's already in a URL or protected
        if '\\url{' in field_content or '\\href{' in field_content:
            return field_content, 0
        
        return SpecialCharacterEscaper.escape_text(
            field_content,
            exclude={'%', '$', '&', '#'}  # Only escape _ for most fields
        )


class UnicodeCleaner:
    """
    Clean Unicode characters in LaTeX files
    """
    
    def __init__(self, preserve_typography: bool = True, aggressive: bool = False):
        """
        Args:
            preserve_typography: Keep typographically valuable Unicode (en dash, etc.)
            aggressive: Replace ALL non-ASCII with ASCII equivalents
        """
        self.preserve_typography = preserve_typography
        self.aggressive = aggressive
        self.char_map = UnicodeCharacterMap()
        self.escaper = SpecialCharacterEscaper()
    
    def analyze_file(self, file_path: str) -> Dict[str, Set[str]]:
        """
        Analyze Unicode characters in file without modifying
        
        Args:
            file_path: Path to file
            
        Returns:
            Dict with 'preserve', 'replace', 'remove', 'unknown' character sets
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        analysis = {
            'preserve': set(),
            'replace': set(),
            'remove': set(),
            'cjk': set(),
            'unknown': set()
        }
        
        for char in content:
            if ord(char) > 127:  # Non-ASCII
                if char in self.char_map.PRESERVE:
                    analysis['preserve'].add(char)
                elif char in self.char_map.REPLACE:
                    analysis['replace'].add(char)
                elif char in self.char_map.REMOVE:
                    analysis['remove'].add(char)
                elif self.char_map.is_cjk_character(char):
                    analysis['cjk'].add(char)
                else:
                    analysis['unknown'].add(char)
        
        return analysis
    
    def clean_content(self, content: str) -> Tuple[str, UnicodeCleaningResult]:
        """
        Clean Unicode in text content
        
        Args:
            content: Text to clean
            
        Returns:
            (cleaned_content, result) tuple
        """
        original_chars = set(c for c in content if ord(c) > 127)
        replaced = {}
        removed = set()
        preserved = set()
        
        result_content = content
        
        # Step 1: Remove problematic characters (including control chars)
        for char in self.char_map.REMOVE:
            if char in result_content:
                result_content = result_content.replace(char, '')
                removed.add(char)
        
        # Step 1.5: Remove CJK characters that cause LaTeX errors
        cjk_removed = 0
        for char in result_content[:]:  # Use slice to avoid modification during iteration
            if self.char_map.is_cjk_character(char):
                result_content = result_content.replace(char, '')
                removed.add(char)
                cjk_removed += 1
        
        if cjk_removed > 0:
            logger.info(f"Removed {cjk_removed} CJK characters")
        
        # Step 2: Replace with LaTeX equivalents
        for char, replacement in self.char_map.REPLACE.items():
            if char in result_content:
                result_content = result_content.replace(char, replacement)
                replaced[char] = replacement
        
        # Step 3: Handle preserve list (or replace if aggressive)
        if self.aggressive:
            # In aggressive mode, replace even "good" Unicode
            for char in self.char_map.PRESERVE:
                if char in result_content:
                    # Simple ASCII fallbacks
                    simple_replace = {
                        '–': '--', '—': '---',
                        ''': "'", ''': "'",
                        '"': '"', '"': '"',
                    }
                    replacement = simple_replace.get(char, '')
                    if replacement:
                        result_content = result_content.replace(char, replacement)
                        replaced[char] = replacement
        else:
            # Preserve mode: keep these characters
            if self.preserve_typography:
                for char in self.char_map.PRESERVE:
                    if char in result_content:
                        preserved.add(char)
        
        num_changes = len(replaced) + len(removed)
        
        result = UnicodeCleaningResult(
            file_path="",
            original_chars=original_chars,
            replaced_chars=replaced,
            removed_chars=removed,
            num_changes=num_changes,
            preserved_unicode=preserved
        )
        
        return result_content, result
    
    def clean_file(self, file_path: str, backup: bool = True) -> UnicodeCleaningResult:
        """
        Clean Unicode in a file
        
        Args:
            file_path: Path to file to clean
            backup: Create .bak backup before modifying
            
        Returns:
            UnicodeCleaningResult with statistics
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            original_content = f.read()
        
        cleaned_content, result = self.clean_content(original_content)
        result.file_path = file_path
        
        if cleaned_content != original_content:
            if backup:
                backup_path = f"{file_path}.bak"
                with open(backup_path, 'w', encoding='utf-8') as f:
                    f.write(original_content)
                logger.info(f"Created backup: {backup_path}")
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(cleaned_content)
            
            logger.info(
                f"Cleaned {file_path}: {result.num_changes} changes, "
                f"{len(result.preserved_unicode)} Unicode chars preserved"
            )
        else:
            logger.info(f"No Unicode cleaning needed for {file_path}")
        
        return result
    
    def clean_bibtex_file(self, bib_path: str, backup: bool = True) -> Dict:
        """
        Clean BibTeX file with special attention to field escaping
        
        Critical: Escape underscores in 'issue' fields
        Example: issue = {15_suppl} -> issue = {15\_suppl}
        
        Args:
            bib_path: Path to .bib file
            backup: Create backup
            
        Returns:
            Cleaning statistics
        """
        with open(bib_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if backup:
            with open(f"{bib_path}.bak", 'w', encoding='utf-8') as f:
                f.write(content)
        
        # First, general Unicode cleaning
        cleaned_content, unicode_result = self.clean_content(content)
        
        # Second, escape special characters in specific fields
        # Pattern to match: field = {value}
        field_pattern = r'(\s+(?:issue|note|title)\s*=\s*\{)([^}]+)(\})'
        
        escapes_made = 0
        
        def escape_field(match):
            nonlocal escapes_made
            prefix = match.group(1)
            value = match.group(2)
            suffix = match.group(3)
            
            escaped_value, num_escapes = self.escaper.escape_bibtex_field(value)
            escapes_made += num_escapes
            
            return f"{prefix}{escaped_value}{suffix}"
        
        final_content = re.sub(field_pattern, escape_field, cleaned_content)
        
        if final_content != content:
            with open(bib_path, 'w', encoding='utf-8') as f:
                f.write(final_content)
            
            logger.info(
                f"Cleaned BibTeX file {bib_path}: "
                f"{unicode_result.num_changes} Unicode changes, "
                f"{escapes_made} field escapes"
            )
        
        return {
            'unicode_changes': unicode_result.num_changes,
            'field_escapes': escapes_made,
            'preserved_unicode': len(unicode_result.preserved_unicode)
        }