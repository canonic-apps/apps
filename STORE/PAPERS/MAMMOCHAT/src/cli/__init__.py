"""
CLI module for LaTeX publication pipeline.

This module provides the main command-line interface for the LaTeX
publication pipeline, organizing functionality by domain (bibliography,
citation management, LaTeX processing, etc.) rather than by technical
implementation details.

The CLI uses Click for command-line parsing and provides a hierarchical
command structure that maps directly to user workflows.
"""

import click
from pathlib import Path

from src.shared.config import get_config, apply_preset

# Import CLI modules
from . import comprehensive, tex, bib, cite, style, config


@click.group(context_settings={"help_option_names": ["-h", "--help"]})
@click.option('--config', type=Path, help='Configuration file path')
@click.option('--verbose', is_flag=True, help='Verbose output')
@click.pass_context
def main(ctx, config, verbose):
    """LaTeX Publication Pipeline - Domain-driven refactoring.
    
    This is the main entry point for the publication pipeline, providing
    access to all domain-specific commands through a hierarchical CLI
    structure. The pipeline supports comprehensive LaTeX document processing
    including bibliography management, citation placement, style validation,
    and automated compilation.
    
    Args:
        ctx: Click context object for passing configuration
        config: Optional path to configuration file
        verbose: Enable verbose output for debugging
    """
    ctx.ensure_object(dict)
    ctx.obj['config'] = config
    ctx.obj['verbose'] = verbose


# Add subcommands
main.add_command(comprehensive.comprehensive)
main.add_command(tex.tex)
main.add_command(bib.bib)
main.add_command(cite.cite)
main.add_command(style.style)
main.add_command(config.config)