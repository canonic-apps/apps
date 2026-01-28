"""
Enhanced data models for the academic publication pipeline using Pydantic

This module provides robust, validated data models that extract parameters
to the preamble and provide bulletproof data mapping for academic publications.
"""

from typing import Dict, List, Optional, Union, Any, Literal
from pydantic import BaseModel, Field, field_validator, model_validator
from enum import Enum
import re
from datetime import datetime


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


class PreambleParameterType(str, Enum):
    """Types of preamble parameters"""
    AUTHOR_INFO = "author_info"
    DOCUMENT_METADATA = "document_metadata"
    FORMATTING_RULES = "formatting_rules"
    CUSTOM_COMMANDS = "custom_commands"
    STYLE_CONFIGURATION = "style_configuration"
    LAYOUT_PARAMETERS = "layout_parameters"


class Author(BaseModel):
    """Author information with Pydantic validation"""
    given: Optional[str] = Field(None, description="Author's given name")
    family: Optional[str] = Field(None, description="Author's family name")
    full_name: Optional[str] = Field(None, description="Author's full name")
    email: Optional[str] = Field(None, description="Author's email")
    affiliation: Optional[str] = Field(None, description="Author's affiliation")
    orcid: Optional[str] = Field(None, description="Author's ORCID ID")
    
    @field_validator('email')
    @classmethod
    def validate_email(cls, v):
        if v and not re.match(r'^[^@]+@[^@]+\.[^@]+$', v):
            raise ValueError('Invalid email format')
        return v
    
    @field_validator('orcid')
    @classmethod
    def validate_orcid(cls, v):
        if v and not re.match(r'^\d{4}-\d{4}-\d{4}-\d{4}$', v):
            raise ValueError('Invalid ORCID format')
        return v
    
    @model_validator(mode='before')
    @classmethod
    def build_full_name(cls, data):
        if isinstance(data, dict):
            given = data.get('given')
            family = data.get('family')
            full_name = data.get('full_name')
            
            if not full_name and given and family:
                data['full_name'] = f"{given} {family}"
            elif not full_name and (given or family):
                data['full_name'] = given or family
        return data
    
    @property
    def last_name(self) -> str:
        """Get last name (family name)"""
        return self.family or ""
    
    @property
    def first_name(self) -> str:
        """Get first name (given name)"""
        return self.given or ""


class BibTeXEntry(BaseModel):
    """BibTeX entry data model with Pydantic validation"""
    entry_type: DocumentType
    key: str = Field(..., min_length=1, description="Unique BibTeX key")
    title: Optional[str] = Field(None, description="Entry title")
    authors: List[Author] = Field(default_factory=list)
    journal: Optional[str] = Field(None, description="Journal name")
    year: Optional[str] = Field(None, description="Publication year")
    doi: Optional[str] = Field(None, description="DOI")
    pmid: Optional[str] = Field(None, description="PubMed ID")
    pmc: Optional[str] = Field(None, description="PubMed Central ID")
    url: Optional[str] = Field(None, description="URL")
    abstract: Optional[str] = Field(None, description="Abstract")
    publisher: Optional[str] = Field(None, description="Publisher")
    booktitle: Optional[str] = Field(None, description="Book title")
    school: Optional[str] = Field(None, description="School")
    institution: Optional[str] = Field(None, description="Institution")
    note: Optional[str] = Field(None, description="Note")
    pages: Optional[str] = Field(None, description="Page range")
    volume: Optional[str] = Field(None, description="Volume")
    number: Optional[str] = Field(None, description="Number")
    issue: Optional[str] = Field(None, description="Issue")
    
    # Additional metadata
    citation_count: int = Field(0, ge=0, description="Citation count")
    quality_score: float = Field(0.0, ge=0.0, le=1.0, description="Quality score")
    source: Optional[str] = Field(None, description="Data source")
    
    @field_validator('year')
    @classmethod
    def validate_year(cls, v):
        if v and not re.match(r'^\d{4}$', v):
            raise ValueError('Year must be 4 digits')
        return v
    
    @field_validator('doi')
    @classmethod
    def validate_doi(cls, v):
        if v and not re.match(r'^10\.\d+/.*', v):
            raise ValueError('Invalid DOI format')
        return v
    
    def get_first_author(self) -> Optional[Author]:
        """Get first author"""
        return self.authors[0] if self.authors else None


