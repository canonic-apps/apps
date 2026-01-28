"""
Configuration management command
"""

import click
from pathlib import Path


@click.command()
@click.option('--preset', type=click.Choice(['development', 'production', 'testing']), help='Configuration preset to apply')
@click.option('--create-config', type=Path, help='Create default config file')
@click.pass_context
def config(ctx, preset, create_config):
    """Configuration management"""
    from shared.config import get_config, apply_preset, PRESETS

    if create_config:
        config = get_config()
        config.create_default_config_file(create_config)
        print(f"Default configuration created: {create_config}")
        return

    config = get_config()

    if preset:
        apply_preset(preset, config)
        print(f"Applied {preset} preset")

    if ctx.obj['verbose']:
        print("Current configuration:")
        print(f"  API rate limit: {config.api.rate_limit}s")
        print(f"  Similarity threshold: {config.processing.similarity_threshold}")
        print(f"  Bibliography file: {config.files.bibliography_file}")
        print(f"  LLM placement: {config.processing.use_llm_placement}")
        print(f"  Verbose: {config.pipeline.verbose}")