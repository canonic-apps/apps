#!/usr/bin/env python3

import re
import requests
import time
import json
import sys
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import xml.etree.ElementTree as ET
from difflib import SequenceMatcher


@dataclass
class VerificationResult:
    entry_id: str
    status: str
    issues: List[str]
    corrections: Dict[str, str]
    metadata: Dict


class IdentifierVerifier:
    def __init__(self, api_email: str = "hadley@stanford.edu", rate_limit: float = 0.34):
        self.api_email = api_email
        self.rate_limit = rate_limit
        self.last_request = {}
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': f'Bibliography-Verifier/1.0 (mailto:{api_email})'
        })
    
    def _rate_limit(self, service: str):
        now = time.time()
        last = self.last_request.get(service, 0)
        elapsed = now - last
        if elapsed < self.rate_limit:
            time.sleep(self.rate_limit - elapsed)
        self.last_request[service] = time.time()
    
    def validate_doi_format(self, doi: str) -> Tuple[bool, Optional[str]]:
        if not doi:
            return False, None
        
        cleaned = doi.strip()
        cleaned = re.sub(r'^(https?://)?(dx\.)?doi\.org/', '', cleaned)
        cleaned = cleaned.strip()
        
        if re.match(r'^10\.\d{4,}/\S+$', cleaned):
            return True, cleaned
        
        return False, None
    
    def resolve_doi(self, doi: str) -> Optional[Dict]:
        self._rate_limit('crossref')
        
        is_valid, cleaned_doi = self.validate_doi_format(doi)
        if not is_valid:
            return None
        
        url = f"https://api.crossref.org/works/{cleaned_doi}"
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
        except requests.exceptions.RequestException:
            return None
        
        data = response.json()
        message = data.get('message', {})
        
        metadata = {
            'doi': cleaned_doi,
            'title': message.get('title', [''])[0],
            'journal': message.get('container-title', [''])[0] if message.get('container-title') else None,
            'year': None,
            'authors': []
        }
        
        published = message.get('published-print') or message.get('published-online')
        if published and 'date-parts' in published:
            date_parts = published['date-parts'][0]
            if date_parts:
                metadata['year'] = str(date_parts[0])
        
        authors = message.get('author', [])
        for author in authors[:5]:
            family = author.get('family', '')
            given = author.get('given', '')
            if family:
                metadata['authors'].append(f"{given} {family}".strip())
        
        return metadata
    
    def fetch_pubmed_ids(self, pmid: str) -> Optional[Dict]:
        self._rate_limit('pubmed')
        
        url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
        params = {
            'db': 'pubmed',
            'id': pmid,
            'retmode': 'xml',
            'email': self.api_email
        }
        
        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
        except requests.exceptions.RequestException:
            return None
        
        xml = response.text
        result = {}
        
        doi_match = re.search(r'<ArticleId IdType="doi">([^<]+)</ArticleId>', xml)
        if doi_match:
            result['doi'] = doi_match.group(1)
        
        pmc_match = re.search(r'<ArticleId IdType="pmc">([^<]+)</ArticleId>', xml)
        if pmc_match:
            pmc = pmc_match.group(1)
            if not pmc.startswith('PMC'):
                pmc = f"PMC{pmc}"
            result['pmc'] = pmc
        
        title_match = re.search(r'<ArticleTitle>([^<]+)</ArticleTitle>', xml)
        if title_match:
            result['title'] = title_match.group(1)
        
        return result if result else None
    
    def canonicalize_pmc(self, pmc: str) -> Optional[str]:
        if not pmc:
            return None
        
        digits = re.sub(r'\D', '', pmc)
        if digits:
            return f"PMC{digits}"
        
        return None
    
    def extract_nct_from_url(self, url: str) -> Optional[str]:
        if not url or 'clinicaltrials.gov' not in url.lower():
            return None
        
        match = re.search(r'NCT\d{8}', url, re.IGNORECASE)
        if match:
            return match.group(0).upper()
        
        return None
    
    def similarity_score(self, str1: str, str2: str) -> float:
        if not str1 or not str2:
            return 0.0
        
        s1 = re.sub(r'[^a-z0-9]', '', str1.lower())
        s2 = re.sub(r'[^a-z0-9]', '', str2.lower())
        
        return SequenceMatcher(None, s1, s2).ratio()
    
    def verify_entry(self, entry: Dict, fix: bool = False) -> VerificationResult:
        entry_id = entry.get('ID', 'unknown')
        issues = []
        corrections = {}
        metadata = {}
        
        doi = entry.get('doi', '').strip()
        pmid = entry.get('eprint', '').strip() if entry.get('eprinttype') == 'pubmed' else entry.get('pmid', '').strip()
        pmc = (entry.get('usera', '') or entry.get('pmc', '') or '').strip()
        has_legacy_pmc_field = 'pmc' in entry
        if not pmc and 'note' in entry and 'PMC' in entry.get('note', ''):
            m = re.search(r'(PMC\d+)', entry.get('note', ''))
            if m:
                pmc = m.group(1)
        url = entry.get('url', '').strip()
        
        entry_title = entry.get('title', '')
        entry_author = entry.get('author', '')
        
        if doi:
            is_valid, cleaned_doi = self.validate_doi_format(doi)
            
            if not is_valid:
                issues.append(f"Invalid DOI format: {doi}")
            else:
                if cleaned_doi != doi:
                    issues.append(f"DOI format corrected: {doi} → {cleaned_doi}")
                    if fix:
                        corrections['doi'] = cleaned_doi
                
                print(f"  Resolving DOI: {cleaned_doi}")
                doi_metadata = self.resolve_doi(cleaned_doi)
                
                if doi_metadata:
                    metadata['doi_title'] = doi_metadata['title']
                    metadata['doi_authors'] = doi_metadata['authors']
                    metadata['doi_journal'] = doi_metadata['journal']
                    metadata['doi_year'] = doi_metadata['year']
                    
                    if entry_title:
                        title_sim = self.similarity_score(entry_title, doi_metadata['title'])
                        if title_sim < 0.5:
                            issues.append(
                                f"DOI title mismatch (similarity: {title_sim:.2f}): "
                                f"Entry='{entry_title[:60]}...' vs DOI='{doi_metadata['title'][:60]}...'"
                            )
                    
                    if entry_author and doi_metadata['authors']:
                        first_author_entry = entry_author.split(' and ')[0].strip()
                        first_author_doi = doi_metadata['authors'][0]
                        author_sim = self.similarity_score(first_author_entry, first_author_doi)
                        if author_sim < 0.5:
                            issues.append(
                                f"DOI author mismatch (similarity: {author_sim:.2f}): "
                                f"Entry='{first_author_entry}' vs DOI='{first_author_doi}'"
                            )
                    if fix and entry_title and doi_metadata['title']:
                        t_sim = self.similarity_score(entry_title, doi_metadata['title'])
                        a_sim = 0.0
                        if entry_author and doi_metadata['authors']:
                            a_sim = self.similarity_score(entry_author.split(' and ')[0].strip(), doi_metadata['authors'][0])
                        if t_sim <= 0.30 and a_sim <= 0.30:
                            corrections['doi'] = None
                else:
                    issues.append(f"DOI could not be resolved: {cleaned_doi}")
        
        if pmid:
            print(f"  Fetching from PubMed (PMID: {pmid})")
            pubmed_data = self.fetch_pubmed_ids(pmid)
            
            if pubmed_data:
                if 'doi' in pubmed_data:
                    if not doi:
                        issues.append(f"Missing DOI (found in PubMed): {pubmed_data['doi']}")
                        if fix:
                            corrections['doi'] = pubmed_data['doi']
                    elif doi != pubmed_data['doi']:
                        issues.append(
                            f"DOI mismatch with PubMed: Entry={doi} vs PubMed={pubmed_data['doi']}"
                        )
                        pub_title = pubmed_data.get('title', '')
                        title_sim_pub = self.similarity_score(entry_title, pub_title) if pub_title and entry_title else 0.0
                        if fix:
                            if title_sim_pub >= 0.6:
                                corrections['doi'] = pubmed_data['doi']
                            elif title_sim_pub <= 0.3:
                                corrections['doi'] = None
                                if entry.get('eprinttype') == 'pubmed' or entry.get('pmid'):
                                    corrections['eprint'] = None
                                    corrections['eprinttype'] = None
                
                if 'pmc' in pubmed_data:
                    canonical_pmc = self.canonicalize_pmc(pubmed_data['pmc'])
                    if not pmc:
                        issues.append(f"Missing PMC (found in PubMed): {canonical_pmc}")
                        if fix:
                            corrections['usera'] = canonical_pmc
                            if has_legacy_pmc_field:
                                corrections['pmc'] = None
                    else:
                        current_pmc_canonical = self.canonicalize_pmc(pmc)
                        if current_pmc_canonical != canonical_pmc:
                            issues.append(
                                f"PMC mismatch: Entry={pmc} vs PubMed={canonical_pmc}"
                            )
                            if fix:
                                corrections['usera'] = canonical_pmc
                                if has_legacy_pmc_field:
                                    corrections['pmc'] = None
        
        if pmc:
            canonical_pmc = self.canonicalize_pmc(pmc)
            if canonical_pmc and canonical_pmc != pmc:
                issues.append(f"PMC format corrected: {pmc} → {canonical_pmc}")
                if fix:
                    corrections['usera'] = canonical_pmc
                    if has_legacy_pmc_field:
                        corrections['pmc'] = None
            elif fix and has_legacy_pmc_field:
                corrections['usera'] = canonical_pmc or pmc
                corrections['pmc'] = None
        
        if url:
            nct = self.extract_nct_from_url(url)
            if nct and not entry.get('eprint') == nct:
                issues.append(f"NCT ID found in URL: {nct}")
                if fix:
                    corrections['eprint'] = nct
                    corrections['eprinttype'] = 'nct'
        
        if url and (doi or pmid):
            if 'doi.org' in url or 'pubmed.ncbi.nlm.nih.gov' in url:
                issues.append("Redundant URL (DOI/PMID present)")
                if fix:
                    corrections['url'] = None
        
        if not issues:
            status = 'ok'
        elif corrections:
            status = 'fixed'
        else:
            has_unresolvable = any('could not be resolved' in i.lower() for i in issues)
            has_invalid = any(i.lower().startswith('invalid doi format') for i in issues)
            has_mismatch = any('mismatch' in i.lower() for i in issues)
            if has_unresolvable or has_invalid:
                status = 'error'
            elif has_mismatch:
                status = 'warning'
        
        return VerificationResult(
            entry_id=entry_id,
            status=status,
            issues=issues,
            corrections=corrections,
            metadata=metadata
        )
    
    def verify_bibliography(self, bib_file: str, fix: bool = False, report_file: str = None) -> Dict:
        import bibtexparser
        from bibtexparser.bwriter import BibTexWriter
        
        with open(bib_file, 'r', encoding='utf-8') as f:
            bib_db = bibtexparser.load(f)
        
        if fix:
            backup_path = f"{bib_file}.before_verify"
            with open(bib_file, 'r', encoding='utf-8') as src:
                with open(backup_path, 'w', encoding='utf-8') as dst:
                    dst.write(src.read())
        
        results = []
        stats = {
            'total': 0,
            'ok': 0,
            'warning': 0,
            'error': 0,
            'fixed': 0,
            'corrections_applied': 0
        }
        
        for entry in bib_db.entries:
            stats['total'] += 1
            
            result = self.verify_entry(entry, fix=fix)
            results.append(result)
            
            stats[result.status] += 1
            
            if fix and result.corrections:
                for field, new_value in result.corrections.items():
                    if new_value is None:
                        if field in entry:
                            del entry[field]
                        stats['corrections_applied'] += 1
                    else:
                        entry[field] = new_value
                        stats['corrections_applied'] += 1
        
        if fix and stats['corrections_applied'] > 0:
            writer = BibTexWriter()
            writer.indent = '    '
            writer.order_entries_by = None
            with open(bib_file, 'w', encoding='utf-8') as f:
                f.write(writer.write(bib_db))
        
        if report_file:
            report_data = {
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
                'file': bib_file,
                'fix_mode': fix,
                'statistics': stats,
                'results': [{'entry_id': r.entry_id, 'status': r.status, 'issues': r.issues} for r in results]
            }
            
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(report_data, f, indent=2)
        
        return stats


def main():
    import argparse
    
    parser = argparse.ArgumentParser()
    parser.add_argument('bib_file', help='Path to .bib file')
    parser.add_argument('--fix', action='store_true')
    parser.add_argument('--report', default='verification_report.json')
    parser.add_argument('--email', default='hadley@stanford.edu')
    parser.add_argument('--rate-limit', type=float, default=0.34)
    
    args = parser.parse_args()
    
    verifier = IdentifierVerifier(api_email=args.email, rate_limit=args.rate_limit)
    
    stats = verifier.verify_bibliography(
        bib_file=args.bib_file,
        fix=args.fix,
        report_file=args.report
    )
    
    sys.exit(1 if stats['error'] > 0 else 0)


if __name__ == '__main__':
    main()