class DocumentMetadata(BaseModel):
    """Document metadata for preamble extraction"""
    title: str = Field(..., min_length=1, description="Document title")
    subtitle: Optional[str] = Field(None, description="Document subtitle")
    authors: List[Author] = Field(..., min_items=1, description="Document authors")
    date: Optional[str] = Field(None, description="Publication date")
    abstract: Optional[str] = Field(None, description="Document abstract")
    keywords: List[str] = Field(default_factory=list, description="Keywords")
    journal: Optional[str] = Field(None, description="Target journal")
    document_class: str = Field("article", description="LaTeX document class")
    document_options: List[str] = Field(default_factory=list, description="Document class options")


class PreambleParameter(BaseModel):
    """Individual preamble parameter for extraction"""
    parameter_type: PreambleParameterType
    name: str = Field(..., min_length=1, description="Parameter name")
    value: Any = Field(..., description="Parameter value")
    latex_command: Optional[str] = Field(None, description="LaTeX command name")
    description: Optional[str] = Field(None, description="Parameter description")
    is_required: bool = Field(True, description="Whether parameter is required")
    
    def to_latex(self) -> str:
        """Convert to LaTeX command"""
        if self.latex_command:
            return f"\\newcommand{{\\{self.latex_command}}}{{{self.value}}}"
        return f"% {self.name}: {self.value}"


class DocumentStructure(BaseModel):
    """Document structure for academic publications"""
    title: str = Field(..., description="Section title")
    content: str = Field(..., description="Section content")
    section_type: Literal["section", "subsection", "subsubsection"] = "section"
    label: Optional[str] = Field(None, description="Section label")
    references: List[str] = Field(default_factory=list, description="Referenced citation keys")
    figures: List[str] = Field(default_factory=list, description="Referenced figure labels")
    tables: List[str] = Field(default_factory=list, description="Referenced table labels")
    
    def to_latex(self) -> str:
        """Convert to LaTeX"""
        section_cmd = f"\\{self.section_type}"
        if self.label:
            return f"{section_cmd}{{{self.title}}}\\label{{{self.label}}}\n{self.content}"
        return f"{section_cmd}{{{self.title}}}\n{self.content}"


class PreambleConfiguration(BaseModel):
    """Complete preamble configuration with all parameters"""
    metadata: DocumentMetadata
    parameters: List[PreambleParameter] = Field(default_factory=list)
    custom_commands: Dict[str, str] = Field(default_factory=dict)
    style_rules: Dict[str, Any] = Field(default_factory=dict)
    layout_config: Dict[str, Any] = Field(default_factory=dict)
    
    def add_parameter(self, param: PreambleParameter):
        """Add a preamble parameter"""
        self.parameters.append(param)
    
    def add_custom_command(self, name: str, definition: str):
        """Add a custom command"""
        self.custom_commands[name] = definition
    
    def to_preamble_latex(self) -> str:
        """Generate LaTeX preamble content"""
        lines = []
        
        # Add custom commands
        for name, definition in self.custom_commands.items():
            lines.append(f"\\newcommand{{\\{name}}}{{{definition}}}")
        
        # Add parameters
        for param in self.parameters:
            lines.append(param.to_latex())
        
        return "\n".join(lines)


class ValidationIssue(BaseModel):
    """Validation issue data model"""
    file_path: str = Field(..., description="File path")
    line_number: int = Field(..., ge=1, description="Line number")
    issue_type: str = Field(..., description="Type of issue")
    severity: ValidationSeverity = Field(..., description="Severity level")
    message: str = Field(..., description="Issue message")
    suggestion: Optional[str] = Field(None, description="Suggested fix")
    context: Optional[str] = Field(None, description="Additional context")
    timestamp: datetime = Field(default_factory=datetime.now, description="When issue was found")


