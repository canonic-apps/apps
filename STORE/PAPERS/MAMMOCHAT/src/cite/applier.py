import re
from typing import List, Dict, Tuple, Optional, DefaultDict
from collections import defaultdict
from dataclasses import dataclass

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from bib.processor import BibTeXProcessor
from cite.manager import CitationConsolidator


REF_LINE_REGEX = re.compile(
    r"^\s*(?:\{\\footnotesize\s+)?\\emph\{References:\}\s+\\autocite\{([^}]*)\}\s*\}?\s*$"
)


def split_sentences(text: str) -> List[str]:
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    return [p.strip() for p in parts if p.strip()]


def insert_citation(sentence: str, keys: List[str]) -> str:
    cite = f"\\autocite{{{','.join(keys)}}}"
    m = re.search(r"([.!?]\s*)$", sentence)
    if m:
        idx = m.start(1)
        return sentence[:idx] + ' ' + cite + sentence[idx:]
    return sentence + ' ' + cite


def is_generic_abstract(text: Optional[str]) -> bool:
    if not text:
        return True
    t = text.strip().lower()
    if len(t) < 80:
        return True
    
    generic_phrases = [
        'this study examines key aspects',
        'we present a method',
        'this paper describes',
        'precision medicine and health informatics'
    ]
    return any(p in t for p in generic_phrases)


def is_valid_paragraph(text: str, min_alpha_chars: int = 20) -> bool:
    if not text or not text.strip():
        return False
    
    if r'\caption{' in text:
        return False
    
    alpha_count = sum(1 for c in text if c.isalpha())
    if alpha_count < min_alpha_chars:
        return False
    
    if not re.search(r'[.!?]', text):
        return False
    
    return True


@dataclass
class InlineResult:
    file: str
    para_start: int
    para_end: int
    keys: List[str]
    applied: int
    fallback: bool


