#!/usr/bin/env python3

import argparse
import re
from pathlib import Path
from typing import List, Dict


def append_citation_to_abstract(tex_path: Path, key: str) -> bool:
    """Append citation to abstract (from append_abstract_citation.py)"""
    ABSTRACT_BEGIN = re.compile(r"\\begin\{abstract\}")
    ABSTRACT_END = re.compile(r"\\end\{abstract\}")
    
    content = tex_path.read_text(encoding="utf-8")
    begin = ABSTRACT_BEGIN.search(content)
    end = ABSTRACT_END.search(content)
    if not begin or not end or end.start() < begin.end():
        return False
    abstract_text = content[begin.end():end.start()]
    if key in abstract_text:
        return False
    insertion = f" \\autocite{{{key}}}"
    new_content = content[:end.start()] + insertion + content[end.start():]
    tex_path.write_text(new_content, encoding="utf-8")
    return True


def fix_moving_citations(path: Path) -> int:
    """Fix citations in moving arguments (from fix_moving_citations.py)"""
    TITLE_CMD_RE = re.compile(r"^(?P<indent>\s*)\\(?P<cmd>section|subsection|subsubsection|paragraph|subparagraph)\*?\{(?P<title>.*)\}\s*$")
    AUTOCITE_RE = re.compile(r"\\autocite\{([^}]*)\}")

    def extract_and_strip_autocites(title: str) -> tuple[str, List[str]]:
        keys: List[str] = []
        def collect(m: re.Match) -> str:
            inner = m.group(1).strip()
            keys.append(inner)
            return ""
        new_title = AUTOCITE_RE.sub(collect, title)
        new_title = re.sub(r"\s+\.", ".", new_title)
        new_title = re.sub(r"\s+", " ", new_title).strip()
        return new_title, keys

    lines = path.read_text(encoding="utf-8").splitlines()
    out: List[str] = []
    changes = 0
    for i, line in enumerate(lines):
        m = TITLE_CMD_RE.match(line)
        if not m:
            out.append(line)
            continue
        title = m.group("title")
        if not AUTOCITE_RE.search(title):
            out.append(line)
            continue
        indent = m.group("indent")
        cmd = m.group("cmd")
        clean_title, cites = extract_and_strip_autocites(title)
        new_line = f"{indent}\\{cmd}*{{{clean_title}}}"
        out.append(new_line)
        if cites:
            cite_blob = ", ".join(cites)
            out.append(f"{indent}References: \\autocite{{{cite_blob}}}")
        changes += 1
    if changes:
        path.write_text("\n".join(out) + "\n", encoding="utf-8")
    return changes


def relocate_citation(key: str, tex_files: List[Path], exclude_files: List[Path], threshold: float = 0.12) -> Dict:
    """Relocate citation to better position (from relocate_citation.py)"""
    from cite.manager import CitationManager
    from cite.applier import InlineCitationApplier, split_sentences, insert_citation
    from bib.processor import BibTeXProcessor
    
    def _remove_key_from_text(text: str, key: str) -> str:
        def drop_from_group(m: re.Match) -> str:
            keys = [k.strip() for k in m.group(1).split(',') if k.strip()]
            keys = [k for k in keys if k != key]
            if not keys:
                return ''
            return f"\\autocite{{{','.join(keys)}}}"

        text = re.sub(r"\\autocite\{([^}]+)\}", drop_from_group, text)
        text = re.sub(r"\s{2,}", " ", text)
        return text

    def remove_key_from_files(files: List[Path], key: str) -> int:
        removed_in = 0
        for fp in files:
            content = fp.read_text(encoding='utf-8')
            new = _remove_key_from_text(content, key)
            if new != content:
                fp.write_text(new, encoding='utf-8')
                removed_in += 1
        return removed_in

    def find_best_paragraph_for_key(key: str, tex_files: List[Path], threshold: float) -> Dict:
        applier = InlineCitationApplier()
        manager = CitationManager()
        abstract = applier._get_abstract(key)
        if not abstract:
            raise SystemExit(f"No abstract found for key: {key}")

        paragraphs: List[Dict] = []
        for f in tex_files:
            paragraphs.extend(manager.extract_paragraphs_from_tex(str(f)))

        placement = manager.find_placement_by_similarity(abstract, paragraphs, key, threshold=threshold)
        if not placement:
            raise SystemExit(f"No suitable placement found for {key} above threshold {threshold}")

        return {
            'file': placement.file_path,
            'line': placement.line_number,
            'similarity': placement.similarity_score,
        }

    def insert_key_inline(file_path: Path, start_line: int, key: str) -> bool:
        applier = InlineCitationApplier()
        abstract = applier._get_abstract(key)
        if not abstract:
            return False

        lines = file_path.read_text(encoding='utf-8').splitlines()

        i = start_line
        while i > 0 and lines[i].strip() and lines[i-1].strip():
            i -= 1
        j = start_line
        while j < len(lines) and lines[j].strip():
            j += 1
        paragraph = ' '.join(l.strip() for l in lines[i:j])

        idx = applier._best_sentence_for_key(paragraph, abstract)
        if idx is None:
            if j-1 >= 0:
                lines[j-1] = lines[j-1].rstrip() + f" \\autocite{{{key}}}"
            else:
                return False
        else:
            sentences = split_sentences(paragraph)
            sentences[idx] = insert_citation(sentences[idx], [key])
            lines[i:j] = [' '.join(sentences)]

        file_path.write_text('\n'.join(lines) + '\n', encoding='utf-8')
        text = file_path.read_text(encoding='utf-8')
        from cite.manager import CitationConsolidator
        consolidated, _ = CitationConsolidator.consolidate_citations(text)
        file_path.write_text(consolidated, encoding='utf-8')
        return True

    # Remove from excluded files
    removed_in = remove_key_from_files(exclude_files, key)
    
    # Find best placement
    placement = find_best_paragraph_for_key(key, tex_files, threshold)
    
    # Insert at new location
    ok = insert_key_inline(Path(placement['file']), placement['line'], key)
    
    return {
        'removed_from_files': removed_in,
        'inserted': ok,
        'placement': placement
    }