class CitationPlacement(BaseModel):
    """Citation placement recommendation"""
    file_path: str = Field(..., description="File path")
    line_number: int = Field(..., ge=1, description="Line number")
    paragraph_text: str = Field(..., description="Paragraph text")
    sentence: str = Field(..., description="Target sentence")
    citation_key: str = Field(..., description="Citation key")
    similarity_score: float = Field(..., ge=0.0, le=1.0, description="Similarity score")
    placement_type: PlacementType = Field(..., description="Placement type")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score")
    warning: Optional[str] = Field(None, description="Warning message")


class ProcessingStats(BaseModel):
    """Processing statistics"""
    total_files: int = Field(0, ge=0, description="Total files processed")
    processed_files: int = Field(0, ge=0, description="Successfully processed files")
    changed_files: int = Field(0, ge=0, description="Files that were changed")
    total_entries: int = Field(0, ge=0, description="Total entries processed")
    enhanced_entries: int = Field(0, ge=0, description="Enhanced entries")
    validation_errors: int = Field(0, ge=0, description="Validation errors")
    validation_warnings: int = Field(0, ge=0, description="Validation warnings")
    citations_consolidated: int = Field(0, ge=0, description="Citations consolidated")
    duplicates_removed: int = Field(0, ge=0, description="Duplicates removed")
    processing_time: float = Field(0.0, ge=0.0, description="Processing time in seconds")
    started_at: datetime = Field(default_factory=datetime.now, description="Processing start time")
    completed_at: Optional[datetime] = Field(None, description="Processing completion time")


class AcademicPublicationPipeline(BaseModel):
    """Main pipeline configuration for academic publications"""
    name: str = Field(..., min_length=1, description="Pipeline name")
    version: str = Field(..., description="Pipeline version")
    config: DocumentMetadata = Field(..., description="Document configuration")
    preamble_config: PreambleConfiguration = Field(default_factory=PreambleConfiguration, description="Preamble configuration")
    bibliography_file: str = Field("refs.bib", description="Bibliography file path")
    source_files: List[str] = Field(default_factory=list, description="Source LaTeX files")
    output_file: str = Field("main.pdf", description="Output file")
    validation_rules: Dict[str, Any] = Field(default_factory=dict, description="Validation rules")
    
    def to_config_dict(self) -> Dict[str, Any]:
        """Convert to configuration dictionary"""
        return {
            "pipeline_name": self.name,
            "pipeline_version": self.version,
            "document_metadata": self.config.dict(),
            "preamble_config": {
                "custom_commands": self.preamble_config.custom_commands,
                "style_rules": self.preamble_config.style_rules,
                "layout_config": self.preamble_config.layout_config
            },
            "files": {
                "bibliography": self.bibliography_file,
                "source": self.source_files,
                "output": self.output_file
            },
            "validation": self.validation_rules
        }


class StyleStandardizationRule(BaseModel):
    """Style standardization rule"""
    name: str = Field(..., description="Rule name")
    pattern: str = Field(..., description="Regex pattern to match")
    replacement: str = Field(..., description="Replacement string")
    is_active: bool = Field(True, description="Whether rule is active")
    priority: int = Field(0, description="Rule priority (higher = earlier)")
    description: Optional[str] = Field(None, description="Rule description")


# Utility functions for academic publications
def create_title_page_data(title: str, subtitle: str, authors: List[Author], 
                          affiliation: str, date: str) -> DocumentMetadata:
    """Create title page data for academic publications"""
    return DocumentMetadata(
        title=title,
        subtitle=subtitle,
        authors=authors,
        journal="Academic Journal Template",
        document_class="article",
        document_options=["11pt", "twocolumn", "letterpaper"]
    )


