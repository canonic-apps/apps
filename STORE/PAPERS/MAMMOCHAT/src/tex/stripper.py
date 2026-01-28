#!/usr/bin/env python3
"""
Generalized LaTeX environment and formatting stripper
Removes unnecessary environments, formatting, and other constructs that may cause compilation issues
"""

import re
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Dict, Set, Optional, Callable, Union
from enum import Enum


class StripMode(Enum):
    """Stripping mode for different types of constructs"""
    ENVIRONMENT = "environment"
    COMMAND = "command" 
    INLINE = "inline"
    CONDITIONAL = "conditional"


@dataclass
class StripRule:
    """Rule for stripping LaTeX constructs"""
    name: str
    mode: StripMode
    pattern: Union[str, re.Pattern]
    description: str
    preserve_content: bool = True
    preserve_newlines: bool = False
    custom_replacer: Optional[Callable[[re.Match], str]] = None


@dataclass
class StrippingResult:
    """Result of LaTeX stripping operation"""
    file_path: str
    content: str = ""
    total_stripped: int = 0
    rules_applied: Dict[str, int] = field(default_factory=dict)
    content_changed: bool = False
    backup_created: bool = False


class LatexStripper:
    """
    Generalized LaTeX environment and formatting stripper
    
    Can remove:
    - Environment blocks (multicols, figure, table, etc.)
    - Inline formatting (textbf, textit, emph, etc.)
    - Commands and constructs
    - Conditional formatting
    - Any custom LaTeX patterns
    """
    
    def __init__(self, strip_mode: str = "auto"):
        """
        Initialize the stripper
        
        Args:
            strip_mode: "auto" (detect common issues), "full" (strip all), 
                       or "custom" (use only specified rules)
        """
        self.strip_mode = strip_mode
        self.rules: List[StripRule] = []
        self._initialize_default_rules()
        
    def _initialize_default_rules(self):
        """Initialize default stripping rules for common problematic constructs"""
        
        # Multicolumn environments (most common issue) - FIXED REGEX
        self.add_rule(StripRule(
            name="multicols_environment",
            mode=StripMode.ENVIRONMENT,
            pattern=r'\\begin\{multicols\}[^}]*?\\end\{multicols\}',
            description="Remove multicolumn environments (document uses twocolumn by default)",
            preserve_content=True,
            preserve_newlines=False,
            custom_replacer=lambda m: m.group(0).replace('\\begin{multicols}', '').replace('\\end{multicols}', '')
        ))
        
        self.add_rule(StripRule(
            name="begin_multicols",
            mode=StripMode.COMMAND,
            pattern=r'\\begin\{multicols\}[^}]*?\}',
            description="Remove begin multicolumn commands",
            preserve_content=False,
            preserve_newlines=False
        ))
        
        self.add_rule(StripRule(
            name="end_multicols",
            mode=StripMode.COMMAND,
            pattern=r'\\end\{multicols\}',
            description="Remove end multicolumn commands",
            preserve_content=False,
            preserve_newlines=False
        ))
        
        # Common problematic environments
        self.add_rule(StripRule(
            name="minipage_environment",
            mode=StripMode.ENVIRONMENT,
            pattern=r'\\begin\{minipage\}.*?\\end\{minipage\}',
            description="Remove minipage environments that may cause layout issues",
            preserve_content=True,
            preserve_newlines=False,
            custom_replacer=lambda m: m.group(0)  # Keep the content, remove the minipage wrapper
        ))
        
        # Inline formatting that often causes issues
        self.add_rule(StripRule(
            name="textbf_formatting",
            mode=StripMode.INLINE,
            pattern=r'\\textbf\{([^}]+)\}',
            description="Remove bold text formatting",
            preserve_content=True,
            custom_replacer=lambda m: m.group(1)
        ))
        
        self.add_rule(StripRule(
            name="textit_formatting", 
            mode=StripMode.INLINE,
            pattern=r'\\textit\{([^}]+)\}',
            description="Remove italic text formatting",
            preserve_content=True,
            custom_replacer=lambda m: m.group(1)
        ))
        
        self.add_rule(StripRule(
            name="emph_formatting",
            mode=StripMode.INLINE,
            pattern=r'\\emph\{([^}]+)\}',
            description="Remove emphasis formatting",
            preserve_content=True,
            custom_replacer=lambda m: m.group(1)
        ))
        
        # Mathematical formatting that may be problematic
        self.add_rule(StripRule(
            name="mathstandard_command",
            mode=StripMode.COMMAND,
            pattern=r'\\mathstandard\{([^}]+)\}',
            description="Remove mathstandard commands",
            preserve_content=True,
            custom_replacer=lambda m: m.group(1)
        ))
        
        # Common figure and table environments that may be problematic
        self.add_rule(StripRule(
            name="wrapfig_environment",
            mode=StripMode.ENVIRONMENT,
            pattern=r'\\begin\{wrapfigure\}.*?\\end\{wrapfigure\}',
            description="Remove wrapfigure environments",
            preserve_content=True,
            preserve_newlines=False
        ))
        
        # Strip figure environments to basic form for style processing
        self.add_rule(StripRule(
            name="figure_environment_strip",
            mode=StripMode.ENVIRONMENT,
            pattern=r'\\begin\{figure[*]?\}(\[[^\]]*\])?',
            description="Strip figure positioning to bare minimum for style processing",
            preserve_content=True,
            preserve_newlines=False,
            custom_replacer=lambda m: "\\begin{figure}"
        ))
        
        self.add_rule(StripRule(
            name="figure_environment_end",
            mode=StripMode.COMMAND,
            pattern=r'\\end\{figure[*]?\}',
            description="Normalize figure environment endings",
            preserve_content=True,
            preserve_newlines=False,
            custom_replacer=lambda m: "\\end{figure}"
        ))
        
    def add_rule(self, rule: StripRule):
        """Add a custom stripping rule"""
        self.rules.append(rule)
        
    def remove_rule(self, rule_name: str):
        """Remove a stripping rule by name"""
        self.rules = [r for r in self.rules if r.name != rule_name]
        
    def strip_file(self, file_path: str, backup: bool = True, 
                   custom_rules: Optional[List[StripRule]] = None) -> StrippingResult:
        """
        Strip LaTeX constructs from a file
        
        Args:
            file_path: Path to the LaTeX file
            backup: Whether to create a backup before modification
            custom_rules: Optional custom rules to use instead of defaults
            
        Returns:
            StrippingResult with statistics about changes
        """
        path = Path(file_path)
        
        # Skip main document and preamble
        if path.name in ('main.tex', 'preamble.tex'):
            return StrippingResult(file_path)
            
        # Read file content
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
        except (IOError, OSError) as e:
            raise IOError(f"Could not read file {file_path}: {e}")
        
        # Determine which rules to use
        rules_to_use = custom_rules or self.rules
        if self.strip_mode == "auto":
            # Auto mode: use only environment-related rules for common issues
            rules_to_use = [r for r in rules_to_use if r.mode in [StripMode.ENVIRONMENT, StripMode.COMMAND]]
        
        # Create backup if requested and content will change
        backup_created = False
        if backup:
            backup_path = path.with_suffix(path.suffix + '.bak_strip')
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(content)
            backup_created = True
        
        # Apply stripping rules
        result = self._apply_stripping_rules(content, rules_to_use)
        
        # Write back if changes were made
        if result.content_changed:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(result.content)
        
        return result
        
    def _apply_stripping_rules(self, content: str, rules: List[StripRule]) -> StrippingResult:
        """Apply stripping rules to content"""
        result = StrippingResult(file_path="", content=content)
        result.content_changed = False
        result.total_stripped = 0
        
        for rule in rules:
            try:
                if isinstance(rule.pattern, str):
                    pattern = re.compile(rule.pattern, re.DOTALL)
                else:
                    pattern = rule.pattern
                
                matches = list(pattern.finditer(result.content))
                if not matches:
                    continue
                
                result.rules_applied[rule.name] = len(matches)
                result.total_stripped += len(matches)
                result.content_changed = True
                
                # Apply the rule
                if rule.custom_replacer:
                    # Use custom replacement function
                    result.content = pattern.sub(rule.custom_replacer, result.content)
                else:
                    # Standard replacement
                    if rule.preserve_content:
                        # Keep the content, remove the formatting
                        result.content = pattern.sub(r'\1', result.content)
                    else:
                        # Remove everything
                        result.content = pattern.sub('', result.content)
                
                # Clean up whitespace if requested
                if rule.preserve_newlines:
                    result.content = re.sub(r'\n\s*\n\s*\n', '\n\n', result.content)
                else:
                    result.content = re.sub(r'\n\s*\n\s*\n+', '\n\n', result.content)
                    
            except re.error as e:
                print(f"Warning: Regex error in rule {rule.name}: {e}")
                continue
            except Exception as e:
                print(f"Warning: Rule {rule.name} failed unexpectedly: {e}")
                continue
        
        return result
        
    def strip_all_tex_files(self, directory: str = '.', backup: bool = True,
                           custom_rules: Optional[List[StripRule]] = None) -> Dict[str, StrippingResult]:
        """
        Strip LaTeX constructs from all LaTeX files in directory
        
        Args:
            directory: Directory containing LaTeX files
            backup: Whether to create backups before modification
            custom_rules: Optional custom rules to use
            
        Returns:
            Dictionary mapping file paths to stripping results
        """
        results = {}
        tex_files = list(Path(directory).glob('*.tex'))
        
        for tex_file in tex_files:
            try:
                result = self.strip_file(str(tex_file), backup=backup, custom_rules=custom_rules)
                results[str(tex_file)] = result
            except IOError as e:
                print(f"Warning: Could not strip {tex_file}: {e}")
                continue
            except Exception as e:
                print(f"Warning: An unexpected error occurred while stripping {tex_file}: {e}")
                continue
                
        return results
    
    def get_available_rules(self) -> List[StripRule]:
        """Get list of available stripping rules"""
        return self.rules.copy()


