import re
from typing import List, Optional
from dataclasses import dataclass
from pathlib import Path

from shared.models import ValidationIssue


@dataclass
class FloatingCitation:
    file: str
    line_num: int
    line_content: str
    citation: str


class LatexValidator:
    def __init__(self):
        self.issues: List[ValidationIssue] = []
    
    def validate_file(self, file_path: str) -> List[ValidationIssue]:
        self.issues = []
        
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        self._check_moving_arguments(file_path, lines)
        self._check_citation_consolidation(file_path, lines)
        self._check_typography(file_path, lines)
        self._check_special_characters(file_path, lines)
        self._check_pdf_strings(file_path, lines)
        self._detect_floating_citations(file_path, lines)
        
        return self.issues
    
    def _check_moving_arguments(self, file_path: str, lines: List[str]):
        moving_patterns = [
            (r'\\(sub)*section\*?\{[^}]*\\(auto)?cite', 'section title'),
            (r'\\caption\*?\{[^}]*\\(auto)?cite', 'caption'),
            (r'\\node.*\{[^}]*\\(auto)?cite', 'TikZ node'),
            (r'\\draw.*\{[^}]*\\(auto)?cite', 'TikZ draw'),
        ]
        
        in_abstract = False
        
        for i, line in enumerate(lines, start=1):
            if r'\begin{abstract}' in line:
                in_abstract = True
            elif r'\end{abstract}' in line:
                in_abstract = False
            
            if in_abstract and r'\cite' in line:
                self.issues.append(ValidationIssue(
                    file_path=file_path,
                    line_number=i,
                    issue_type='moving_argument',
                    severity='error',
                    message='Citation in abstract environment (moving argument)',
                    suggestion='Move citation to a "References:" line after abstract',
                    context=line.strip()
                ))
            
            for pattern, context_name in moving_patterns:
                if re.search(pattern, line, re.IGNORECASE):
                    sev = 'warning' if context_name == 'caption' else 'error'
                    self.issues.append(ValidationIssue(
                        file_path=file_path,
                        line_number=i,
                        issue_type='moving_argument',
                        severity=sev,
                        message=f'Citation in {context_name} (moving argument)',
                        suggestion=f'Move citation to adjacent "References:" line or paragraph',
                        context=line.strip()[:100]
                    ))
    
    def _check_citation_consolidation(self, file_path: str, lines: List[str]):
        sequential_pattern = r'\\autocite\{[^}]+\}\s*\\autocite\{[^}]+\}'
        
        for i, line in enumerate(lines, start=1):
            if re.search(sequential_pattern, line):
                self.issues.append(ValidationIssue(
                    file_path=file_path,
                    line_number=i,
                    issue_type='citation_consolidation',
                    severity='warning',
                    message='Sequential citations should be consolidated',
                    suggestion='Merge into single \\autocite{key1,key2,...}',
                    context=line.strip()[:100]
                ))
    
    def _check_typography(self, file_path: str, lines: List[str]):
        for i, line in enumerate(lines, start=1):
            year_range_pattern = r'\b(19|20)\d{2}-(19|20)\d{2}\b'
            if re.search(year_range_pattern, line):
                self.issues.append(ValidationIssue(
                    file_path=file_path,
                    line_number=i,
                    issue_type='typography',
                    severity='warning',
                    message='Year range uses hyphen instead of en dash',
                    suggestion='Use en dash (–) for ranges: 2025–2030',
                    context=line.strip()[:100]
                ))
            
            large_number_pattern = r'\b\d{5,}\b'
            matches = re.findall(large_number_pattern, line)
            for match in matches:
                if not re.match(r'^(19|20)\d{2}$', match):
                    self.issues.append(ValidationIssue(
                        file_path=file_path,
                        line_number=i,
                        issue_type='typography',
                        severity='info',
                        message=f'Large number without formatting: {match}',
                        suggestion='Consider using \\num{{{match}}} for proper formatting',
                        context=line.strip()[:100]
                    ))
    
    def _check_special_characters(self, file_path: str, lines: List[str]):
        in_display_math = False
        
        for i, line in enumerate(lines, start=1):
            if r'\[' in line:
                in_display_math = True
            if r'\]' in line:
                in_display_math = False
                continue
            
            if in_display_math or line.strip().startswith('%') or '\\url{' in line or '\\href{' in line:
                continue
            
            if '_' in line and not '$' in line:
                if r'\mathrm{' in line:
                    continue
                
                temp_line = line
                temp_line = re.sub(r'\\autocite\{[^}]*\}', '', temp_line)
                temp_line = re.sub(r'\\cite\{[^}]*\}', '', temp_line)
                temp_line = re.sub(r'\\label\{[^}]*\}', '', temp_line)
                temp_line = re.sub(r'\\ref\{[^}]*\}', '', temp_line)
                temp_line = re.sub(r'\\texttt\{[^}]*\}', '', temp_line)
                temp_line = re.sub(r'\\input\{[^}]*\}', '', temp_line)
                temp_line = re.sub(r'\\includegraphics(\[[^\]]*\])?\{[^}]*\}', '', temp_line)
                
                if re.search(r'(?<!\\)(?<!\$)_(?!\$)', temp_line):
                    self.issues.append(ValidationIssue(
                        file_path=file_path,
                        line_number=i,
                        issue_type='special_characters',
                        severity='warning',
                        message='Possible unescaped underscore in text mode',
                        suggestion='Escape with backslash: \\_',
                        context=line.strip()[:100]
                    ))
    
    def _check_pdf_strings(self, file_path: str, lines: List[str]):
        problematic_in_pdf = [
            r'\\texttrademark',
            r'\\emph\{',
            r'\\textbf\{',
            r'\\textit\{',
        ]
        
        section_pattern = r'\\(sub)*section\*?\{([^}]+)\}'
        
        for i, line in enumerate(lines, start=1):
            section_match = re.search(section_pattern, line)
            if section_match:
                title_content = section_match.group(2)
                
                for pattern in problematic_in_pdf:
                    if re.search(pattern, title_content):
                        self.issues.append(ValidationIssue(
                            file_path=file_path,
                            line_number=i,
                            issue_type='pdf_string',
                            severity='warning',
                            message='Command in section title may cause PDF bookmark issues',
                            suggestion='Ensure \\pdfstringdefDisableCommands is configured in preamble',
                            context=line.strip()[:100]
                        ))
    
    def _detect_floating_citations(self, file_path: str, lines: List[str]):
        """Detect floating citations (merged from detect_floating_citations.py)"""
        for i, line in enumerate(lines, start=1):
            stripped = line.strip()
            
            if not stripped or stripped.startswith('%') or stripped.startswith('\\begin') or stripped.startswith('\\end'):
                continue
            
            only_cite = re.match(r'^\s*\\autocite\{([^}]+)\}\s*\.?\s*$', stripped)
            if only_cite:
                self.issues.append(ValidationIssue(
                    file_path=file_path,
                    line_number=i,
                    issue_type='floating_citation',
                    severity='warning',
                    message='Floating citation (standalone citation)',
                    suggestion='Add citation to appropriate sentence or create References: line',
                    context=line.strip()
                ))
                continue
            
            trailing_cite = re.search(r'[.!?)\]}]\s+\\autocite\{([^}]+)\}\s*$', stripped)
            if trailing_cite:
                before_cite = stripped[:trailing_cite.start()].strip()
                if len(before_cite) < 20:
                    self.issues.append(ValidationIssue(
                        file_path=file_path,
                        line_number=i,
                        issue_type='floating_citation',
                        severity='warning',
                        message=f'Citation after short text: {before_cite}',
                        suggestion='Move citation to a more substantial sentence',
                        context=line.strip()
                    ))