def create_preamble_parameters(metadata: DocumentMetadata) -> List[PreambleParameter]:
    """Create preamble parameters from document metadata"""
    params = []
    
    # Add author information
    for i, author in enumerate(metadata.authors):
        params.append(PreambleParameter(
            parameter_type=PreambleParameterType.AUTHOR_INFO,
            name=f"author_{i+1}_name",
            value=author.full_name,
            latex_command=f"author{i+1}Name"
        ))
        if author.affiliation:
            params.append(PreambleParameter(
                parameter_type=PreambleParameterType.AUTHOR_INFO,
                name=f"author_{i+1}_affiliation",
                value=author.affiliation,
                latex_command=f"author{i+1}Affiliation"
            ))
    
    # Add document metadata
    params.extend([
        PreambleParameter(
            parameter_type=PreambleParameterType.DOCUMENT_METADATA,
            name="document_title",
            value=metadata.title,
            latex_command="documentTitle"
        ),
        PreambleParameter(
            parameter_type=PreambleParameterType.DOCUMENT_METADATA,
            name="document_subtitle",
            value=metadata.subtitle or "",
            latex_command="documentSubtitle"
        ),
        PreambleParameter(
            parameter_type=PreambleParameterType.DOCUMENT_METADATA,
            name="publication_date",
            value=metadata.date or datetime.now().strftime("%Y"),
            latex_command="publicationDate"
        )
    ])
    
    return params


def generate_academic_preamble(pipeline: AcademicPublicationPipeline) -> str:
    """Generate complete LaTeX preamble for academic publication"""
    lines = []
    
    # Document class and options
    lines.append(f"\\documentclass[{','.join(pipeline.config.document_options)}]{{{pipeline.config.document_class}}}")
    lines.append("")
    
    # Add custom commands
    lines.append("% Custom commands for academic publication")
    for name, definition in pipeline.preamble_config.custom_commands.items():
        lines.append(f"\\newcommand{{\\{name}}}{{{definition}}}")
    lines.append("")
    
    # Add preamble parameters
    lines.append("% Document parameters")
    for param in pipeline.preamble_config.parameters:
        if param.latex_command:
            lines.append(f"\\newcommand{{\\{param.latex_command}}}{{{param.value}}}")
    lines.append("")
    
    # Add style rules
    if pipeline.preamble_config.style_rules:
        lines.append("% Style rules")
        # Add any additional style configuration here
        lines.append("")
    
    return "\n".join(lines)


def validate_document_structure(sections: List[DocumentStructure]) -> List[ValidationIssue]:
    """Validate document structure for academic publications"""
    issues = []
    
    # Check for duplicate labels
    labels = set()
    for section in sections:
        if section.label:
            if section.label in labels:
                issues.append(ValidationIssue(
                    file_path="document_structure",
                    line_number=0,
                    issue_type="duplicate_label",
                    severity=ValidationSeverity.ERROR,
                    message=f"Duplicate section label: {section.label}",
                    suggestion="Use unique labels for each section"
                ))
            labels.add(section.label)
    
    # Check for empty sections
    for i, section in enumerate(sections):
        if not section.content.strip():
            issues.append(ValidationIssue(
                file_path="document_structure",
                line_number=i+1,
                issue_type="empty_section",
                severity=ValidationSeverity.WARNING,
                message=f"Empty section: {section.title}",
                suggestion="Add content to section or remove if unnecessary"
            ))
    
    return issues


def extract_numeric_parameters(content: str) -> List[str]:
    """Extract numeric values that should use \\num{} commands"""
    # Common patterns for numbers in academic writing
    patterns = [
        r'\b\d{4}\b',  # Years
        r'\b\d+(?:\.\d+)?\s*(?:million|billion|thousand|percent|%)\b',  # Numbers with units
        r'\b\d+(?:,\d{3})*\b',  # Large numbers with commas
        r'\b\d+(?:\.\d+)?\s*×\s*10\^?\d+\b',  # Scientific notation
    ]
    
    numbers = []
    for pattern in patterns:
        matches = re.findall(pattern, content, re.IGNORECASE)
        numbers.extend(matches)
    
    return list(set(numbers))  # Remove duplicates