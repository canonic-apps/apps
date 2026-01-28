#!/usr/bin/env python3

import re
import shutil
from pathlib import Path
from collections import OrderedDict
from typing import Tuple, List, Dict


def parse_citation_keys(cite_text: str) -> List[str]:
    """Parse citation keys from a citation string"""
    match = re.search(r'\\autocite\{([^}]+)\}', cite_text)
    if match:
        keys = [k.strip() for k in match.group(1).split(',')]
        return keys
    return []


def merge_adjacent_citations(content: str) -> Tuple[str, List[Dict]]:
    """Merge adjacent citations into consolidated format"""
    pattern = r'(\\autocite\{[^}]+\})([.\s]*)(\\autocite\{[^}]+\})'
    
    changes = []
    
    def merge_cites(match):
        first = match.group(1)
        sep = match.group(2)
        second = match.group(3)
        
        keys1 = parse_citation_keys(first)
        keys2 = parse_citation_keys(second)
        
        all_keys = list(OrderedDict.fromkeys(keys1 + keys2))
        
        total_before = len(keys1) + len(keys2)
        total_after = len(all_keys)
        
        if total_before != total_after:
            changes.append({
                'removed': total_before - total_after,
                'keys1': keys1,
                'keys2': keys2,
                'merged': all_keys
            })
        
        merged = f"\\autocite{{{','.join(all_keys)}}}"
        return merged
    
    new_content = re.sub(pattern, merge_cites, content)
    
    return new_content, changes


def remove_internal_duplicates(content: str) -> Tuple[str, List[Dict]]:
    """Remove duplicate keys within citations"""
    pattern = r'\\autocite\{([^}]+)\}'
    changes = []
    
    def deduplicate_keys(match):
        keys_str = match.group(1)
        keys = [k.strip() for k in keys_str.split(',')]
        
        unique_keys = list(OrderedDict.fromkeys(keys))
        
        if len(unique_keys) != len(keys):
            duplicates_removed = len(keys) - len(unique_keys)
            changes.append({
                'removed': duplicates_removed,
                'original': keys,
                'deduplicated': unique_keys
            })
        
        return f"\\autocite{{{','.join(unique_keys)}}}"
    
    new_content = re.sub(pattern, deduplicate_keys, content)
    return new_content, changes


def fix_citations_in_file(filepath: Path) -> Tuple[bool, int, List[Dict]]:
    """Fix duplicate citations in a single file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        original = f.read()
    
    fixed, internal_changes = remove_internal_duplicates(original)
    fixed, adjacent_changes = merge_adjacent_citations(fixed)
    
    all_changes = internal_changes + adjacent_changes
    
    if fixed != original:
        backup = filepath.with_suffix('.tex.bak_citations')
        shutil.copy2(filepath, backup)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(fixed)
        
        return True, len(all_changes), all_changes
    
    return False, 0, []


def consolidate_all_tex_files(base_path: Path = Path('.')) -> Dict[str, int]:
    """Consolidate citations in all .tex files"""
    tex_files = list(base_path.glob('*.tex'))
    results = {
        'files_processed': 0,
        'files_changed': 0,
        'total_merges': 0
    }
    
    for tex_file in sorted(tex_files):
        results['files_processed'] += 1
        changed, merge_count, changes = fix_citations_in_file(tex_file)
        if changed:
            results['files_changed'] += 1
            results['total_merges'] += merge_count
    
    return results


def main():
    """Main function for fixing duplicate citations"""
    base_path = Path('.')
    results = consolidate_all_tex_files(base_path)
    
    print(f"Citation consolidation complete:")
    print(f"  Files processed: {results['files_processed']}")
    print(f"  Files changed: {results['files_changed']}")
    print(f"  Total merges: {results['total_merges']}")
    
    if results['files_changed'] == 0:
        print("No citation fixes needed!")


if __name__ == '__main__':
    main()