class NatureStyleValidator:
    def __init__(self):
        self.issues: List[ValidationIssue] = []
    
    def validate_preamble(self, preamble_path: str) -> List[ValidationIssue]:
        self.issues = []
        
        with open(preamble_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if r'\usepackage' not in content or 'biblatex' not in content:
            self.issues.append(ValidationIssue(
                file_path=preamble_path,
                line_number=0,
                issue_type='nature_style',
                severity='error',
                message='biblatex package not found',
                suggestion='Add \\usepackage[style=nature,...]{biblatex}'
            ))
            return self.issues
        
        required_options = {
            'style=nature': 'Nature journal citation style',
            'backend=biber': 'Biber backend for biblatex',
            'sorting=none': 'Citation order (not alphabetical)',
            'sortcites=true': 'Sort multiple citations in one command',
            'autocite=superscript': 'Superscript citation format'
        }
        
        for option, description in required_options.items():
            if option not in content:
                self.issues.append(ValidationIssue(
                    file_path=preamble_path,
                    line_number=0,
                    issue_type='nature_style',
                    severity='warning',
                    message=f'Missing biblatex option: {option}',
                    suggestion=f'Add to biblatex options for {description}'
                ))
        
        if r'\usepackage' in content and 'hyperref' in content:
            if 'unicode=true' not in content:
                self.issues.append(ValidationIssue(
                    file_path=preamble_path,
                    line_number=0,
                    issue_type='nature_style',
                    severity='warning',
                    message='hyperref should have unicode=true for proper PDF metadata',
                    suggestion='Add unicode=true to hyperref options'
                ))
        
        if r'\pdfstringdefDisableCommands' not in content:
            self.issues.append(ValidationIssue(
                file_path=preamble_path,
                line_number=0,
                issue_type='nature_style',
                severity='info',
                message='No PDF string sanitization found',
                suggestion='Add \\pdfstringdefDisableCommands for clean bookmarks'
            ))
        
        return self.issues


class TypographyValidator:
    def __init__(self):
        self.issues: List[ValidationIssue] = []
    
    def validate_file(self, file_path: str) -> List[ValidationIssue]:
        self.issues = []
        
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        for i, line in enumerate(lines, start=1):
            if line.strip().startswith('%'):
                continue
            
            numeric_range_hyphen = r'\b\d+-\d+\b'
            if re.search(numeric_range_hyphen, line):
                if re.search(r'\b\d{4}-\d{4}\b', line):
                    self.issues.append(ValidationIssue(
                        file_path=file_path,
                        line_number=i,
                        issue_type='typography',
                        severity='warning',
                        message='Numeric range uses hyphen, should use en dash',
                        suggestion='Replace hyphen with en dash: 2025–2030',
                        context=line.strip()[:100]
                    ))
            
            standalone_numbers = r'\b\d{1,3}(?:,\d{3})+(?:\.\d+)?\b'
            if re.search(standalone_numbers, line) and '\\num{' not in line:
                self.issues.append(ValidationIssue(
                    file_path=file_path,
                    line_number=i,
                    issue_type='typography',
                    severity='info',
                    message='Large number could use siunitx formatting',
                    suggestion='Wrap in \\num{} for consistent formatting',
                    context=line.strip()[:100]
                ))
        
        return self.issues


def detect_floating_citations(tex_path: Path) -> List[FloatingCitation]:
    """Detect floating citations (standalone function from detect_floating_citations.py)"""
    floaters: List[FloatingCitation] = []
    lines = tex_path.read_text(encoding="utf-8").splitlines()
    
    for i, line in enumerate(lines, start=1):
        stripped = line.strip()
        
        if not stripped or stripped.startswith('%') or stripped.startswith('\\begin') or stripped.startswith('\\end'):
            continue
        
        only_cite = re.match(r'^\s*\\autocite\{([^}]+)\}\s*\.?\s*$', stripped)
        if only_cite:
            floaters.append(FloatingCitation(
                file=tex_path.name,
                line_num=i,
                line_content=line,
                citation=only_cite.group(1)
            ))
            continue
        
        trailing_cite = re.search(r'[.!?)\]}]\s+\\autocite\{([^}]+)\}\s*$', stripped)
        if trailing_cite:
            before_cite = stripped[:trailing_cite.start()].strip()
            if len(before_cite) < 20:
                floaters.append(FloatingCitation(
                    file=tex_path.name,
                    line_num=i,
                    line_content=line,
                    citation=trailing_cite.group(1)
                ))
    
    return floaters


class StyleStandardizationValidator:
    """Validator for style standardization compliance"""
    
    def __init__(self):
        self.issues: List[ValidationIssue] = []
    
    def validate_style_standards(self, file_path: str) -> List[ValidationIssue]:
        """Validate compliance with new style standardization commands"""
        self.issues = []
        
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Check for new style command usage
        self._check_standard_commands(file_path, lines)
        
        # Check for standardization opportunities
        self._check_standardization_opportunities(file_path, lines)
        
        return self.issues
    
    def _check_standard_commands(self, file_path: str, lines: List[str]):
        """Check for proper usage of standardized commands"""
        
        for i, line in enumerate(lines, start=1):
            if line.strip().startswith('%'):
                continue
                
            # Check for non-standardized section headings
            if r'\section*{' in line and r'\sectionstandard{' not in line:
                self.issues.append(ValidationIssue(
                    file_path=file_path,
                    line_number=i,
                    issue_type='section_heading',
                    severity='warning',
                    message='Non-standardized section heading',
                    suggestion='Use \\sectionstandard{} instead of \\section*{}',
                    context=line.strip()[:100]
                ))
            
            # Check for non-standardized math expressions
            if r'$' in line and r'\mathstandard{' not in line:
                # Simple check for inline math that should be standardized
                math_content = re.findall(r'\$([^$]+)\$', line)
                if math_content and not re.search(r'\\mathstandard\{', line):
                    self.issues.append(ValidationIssue(
                        file_path=file_path,
                        line_number=i,
                        issue_type='math_expression',
                        severity='info',
                        message='Non-standardized inline math expression',
                        suggestion='Wrap in \\mathstandard{} for consistency',
                        context=line.strip()[:100]
                    ))
            
            # Check for technical terms that should be standardized
            tech_terms = [
                'artificial intelligence', 'clinical medicine', 'machine learning',
                'data science', 'precision medicine', 'healthcare', 'regulatory',
                'compliance', 'algorithm', 'framework', 'standard', 'protocol'
            ]
            
            for term in tech_terms:
                if re.search(rf'\b{re.escape(term)}\b', line, re.IGNORECASE):
                    if r'\techterm{' not in line:
                        self.issues.append(ValidationIssue(
                            file_path=file_path,
                            line_number=i,
                            issue_type='technical_term',
                            severity='info',
                            message=f'Technical term should be standardized: {term}',
                            suggestion='Consider using \\techterm{} for consistency',
                            context=line.strip()[:100]
                        ))
                        break  # Only report first occurrence per line
    
    def _check_standardization_opportunities(self, file_path: str, lines: List[str]):
        """Check for opportunities to apply style standardization"""
        
        for i, line in enumerate(lines, start=1):
            if line.strip().startswith('%'):
                continue
                
            # Check for large numbers that could use \num{}
            large_numbers = re.findall(r'\b\d{4,}\b', line)
            for num in large_numbers:
                if not re.match(r'^(19|20)\d{2}$', num) and r'\num{' not in line:
                    self.issues.append(ValidationIssue(
                        file_path=file_path,
                        line_number=i,
                        issue_type='number_formatting',
                        severity='info',
                        message=f'Number could use siunitx formatting: {num}',
                        suggestion='Wrap in \\num{} for consistent formatting',
                        context=line.strip()[:100]
                    ))
                    break  # Only report one per line
            
            # Check for backtick code that could be standardized
            backtick_code = re.findall(r'`([^`]+)`', line)
            if backtick_code:
                self.issues.append(ValidationIssue(
                    file_path=file_path,
                    line_number=i,
                    issue_type='code_formatting',
                    severity='info',
                    message='Inline code could be standardized',
                    suggestion='Consider using \\codestandard{} or \\texttt{} for consistency',
                    context=line.strip()[:100]
                ))
            
            # Check for unstandardized captions
            if r'\caption{' in line and r'\caption*{' not in line and r'\textbf{' not in line:
                self.issues.append(ValidationIssue(
                    file_path=file_path,
                    line_number=i,
                    issue_type='figure_caption',
                    severity='info',
                    message='Figure caption could be improved',
                    suggestion='Consider using \\caption*{} with \\textbf{} for better formatting',
                    context=line.strip()[:100]
                ))


class ComprehensiveStyleValidator:
    """Combined validator for all style standards"""
    
    def __init__(self):
        self.latex_validator = LatexValidator()
        self.style_validator = StyleStandardizationValidator()
        self.nature_validator = NatureStyleValidator()
        self.typography_validator = TypographyValidator()
    
    def validate_file(self, file_path: str) -> List[ValidationIssue]:
        """Validate a single file with all validators"""
        all_issues = []
        
        # Run all validators
        all_issues.extend(self.latex_validator.validate_file(file_path))
        all_issues.extend(self.style_validator.validate_style_standards(file_path))
        
        # Only run typography validator for content files, not preamble
        if file_path != 'preamble.tex':
            all_issues.extend(self.typography_validator.validate_file(file_path))
        
        return all_issues
    
    def validate_preamble(self, preamble_path: str) -> List[ValidationIssue]:
        """Validate preamble with style standards"""
        return self.nature_validator.validate_preamble(preamble_path)
    
    def generate_report(self, files: List[str], output_file: str = None) -> dict:
        """Generate comprehensive validation report"""
        all_issues = {}
        total_errors = 0
        total_warnings = 0
        total_info = 0
        
        for file_path in files:
            if file_path == 'preamble.tex':
                issues = self.validate_preamble(file_path)
            else:
                issues = self.validate_file(file_path)
            
            all_issues[file_path] = [
                {
                    'line': issue.line_number,
                    'type': issue.issue_type,
                    'severity': issue.severity,
                    'message': issue.message,
                    'suggestion': issue.suggestion,
                    'context': issue.context
                }
                for issue in issues
            ]
            
            total_errors += len([i for i in issues if i.severity == 'error'])
            total_warnings += len([i for i in issues if i.severity == 'warning'])
            total_info += len([i for i in issues if i.severity == 'info'])
        
        report = {
            'summary': {
                'files_processed': len(files),
                'total_issues': total_errors + total_warnings + total_info,
                'errors': total_errors,
                'warnings': total_warnings,
                'info': total_info
            },
            'issues_by_file': all_issues,
            'generated_at': str(Path().resolve())
        }
        
        if output_file:
            import json
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2)
        
        return report