def strip_references_prefix(tex_path: Path) -> int:
    """Strip References: prefix from lines (from strip_references_prefix.py)"""
    content = tex_path.read_text(encoding="utf-8")
    pattern = re.compile(r'\bReferences:\s*', re.MULTILINE)
    new_content, count = pattern.subn('', content)
    if count:
        tex_path.write_text(new_content, encoding="utf-8")
    return count


def main():
    """Main function for LaTeX utilities"""
    parser = argparse.ArgumentParser(description='LaTeX utilities')
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # append-abstract
    append_parser = subparsers.add_parser('append-abstract', help='Append citation to abstract')
    append_parser.add_argument('--file', required=True, help='LaTeX file path')
    append_parser.add_argument('--key', required=True, help='Citation key')
    
    # fix-moving
    moving_parser = subparsers.add_parser('fix-moving', help='Fix citations in moving arguments')
    moving_parser.add_argument('--files', nargs='+', required=True, help='LaTeX files to process')
    
    # relocate
    relocate_parser = subparsers.add_parser('relocate', help='Relocate citation to better position')
    relocate_parser.add_argument('--key', required=True, help='Citation key to relocate')
    relocate_parser.add_argument('--threshold', type=float, default=0.12, help='Similarity threshold')
    relocate_parser.add_argument('--exclude', action='append', default=['00_titlepage.tex', '01_founders_preface.tex'], help='Files to exclude')
    
    # strip-prefix
    strip_parser = subparsers.add_parser('strip-prefix', help='Strip References: prefix')
    strip_parser.add_argument('--files', nargs='+', required=True, help='LaTeX files to process')
    
    args = parser.parse_args()
    
    if args.command == 'append-abstract':
        success = append_citation_to_abstract(Path(args.file), args.key)
        if success:
            print(f"Added citation {args.key} to abstract in {args.file}")
        else:
            print(f"Failed to add citation to abstract")
    
    elif args.command == 'fix-moving':
        total = 0
        for f in args.files:
            p = Path(f)
            if p.exists():
                c = fix_moving_citations(p)
                if c:
                    total += c
        print(f"Fixed {total} moving citations")
    
    elif args.command == 'relocate':
        cwd = Path('.')
        tex_files = [Path(p) for p in cwd.glob('*.tex') if p.name not in set(args.exclude)]
        exclude_files = [Path(name) for name in args.exclude if Path(name).exists()]
        
        result = relocate_citation(args.key, tex_files, exclude_files, args.threshold)
        print(f"Relocated citation {args.key}: {result}")
    
    elif args.command == 'strip-prefix':
        total = 0
        for f in args.files:
            p = Path(f)
            if p.exists():
                c = strip_references_prefix(p)
                if c:
                    total += c
        print(f"Stripped {total} reference prefixes")


if __name__ == '__main__':
    main()