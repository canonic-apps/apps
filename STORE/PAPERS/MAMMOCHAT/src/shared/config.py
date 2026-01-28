"""
Configuration management for the LaTeX publication pipeline

This module provides centralized configuration management across all domains.
"""

import os
import json
import yaml
from pathlib import Path
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field, asdict
from .models import CitationStyle, DocumentType

# Add .env file support
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # python-dotenv is optional - warn if not available
    pass

@dataclass
class APIConfig:
    """API configuration for external services"""
    email: str = "hadley@stanford.edu"
    rate_limit: float = 0.34
    max_retries: int = 3
    timeout: int = 10
    
    # LLM provider settings
    llm_provider: str = "deepseek"  # "openai", "deepseek", or "anthropic"
    deepseek_api_key: Optional[str] = None
    deepseek_base_url: str = "https://api.deepseek.com"
    deepseek_model: str = "deepseek-chat"
    
    # Legacy API keys (for backward compatibility)
    openai_api_key: Optional[str] = None
    semantic_scholar_key: Optional[str] = None


@dataclass
class ProcessingConfig:
    """Document processing configuration"""
    similarity_threshold: float = 0.12
    tfidf_max_features: int = 1000
    forward_scan_limit: int = 5
    min_alpha_chars: int = 20
    
    # Citation settings
    consolidate_citations: bool = True
    remove_duplicate_keys: bool = True
    use_llm_placement: bool = False
    preserve_typography: bool = True
    aggressive_unicode: bool = False


@dataclass
class ValidationConfig:
    """Document validation configuration"""
    check_moving_arguments: bool = True
    check_citation_consolidation: bool = True
    check_typography: bool = True
    check_special_characters: bool = True
    check_pdf_strings: bool = True
    check_floating_citations: bool = True
    
    # Severity thresholds
    max_errors: int = 0  # Fail if more than this many errors
    max_warnings: int = 100  # Warn if more than this many warnings


@dataclass
class FileConfig:
    """File and path configuration"""
    # Default file paths
    bibliography_file: str = "refs.bib"
    main_tex_file: str = "main.tex"
    preamble_file: str = "preamble.tex"
    
    # Backup configuration
    create_backups: bool = True
    backup_suffix: str = ".bak"
    
    # Output directories
    output_dir: Optional[Path] = None
    cache_dir: Optional[Path] = None
    log_dir: Optional[Path] = None


@dataclass
class PipelineConfig:
    """Pipeline execution configuration"""
    # Pipeline steps
    fix_bibtex: bool = True
    enhance_metadata: bool = True
    clean_unicode: bool = True
    consolidate_citations: bool = True
    validate_documents: bool = True
    compile_pdf: bool = True
    
    # Error handling
    continue_on_error: bool = False
    stop_on_validation_error: bool = True
    
    # Output options
    verbose: bool = False
    dry_run: bool = False
    progress_bar: bool = True


