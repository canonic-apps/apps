#!/usr/bin/env python3

import re
import requests
import time
from typing import Dict, List, Optional, Tuple
import bibtexparser
from bibtexparser.bwriter import BibTexWriter
from bibtexparser.bibdatabase import BibDatabase


STANDARD_FIXES = {
    'loinc': {
        'author': 'Regenstrief Institute',
        'title': 'LOINC: The international standard for identifying health measurements, observations, and documents'
    },
    'rxnorm': {
        'author': 'National Library of Medicine',
        'title': 'RxNorm: Normalized names for clinical drugs'
    },
    'umls': {
        'author': 'National Library of Medicine',
        'title': 'UMLS Metathesaurus: Unified medical language system'
    },
    'snomedct': {
        'author': 'SNOMED International',
        'title': 'SNOMED CT: Systematized Nomenclature of Medicine Clinical Terms'
    },
    'icd10cm': {
        'author': 'Centers for Disease Control and Prevention',
        'title': 'ICD-10-CM: International Classification of Diseases, 10th Revision, Clinical Modification'
    },
    'ga4gh_beacon': {
        'author': 'Global Alliance for Genomics and Health',
        'title': 'Beacon v2: Discovery API for genomic variants'
    },
    'ga4gh_htsget': {
        'author': 'Global Alliance for Genomics and Health',
        'title': 'htsget: Streaming access protocol for genomic data'
    },
    'ga4gh_phenopackets': {
        'author': 'Global Alliance for Genomics and Health',
        'title': 'Phenopackets: Exchange standard for phenotypic information'
    },
    'ga4gh_policy': {
        'author': 'Global Alliance for Genomics and Health',
        'title': 'Framework for Responsible Sharing of Genomic and Health-Related Data'
    },
    'ga4gh_vr': {
        'author': 'Global Alliance for Genomics and Health',
        'title': 'Variation Representation: Standard for representing genomic variation'
    },
    'w3c_did_2022': {
        'author': 'World Wide Web Consortium',
        'title': 'Decentralized Identifiers (DIDs) v1.0: Core architecture, data model, and representations'
    },
    'w3c_vc_11': {
        'author': 'World Wide Web Consortium',
        'title': 'Verifiable Credentials Data Model 1.1: Expressing verifiable information on the Web'
    }
}