class InlineCitationApplier:
    def __init__(
        self,
        bib_path: str = 'refs.bib',
        similarity_threshold: float = 0.12,
        tfidf_max_features: int = 1000,
        stop_words: Optional[str] = 'english',
        forward_scan_limit: int = 5,
        min_alpha_chars: int = 20,
    ):
        self.processor = BibTeXProcessor(bib_path)
        self.processor.load()
        self.threshold = similarity_threshold
        self.tfidf_max_features = tfidf_max_features
        self.stop_words = stop_words
        self.forward_scan_limit = forward_scan_limit
        self.min_alpha_chars = min_alpha_chars
        self.consolidator = CitationConsolidator()

    def _get_abstract(self, key: str) -> Optional[str]:
        entry = next((e for e in self.processor.database.entries if e['ID'] == key), None)
        if not entry:
            return None
        return entry.get('abstract')

    def _best_sentence_for_key(self, paragraph: str, abstract: str) -> Optional[int]:
        sentences = split_sentences(paragraph)
        if not sentences:
            return None
        corpus = sentences + [abstract]

        vectorizer = TfidfVectorizer(
            stop_words=self.stop_words,
            max_features=self.tfidf_max_features
        )
        tfidf = vectorizer.fit_transform(corpus)
        sims = cosine_similarity(tfidf[-1], tfidf[:-1])[0]
        best_idx = int(sims.argmax())

        if sims[best_idx] < self.threshold:
            return None
        return best_idx

    def apply_file(self, tex_path: str) -> Optional[InlineResult]:
        with open(tex_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        changed = False
        i = 0
        last_result: Optional[InlineResult] = None

        while i < len(lines):
            line = lines[i]
            m = REF_LINE_REGEX.match(line.strip())
            if not m:
                i += 1
                continue

            raw_keys = m.group(1)
            keys = [k.strip() for k in raw_keys.split(',') if k.strip()]

            def extract_paragraph(start_idx: int, direction: int = -1) -> Tuple[int, int, str]:
                if direction == -1:
                    end = start_idx - 1
                    while end >= 0 and not lines[end].strip():
                        end -= 1
                    start = end
                    while start >= 0 and lines[start].strip():
                        start -= 1
                    start += 1
                else:
                    start = start_idx + 1
                    n = len(lines)
                    while start < n and not lines[start].strip():
                        start += 1
                    end = start
                    while end < n and lines[end].strip():
                        end += 1
                    end -= 1
                if start < 0 or end < start:
                    return -1, -1, ''
                text = ' '.join([lines[j].strip() for j in range(start, end + 1)])
                return start, end, text

            para_start, para_end, paragraph = extract_paragraph(i, direction=-1)
            if not is_valid_paragraph(paragraph, self.min_alpha_chars):
                scan_idx = i
                found = False
                for _ in range(self.forward_scan_limit):
                    next_start, next_end, next_para = extract_paragraph(scan_idx, direction=1)
                    if next_start == -1:
                        break
                    if is_valid_paragraph(next_para, self.min_alpha_chars):
                        para_start, para_end, paragraph = next_start, next_end, next_para
                        found = True
                        break
                    scan_idx = next_end + 1
                if not found:
                    last_result = InlineResult(tex_path, -1, -1, keys, 0, True)
                    i += 1
                    continue

            sent_list = split_sentences(paragraph)
            if not sent_list:
                i += 1
                continue

            sentence_to_keys: DefaultDict[int, List[str]] = defaultdict(list)
            applied = 0
            for key in keys:
                abstract = self._get_abstract(key)
                if not abstract:
                    continue
                best_idx = self._best_sentence_for_key(paragraph, abstract)
                if best_idx is None:
                    continue
                sentence_to_keys[best_idx].append(key)
                applied += 1

            if applied == 0:
                if any(is_generic_abstract(self._get_abstract(k)) for k in keys):
                    sentence_to_keys[len(sent_list) - 1] = keys[:]
                    applied = len(keys)
                else:
                    last_result = InlineResult(tex_path, para_start, para_end, keys, 0, True)
                    i += 1
                    continue

            new_sentences = []
            for idx, s in enumerate(sent_list):
                if idx in sentence_to_keys:
                    new_sentences.append(insert_citation(s, sentence_to_keys[idx]))
                else:
                    new_sentences.append(s)
            new_paragraph = ' '.join(new_sentences)

            new_paragraph, _ = self.consolidator.consolidate_citations(new_paragraph)

            lines[para_start:para_end + 1] = [new_paragraph + "\n"]
            del lines[i]

            changed = True
            last_result = InlineResult(tex_path, para_start, para_end, keys, applied, False)
            i = para_start + 1

        if changed:
            with open(tex_path, 'w', encoding='utf-8') as f:
                f.writelines(lines)
            return last_result

        return None

    def apply_all(self, tex_files: List[str]) -> List[InlineResult]:
        results: List[InlineResult] = []
        for fp in tex_files:
            res = self.apply_file(fp)
            if res:
                results.append(res)
        return results


def main():
    """Main function for applying inline citations."""
    import argparse
    from pathlib import Path

    parser = argparse.ArgumentParser(description='Apply inline citations to LaTeX files')
    parser.add_argument('files', nargs='*', help='LaTeX files to process')
    parser.add_argument('--bib', default='refs.bib', help='Path to bibliography file')
    parser.add_argument('--threshold', type=float, default=0.12, help='Similarity threshold')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be done without making changes')

    args = parser.parse_args()

    if args.files:
        tex_files = args.files
    else:
        tex_files = sorted(Path('.').glob('*.tex'))
        tex_files = [str(f) for f in tex_files if f.name not in ('main.tex', 'preamble.tex')]

    if not tex_files:
        print("No .tex files found to process")
        return

    applier = InlineCitationApplier(
        bib_path=args.bib,
        similarity_threshold=args.threshold
    )

    if args.dry_run:
        print(f"Would process {len(tex_files)} files: {', '.join(tex_files)}")
        return

    results = applier.apply_all(tex_files)
    total_applied = sum(r.applied for r in results if r)

    print(f"Applied {total_applied} citations across {len(results)} files")
    for r in results:
        if r and r.applied > 0:
            print(f"  {r.file}: {r.applied} citations")


if __name__ == '__main__':
    main()