class Config:
    """Main configuration class"""
    
    def __init__(self, config_file: Optional[Path] = None):
        self.api = APIConfig()
        self.processing = ProcessingConfig()
        self.validation = ValidationConfig()
        self.files = FileConfig()
        self.pipeline = PipelineConfig()
        
        # Load configuration if provided
        if config_file and config_file.exists():
            self.load_from_file(config_file)
        
        # Load from environment variables
        self.load_from_env()
        
        # Set default paths
        self._set_default_paths()
    
    def load_from_file(self, config_file: Path):
        """Load configuration from file (JSON or YAML)"""
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                if config_file.suffix.lower() in ['.yml', '.yaml']:
                    data = yaml.safe_load(f)
                else:
                    data = json.load(f)
            
            self._apply_config_dict(data)
        except Exception as e:
            print(f"Warning: Could not load config from {config_file}: {e}")
    
    def load_from_env(self):
        """Load configuration from environment variables"""
        # API settings
        if os.getenv('PIPELINE_EMAIL'):
            self.api.email = os.getenv('PIPELINE_EMAIL')
        
        if os.getenv('PIPELINE_RATE_LIMIT'):
            self.api.rate_limit = float(os.getenv('PIPELINE_RATE_LIMIT'))
        
        # LLM provider settings
        if os.getenv('LLM_PROVIDER'):
            self.api.llm_provider = os.getenv('LLM_PROVIDER')
        
        if os.getenv('DEEPSEEK_API_KEY'):
            self.api.deepseek_api_key = os.getenv('DEEPSEEK_API_KEY')
        
        if os.getenv('DEEPSEEK_BASE_URL'):
            self.api.deepseek_base_url = os.getenv('DEEPSEEK_BASE_URL')
        
        if os.getenv('DEEPSEEK_MODEL'):
            self.api.deepseek_model = os.getenv('DEEPSEEK_MODEL')
        
        # Legacy API keys (for backward compatibility)
        if os.getenv('OPENAI_API_KEY'):
            self.api.openai_api_key = os.getenv('OPENAI_API_KEY')
        
        if os.getenv('SEMANTIC_SCHOLAR_KEY'):
            self.api.semantic_scholar_key = os.getenv('SEMANTIC_SCHOLAR_KEY')
        
        # Processing settings
        if os.getenv('SIMILARITY_THRESHOLD'):
            self.processing.similarity_threshold = float(os.getenv('SIMILARITY_THRESHOLD'))
        
        if os.getenv('USE_LLM_PLACEMENT'):
            self.processing.use_llm_placement = os.getenv('USE_LLM_PLACEMENT').lower() == 'true'
        
        # File settings
        if os.getenv('BIBLIOGRAPHY_FILE'):
            self.files.bibliography_file = os.getenv('BIBLIOGRAPHY_FILE')
        
        if os.getenv('MAIN_TEX_FILE'):
            self.files.main_tex_file = os.getenv('MAIN_TEX_FILE')
        
        # Pipeline settings
        if os.getenv('VERBOSE'):
            self.pipeline.verbose = os.getenv('VERBOSE').lower() == 'true'
        
        if os.getenv('DRY_RUN'):
            self.pipeline.dry_run = os.getenv('DRY_RUN').lower() == 'true'
        
        if os.getenv('CONTINUE_ON_ERROR'):
            self.pipeline.continue_on_error = os.getenv('CONTINUE_ON_ERROR').lower() == 'true'
    
    def _apply_config_dict(self, data: Dict[str, Any]):
        """Apply configuration from dictionary"""
        for section_name, section_data in data.items():
            if hasattr(self, section_name):
                section = getattr(self, section_name)
                if isinstance(section_data, dict):
                    for key, value in section_data.items():
                        if hasattr(section, key):
                            setattr(section, key, value)
    
    def _set_default_paths(self):
        """Set default file paths"""
        if not self.files.output_dir:
            self.files.output_dir = Path.cwd() / 'output'
        
        if not self.files.cache_dir:
            self.files.cache_dir = Path.cwd() / '.cache'
        
        if not self.files.log_dir:
            self.files.log_dir = Path.cwd() / 'logs'
    
    def save_to_file(self, config_file: Path):
        """Save current configuration to file"""
        config_dict = {
            'api': asdict(self.api),
            'processing': asdict(self.processing),
            'validation': asdict(self.validation),
            'files': asdict(self.files),
            'pipeline': asdict(self.pipeline)
        }
        
        config_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(config_file, 'w', encoding='utf-8') as f:
            if config_file.suffix.lower() in ['.yml', '.yaml']:
                yaml.dump(config_dict, f, default_flow_style=False, indent=2)
            else:
                json.dump(config_dict, f, indent=2)
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value using dot notation (e.g., 'api.email')"""
        keys = key.split('.')
        value = self
        
        for k in keys:
            if hasattr(value, k):
                value = getattr(value, k)
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any):
        """Set configuration value using dot notation"""
        keys = key.split('.')
        obj = self
        
        for k in keys[:-1]:
            if hasattr(obj, k):
                obj = getattr(obj, k)
            else:
                setattr(obj, k, type('Config', (), {})())
                obj = getattr(obj, k)
        
        setattr(obj, keys[-1], value)
    
    def validate(self) -> List[str]:
        """Validate configuration and return list of errors"""
        errors = []
        
        # Validate API configuration
        if not self.api.email or '@' not in self.api.email:
            errors.append("API email is required and must be valid")
        
        if self.api.rate_limit < 0.1:
            errors.append("API rate limit should be at least 0.1 seconds")
        
        if self.api.timeout < 5:
            errors.append("API timeout should be at least 5 seconds")
        
        # Validate processing configuration
        if not 0 <= self.processing.similarity_threshold <= 1:
            errors.append("Similarity threshold must be between 0 and 1")
        
        if self.processing.tfidf_max_features < 100:
            errors.append("TF-IDF max features should be at least 100")
        
        # Validate file configuration
        if not self.files.bibliography_file:
            errors.append("Bibliography file path is required")
        
        if not self.files.main_tex_file:
            errors.append("Main TeX file path is required")
        
        # Validate pipeline configuration
        if self.validation.max_errors < 0:
            errors.append("Maximum errors must be non-negative")
        
        if self.validation.max_warnings < 0:
            errors.append("Maximum warnings must be non-negative")
        
        return errors
    
    def create_default_config_file(self, path: Path):
        """Create a default configuration file"""
        config = {
            'api': {
                'email': 'hadley@stanford.edu',
                'rate_limit': 0.34,
                'max_retries': 3,
                'timeout': 10,
                'llm_provider': 'deepseek',
                'deepseek_api_key': None,
                'deepseek_base_url': 'https://api.deepseek.com',
                'deepseek_model': 'deepseek-chat',
                'openai_api_key': None
            },
            'processing': {
                'similarity_threshold': 0.12,
                'tfidf_max_features': 1000,
                'forward_scan_limit': 5,
                'min_alpha_chars': 20,
                'consolidate_citations': True,
                'remove_duplicate_keys': True,
                'use_llm_placement': False,
                'preserve_typography': True,
                'aggressive_unicode': False
            },
            'validation': {
                'check_moving_arguments': True,
                'check_citation_consolidation': True,
                'check_typography': True,
                'check_special_characters': True,
                'check_pdf_strings': True,
                'check_floating_citations': True,
                'max_errors': 0,
                'max_warnings': 100
            },
            'files': {
                'bibliography_file': 'refs.bib',
                'main_tex_file': 'main.tex',
                'preamble_file': 'preamble.tex',
                'create_backups': True,
                'backup_suffix': '.bak',
                'output_dir': None,
                'cache_dir': None,
                'log_dir': None
            },
            'pipeline': {
                'fix_bibtex': True,
                'enhance_metadata': True,
                'clean_unicode': True,
                'consolidate_citations': True,
                'validate_documents': True,
                'compile_pdf': True,
                'continue_on_error': False,
                'stop_on_validation_error': True,
                'verbose': False,
                'dry_run': False,
                'progress_bar': True
            }
        }
        
        with open(path, 'w', encoding='utf-8') as f:
            if path.suffix.lower() in ['.yml', '.yaml']:
                yaml.dump(config, f, default_flow_style=False, indent=2)
            else:
                json.dump(config, f, indent=2)


# Global configuration instance
_config_instance: Optional[Config] = None


def get_config() -> Config:
    """Get global configuration instance"""
    global _config_instance
    if _config_instance is None:
        _config_instance = Config()
    return _config_instance


def set_config(config: Config):
    """Set global configuration instance"""
    global _config_instance
    _config_instance = config


# Default configuration presets
PRESETS = {
    'development': {
        'api': {'rate_limit': 1.0},
        'processing': {'similarity_threshold': 0.05, 'use_llm_placement': True},
        'pipeline': {'verbose': True, 'dry_run': True}
    },
    'production': {
        'api': {'rate_limit': 0.1, 'max_retries': 5},
        'processing': {'similarity_threshold': 0.2},
        'pipeline': {'verbose': False, 'dry_run': False, 'continue_on_error': True}
    },
    'testing': {
        'api': {'rate_limit': 0.01, 'timeout': 30},
        'processing': {'similarity_threshold': 0.01},
        'pipeline': {'verbose': True, 'dry_run': True}
    }
}


def apply_preset(preset_name: str, config: Optional[Config] = None) -> Config:
    """Apply a configuration preset"""
    if config is None:
        config = get_config()
    
    if preset_name not in PRESETS:
        raise ValueError(f"Unknown preset: {preset_name}. Available: {list(PRESETS.keys())}")
    
    preset_data = PRESETS[preset_name]
    config._apply_config_dict(preset_data)
    
    return config