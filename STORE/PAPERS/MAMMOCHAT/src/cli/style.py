"""
Style standardization and validation commands
"""

import click
import glob
import subprocess
import sys
from pathlib import Path


@click.group()
def style():
    """Style standardization and validation commands"""
    pass


@style.command()
@click.option('--tex-files', help='LaTeX files to validate (glob pattern)')
@click.option('--preamble', help='Preamble file to validate')
@click.option('--output', help='Output report file (JSON format)')
@click.option('--fail-on-errors', is_flag=True, help='Exit with error code if validation errors found')
@click.pass_context
def validate(ctx, tex_files, preamble, output, fail_on_errors):
    """Comprehensive style validation for LaTeX documents"""
    from tex.validator import ComprehensiveStyleValidator

    # Determine files to validate
    if tex_files:
        files = glob.glob(tex_files)
    else:
        files = list(Path('.').glob('*.tex'))
        # Filter out main files
        files = [f for f in files if f.name not in ('main.tex', 'main.bbl', 'main.bcf')]

    if preamble:
        files = [f for f in files if f.name != 'preamble.tex']
        if Path(preamble).exists():
            files.insert(0, preamble)
        else:
            print(f"Warning: Preamble file {preamble} not found")

    if not files:
        print("No LaTeX files found to validate")
        return

    print(f"Validating {len(files)} files with comprehensive style validation...")

    # Use comprehensive validator
    validator = ComprehensiveStyleValidator()

    # Generate report
    if output:
        report = validator.generate_report([str(f) for f in files], output)
    else:
        report = validator.generate_report([str(f) for f in files])

    # Display summary
    summary = report['summary']
    print(f"Validation complete:")
    print(f"  Files processed: {summary['files_processed']}")
    print(f"  Total issues: {summary['total_issues']}")
    print(f"  Errors: {summary['errors']}")
    print(f"  Warnings: {summary['warnings']}")
    print(f"  Info: {summary['info']}")

    if output:
        print(f"  Detailed report saved to: {output}")

    # Show critical issues if verbose
    if ctx.obj['verbose']:
        print(f"\nDetailed issues by file:")
        for file_path, issues in report['issues_by_file'].items():
            if issues:
                print(f"\n{file_path}: {len(issues)} issues")
                for issue in issues[:3]:  # Show first 3 issues per file
                    severity_emoji = "❌" if issue['severity'] == 'error' else "⚠️" if issue['severity'] == 'warning' else "ℹ️"
                    print(f"  {severity_emoji} Line {issue['line']}: {issue['message']}")
                if len(issues) > 3:
                    print(f"  ... and {len(issues) - 3} more issues")

    if fail_on_errors and summary['errors'] > 0:
        print(f"\nValidation failed with {summary['errors']} errors")
        sys.exit(1)


@style.command()
@click.option('--chapters', type=str, help='Chapter files to process (space-separated glob patterns like "0*.tex")')
@click.option('--files', type=str, help='Specific LaTeX files to process (space-separated)')
@click.option('--all', is_flag=True, help='Apply all style standardizations')
@click.option('--section-headings', is_flag=True, help='Apply section heading standardization')
@click.option('--citations', is_flag=True, help='Apply citation standardization')
@click.option('--technical-terms', is_flag=True, help='Apply technical term standardization')
@click.option('--numbers', is_flag=True, help='Apply number formatting standardization')
@click.option('--math-expressions', is_flag=True, help='Apply mathematical expression standardization')
@click.option('--figures-tables', is_flag=True, help='Apply figure and table formatting')
@click.option('--code-blocks', is_flag=True, help='Apply code block formatting')
@click.option('--validate', is_flag=True, help='Run validation after standardization')
@click.option('--output-report', help='Output JSON report to file')
@click.option('--dry-run', is_flag=True, help='Show what would be changed without making changes')
@click.pass_context
def standardize(ctx, chapters, files, all, section_headings, citations, technical_terms, numbers, math_expressions, figures_tables, code_blocks, validate, output_report, dry_run):
    """Apply style standardization using the style standardization CLI"""

    # Build command arguments
    cmd_args = ['python3', '-m', 'src.bib.cmd_standardize']

    if chapters:
        # Split chapters by spaces to handle multiple patterns
        chapter_list = chapters.split()
        cmd_args.extend(['--chapters'] + chapter_list)
    elif files:
        # Split files by spaces to handle multiple files
        file_list = files.split()
        cmd_args.extend(['--files'] + file_list)
    else:
        print("Error: Must specify either --chapters or --files")
        sys.exit(1)

    if all:
        cmd_args.append('--all')
    else:
        if section_headings:
            cmd_args.append('--section-headings')
        if citations:
            cmd_args.append('--citations')
        if technical_terms:
            cmd_args.append('--technical-terms')
        if numbers:
            cmd_args.append('--numbers')
        if math_expressions:
            cmd_args.append('--math-expressions')
        if figures_tables:
            cmd_args.append('--figures-tables')
        if code_blocks:
            cmd_args.append('--code-blocks')

        # If no specific flags, apply all by default
        if not any([section_headings, citations, technical_terms, numbers, math_expressions, figures_tables, code_blocks]):
            cmd_args.append('--all')

    if validate:
        cmd_args.append('--validate')
    if output_report:
        cmd_args.extend(['--output-report', output_report])
    if dry_run:
        cmd_args.append('--dry-run')
    if ctx.obj['verbose']:
        cmd_args.append('--verbose')

    print(f"Running style standardization: {' '.join(cmd_args)}")

    try:
        result = subprocess.run(cmd_args, capture_output=True, text=True)
        if result.returncode == 0:
            print("Style standardization completed successfully!")
            if ctx.obj['verbose'] and result.stdout:
                print(result.stdout)
        else:
            print("Style standardization failed!")
            if result.stderr:
                print("STDERR:", result.stderr)
            if result.stdout:
                print("STDOUT:", result.stdout)
            sys.exit(1)
    except Exception as e:
        print(f"Error running style standardization: {e}")