def create_multicolumn_only_stripper() -> LatexStripper:
    """Create a stripper focused only on multicolumn issues"""
    stripper = LatexStripper(strip_mode="auto")
    # Keep only multicolumn-related rules
    stripper.rules = [r for r in stripper.rules if "multicol" in r.name]
    return stripper


def create_aggressive_stripper() -> LatexStripper:
    """Create a stripper that removes all formatting"""
    stripper = LatexStripper(strip_mode="full")
    return stripper


def main():
    """Command-line interface for LaTeX stripping"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Strip unnecessary LaTeX environments and formatting')
    parser.add_argument('--dir', '-d', default='.', help='Directory containing LaTeX files')
    parser.add_argument('--mode', '-m', choices=['auto', 'full', 'custom'], default='auto',
                        help='Stripping mode: auto (common issues), full (all), or custom')
    parser.add_argument('--no-backup', action='store_true', help='Do not create backup files')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    parser.add_argument('--list-rules', action='store_true', help='List available stripping rules')
    
    args = parser.parse_args()
    
    if args.list_rules:
        stripper = LatexStripper(strip_mode="auto")
        print("Available stripping rules:")
        for rule in stripper.get_available_rules():
            print(f"  {rule.name}: {rule.description}")
        return
    
    # Create appropriate stripper
    if args.mode == "multicolumn":
        stripper = create_multicolumn_only_stripper()
    elif args.mode == "aggressive":
        stripper = create_aggressive_stripper()
    else:
        stripper = LatexStripper(strip_mode=args.mode)
    
    # Strip files
    results = stripper.strip_all_tex_files(args.dir, backup=not args.no_backup)
    
    total_stripped = 0
    files_changed = 0
    for file_path, result in results.items():
        if result.total_stripped > 0:
            total_stripped += result.total_stripped
            files_changed += 1
            if args.verbose:
                print(f"Stripped {result.total_stripped} constructs from {file_path}")
                for rule_name, count in result.rules_applied.items():
                    print(f"  - {rule_name}: {count} removed")
    
    print(f"Total constructs stripped: {total_stripped}")
    print(f"Files changed: {files_changed}/{len(results)}")


if __name__ == '__main__':
    main()