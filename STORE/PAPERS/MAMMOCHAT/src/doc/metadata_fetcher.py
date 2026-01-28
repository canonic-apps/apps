import requests
import time
import re
import json
import hashlib
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from pathlib import Path
import xml.etree.ElementTree as ET


@dataclass
class MetadataResult:
    abstract: Optional[str] = None
    title: Optional[str] = None
    authors: Optional[List[str]] = None
    year: Optional[str] = None
    doi: Optional[str] = None
    pmid: Optional[str] = None
    source: Optional[str] = None
    quality_score: float = 0.0
    fetch_time: float = 0.0


class MetadataFetcher:
    def __init__(self, rate_limit: float = 0.34, cache_dir: Optional[str] = None, max_retries: int = 3):
        self.rate_limit = rate_limit
        self.max_retries = max_retries
        self.last_request = {}
        self.cache_dir = Path(cache_dir or '.metadata_cache')
        self.cache_dir.mkdir(exist_ok=True)
        
        self.endpoints = {
            'pubmed': 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/',
            'crossref': 'https://api.crossref.org/works/',
            'semantic_scholar': 'https://api.semanticscholar.org/v1/paper/',
            'clinicaltrials': 'https://clinicaltrials.gov/api/query/full_studies',
            'openlibrary': 'https://openlibrary.org/api/books'
        }
    
    def _cache_key(self, service: str, identifier: str) -> str:
        key_string = f"{service}:{identifier}"
        return hashlib.md5(key_string.encode()).hexdigest()
    
    def _get_cached(self, service: str, identifier: str) -> Optional[MetadataResult]:
        cache_key = self._cache_key(service, identifier)
        cache_file = self.cache_dir / f"{cache_key}.json"
        
        if cache_file.exists():
            with open(cache_file, 'r') as f:
                data = json.load(f)
            return MetadataResult(**data)
        
        return None
    
    def _set_cached(self, service: str, identifier: str, result: MetadataResult):
        cache_key = self._cache_key(service, identifier)
        cache_file = self.cache_dir / f"{cache_key}.json"
        
        with open(cache_file, 'w') as f:
            json.dump(result.__dict__, f, indent=2)
    
    def _rate_limit(self, service: str):
        now = time.time()
        last = self.last_request.get(service, 0)
        elapsed = now - last
        
        if elapsed < self.rate_limit:
            time.sleep(self.rate_limit - elapsed)
        
        self.last_request[service] = time.time()
    
    def fetch_from_pubmed(self, pmid: str) -> Optional[MetadataResult]:
        cached = self._get_cached('pubmed', pmid)
        if cached:
            return cached
        
        self._rate_limit('pubmed')
        start_time = time.time()
        
        url = f"{self.endpoints['pubmed']}efetch.fcgi"
        params = {
            'db': 'pubmed',
            'id': pmid,
            'retmode': 'xml',
            'rettype': 'abstract'
        }
        
        response = requests.get(url, params=params)
        if response.status_code != 200:
            return None
        
        root = ET.fromstring(response.content)
        article = root.find('.//PubmedArticle')
        
        if article is None:
            return None
        
        result = MetadataResult()
        result.source = 'PubMed'
        result.pmid = pmid
        
        abstract_elem = article.find('.//Abstract')
        if abstract_elem is not None:
            abstract_texts = []
            for text in abstract_elem.findall('.//AbstractText'):
                label = text.get('Label', '')
                content = ''.join(text.itertext()).strip()
                if label:
                    abstract_texts.append(f"{label}: {content}")
                else:
                    abstract_texts.append(content)
            result.abstract = ' '.join(abstract_texts)
        
        title_elem = article.find('.//ArticleTitle')
        if title_elem is not None:
            result.title = ''.join(title_elem.itertext()).strip()
        
        authors_elem = article.findall('.//Author')
        if authors_elem:
            authors = []
            for author in authors_elem:
                lastname = author.find('LastName')
                forename = author.find('ForeName')
                if lastname is not None:
                    name = lastname.text
                    if forename is not None:
                        name = f"{forename.text} {name}"
                    authors.append(name)
            result.authors = authors
        
        year_elem = article.find('.//PubDate/Year')
        if year_elem is not None:
            result.year = year_elem.text
        
        doi_elem = article.find('.//ArticleId[@IdType="doi"]')
        if doi_elem is not None:
            result.doi = doi_elem.text
        
        result.quality_score = self._calculate_quality_score(result)
        result.fetch_time = time.time() - start_time
        
        self._set_cached('pubmed', pmid, result)
        
        return result
    
    def fetch_from_doi(self, doi: str) -> Optional[MetadataResult]:
        cached = self._get_cached('crossref', doi)
        if cached:
            return cached
        
        self._rate_limit('crossref')
        start_time = time.time()
        
        doi = doi.strip().replace('https://doi.org/', '').replace('http://dx.doi.org/', '')
        
        url = f"{self.endpoints['crossref']}{doi}"
        headers = {'User-Agent': 'LaTeX-Publication-Pipeline/1.0 (mailto:research@example.com)'}
        
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            return None
        
        data = response.json()
        message = data.get('message', {})
        
        result = MetadataResult()
        result.source = 'CrossRef'
        result.doi = doi
        
        result.abstract = message.get('abstract')
        if result.abstract:
            result.abstract = re.sub(r'<[^>]+>', '', result.abstract)
        
        titles = message.get('title', [])
        if titles:
            result.title = titles[0]
        
        authors = message.get('author', [])
        if authors:
            result.authors = [
                f"{a.get('given', '')} {a.get('family', '')}".strip()
                for a in authors
            ]
        
        published = message.get('published-print') or message.get('published-online')
        if published and 'date-parts' in published:
            date_parts = published['date-parts'][0]
            if date_parts:
                result.year = str(date_parts[0])
        
        result.quality_score = self._calculate_quality_score(result)
        result.fetch_time = time.time() - start_time
        
        self._set_cached('crossref', doi, result)
        
        return result
    
    def fetch_from_semantic_scholar(self, identifier: str, id_type: str = 'doi') -> Optional[MetadataResult]:
        self._rate_limit('semantic_scholar')
        start_time = time.time()
        
        if id_type == 'doi':
            identifier = identifier.replace('https://doi.org/', '').replace('http://dx.doi.org/', '')
        elif id_type == 'arxiv':
            identifier = f"arXiv:{identifier}"
        
        url = f"{self.endpoints['semantic_scholar']}{identifier}"
        
        response = requests.get(url)
        if response.status_code != 200:
            return None
        
        data = response.json()
        
        result = MetadataResult()
        result.source = 'Semantic Scholar'
        
        result.abstract = data.get('abstract')
        result.title = data.get('title')
        result.year = str(data.get('year')) if data.get('year') else None
        result.doi = data.get('doi')
        
        authors = data.get('authors', [])
        if authors:
            result.authors = [a.get('name') for a in authors if a.get('name')]
        
        result.quality_score = self._calculate_quality_score(result)
        result.fetch_time = time.time() - start_time
        
        return result
    
    def fetch_from_clinicaltrials(self, nct_id: str) -> Optional[MetadataResult]:
        self._rate_limit('clinicaltrials')
        start_time = time.time()
        
        url = self.endpoints['clinicaltrials']
        params = {
            'expr': nct_id,
            'fmt': 'json',
            'min_rnk': 1,
            'max_rnk': 1
        }
        
        response = requests.get(url, params=params)
        if response.status_code != 200:
            return None
        
        data = response.json()
        studies = data.get('FullStudiesResponse', {}).get('FullStudies', [])
        
        if not studies:
            return None
        
        study = studies[0].get('Study', {})
        protocol = study.get('ProtocolSection', {})
        
        result = MetadataResult()
        result.source = 'ClinicalTrials.gov'
        
        desc = protocol.get('DescriptionModule', {})
        result.abstract = desc.get('BriefSummary') or desc.get('DetailedDescription')
        
        ident = protocol.get('IdentificationModule', {})
        result.title = ident.get('OfficialTitle') or ident.get('BriefTitle')
        
        result.quality_score = self._calculate_quality_score(result)
        result.fetch_time = time.time() - start_time
        
        return result
    
    def _calculate_quality_score(self, result: MetadataResult) -> float:
        score = 0.0
        
        if result.abstract:
            length = len(result.abstract)
            if length > 500:
                score += 0.4
            elif length > 200:
                score += 0.3
            elif length > 100:
                score += 0.2
            else:
                score += 0.1
        
        if result.title:
            score += 0.2
        
        if result.authors and len(result.authors) > 0:
            score += 0.2
        
        if result.year:
            score += 0.1
        
        if result.doi or result.pmid:
            score += 0.1
        
        return score
    
    def fetch_metadata(self, entry: Dict) -> Optional[MetadataResult]:
        results = []
        
        pmid = entry.get('pmid') or entry.get('PMID')
        if pmid:
            result = self.fetch_from_pubmed(pmid)
            if result:
                results.append(result)
        
        doi = entry.get('doi') or entry.get('DOI')
        if doi:
            result = self.fetch_from_semantic_scholar(doi, 'doi')
            if result:
                results.append(result)
        
        arxiv = entry.get('arxiv') or entry.get('eprint')
        if arxiv:
            result = self.fetch_from_semantic_scholar(arxiv, 'arxiv')
            if result:
                results.append(result)
        
        if doi and not any(r.source == 'CrossRef' for r in results):
            result = self.fetch_from_doi(doi)
            if result:
                results.append(result)
        
        nct_match = re.search(r'NCT\d{8}', str(entry))
        if nct_match:
            result = self.fetch_from_clinicaltrials(nct_match.group())
            if result:
                results.append(result)
        
        if results:
            best = max(results, key=lambda r: r.quality_score)
            return best
        
        return None