"""
LaTeX Style Manager for standardized document styling

This module provides utilities for applying consistent styles across LaTeX documents,
including color schemes, section formatting, header/footer styling, and vignette boxes.
"""

import re
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class StyleConfig:
    """Configuration for LaTeX styling"""
    brand_colors: Dict[str, str]
    section_format: Dict[str, str]
    header_footer: Dict[str, str]
    vignette_style: Dict[str, str]


class LatexStyleManager:
    """
    Manages LaTeX styling across multiple documents with consistent branding
    """
    
    def __init__(self, config: Optional[StyleConfig] = None):
        """Initialize with default MammoChat branding configuration"""
        self.config = config or self._default_mammochat_config()
    
    def _default_mammochat_config(self) -> StyleConfig:
        """Default MammoChat branding configuration"""
        return StyleConfig(
            brand_colors={
                'mammo_pink': 'F8C7CF',
                'slate': '4B5563', 
                'link_blue': '1B4F72'
            },
            section_format={
                'section': '{\\color{slate}\\Large\\bfseries}',
                'subsection': '{\\color{slate}\\large\\bfseries}'
            },
            header_footer={
                'left_header': '\\textcolor{slate}{\\textbf{MammoChat\\texttrademark}}',
                'right_header': '\\textcolor{mammo_pink}{\\textbf{The Empathy Edition}}',
                'footer': '\\textcolor{slate}{\\small MammoChat.com — Your Journey, Together. \\quad Page \\thepage}'
            },
            vignette_style={
                'name': 'redvignette',
                'back_color': 'red!1',
                'frame_color': 'red!60!black',
                'box_rule': '0.6pt',
                'arc': '2pt',
                'padding': '4pt,4pt,3pt,3pt'
            }
        )
    
    def generate_preamble_styles(self) -> str:
        """Generate complete style definitions for preamble.tex"""
        colors = self.config.brand_colors
        sections = self.config.section_format
        headers = self.config.header_footer
        vignette = self.config.vignette_style
        
        return f"""% === Colors and Branding ===
\\usepackage{{xcolor}}
\\definecolor{{mammoPink}}{{HTML}}{{{colors['mammo_pink']}}}
\\definecolor{{slate}}{{HTML}}{{{colors['slate']}}}
\\definecolor{{linkblue}}{{HTML}}{{{colors['link_blue']}}}

% === Section Styling ===
\\usepackage{{titlesec}}
\\titleformat{{\\section}}
  {{{sections['section']}}}
  {{\\thesection.}}{{0.5em}}{{}}
\\titleformat{{\\subsection}}
  {{{sections['subsection']}}}
  {{\\thesubsection}}{{0.5em}}{{}}

% === Header / Footer ===
\\usepackage{{fancyhdr}}
\\pagestyle{{fancy}}
\\fancyhf{{}}
\\fancyhead[L]{{{headers['left_header']}}}
\\fancyhead[R]{{{headers['right_header']}}}
\\fancyfoot[C]{{{headers['footer']}}}

% === Vignette Box Style ===
\\usepackage[most]{{tcolorbox}}
\\tcbset{{
  {vignette['name']}/.style={{
    enhanced,
    colback={vignette['back_color']},
    colframe={vignette['frame_color']},
    boxrule={vignette['box_rule']},
    arc={vignette['arc']},
    left={vignette['padding'].split(',')[0]}, right={vignette['padding'].split(',')[1]}, top={vignette['padding'].split(',')[2]}, bottom={vignette['padding'].split(',')[3]},
    fonttitle=\\bfseries\\small,
    coltitle=white,
    title={{#1}},
    halign=justify, valign=top
  }}
}}"""
    
    def apply_styles_to_tex_files(self, tex_dir: Path, backup: bool = True) -> Dict[str, int]:
        """
        Apply standardized styles to all .tex files in directory
        
        Args:
            tex_dir: Directory containing .tex files
            backup: Whether to create backup files
            
        Returns:
            Dictionary mapping file paths to number of changes made
        """
        results = {}
        
        # Find all .tex files
        tex_files = list(tex_dir.glob('*.tex'))
        
        for tex_file in tex_files:
            changes = self._apply_styles_to_file(tex_file, backup)
            results[str(tex_file)] = changes
            
        return results
    
    def _apply_styles_to_file(self, tex_file: Path, backup: bool = True) -> int:
        """Apply styles to a single .tex file"""
        with open(tex_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        changes = 0
        
        # Remove duplicate style definitions
        content = self._remove_duplicate_styles(content)
        
        # Add missing style includes
        content = self._ensure_style_includes(content)
        
        # Apply consistent formatting
        content = self._apply_consistent_formatting(content)
        
        changes = len(content) - len(original_content)
        
        if changes != 0:
            if backup:
                backup_file = tex_file.with_suffix('.tex.backup')
                backup_file.write_text(original_content, encoding='utf-8')
            
            tex_file.write_text(content, encoding='utf-8')
        
        return abs(changes)
    
    def _remove_duplicate_styles(self, content: str) -> str:
        """Remove duplicate style definitions"""
        # Remove standalone styles.tex references
        content = re.sub(r'\\input\{styles\.tex\}\s*', '', content)
        
        # Remove duplicate color definitions
        content = re.sub(
            r'\\definecolor\{mammoPink\}\{HTML\}\{F8C7CF\}\s*',
            '',
            content
        )
        content = re.sub(
            r'\\definecolor\{slate\}\{HTML\}\{4B5563\}\s*',
            '',
            content
        )
        content = re.sub(
            r'\\definecolor\{linkblue\}\{HTML\}\{1B4F72\}\s*',
            '',
            content
        )
        
        return content
    
    def _ensure_style_includes(self, content: str) -> str:
        """Ensure proper style includes in preamble"""
        # This would typically ensure \input{preamble} is present
        # For now, just return content as-is
        return content
    
    def _apply_consistent_formatting(self, content: str) -> str:
        """Apply consistent formatting across the document"""
        # Normalize whitespace
        content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)
        
        # Ensure proper section spacing
        content = re.sub(r'(\\section\{[^}]+\})\s*\n\s*\\subsection', r'\1\n\n\\subsection', content)
        
        return content
    
    def validate_style_consistency(self, tex_dir: Path) -> Dict[str, List[str]]:
        """Validate style consistency across all .tex files"""
        issues = {}
        tex_files = list(tex_dir.glob('*.tex'))
        
        for tex_file in tex_files:
            file_issues = []
            
            with open(tex_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check for duplicate color definitions
            if re.search(r'\\definecolor\{mammoPink\}', content):
                file_issues.append("Duplicate mammoPink color definition")
            
            if re.search(r'\\definecolor\{slate\}', content):
                file_issues.append("Duplicate slate color definition")
            
            # Check for styles.tex references
            if re.search(r'\\input\{styles\.tex\}', content):
                file_issues.append("References unused styles.tex")
            
            if file_issues:
                issues[str(tex_file)] = file_issues
        
        return issues


def create_standardized_styles():
    """Create a standardized style configuration"""
    manager = LatexStyleManager()
    return manager.generate_preamble_styles()


if __name__ == "__main__":
    # Example usage
    manager = LatexStyleManager()
    styles = manager.generate_preamble_styles()
    print("Generated standardized styles:")
    print(styles)