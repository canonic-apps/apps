import bibtexparser
from bibtexparser.bparser import BibTexParser
from bibtexparser.bwriter import BibTexWriter
from bibtexparser.bibdatabase import BibDatabase
import re
from typing import Dict, List, Set, Optional, Tuple
from collections import defaultdict
from pathlib import Path


class BibTeXProcessor:
    def __init__(self, bib_path: str = 'refs.bib'):
        self.bib_path = bib_path
        self.database = None
        self.parser = BibTexParser(common_strings=True)
        self.parser.ignore_nonstandard_types = False
        self.parser.homogenize_fields = False
    
    def load(self) -> BibDatabase:
        """Load bibliography file.

        Returns:
            BibDatabase: Parsed bibliography database

        Raises:
            FileNotFoundError: If bibliography file doesn't exist
            UnicodeDecodeError: If file has encoding issues
            ValueError: If BibTeX parsing fails
        """
        try:
            with open(self.bib_path, 'r', encoding='utf-8') as f:
                self.database = bibtexparser.load(f, self.parser)
        except FileNotFoundError:
            raise FileNotFoundError(f"Bibliography file not found: {self.bib_path}")
        except UnicodeDecodeError as e:
            raise UnicodeDecodeError(
                e.encoding, e.object, e.start, e.end,
                f"Encoding error in {self.bib_path}: {e.reason}"
            )
        except Exception as e:
            raise ValueError(f"Failed to parse BibTeX file {self.bib_path}: {e}")

        return self.database
    
    def save(self, output_path: Optional[str] = None, backup: bool = True):
        if not self.database:
            raise ValueError("No database loaded")
        
        output_path = output_path or self.bib_path
        
        if backup and output_path == self.bib_path:
            backup_path = f"{self.bib_path}.bak"
            with open(self.bib_path, 'r', encoding='utf-8') as f:
                with open(backup_path, 'w', encoding='utf-8') as b:
                    b.write(f.read())
        
        writer = BibTexWriter()
        writer.indent = '  '
        writer.order_entries_by = None
        
        with open(output_path, 'w', encoding='utf-8') as f:
            bibtexparser.dump(self.database, f, writer)
    
    def normalize_keys(self, to_lowercase: bool = True) -> Dict[str, str]:
        if not self.database:
            self.load()
        
        key_map = {}
        
        for entry in self.database.entries:
            old_key = entry['ID']
            new_key = old_key
            
            if to_lowercase:
                new_key = new_key.lower()
            
            new_key = re.sub(r'[^a-zA-Z0-9_-]', '', new_key)
            
            if new_key != old_key:
                entry['ID'] = new_key
                key_map[old_key] = new_key
        
        return key_map
    
    def find_duplicates(self) -> Dict[str, List[str]]:
        if not self.database:
            self.load()
        
        doi_map = defaultdict(list)
        pmid_map = defaultdict(list)
        title_map = defaultdict(list)
        
        for entry in self.database.entries:
            entry_id = entry['ID']
            
            doi = entry.get('doi') or entry.get('DOI')
            if doi:
                doi_clean = doi.lower().strip()
                doi_map[doi_clean].append(entry_id)
            
            pmid = entry.get('pmid') or entry.get('PMID')
            if pmid:
                pmid_map[pmid].append(entry_id)
            
            title = entry.get('title', '')
            if title:
                title_norm = re.sub(r'[^a-z0-9]', '', title.lower())
                if len(title_norm) > 10:
                    title_map[title_norm].append(entry_id)
        
        duplicates = {}
        
        for doi, entries in doi_map.items():
            if len(entries) > 1:
                duplicates[f"DOI:{doi}"] = entries
        
        for pmid, entries in pmid_map.items():
            if len(entries) > 1:
                duplicates[f"PMID:{pmid}"] = entries
        
        for title, entries in title_map.items():
            if len(entries) > 1:
                key = f"Title:{title[:30]}"
                if key not in duplicates:
                    duplicates[key] = entries
        
        return duplicates
    
    def remove_entries(self, keys_to_remove: Set[str]) -> int:
        if not self.database:
            self.load()
        
        original_count = len(self.database.entries)
        self.database.entries = [
            entry for entry in self.database.entries
            if entry['ID'] not in keys_to_remove
        ]
        return original_count - len(self.database.entries)
    
    def add_metadata(self, entry_id: str, metadata: Dict) -> bool:
        if not self.database:
            self.load()
        
        for entry in self.database.entries:
            if entry['ID'] == entry_id:
                for field, value in metadata.items():
                    if value:
                        entry[field] = value
                return True
        
        return False
    
    def extract_cited_keys_from_tex(self, tex_files: List[str]) -> Set[str]:
        cited = set()
        
        cite_pattern = r'\\(?:auto)?cite(?:\*|\w*)\{([^}]+)\}'
        
        for tex_file in tex_files:
            with open(tex_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            matches = re.findall(cite_pattern, content)
            for match in matches:
                keys = [k.strip() for k in match.split(',')]
                cited.update(keys)
        
        return cited
    
    def find_uncited_entries(self, tex_files: List[str]) -> Set[str]:
        if not self.database:
            self.load()
        
        all_keys = {entry['ID'] for entry in self.database.entries}
        cited_keys = self.extract_cited_keys_from_tex(tex_files)
        
        return all_keys - cited_keys
    
    def validate_syntax(self) -> List[Dict]:
        if not self.database:
            self.load()
        
        errors = []
        
        for entry in self.database.entries:
            entry_id = entry['ID']
            entry_type = entry['ENTRYTYPE']
            
            required_fields = self._get_required_fields(entry_type)
            missing_fields = [f for f in required_fields if f not in entry]
            
            if missing_fields:
                errors.append({
                    'entry': entry_id,
                    'type': 'missing_required_fields',
                    'fields': missing_fields
                })
            
            for field, value in entry.items():
                if field in ['ID', 'ENTRYTYPE']:
                    continue
                
                value_str = str(value)
                if value_str.count('{') != value_str.count('}'):
                    errors.append({
                        'entry': entry_id,
                        'type': 'unbalanced_braces',
                        'field': field
                    })
            
            if not re.match(r'^[a-zA-Z0-9_-]+$', entry_id):
                errors.append({
                    'entry': entry_id,
                    'type': 'invalid_key_format',
                    'message': 'Key contains invalid characters'
                })
        
        return errors
    
    def _get_required_fields(self, entry_type: str) -> List[str]:
        required = {
            'article': ['author', 'title', 'journal', 'year'],
            'book': ['author', 'title', 'publisher', 'year'],
            'inproceedings': ['author', 'title', 'booktitle', 'year'],
            'phdthesis': ['author', 'title', 'school', 'year'],
            'mastersthesis': ['author', 'title', 'school', 'year'],
            'techreport': ['author', 'title', 'institution', 'year'],
            'misc': ['title'],
        }
        
        return required.get(entry_type.lower(), [])
    
    def get_statistics(self) -> Dict:
        if not self.database:
            self.load()
        
        stats = {
            'total_entries': len(self.database.entries),
            'entry_types': defaultdict(int),
            'entries_with_doi': 0,
            'entries_with_pmid': 0,
            'entries_with_abstract': 0,
            'entries_with_url': 0,
        }
        
        for entry in self.database.entries:
            stats['entry_types'][entry['ENTRYTYPE']] += 1
            
            if entry.get('doi') or entry.get('DOI'):
                stats['entries_with_doi'] += 1
            
            if entry.get('pmid') or entry.get('PMID'):
                stats['entries_with_pmid'] += 1
            
            if entry.get('abstract'):
                stats['entries_with_abstract'] += 1
            
            if entry.get('url'):
                stats['entries_with_url'] += 1
        
        return dict(stats)


class BibTeXFixer:
    def __init__(self, refs_path: str = 'refs.bib', preamble_path: str = 'preamble.tex'):
        self.refs_path = refs_path
        self.preamble_path = preamble_path
        self.standard_abstract = "This study examines key aspects of precision medicine and health informatics."
        self.max_abstract_length = 2000
        self.invalid_isbn_patterns = [r'\r', r'\n', r'\d{4}-\d{4}', r'.*\(Electronic\).*\(Linking\)']
    
    def fix_all(self) -> Dict[str, int]:
        fixes = {
            'invalid_isbn_removed': 0,
            'long_abstracts_replaced': 0,
            'control_chars_removed': 0,
            'preamble_autocites_removed': 0,
        }
        
        with open(self.refs_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        content, fixes['invalid_isbn_removed'] = self._remove_invalid_isbn(content)
        content, fixes['long_abstracts_replaced'] = self._fix_long_abstracts(content)
        content, fixes['control_chars_removed'] = self._remove_control_chars(content)
        
        if content != original_content:
            with open(self.refs_path, 'w', encoding='utf-8') as f:
                f.write(content)
        
        if Path(self.preamble_path).exists():
            with open(self.preamble_path, 'r', encoding='utf-8') as f:
                preamble = f.read()
            
            original_preamble = preamble
            preamble, fixes['preamble_autocites_removed'] = self._remove_comment_autocites(preamble)
            
            if preamble != original_preamble:
                with open(self.preamble_path, 'w', encoding='utf-8') as f:
                    f.write(preamble)
        
        return fixes
    
    def _remove_invalid_isbn(self, content: str) -> Tuple[str, int]:
        removed = 0
        isbn_pattern = r'(\s+isbn\s*=\s*\{[^}]+\},?\s*\n)'
        
        matches = list(re.finditer(isbn_pattern, content, re.IGNORECASE))
        
        for match in reversed(matches):
            isbn_value = match.group(1)
            
            is_invalid = False
            for invalid_pattern in self.invalid_isbn_patterns:
                if re.search(invalid_pattern, isbn_value):
                    is_invalid = True
                    break
            
            if is_invalid:
                content = content[:match.start()] + content[match.end():]
                removed += 1
        
        return content, removed
    
    def _fix_long_abstracts(self, content: str) -> Tuple[str, int]:
        replaced = 0
        abstract_pattern = r'(@\w+\{[^,]+,\s*abstract\s*=\s*\{)([^}]+)(},)'
        
        def replace_if_problematic(match):
            nonlocal replaced
            prefix = match.group(1)
            abstract_content = match.group(2)
            suffix = match.group(3)
            
            is_problematic = False
            
            if len(abstract_content) > self.max_abstract_length:
                is_problematic = True
            
            if re.search(r'\n\s+\n\s+(Study Design|Objective|Methods|Results|Conclusion)\.', abstract_content):
                is_problematic = True
            
            if re.search(r'R\s+2=', abstract_content):
                is_problematic = True
            
            if is_problematic:
                replaced += 1
                return f"{prefix}{self.standard_abstract}{suffix}"
            else:
                return match.group(0)
        
        content = re.sub(abstract_pattern, replace_if_problematic, content, flags=re.DOTALL)
        
        return content, replaced
    
    def _remove_control_chars(self, content: str) -> Tuple[str, int]:
        original = content
        
        content = content.replace('\r', '')
        content = re.sub(r'\n{3,}', '\n\n', content)
        
        removed = len(original) - len(content)
        
        return content, removed if removed > 0 else 0
    
    def _remove_comment_autocites(self, content: str) -> Tuple[str, int]:
        removed = 0
        lines = content.split('\n')
        
        for i, line in enumerate(lines):
            if line.strip().startswith('%'):
                if '\\autocite{' in line or '\\cite{' in line:
                    original = line
                    line = re.sub(r'\\autocite\{[^}]+\}', '', line)
                    line = re.sub(r'\\cite\{[^}]+\}', '', line)
                    if line != original:
                        lines[i] = line
                        removed += 1
        
        return '\n'.join(lines), removed


def fix_missing_commas(bib_path: Path) -> int:
    """Fix missing commas in BibTeX entries (merged from fix_missing_commas.py)"""
    backup_path = bib_path.with_suffix('.bib.backup_commas')
    import shutil
    shutil.copy2(bib_path, backup_path)
    
    with open(bib_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    pattern = r'(\n  \w+ = \{[^}]+\})\n(  \w+ = )'
    
    fixed_count = 0
    def add_comma(match):
        nonlocal fixed_count
        fixed_count += 1
        return match.group(1) + ',\n' + match.group(2)
    
    prev_count = -1
    while prev_count != fixed_count:
        prev_count = fixed_count
        content = re.sub(pattern, add_comma, content)
    
    with open(bib_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return fixed_count


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Fix problematic BibTeX entries')
    parser.add_argument('--refs', default='refs.bib', help='Path to refs.bib')
    parser.add_argument('--preamble', default='preamble.tex', help='Path to preamble.tex')
    
    args = parser.parse_args()
    
    fixer = BibTeXFixer(args.refs, args.preamble)
    fixes = fixer.fix_all()
    
    print("Fixes applied:")
    for fix_type, count in fixes.items():
        if count > 0:
            print(f"  {fix_type}: {count}")
    
    total = sum(fixes.values())
    if total == 0:
        print("  No fixes needed!")
    else:
        print(f"\nTotal fixes: {total}")


if __name__ == '__main__':
    main()