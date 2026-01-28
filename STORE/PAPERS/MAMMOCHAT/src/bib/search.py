#!/usr/bin/env python3

import json
import time
import re
from dataclasses import dataclass
from typing import List, Dict, Optional

import requests

@dataclass
class ReferenceItem:
    title: str
    year: Optional[int]
    authors: List[Dict[str, str]]
    journal: Optional[str]
    doi: Optional[str]
    url: Optional[str]
    citation_count: int
    entry_type: str

    def first_author_lastname(self) -> str:
        if self.authors:
            return (self.authors[0].get('family') or '').strip()
        return ''

class ReferenceSearcher:
    def __init__(self, api_email: str = "hadley@stanford.edu", rate_limit: float = 0.34):
        self.api_email = api_email
        self.rate_limit = rate_limit
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': f'WhitePaper-RefSearch/1.0 (mailto:{api_email})'
        })
        self._last_request = 0.0

    def _rl(self):
        now = time.time()
        if now - self._last_request < self.rate_limit:
            time.sleep(self.rate_limit - (now - self._last_request))
        self._last_request = time.time()

    def _clean_doi(self, doi: Optional[str]) -> Optional[str]:
        if not doi:
            return None
        cleaned = re.sub(r'^(https?://)?(dx\.)?doi\.org/', '', doi.strip(), flags=re.I)
        return cleaned or None

    def search_by_author(
        self,
        author: str,
        limit: int = 20,
        coauthor: Optional[str] = None,
        since: Optional[int] = None,
        until: Optional[int] = None,
        min_citations: Optional[int] = None,
    ) -> List[ReferenceItem]:
        try:
            results = self._search_semantic_scholar(author, limit)
        except Exception:
            results = self._search_crossref(author, limit)

        results = [r for r in results if self._matches_filters(r, coauthor, since, until, min_citations)]
        results.sort(key=lambda x: x.citation_count, reverse=True)
        return results

    def _matches_filters(
        self,
        item: ReferenceItem,
        coauthor: Optional[str],
        since: Optional[int],
        until: Optional[int],
        min_citations: Optional[int],
    ) -> bool:
        if coauthor:
            needle = coauthor.lower().strip()
            names = []
            for a in item.authors:
                given = (a.get('given') or '').strip()
                family = (a.get('family') or '').strip()
                names.append(f"{given} {family}".strip())
                names.append(f"{family}, {given}".strip(', '))
            if not any(needle in n.lower() for n in names if n):
                return False

        if since is not None and item.year is not None and item.year < int(since):
            return False
        if until is not None and item.year is not None and item.year > int(until):
            return False

        if min_citations is not None and item.citation_count < int(min_citations):
            return False

        return True

    def _search_semantic_scholar(self, author: str, limit: int) -> List[ReferenceItem]:
        self._rl()
        au_r = self.session.get(
            'https://api.semanticscholar.org/graph/v1/author/search',
            params={'query': author, 'limit': 5, 'fields': 'name,paperCount,hIndex'},
            timeout=15
        )
        au_r.raise_for_status()
        data = au_r.json()
        if not data.get('data'):
            return []
        candidates = data['data']
        exact = [a for a in candidates if a.get('name', '').lower() == author.lower()]
        chosen = (exact[0] if exact else max(candidates, key=lambda a: a.get('paperCount', 0)))
        author_id = chosen.get('authorId') or chosen.get('id')
        if not author_id:
            return []

        self._rl()
        p_r = self.session.get(
            f'https://api.semanticscholar.org/graph/v1/author/{author_id}/papers',
            params={
                'limit': min(max(limit, 1), 100),
                'fields': 'title,year,citationCount,externalIds,venue,authors,url',
                'sort': 'citationCount'
            },
            timeout=20
        )
        p_r.raise_for_status()
        pdata = p_r.json()
        papers = pdata.get('data') or pdata.get('papers') or []

        results: List[ReferenceItem] = []
        for p in papers:
            paper = p.get('paper') if isinstance(p, dict) and 'paper' in p else p
            if not paper:
                continue
            ext = paper.get('externalIds') or {}
            doi = self._clean_doi(ext.get('DOI'))
            auths = []
            for a in paper.get('authors') or []:
                name = (a.get('name') or '').strip()
                parts = name.split()
                family = parts[-1] if parts else ''
                given = ' '.join(parts[:-1]) if len(parts) > 1 else ''
                auths.append({'given': given, 'family': family})

            results.append(ReferenceItem(
                title=paper.get('title') or '',
                year=paper.get('year'),
                authors=auths,
                journal=paper.get('venue') or None,
                doi=doi,
                url=paper.get('url') or None,
                citation_count=int(paper.get('citationCount') or 0),
                entry_type='article'
            ))

        results.sort(key=lambda x: x.citation_count, reverse=True)
        return results

    def _search_crossref(self, author: str, limit: int) -> List[ReferenceItem]:
        self._rl()
        params = {
            'query.author': author,
            'rows': min(max(limit, 1), 100),
            'sort': 'is-referenced-by-count',
            'order': 'desc'
        }
        url = 'https://api.crossref.org/works'
        r = self.session.get(url, params=params, timeout=15)
        r.raise_for_status()
        items = r.json().get('message', {}).get('items', [])

        results: List[ReferenceItem] = []
        for it in items:
            year = None
            pub = it.get('published-print') or it.get('published-online') or it.get('issued')
            if pub and 'date-parts' in pub and pub['date-parts'] and pub['date-parts'][0]:
                year = int(pub['date-parts'][0][0])

            authors = []
            for a in it.get('author', []) or []:
                authors.append({'given': a.get('given', ''), 'family': a.get('family', '')})

            cr_type = (it.get('type') or '').lower()
            entry_type = 'article'
            if 'proceedings' in cr_type:
                entry_type = 'inproceedings'
            elif 'chapter' in cr_type:
                entry_type = 'incollection'
            elif 'book' in cr_type:
                entry_type = 'book'

            results.append(ReferenceItem(
                title=(it.get('title') or [''])[0],
                year=year,
                authors=authors,
                journal=(it.get('container-title') or [''])[0] or None,
                doi=self._clean_doi(it.get('DOI')),
                url=(it.get('URL') or None),
                citation_count=int(it.get('is-referenced-by-count') or 0),
                entry_type=entry_type
            ))

        results.sort(key=lambda x: x.citation_count, reverse=True)
        return results

    def _slug(self, text: str, max_words: int = 2) -> str:
        words = re.findall(r"[A-Za-z0-9]+", text)
        filtered = [w for w in words if len(w) > 3] or words
        slug = ''.join(filtered[:max_words])
        return slug[:20]

    def _make_key(self, item: ReferenceItem, existing_keys: set[str]) -> str:
        base = (item.first_author_lastname() or 'ref').lower()
        year = str(item.year or '')
        slug = self._slug(item.title)
        key = f"{base}{year}{slug}" if slug else f"{base}{year}"
        key = re.sub(r'[^a-z0-9]', '', key)
        if key in existing_keys or not key:
            h = re.sub(r'[^a-z0-9]', '', (item.doi or ''))[-6:]
            key = f"{key}{h}" if key else (h or f"ref{int(time.time())}")
        return key

    def to_bibtex_entry(self, item: ReferenceItem, key: str) -> Dict[str, str]:
        author_field = ' and '.join([
            f"{a.get('family','')}, {a.get('given','')}".strip(', ')
            for a in item.authors
            if (a.get('family') or a.get('given'))
        ])

        entry = {
            'ENTRYTYPE': item.entry_type,
            'ID': key,
            'title': item.title or '',
            'author': author_field,
            'year': str(item.year) if item.year else '',
        }
        if item.journal and item.entry_type == 'article':
            entry['journal'] = item.journal
        if item.doi:
            entry['doi'] = item.doi
        if item.url:
            entry['url'] = item.url
        return entry

    def append_to_bib(self, bib_path: str, items: List[ReferenceItem], top: int = 5) -> Dict:
        import bibtexparser
        from bibtexparser.bwriter import BibTexWriter

        with open(bib_path, 'r', encoding='utf-8') as f:
            db = bibtexparser.load(f)

        existing_dois = {re.sub(r'\s+', '', (e.get('doi') or '').lower()) for e in db.entries}
        existing_keys = {e.get('ID') for e in db.entries}

        backup = f"{bib_path}.backup_search_{time.strftime('%Y%m%d_%H%M%S')}"
        with open(bib_path, 'r', encoding='utf-8') as src, open(backup, 'w', encoding='utf-8') as dst:
            dst.write(src.read())

        added: List[str] = []
        skipped: List[str] = []
        for item in items[:top]:
            if not item.doi:
                skipped.append(item.title)
                continue
            doi_norm = re.sub(r'\s+', '', item.doi.lower())
            if doi_norm in existing_dois:
                skipped.append(item.title)
                continue
            key = self._make_key(item, existing_keys)
            entry = self.to_bibtex_entry(item, key)
            db.entries.append(entry)
            existing_dois.add(doi_norm)
            existing_keys.add(key)
            added.append(key)

        if added:
            writer = BibTexWriter()
            writer.indent = '    '
            writer.order_entries_by = None
            with open(bib_path, 'w', encoding='utf-8') as f:
                f.write(writer.write(db))

        return {
            'backup': backup,
            'added': added,
            'skipped': skipped,
        }

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--author', required=True)
    parser.add_argument('--limit', type=int, default=20)
    parser.add_argument('--insert', action='store_true')
    parser.add_argument('--top', type=int, default=5)
    parser.add_argument('--bib-file', default='refs.bib')
    parser.add_argument('--coauthor')
    parser.add_argument('--since', type=int)
    parser.add_argument('--until', type=int)
    parser.add_argument('--min-cites', type=int)
    parser.add_argument('--output')

    args = parser.parse_args()
    searcher = ReferenceSearcher()
    results = searcher.search_by_author(
        args.author,
        limit=args.limit,
        coauthor=args.coauthor,
        since=args.since,
        until=args.until,
        min_citations=args.min_cites,
    )

    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump([{
                'title': it.title,
                'year': it.year,
                'authors': it.authors,
                'journal': it.journal,
                'doi': it.doi,
                'url': it.url,
                'citation_count': it.citation_count,
                'entry_type': it.entry_type
            } for it in results], f, indent=2)

    if args.insert:
        searcher.append_to_bib(args.bib_file, results, top=args.top)

if __name__ == '__main__':
    main()