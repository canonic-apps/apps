#!/usr/bin/env python3
"""
Academic Publication Pipeline with Parameter Extraction to Preamble

This module provides a comprehensive, Pydantic-validated pipeline for academic publications
that extracts all parameters to the preamble for bulletproof consistency.
"""

from pathlib import Path
from typing import List, Dict, Optional, Any
import json
from datetime import datetime

from pydantic import ValidationError
from shared.models_enhanced import (
    AcademicPublicationPipeline, DocumentMetadata, PreambleConfiguration,
    PreambleParameter, PreambleParameterType, Author, DocumentStructure,
    create_title_page_data, create_preamble_parameters, 
    generate_academic_preamble, validate_document_structure
)


class AcademicPublicationProcessor:
    """Main processor for academic publications with preamble parameter extraction"""
    
    def __init__(self, config_file: Optional[str] = None):
        self.config_file = config_file
        self.pipeline_config: Optional[AcademicPublicationPipeline] = None
        self.preamble_config: Optional[PreambleConfiguration] = None
        
    def load_config(self, config_data: Dict[str, Any]) -> AcademicPublicationPipeline:
        """Load and validate configuration using Pydantic"""
        try:
            # Create author objects
            authors = []
            for author_data in config_data.get('authors', []):
                if isinstance(author_data, str):
                    # Simple string format: "First Last"
                    parts = author_data.split()
                    author = Author(
                        given=parts[0] if parts else "",
                        family=" ".join(parts[1:]) if len(parts) > 1 else ""
                    )
                else:
                    # Dict format
                    author = Author(**author_data)
                authors.append(author)
            
            # Create document metadata
            metadata = DocumentMetadata(
                title=config_data.get('title', ''),
                subtitle=config_data.get('subtitle', ''),
                authors=authors,
                date=config_data.get('date', datetime.now().strftime("%Y-%m-%d")),
                abstract=config_data.get('abstract', ''),
                keywords=config_data.get('keywords', []),
                journal=config_data.get('journal', 'Academic Journal'),
                document_class=config_data.get('document_class', 'article'),
                document_options=config_data.get('document_options', ['11pt', 'twocolumn', 'letterpaper'])
            )
            
            # Create pipeline configuration
            self.pipeline_config = AcademicPublicationPipeline(
                name=config_data.get('name', 'Academic Publication'),
                version=config_data.get('version', '1.0.0'),
                config=metadata,
                bibliography_file=config_data.get('bibliography_file', 'refs.bib'),
                source_files=config_data.get('source_files', []),
                output_file=config_data.get('output_file', 'main.pdf')
            )
            
            return self.pipeline_config
            
        except ValidationError as e:
            raise ValueError(f"Invalid configuration: {e}")
    
    def extract_preamble_parameters(self) -> PreambleConfiguration:
        """Extract all document parameters to preamble configuration"""
        if not self.pipeline_config:
            raise ValueError("No pipeline configuration loaded")
        
        metadata = self.pipeline_config.config
        
        # Create preamble configuration
        preamble_config = PreambleConfiguration(metadata=metadata)
        
        # Add title page parameters
        preamble_config.add_parameter(PreambleParameter(
            parameter_type=PreambleParameterType.DOCUMENT_METADATA,
            name="main_title",
            value=metadata.title,
            latex_command="mainTitle",
            description="Main document title"
        ))
        
        if metadata.subtitle:
            preamble_config.add_parameter(PreambleParameter(
                parameter_type=PreambleParameterType.DOCUMENT_METADATA,
                name="subtitle",
                value=metadata.subtitle,
                latex_command="subtitle",
                description="Document subtitle"
            ))
        
        # Add author parameters
        for i, author in enumerate(metadata.authors):
            author_num = i + 1
            
            # Author name
            preamble_config.add_parameter(PreambleParameter(
                parameter_type=PreambleParameterType.AUTHOR_INFO,
                name=f"author_{author_num}_name",
                value=author.full_name,
                latex_command=f"author{author_num}Name",
                description=f"Author {author_num} full name"
            ))
            
            # Given name
            if author.given:
                preamble_config.add_parameter(PreambleParameter(
                    parameter_type=PreambleParameterType.AUTHOR_INFO,
                    name=f"author_{author_num}_given",
                    value=author.given,
                    latex_command=f"author{author_num}Given",
                    description=f"Author {author_num} given name"
                ))
            
            # Family name
            if author.family:
                preamble_config.add_parameter(PreambleParameter(
                    parameter_type=PreambleParameterType.AUTHOR_INFO,
                    name=f"author_{author_num}_family",
                    value=author.family,
                    latex_command=f"author{author_num}Family",
                    description=f"Author {author_num} family name"
                ))
            
            # Affiliation
            if author.affiliation:
                preamble_config.add_parameter(PreambleParameter(
                    parameter_type=PreambleParameterType.AUTHOR_INFO,
                    name=f"author_{author_num}_affiliation",
                    value=author.affiliation,
                    latex_command=f"author{author_num}Affiliation",
                    description=f"Author {author_num} affiliation"
                ))
            
            # Email
            if author.email:
                preamble_config.add_parameter(PreambleParameter(
                    parameter_type=PreambleParameterType.AUTHOR_INFO,
                    name=f"author_{author_num}_email",
                    value=author.email,
                    latex_command=f"author{author_num}Email",
                    description=f"Author {author_num} email"
                ))
        
        # Add date
        preamble_config.add_parameter(PreambleParameter(
            parameter_type=PreambleParameterType.DOCUMENT_METADATA,
            name="publication_date",
            value=metadata.date or datetime.now().strftime("%B %Y"),
            latex_command="publicationDate",
            description="Publication date"
        ))
        
        # Add abstract (if provided)
        if metadata.abstract:
            preamble_config.add_parameter(PreambleParameter(
                parameter_type=PreambleParameterType.DOCUMENT_METADATA,
                name="abstract_text",
                value=metadata.abstract,
                latex_command="abstractText",
                description="Document abstract"
            ))
        
        # Add journal information
        if metadata.journal:
            preamble_config.add_parameter(PreambleParameter(
                parameter_type=PreambleParameterType.DOCUMENT_METADATA,
                name="journal_name",
                value=metadata.journal,
                latex_command="journalName",
                description="Target journal name"
            ))
        
        # Add document formatting parameters
        preamble_config.add_parameter(PreambleParameter(
            parameter_type=PreambleParameterType.FORMATTING_RULES,
            name="document_class",
            value=metadata.document_class,
            latex_command="documentClass",
            description="LaTeX document class"
        ))
        
        preamble_config.add_parameter(PreambleParameter(
            parameter_type=PreambleParameterType.FORMATTING_RULES,
            name="document_options",
            value=", ".join(metadata.document_options),
            latex_command="documentOptions",
            description="LaTeX document class options"
        ))
        
        return preamble_config
    
    def generate_titlepage_latex(self) -> str:
        """Generate title page LaTeX using preamble parameters"""
        if not self.pipeline_config:
            raise ValueError("No pipeline configuration loaded")
        
        metadata = self.pipeline_config.config
        
        lines = [
            "% Generated title page",
            "\\begin{titlepage}",
            "\\thispagestyle{empty}",
            "\\centering",
            "",
            "\\vspace*{2cm}",
            "",
            f"\\LARGE\\bfseries \\mainTitle",
            "\\vspace{1em}",
        ]
        
        if metadata.subtitle:
            lines.append(f"\\large\\itshape \\subtitle")
            lines.append("\\vspace{1em}")
        
        # Add date
        lines.append(f"\\normalsize \\publicationDate")
        lines.append("\\vspace{2em}")
        
        # Add authors
        for i, author in enumerate(metadata.authors):
            author_num = i + 1
            lines.append(f"\\large\\bfseries \\author{author_num}Name")
            if author.affiliation:
                lines.append(f"\\normalsize \\author{author_num}Affiliation")
            lines.append("\\vspace{1em}")
        
        lines.extend([
            "\\hrule",
            "",
            "\\begin{abstract}",
            "\\setlength{\\parindent}{0pt}",
            "\\setlength{\\parskip}{0.5em}",
            f"\\abstractText",
            "\\end{abstract}",
            "",
            "\\end{titlepage}"
        ])
        
        return "\n".join(lines)
    
    def generate_enhanced_preamble(self) -> str:
        """Generate enhanced preamble with all extracted parameters"""
        if not self.pipeline_config:
            raise ValueError("No pipeline configuration loaded")
        
        preamble_config = self.extract_preamble_parameters()
        
        lines = [
            "% Enhanced Academic Publication Preamble",
            "% Generated by AcademicPublicationPipeline",
            "",
            "% Document class and basic packages",
            f"\\documentclass[{','.join(self.pipeline_config.config.document_options)}]{{{self.pipeline_config.config.document_class}}}",
            "\\usepackage[T1]{fontenc}",
            "\\usepackage[utf8]{inputenc}",
            "",
            "% Bibliography setup",
            "\\usepackage[style=nature, backend=biber, sorting=none, sortcites=true, autocite=superscript, maxcitenames=2, mincitenames=1]{biblatex}",
            "\\addbibresource{refs.bib}",
            "",
            "% Mathematics and symbols",
            "\\usepackage{amsmath, amssymb, amsthm, mathtools}",
            "\\usepackage{siunitx}",
            "\\sisetup{",
            "  group-separator = {\\,},",
            "  group-minimum-digits = 4,",
            "  output-decimal-marker = {.},",
            "  range-phrase = {\\text{--}},",
            "  range-units = single,",
            "  per-mode = symbol,",
            "  parse-numbers = true,",
            "  detect-all = true",
            "}",
            "",
            "% Typography and layout",
            "\\usepackage{lmodern, microtype}",
            "\\usepackage{setspace}",
            "\\setlength{\\baselinestretch}{1.2}",
            "\\setlength{\\parskip}{0.5em}",
            "\\setlength{\\parindent}{0pt}",
            "",
            "% Page geometry",
            "\\usepackage[a4paper, margin=1in]{geometry}",
            "\\usepackage{multicol}",
            "\\setlength{\\columnsep}{1cm}",
            "",
            "% Graphics and floats",
            "\\usepackage{graphicx, float, caption, subcaption}",
            "\\usepackage{wrapfig}",
            "",
            "% Tables",
            "\\usepackage{tabularx, booktabs, array, multirow}",
            "",
            "% References and links",
            "\\usepackage{hyperref}",
            "\\hypersetup{",
            "  unicode=true,",
            "  colorlinks=true,",
            "  linkcolor=blue,",
            "  citecolor=blue,",
            "  urlcolor=blue",
            "}",
            "",
            "% Section styling",
            "\\usepackage{titlesec}",
            "\\titleformat{\\section}{\\large\\bfseries}{\\thesection.}{0.5em}{}",
            "\\titleformat{\\subsection}{\\normalsize\\bfseries}{\\thesubsection}{0.5em}{}",
            "",
            "% Custom commands from extracted parameters",
            ""
        ]
        
        # Add extracted parameters as LaTeX commands
        for param in preamble_config.parameters:
            if param.latex_command:
                lines.append(f"\\newcommand{{\\{param.latex_command}}}{{{param.value}}}")
        
        lines.extend([
            "",
            "% Academic publication helper commands",
            "\\newcommand{\\sectionstandard}[1]{%",
            "  \\section{#1}%",
            "  \\addcontentsline{toc}{section}{#1}%",
            "}",
            "",
            "\\newcommand{\\subsectionstandard}[1]{%",
            "  \\subsection{#1}%",
            "  \\addcontentsline{toc}{subsection}{#1}%",
            "}",
            "",
            "\\newcommand{\\techterm}[1]{%",
            "  \\textbf{\\textit{#1}}%",
            "}",
            "",
            "\\newcommand{\\mathstandard}[1]{%",
            "  \\textit{#1}%",
            "}",
            "",
            "\\newcommand{\\equationstandard}[1]{%",
            "  \\begin{equation}",
            "    #1",
            "  \\end{equation}",
            "}",
            "",
            "% Safe numeric formatting (no nested \\num commands)",
            "\\newcommand{\\safenum}[1]{%",
            "  \\num{#1}%",
            "}",
            "",
            "% Title page commands",
            "\\newcommand{\\maintitle}[1]{%",
            "  \\vspace*{1cm}",
            "  {\\LARGE\\bfseries #1}",
            "  \\par",
            "  \\vspace*{0.5cm}",
            "}",
            "",
            "\\newcommand{\\subtitle}[1]{%",
            "  {\\large\\itshape #1}",
            "  \\par",
            "  \\vspace*{0.5cm}",
            "}",
            "",
            "\\newcommand{\\affiliation}[1]{%",
            "  {\\normalsize #1}",
            "  \\par",
            "  \\vspace*{0.3cm}",
            "}",
            ""
        ])
        
        return "\n".join(lines)
    
    def process_document_structure(self, sections: List[DocumentStructure]) -> str:
        """Process document structure with validation"""
        if not self.pipeline_config:
            raise ValueError("No pipeline configuration loaded")
        
        # Validate structure
        issues = validate_document_structure(sections)
        if issues:
            print(f"Validation issues found: {len(issues)}")
            for issue in issues:
                print(f"  {issue.severity.value.upper()}: {issue.message}")
        
        # Generate LaTeX for sections
        lines = ["% Document content", ""]
        
        for section in sections:
            lines.append(section.to_latex())
            lines.append("")
        
        return "\n".join(lines)
    
    def create_complete_document(self) -> Dict[str, str]:
        """Create complete LaTeX document structure"""
        if not self.pipeline_config:
            raise ValueError("No pipeline configuration loaded")
        
        # Generate preamble
        preamble_content = self.generate_enhanced_preamble()
        
        # Generate title page
        titlepage_content = self.generate_titlepage_latex()
        
        # Create main document structure
        main_content = [
            "\\input{preamble}",
            "",
            "\\begin{document}",
            "",
            "% Title page",
            "\\input{titlepage}",
            "\\clearpage",
            "",
            "% Main content",
            "\\pagestyle{fancy}",
            "\\input{01_introduction}",
            "\\input{02_methods}",
            "\\input{03_results}",
            "\\input{04_discussion}",
            "\\input{05_conclusion}",
            "",
            "% Bibliography",
            "\\cleardoublepage",
            "\\onecolumn",
            "\\printbibliography",
            "",
            "\\end{document}"
        ]
        
        return {
            "preamble.tex": preamble_content,
            "titlepage.tex": titlepage_content,
            "main.tex": "\n".join(main_content)
        }

