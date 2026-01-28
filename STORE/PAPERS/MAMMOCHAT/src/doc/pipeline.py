"""
Comprehensive Pipeline for document processing
"""

import sys
from pathlib import Path
from typing import List, Optional
from dataclasses import dataclass
from shared.config import get_config
from bib.processor import BibTeXFixer, BibTeXProcessor
from tex.unicode import UnicodeCleaner
from tex.validator import LatexValidator
from cite.consolidator import consolidate_all_tex_files
from cite.applier import InlineCitationApplier
from doc.metadata_fetcher import MetadataFetcher
from tex.stripper import LatexStripper, create_multicolumn_only_stripper


@dataclass
class ProcessingResult:
    """Result of a processing step"""
    step_name: str
    success: bool
    message: str
    details: Optional[dict] = None


class ComprehensivePipeline:
    """
    Comprehensive document processing pipeline that orchestrates all processing steps
    """
    
    def __init__(self, email: str = "hadley@stanford.edu", dry_run: bool = False):
        """
        Initialize the comprehensive pipeline
        
        Args:
            email: Email for API access
            dry_run: If True, don't make actual changes
        """
        self.email = email
        self.dry_run = dry_run
        self.config = get_config()
        self.results: List[ProcessingResult] = []
        
    def run(self, bib_path: Path, clean_citations: bool = True) -> None:
        """
        Run the complete comprehensive pipeline
        
        Args:
            bib_path: Path to the bibliography file
            clean_citations: Whether to clean and consolidate citations
        """
        self.bib_path = bib_path
        print(f"Starting comprehensive pipeline (dry_run={self.dry_run})")
        
        # Step 1: Fix BibTeX entries
        self._step_fix_bibtex(bib_path)
        
        # Step 2: Clean Unicode characters
        self._step_clean_unicode()
        
        # Step 3: Strip problematic LaTeX constructs
        self._step_strip_problematic_constructs()
        
        # Step 4: Process citations if requested
        if clean_citations:
            self._step_consolidate_citations()
            self._step_apply_inline_citations()
        
        # Step 5: Validate document
        self._step_validate()
        
        # Step 6: Compile document
        self._step_compile()
        
        # Print summary
        self._print_summary()
        
    def _step_fix_bibtex(self, bib_path: Path) -> None:
        """Step: Fix problematic BibTeX entries"""
        print("Step: Fix BibTeX entries")
        
        try:
            if self.dry_run:
                # For dry run, just check what would be fixed
                fixer = BibTeXFixer(str(bib_path))
                # Simulate fixing without actually making changes
                print(f"  [DRY RUN] Would fix BibTeX entries in {bib_path}")
                self.results.append(ProcessingResult(
                    step_name="fix_bibtex",
                    success=True,
                    message="BibTeX fixing (dry run)",
                    details={"dry_run": True}
                ))
            else:
                fixer = BibTeXFixer(str(bib_path))
                fixes = fixer.fix_all()
                total_fixes = sum(fixes.values())
                
                print(f"  Fixed {total_fixes} BibTeX issues")
                self.results.append(ProcessingResult(
                    step_name="fix_bibtex",
                    success=True,
                    message=f"Fixed {total_fixes} BibTeX issues",
                    details=fixes
                ))
                
        except Exception as e:
            error_msg = f"BibTeX fixing failed: {str(e)}"
            print(f"  ERROR: {error_msg}")
            self.results.append(ProcessingResult(
                step_name="fix_bibtex",
                success=False,
                message=error_msg
            ))
            if not self.dry_run:
                raise
    
    def _step_clean_unicode(self) -> None:
        """Step: Clean Unicode characters in LaTeX files"""
        print("Step: Clean Unicode characters")
        
        try:
            cleaner = UnicodeCleaner()
            tex_files = [f for f in Path('.').glob('*.tex') if f.name not in ('main.tex', 'preamble.tex')]
            
            total_changes = 0
            for tex_file in tex_files:
                if self.dry_run:
                    # For dry run, just count what would be cleaned
                    print(f"  [DRY RUN] Would clean Unicode in {tex_file.name}")
                else:
                    result = cleaner.clean_file(str(tex_file))
                    total_changes += result.num_changes
                    if result.num_changes > 0:
                        print(f"  Cleaned {tex_file.name}: {result.num_changes} changes")
            
            if not self.dry_run:
                print(f"  Total Unicode changes: {total_changes}")
            
            self.results.append(ProcessingResult(
                step_name="clean_unicode",
                success=True,
                message=f"Cleaned Unicode in {len(tex_files)} files",
                details={"files_processed": len(tex_files), "total_changes": total_changes, "dry_run": self.dry_run}
            ))
            
        except Exception as e:
            error_msg = f"Unicode cleaning failed: {str(e)}"
            print(f"  ERROR: {error_msg}")
            self.results.append(ProcessingResult(
                step_name="clean_unicode",
                success=False,
                message=error_msg
            ))
            if not self.dry_run:
                raise
    
    def _step_strip_problematic_constructs(self) -> None:
        """Step: Strip problematic LaTeX constructs (environments, formatting, etc.)"""
        print("Step: Strip problematic LaTeX constructs")
        
        try:
            if self.dry_run:
                print("  [DRY RUN] Would strip problematic LaTeX constructs")
                stripper = create_multicolumn_only_stripper()
                tex_files = list(Path('.').glob('*.tex'))
                tex_files = [str(f) for f in tex_files if f.name not in ('main.tex', 'preamble.tex')]
                results = {f: None for f in tex_files}
            else:
                stripper = create_multicolumn_only_stripper()
                results = stripper.strip_all_tex_files('.', backup=True)
            
            total_stripped = sum(r.total_stripped for r in results.values() if r)
            files_changed = sum(1 for r in results.values() if r and r.total_stripped > 0)
            
            print(f"  Total constructs stripped: {total_stripped}")
            print(f"  Files changed: {files_changed}")
            
            if not self.dry_run:
                # Show detailed changes
                for file_path, result in results.items():
                    if result and result.total_stripped > 0:
                        print(f"  Cleaned {Path(file_path).name}: {result.total_stripped} constructs removed")
                        for rule_name, count in result.rules_applied.items():
                            print(f"    - {rule_name}: {count} removed")
            
            self.results.append(ProcessingResult(
                step_name="strip_problematic_constructs",
                success=True,
                message=f"Stripped {total_stripped} constructs from {files_changed} files",
                details={"total_stripped": total_stripped, "files_changed": files_changed, "results": results, "dry_run": self.dry_run}
            ))
            
        except Exception as e:
            error_msg = f"LaTeX stripping failed: {str(e)}"
            print(f"  ERROR: {error_msg}")
            self.results.append(ProcessingResult(
                step_name="strip_problematic_constructs",
                success=False,
                message=error_msg
            ))
            if not self.dry_run:
                raise
    
    def _step_consolidate_citations(self) -> None:
        """Step: Consolidate duplicate citations"""
        print("Step: Consolidate citations")
        
        try:
            if self.dry_run:
                print("  [DRY RUN] Would consolidate citations")
                results = {'files_processed': 0, 'files_changed': 0, 'total_merges': 0}
            else:
                results = consolidate_all_tex_files()
                print(f"  Files processed: {results['files_processed']}")
                print(f"  Files changed: {results['files_changed']}")
                print(f"  Total merges: {results['total_merges']}")
            
            self.results.append(ProcessingResult(
                step_name="consolidate_citations",
                success=True,
                message=f"Citation consolidation complete",
                details=results
            ))
            
        except Exception as e:
            error_msg = f"Citation consolidation failed: {str(e)}"
            print(f"  ERROR: {error_msg}")
            self.results.append(ProcessingResult(
                step_name="consolidate_citations",
                success=False,
                message=error_msg
            ))
            if not self.dry_run:
                raise
    
    def _step_apply_inline_citations(self) -> None:
        """Step: Apply inline citations"""
        print("Step: Apply inline citations")
        
        try:
            if self.dry_run:
                print("  [DRY RUN] Would apply inline citations")
                total_applied = 0
                files_processed = 0
            else:
                applier = InlineCitationApplier(bib_path=str(self.bib_path), similarity_threshold=self.config.processing.similarity_threshold)
                tex_files = sorted(Path('.').glob('*.tex'))
                tex_files = [str(f) for f in tex_files if f.name not in ('main.tex', 'preamble.tex')]
                
                results = applier.apply_all(tex_files)
                total_applied = sum(r.applied for r in results if r)
                files_processed = len([r for r in results if r])
                
                print(f"  Applied {total_applied} citations in {files_processed} files")
            
            self.results.append(ProcessingResult(
                step_name="apply_inline_citations",
                success=True,
                message=f"Applied {total_applied} inline citations",
                details={"total_applied": total_applied, "files_processed": files_processed, "dry_run": self.dry_run}
            ))
            
        except Exception as e:
            error_msg = f"Inline citation application failed: {str(e)}"
            print(f"  ERROR: {error_msg}")
            self.results.append(ProcessingResult(
                step_name="apply_inline_citations",
                success=False,
                message=error_msg
            ))
            if not self.dry_run:
                raise
    
    def _step_validate(self) -> None:
        """Step: Validate LaTeX documents"""
        print("Step: Validate documents")
        
        try:
            validator = LatexValidator()
            tex_files = list(Path('.').glob('*.tex'))
            
            all_errors = []
            all_warnings = []
            
            for tex_file in tex_files:
                issues = validator.validate_file(str(tex_file))
                errors = [i for i in issues if i.severity == 'error']
                warnings = [i for i in issues if i.severity == 'warning']
                
                if errors:
                    all_errors.extend(errors)
                    print(f"  {tex_file.name}: {len(errors)} errors")
                    for error in errors:
                        print(f"    Line {error.line_number}: {error.message}")
                
                if warnings:
                    all_warnings.extend(warnings)
                    print(f"  {tex_file.name}: {len(warnings)} warnings")
            
            print(f"  Total errors: {len(all_errors)}")
            print(f"  Total warnings: {len(all_warnings)}")
            
            self.results.append(ProcessingResult(
                step_name="validate",
                success=True,
                message=f"Validation complete: {len(all_errors)} errors, {len(all_warnings)} warnings",
                details={"errors": len(all_errors), "warnings": len(all_warnings), "files_checked": len(tex_files)}
            ))
            
            # If there are errors and not in dry run, we might want to fail
            if all_errors and not self.dry_run:
                print("  WARNING: Validation errors found!")
                
        except Exception as e:
            error_msg = f"Validation failed: {str(e)}"
            print(f"  ERROR: {error_msg}")
            self.results.append(ProcessingResult(
                step_name="validate",
                success=False,
                message=error_msg
            ))
            if not self.dry_run:
                raise
    
    def _step_compile(self) -> None:
        """Step: Compile LaTeX document"""
        print("Step: Compile document")
        
        try:
            if self.dry_run:
                print("  [DRY RUN] Would compile main.tex")
            else:
                from tex.compiler import compile_latex_document
                compile_latex_document('tex/main.tex')
                print("  Successfully compiled main.tex")
            
            self.results.append(ProcessingResult(
                step_name="compile",
                success=True,
                message="Document compilation complete",
                details={"dry_run": self.dry_run}
            ))
            
        except Exception as e:
            error_msg = f"Compilation failed: {str(e)}"
            print(f"  ERROR: {error_msg}")
            self.results.append(ProcessingResult(
                step_name="compile",
                success=False,
                message=error_msg
            ))
            if not self.dry_run:
                raise
    
    def _print_summary(self) -> None:
        """Print a summary of all processing results"""
        print("\n" + "=" * 60)
        print("PIPELINE SUMMARY")
        print("=" * 60)
        
        successful_steps = [r for r in self.results if r.success]
        failed_steps = [r for r in self.results if not r.success]
        
        print(f"Steps completed: {len(successful_steps)}")
        print(f"Steps failed: {len(failed_steps)}")
        
        if failed_steps:
            print("\nFailed steps:")
            for result in failed_steps:
                print(f"  - {result.step_name}: {result.message}")
        
        print(f"\nPipeline {'completed successfully' if not failed_steps else 'completed with failures'}")