class BibliographyStandardizer:
    def __init__(self, api_email: str = "hadley@stanford.edu"):
        self.api_email = api_email
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'MammoChat Bibliography Tool/1.0 (mailto:hadley@stanford.edu)'
        })
    
    def standardize_entry_type(self, entry: Dict) -> str:
        entry_id = entry.get('ID', '').lower()
        title = entry.get('title', '').lower()
        
        databases = ['umls', 'rxnorm', 'snomed', 'loinc', 'uscdi', 'tefca', 'tcia']
        standards = ['fhir', 'hl7', 'mcode', 'dicom', 'w3c', 'oauth', 'json']
        
        for db in databases + standards:
            if db in entry_id or db in title:
                return 'online'
        
        if 'nct' in entry_id or 'clinicaltrials.gov' in entry.get('url', ''):
            return 'online'
        
        if any(x in entry_id for x in ['nih_', 'fda_', 'onc_', 'hhs_', 'who_']):
            return 'techreport'
        
        current_type = entry.get('ENTRYTYPE', 'misc')
        if current_type in ['article', 'book', 'inproceedings', 'incollection']:
            return current_type
        
        return 'misc'
    
    def fetch_pubmed_metadata(self, pmid: str) -> Optional[Dict]:
        url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
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
        metadata = {'pmid': pmid}
        
        doi_match = re.search(r'<ArticleId IdType="doi">([^<]+)</ArticleId>', xml)
        if doi_match:
            metadata['doi'] = doi_match.group(1)
        
        pmc_match = re.search(r'<ArticleId IdType="pmc">([^<]+)</ArticleId>', xml)
        if pmc_match:
            metadata['pmc'] = pmc_match.group(1)
        
        time.sleep(0.34)
        return metadata
    
    def fetch_doi_metadata(self, doi: str) -> Optional[Dict]:
        url = f"https://api.crossref.org/works/{doi}"
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
        except requests.exceptions.RequestException:
            return None
        
        data = response.json()
        work = data.get('message', {})
        
        metadata = {'doi': doi}
        
        if 'link' in work:
            for link in work['link']:
                if 'URL' in link:
                    url = link['URL']
                    if 'pmc/articles/PMC' in url:
                        pmc_match = re.search(r'PMC(\d+)', url)
                        if pmc_match:
                            metadata['pmc'] = f"PMC{pmc_match.group(1)}"
        
        time.sleep(0.1)
        return metadata
    
    def standardize_identifiers(self, entry: Dict) -> Dict:
        pmid = entry.get('pmid', '').strip()
        doi = entry.get('doi', '').strip()
        pmc = entry.get('pmc', '').strip()
        nct = entry.get('nct', '').strip()
        url = entry.get('url', '').strip()
        
        if pmid:
            pmid = re.sub(r'\D', '', pmid)
        
        if doi:
            doi = re.sub(r'^(https?://)?(dx\.)?doi\.org/', '', doi)
            doi = doi.strip()
        
        if pmc:
            if not pmc.startswith('PMC'):
                digits = re.sub(r'\D', '', pmc)
                pmc = f"PMC{digits}"
        
        if nct or 'clinicaltrials.gov' in url.lower():
            if not nct and url:
                nct_match = re.search(r'NCT\d+', url, re.IGNORECASE)
                if nct_match:
                    nct = nct_match.group(0).upper()
        
        if pmid and not (doi or pmc):
            print(f"  Fetching metadata for PMID {pmid}...")
            metadata = self.fetch_pubmed_metadata(pmid)
            if metadata:
                if 'doi' in metadata and not doi:
                    doi = metadata['doi']
                if 'pmc' in metadata and not pmc:
                    pmc = metadata['pmc']
        
        elif doi and not pmc and not pmid:
            metadata = self.fetch_doi_metadata(doi)
            if metadata and 'pmc' in metadata:
                pmc = metadata['pmc']
        
        result = {}
        
        if pmid:
            result['pmid'] = pmid
        if doi:
            result['doi'] = doi
        if pmc:
            result['pmc'] = pmc
        if nct:
            result['nct'] = nct
        
        entry_id = entry.get('ID', '').lower()
        is_standard = any(x in entry_id for x in ['umls', 'rxnorm', 'snomed', 'loinc', 
                                                     'uscdi', 'tefca', 'fhir', 'hl7', 
                                                     'mcode', 'w3c', 'nih_', 'fda_', 'onc_'])
        
        if url and (not any([pmid, doi, pmc, nct]) or is_standard):
            result['url'] = url
        
        return result
    
    def beautify_entry(self, entry: Dict) -> Dict:
        new_type = self.standardize_entry_type(entry)
        entry['ENTRYTYPE'] = new_type
        
        identifiers = self.standardize_identifiers(entry)
        
        for key in ['pmid', 'doi', 'pmc', 'nct', 'url', 'note', 'howpublished']:
            entry.pop(key, None)
        
        entry.update(identifiers)
        
        if 'author' in entry:
            author = entry['author']
            author = re.sub(r'\s+', ' ', author)
            author = re.sub(r'\s*,\s*and\s+', ' and ', author)
            entry['author'] = author.strip()
        
        if 'title' in entry:
            title = entry['title']
            title = re.sub(r'\s+', ' ', title)
            title = re.sub(r'\.\s*$', '', title)
            entry['title'] = title.strip()
        
        if 'journal' in entry:
            journal = entry['journal']
            journal = re.sub(r'\s+', ' ', journal)
            entry['journal'] = journal.strip()
        
        if 'year' in entry:
            year_match = re.search(r'\d{4}', str(entry['year']))
            if year_match:
                entry['year'] = year_match.group(0)
        
        entry = {k: v for k, v in entry.items() if v and str(v).strip()}
        
        return entry
    
    def standardize_bibliography(self, bib_file: str, output_file: str = None):
        if output_file is None:
            output_file = bib_file
        
        with open(bib_file, 'r', encoding='utf-8') as f:
            bib_database = bibtexparser.load(f)
        
        with open(f"{bib_file}.backup", 'w', encoding='utf-8') as f:
            with open(bib_file, 'r', encoding='utf-8') as orig:
                f.write(orig.read())
        
        processed_entries = []
        stats = {
            'pmid_added': 0,
            'doi_added': 0,
            'pmc_added': 0,
            'nct_added': 0,
            'url_removed': 0,
            'type_changed': 0
        }
        
        for i, entry in enumerate(bib_database.entries):
            entry_id = entry.get('ID', 'unknown')
            old_type = entry.get('ENTRYTYPE', 'misc')
            
            had_pmid = bool(entry.get('pmid'))
            had_doi = bool(entry.get('doi'))
            had_pmc = bool(entry.get('pmc'))
            had_nct = bool(entry.get('nct'))
            had_url = bool(entry.get('url'))
            
            new_entry = self.beautify_entry(entry)
            
            if new_entry.get('pmid') and not had_pmid:
                stats['pmid_added'] += 1
            if new_entry.get('doi') and not had_doi:
                stats['doi_added'] += 1
            if new_entry.get('pmc') and not had_pmc:
                stats['pmc_added'] += 1
            if new_entry.get('nct') and not had_nct:
                stats['nct_added'] += 1
            if had_url and not new_entry.get('url'):
                stats['url_removed'] += 1
            if new_entry.get('ENTRYTYPE') != old_type:
                stats['type_changed'] += 1
            
            processed_entries.append(new_entry)
        
        new_db = BibDatabase()
        new_db.entries = processed_entries
        
        writer = BibTexWriter()
        writer.indent = '  '
        writer.order_entries_by = None
        writer.align_values = True
        writer.add_trailing_comma = False
        
        with open(output_file, 'w', encoding='utf-8') as f:
            bibtexparser.dump(new_db, f, writer)
    
    def fix_standards(self, bib_file: str):
        """Fix standard entries (merged from fix_standards.py)"""
        with open(bib_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        with open(f"{bib_file}.backup_standards", 'w', encoding='utf-8') as f:
            f.write(content)
        
        for entry_id, fixes in STANDARD_FIXES.items():
            pattern = rf'(@misc\{{{entry_id},.*?^\}})'
            match = re.search(pattern, content, re.MULTILINE | re.DOTALL)
            
            if not match:
                continue
            
            entry = match.group(1)
            new_entry = entry
            
            if 'author' in fixes:
                author_pattern = r'author = \{[^}]+\}'
                new_entry = re.sub(author_pattern, f"author = {{{fixes['author']}}}", new_entry)
            
            if 'title' in fixes:
                title_pattern = r'title = \{[^}]+\}'
                new_entry = re.sub(title_pattern, f"title = {{{fixes['title']}}}", new_entry)
            
            if new_entry != entry:
                content = content.replace(entry, new_entry)
        
        with open(bib_file, 'w', encoding='utf-8') as f:
            f.write(content)


if __name__ == '__main__':
    import sys
    
    bib_file = sys.argv[1] if len(sys.argv) > 1 else 'refs.bib'
    
    standardizer = BibliographyStandardizer()
    standardizer.standardize_bibliography(bib_file)