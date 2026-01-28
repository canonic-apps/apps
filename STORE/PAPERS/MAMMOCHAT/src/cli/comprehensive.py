"""
Comprehensive pipeline command
"""

import click
import glob
import sys
from pathlib import Path

from src.bib.llm_enhancer import LLMAuthorBiasEnhancer
from src.doc.pipeline import ComprehensivePipeline
from src.shared.config import get_config


@click.command()
@click.option('--bib', default='refs.bib', help='Bibliography file path')
@click.option('--dry-run', is_flag=True, help='Show what would be done without making changes')
@click.option('--email', default='hadley@stanford.edu', help='Email for API access')
@click.option('--skip-citations', is_flag=True, help='Skip citation consolidation')
@click.option('--llm-enhance', is_flag=True, help='Apply LLM abstract-based enhancement')
@click.option('--author-bias', is_flag=True, help='Apply author bias for featured authors')
@click.option('--openai-key', help='OpenAI API key for LLM enhancement (legacy)')
@click.option('--deepseek-key', help='DeepSeek API key for LLM enhancement')
@click.option('--llm-provider', type=click.Choice(['deepseek', 'openai']),
              help='LLM provider to use (default: deepseek)')
@click.option('--fast', is_flag=True, help='Fast mode: run latexmk compilation only')
@click.pass_context
def comprehensive(ctx, bib, dry_run, email, skip_citations, llm_enhance, author_bias,
                 openai_key, deepseek_key, llm_provider, fast):
    """Run comprehensive document processing pipeline"""
    print("=" * 60)
    print("COMPREHENSIVE DOCUMENT PIPELINE")
    print("=" * 60)

    bib_path = Path(bib)
    if not bib_path.exists():
        print(f"Error: Bibliography file {bib} not found")
        sys.exit(1)

    # Fast mode: just run latexmk compilation
    if fast:
        import subprocess
        print("Fast mode: Running latexmk compilation only")
        subprocess.run(['latexmk', '-pdf', 'main.tex'], cwd='tex')
        return

    pipeline = ComprehensivePipeline(email=email, dry_run=dry_run)
    pipeline.run(bib_path, clean_citations=not skip_citations)

    # Apply LLM enhancement if requested
    if llm_enhance:
        print("Applying LLM abstract-based enhancement...")

        # Get LLM configuration - fail fast if provider not properly configured
        config = get_config()
        deepseek_key = deepseek_key or config.get('api.deepseek_api_key')
        openai_key = openai_key or config.get('api.openai_api_key')
        llm_provider = llm_provider or config.get('api.llm_provider', 'deepseek')

        # Fail fast if LLM provider not configured
        if llm_provider == 'deepseek' and not deepseek_key:
            print("Error: DeepSeek provider selected but no DEEPSEEK_API_KEY found")
            sys.exit(1)
        elif llm_provider == 'openai' and not openai_key:
            print("Error: OpenAI provider selected but no OPENAI_API_KEY found")
            sys.exit(1)

        enhancer = LLMAuthorBiasEnhancer(
            bib_path=bib,
            similarity_threshold=0.12,
            openai_api_key=openai_key if llm_provider == 'openai' else None,
            deepseek_api_key=deepseek_key if llm_provider == 'deepseek' else None,
            use_llm=True,
            llm_provider=llm_provider
        )

        # Auto-detect .tex files
        tex_files = list(Path('.').glob('*.tex'))
        tex_files = [str(f) for f in tex_files if f.name not in ('main.tex', 'preamble.tex')]

        # Strip abstract citations first, then apply with or without author bias
        print("Stripping citations of abstract entries...")
        enhancer.strip_abstract_citations(tex_files)

        if author_bias:
            print("Applying author-biased citations...")
            enhancer.apply_all_with_author_bias(tex_files)
        else:
            print("Applying standard citations...")
            enhancer.apply_all(tex_files)

    print("Comprehensive pipeline completed")