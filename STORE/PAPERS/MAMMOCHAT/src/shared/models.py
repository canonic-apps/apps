"""
Shared data models for the LaTeX publication pipeline

This module contains data classes and models that are used across multiple domains
(bib, tex, cite, doc) to ensure consistency and avoid duplication.
"""

from typing import Dict, List, Optional, Union, Any
from dataclasses import dataclass, field
from enum import Enum
import re


class CitationStyle(str, Enum):
    """Supported citation styles"""
    NATURE = "nature"
    IEEE = "ieee"
    APA = "apa"
    MLA = "mla"
    CHICAGO = "chicago"


class DocumentType(str, Enum):
    """Document types for processing"""
    ARTICLE = "article"
    BOOK = "book"
    INPROCEEDINGS = "inproceedings"
    INCOLLECTION = "incollection"
    PHDTHESIS = "phdthesis"
    MASTERSTHESIS = "mastersthesis"
    TECHREPORT = "techreport"
    MISC = "misc"
    ONLINE = "online"


class ValidationSeverity(str, Enum):
    """Validation issue severity levels"""
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


class PlacementType(str, Enum):
    """Citation placement strategies"""
    INLINE = "inline"
    REFERENCE_LINE = "reference_line"
    PARAGRAPH_END = "paragraph_end"
    DIRECT_INLINE = "direct_inline"
    REFERENCE_LINE_AFTER = "reference_line_after"
    REFERENCE_LINE_FALLBACK = "reference_line_fallback"


@dataclass
class Author:
    """Author information"""
    given: Optional[str] = None
    family: Optional[str] = None
    full_name: Optional[str] = None
    
    def __post_init__(self):
        if not self.full_name and self.given and self.family:
            self.full_name = f"{self.given} {self.family}"
    
    @property
    def last_name(self) -> str:
        """Get last name (family name)"""
        return self.family or ""
    
    @property
    def first_name(self) -> str:
        """Get first name (given name)"""
        return self.given or ""


@dataclass
class BibTeXEntry:
    """BibTeX entry data model"""
    entry_type: DocumentType
    key: str
    title: Optional[str] = None
    authors: List[Author] = field(default_factory=list)
    journal: Optional[str] = None
    year: Optional[str] = None
    doi: Optional[str] = None
    pmid: Optional[str] = None
    pmc: Optional[str] = None
    url: Optional[str] = None
    abstract: Optional[str] = None
    publisher: Optional[str] = None
    booktitle: Optional[str] = None
    school: Optional[str] = None
    institution: Optional[str] = None
    note: Optional[str] = None
    pages: Optional[str] = None
    volume: Optional[str] = None
    number: Optional[str] = None
    issue: Optional[str] = None
    
    # Additional metadata
    citation_count: int = 0
    quality_score: float = 0.0
    source: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            'entry_type': self.entry_type.value,
            'key': self.key,
            'title': self.title,
            'authors': [self._author_to_dict(author) for author in self.authors],
            'journal': self.journal,
            'year': self.year,
            'doi': self.doi,
            'pmid': self.pmid,
            'pmc': self.pmc,
            'url': self.url,
            'abstract': self.abstract,
            'publisher': self.publisher,
            'booktitle': self.booktitle,
            'school': self.school,
            'institution': self.institution,
            'note': self.note,
            'pages': self.pages,
            'volume': self.volume,
            'number': self.number,
            'issue': self.issue,
            'citation_count': self.citation_count,
            'quality_score': self.quality_score,
            'source': self.source
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'BibTeXEntry':
        """Create from dictionary"""
        authors = [cls._dict_to_author(author_data) for author_data in data.get('authors', [])]
        return cls(
            entry_type=DocumentType(data.get('entry_type', 'misc')),
            key=data['key'],
            title=data.get('title'),
            authors=authors,
            journal=data.get('journal'),
            year=data.get('year'),
            doi=data.get('doi'),
            pmid=data.get('pmid'),
            pmc=data.get('pmc'),
            url=data.get('url'),
            abstract=data.get('abstract'),
            publisher=data.get('publisher'),
            booktitle=data.get('booktitle'),
            school=data.get('school'),
            institution=data.get('institution'),
            note=data.get('note'),
            pages=data.get('pages'),
            volume=data.get('volume'),
            number=data.get('number'),
            issue=data.get('issue'),
            citation_count=data.get('citation_count', 0),
            quality_score=data.get('quality_score', 0.0),
            source=data.get('source')
        )
    
    def _author_to_dict(self, author: Author) -> Dict[str, str]:
        """Convert author to dictionary"""
        return {
            'given': author.given,
            'family': author.family,
            'full_name': author.full_name
        }
    
    @classmethod
    def _dict_to_author(cls, data: Dict[str, str]) -> Author:
        """Create author from dictionary"""
        return Author(
            given=data.get('given'),
            family=data.get('family'),
            full_name=data.get('full_name')
        )
    
    def get_first_author(self) -> Optional[Author]:
        """Get first author"""
        return self.authors[0] if self.authors else None
    
    def has_identifier(self, identifier_type: str) -> bool:
        """Check if entry has a specific identifier"""
        identifiers = {
            'doi': self.doi,
            'pmid': self.pmid,
            'pmc': self.pmc,
            'url': self.url
        }
        return bool(identifiers.get(identifier_type.lower()))