@style.command()
@click.option('--tex-dir', default='tex', help='Directory containing LaTeX files')
@click.option('--backup/--no-backup', default=True, help='Create backup files before changes')
@click.option('--validate/--no-validate', default=True, help='Validate style consistency after changes')
@click.option('--output-report', help='Output JSON report to file')
@click.pass_context
def apply_standardization(ctx, tex_dir, backup, validate, output_report):
    """Apply standardized LaTeX styling to all documents"""
    from tex.style_manager import LatexStyleManager
    
    tex_path = Path(tex_dir)
    if not tex_path.exists():
        print(f"Error: LaTeX directory {tex_dir} not found")
        sys.exit(1)
    
    print("=" * 60)
    print("STANDARDIZED LaTeX STYLE APPLICATION")
    print("=" * 60)
    
    # Initialize style manager
    manager = LatexStyleManager()
    
    # Remove unused styles.tex if it exists
    styles_file = tex_path / 'styles.tex'
    if styles_file.exists():
        print(f"Removing unused styles.tex")
        styles_file.unlink()
    
    # Apply styles to all .tex files
    print(f"Applying standardized styles to {tex_dir}/*.tex files...")
    results = manager.apply_styles_to_tex_files(tex_path, backup=backup)
    
    total_changes = 0
    files_changed = 0
    
    for file_path, changes in results.items():
        if changes > 0:
            files_changed += 1
            total_changes += changes
            if ctx.obj['verbose']:
                print(f"  {file_path}: {changes} changes")
    
    print(f"Style standardization complete:")
    print(f"  Files processed: {len(results)}")
    print(f"  Files changed: {files_changed}")
    print(f"  Total changes: {total_changes}")
    
    # Validate style consistency
    if validate:
        print("\nValidating style consistency...")
        issues = manager.validate_style_consistency(tex_path)
        
        if issues:
            print(f"Found style consistency issues in {len(issues)} files:")
            for file_path, file_issues in issues.items():
                print(f"  {file_path}:")
                for issue in file_issues:
                    print(f"    - {issue}")
        else:
            print("✓ All files pass style consistency validation")
    
    # Generate report if requested
    if output_report:
        import json
        report = {
            'summary': {
                'files_processed': len(results),
                'files_changed': files_changed,
                'total_changes': total_changes
            },
            'file_results': results,
            'style_issues': issues if validate else {}
        }
        
        with open(output_report, 'w') as f:
            json.dump(report, f, indent=2)
        print(f"  Report saved to: {output_report}")
    
    print("Style standardization completed successfully!")


@style.command()
@click.option('--output', help='Output file for generated styles (default: tex/preamble_styles.tex)')
@click.option('--brand', type=click.Choice(['mammochat', 'custom']), default='mammochat', help='Brand configuration to use')
def generate_styles(output, brand):
    """Generate standardized style definitions"""
    from tex.style_manager import LatexStyleManager
    
    if not output:
        output = 'tex/preamble_styles.tex'
    
    print(f"Generating standardized styles for {brand} brand...")
    
    manager = LatexStyleManager()
    styles = manager.generate_preamble_styles()
    
    # Write to file
    with open(output, 'w') as f:
        f.write(f"% Generated style definitions for {brand} brand\n")
        f.write(f"% Generated on: {subprocess.run(['date'], capture_output=True, text=True).stdout.strip()}\n")
        f.write("\n")
        f.write(styles)
    
    print(f"Generated styles written to: {output}")
    print(f"To use these styles, add to your preamble:")
    print(f"  \\input{{{Path(output).name}}}")


@style.command()
@click.option('--tex-dir', default='tex', help='Directory containing LaTeX files')
@click.option('--output', help='Output file for report (default: style_report.json)')
@click.option('--fail-on-issues', is_flag=True, help='Exit with error code if issues found')
def check_consistency(tex_dir, output, fail_on_issues):
    """Check style consistency across all LaTeX files"""
    from tex.style_manager import LatexStyleManager
    
    tex_path = Path(tex_dir)
    if not tex_path.exists():
        print(f"Error: LaTeX directory {tex_dir} not found")
        sys.exit(1)
    
    print("Checking style consistency...")
    
    manager = LatexStyleManager()
    issues = manager.validate_style_consistency(tex_path)
    
    if issues:
        print(f"\nFound style consistency issues in {len(issues)} files:")
        total_issues = 0
        for file_path, file_issues in issues.items():
            print(f"\n{file_path}:")
            for issue in file_issues:
                print(f"  ❌ {issue}")
                total_issues += 1
        
        print(f"\nTotal issues found: {total_issues}")
        
        if fail_on_issues:
            sys.exit(1)
    else:
        print("✓ All files pass style consistency validation")
    
    # Save report if requested
    if output:
        import json
        with open(output, 'w') as f:
            json.dump({
                'tex_directory': str(tex_path),
                'issues_found': bool(issues),
                'total_files_checked': len(list(tex_path.glob('*.tex'))),
                'files_with_issues': list(issues.keys()),
                'issues_by_file': issues
            }, f, indent=2)
        print(f"  Report saved to: {output}")
        sys.exit(1)