@dataclass
class ValidationIssue:
    """Validation issue data model"""
    file_path: str
    line_number: int
    issue_type: str
    severity: ValidationSeverity
    message: str
    suggestion: Optional[str] = None
    context: Optional[str] = None


@dataclass
class CitationPlacement:
    """Citation placement recommendation"""
    file_path: str
    line_number: int
    paragraph_text: str
    sentence: str
    citation_key: str
    similarity_score: float
    placement_type: PlacementType
    confidence: float
    warning: Optional[str] = None


@dataclass
class ProcessingStats:
    """Processing statistics"""
    total_files: int = 0
    processed_files: int = 0
    changed_files: int = 0
    total_entries: int = 0
    enhanced_entries: int = 0
    validation_errors: int = 0
    validation_warnings: int = 0
    citations_consolidated: int = 0
    duplicates_removed: int = 0
    processing_time: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'total_files': self.total_files,
            'processed_files': self.processed_files,
            'changed_files': self.changed_files,
            'total_entries': self.total_entries,
            'enhanced_entries': self.enhanced_entries,
            'validation_errors': self.validation_errors,
            'validation_warnings': self.validation_warnings,
            'citations_consolidated': self.citations_consolidated,
            'duplicates_removed': self.duplicates_removed,
            'processing_time': self.processing_time
        }


@dataclass
class UnicodeCleaningResult:
    """Results from Unicode cleaning operation"""
    file_path: str
    original_chars: List[str]
    replaced_chars: Dict[str, str]
    removed_chars: List[str]
    num_changes: int
    preserved_unicode: List[str]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'file_path': self.file_path,
            'original_chars': list(self.original_chars),
            'replaced_chars': self.replaced_chars,
            'removed_chars': list(self.removed_chars),
            'num_changes': self.num_changes,
            'preserved_unicode': list(self.preserved_unicode)
        }


# Utility functions for data models
def normalize_key(key: str) -> str:
    """Normalize BibTeX key for consistency"""
    if not key:
        return ""
    
    # Convert to lowercase
    normalized = key.lower()
    
    # Remove special characters, keep alphanumeric, hyphens, underscores
    normalized = re.sub(r'[^a-z0-9_-]', '', normalized)
    
    return normalized


def extract_year_from_text(text: str) -> Optional[str]:
    """Extract 4-digit year from text"""
    if not text:
        return None
    
    # Look for 4-digit years between 1800 and 2100
    year_match = re.search(r'\b(1[89]\d{2}|20\d{2}|2100)\b', str(text))
    if year_match:
        return year_match.group(1)
    
    return None


def sanitize_filename(filename: str) -> str:
    """Sanitize filename for cross-platform compatibility"""
    if not filename:
        return "unnamed"
    
    # Remove or replace invalid characters
    sanitized = re.sub(r'[<>:"/\\|?*]', '_', filename)
    
    # Limit length
    if len(sanitized) > 255:
        name, ext = sanitized.rsplit('.', 1) if '.' in sanitized else (sanitized, '')
        sanitized = name[:250] + ('.' + ext if ext else '')
    
    return sanitized


def format_author_list(authors: List[Author], style: str = 'bibtex') -> str:
    """Format author list for different styles"""
    if not authors:
        return ""
    
    if style == 'bibtex':
        # Format: "Last, First and Last, First"
        author_strings = []
        for author in authors:
            if author.family and author.given:
                author_strings.append(f"{author.family}, {author.given}")
            elif author.family:
                author_strings.append(author.family)
            elif author.full_name:
                author_strings.append(author.full_name)
        return " and ".join(author_strings)
    
    elif style == 'apa':
        # Format: "Last, F., Last, F., & Last, F."
        author_strings = []
        for i, author in enumerate(authors):
            if author.family and author.given:
                initial = author.given[0] if author.given else ""
                author_str = f"{author.family}, {initial}."
            elif author.family:
                author_str = author.family
            elif author.full_name:
                author_str = author.full_name
            else:
                continue
            
            # Add ampersand before last author
            if i == len(authors) - 1 and len(authors) > 1:
                author_str = f"& {author_str}"
            elif i == 0:
                author_str = author_str  # First author, no prefix
            
            author_strings.append(author_str)
        
        return ", ".join(author_strings)
    
    else:
        # Default: simple list
        return ", ".join(author.full_name or author.family or "" for author in authors if author.full_name or author.family)