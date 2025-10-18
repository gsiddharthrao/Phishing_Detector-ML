import re
import os
import time
import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup

# Common URL shortener domains (not exhaustive)
SHORTENER_DOMAINS = {
    'bit.ly', 'tinyurl.com', 't.co', 'goo.gl', 'ow.ly', 'buff.ly', 'adf.ly', 'bitly.com', 'is.gd', 'cutt.ly'
}

# TLDs that are often abused for malicious links (example list)
SUSPICIOUS_TLDS = {'.tk', '.ml', '.ga', '.cf', '.gq'}

# Simple URL extraction regex
URL_REGEX = re.compile(r"https?://[^\s<>\)\]]+")


def extract_urls(text):
    """Return a list of unique URLs found in text."""
    if not text:
        return []
    urls = URL_REGEX.findall(text)
    # normalize trailing punctuation
    urls = [u.rstrip('.,;:!?)\"\'') for u in urls]
    # unique preserving order
    seen = set()
    result = []
    for u in urls:
        if u not in seen:
            seen.add(u)
            result.append(u)
    return result


def _is_ip_based(netloc):
    # strip port
    host = netloc.split(':')[0]
    return bool(re.match(r'^(\d{1,3}\.){3}\d{1,3}$', host))


def _get_tld(domain):
    parts = domain.rsplit('.', 1)
    if len(parts) == 2:
        return '.' + parts[1].lower()
    return ''


def _call_virustotal(url, api_key, timeout=10):
    """
    Call VirusTotal (v3) URL analysis endpoint. Returns dict with limited fields.
    NOTE: Requires environment variable VIRUSTOTAL_API_KEY or pass `api_key`.
    """
    if not api_key:
        return {'service': 'virustotal', 'available': False, 'error': 'No API key provided'}

    headers = {
        'x-apikey': api_key
    }
    try:
        # v3 URL scan: POST /api/v3/urls with form field 'url'
        scan_resp = requests.post('https://www.virustotal.com/api/v3/urls', data={'url': url}, headers=headers, timeout=timeout)
        if scan_resp.status_code not in (200, 201):
            return {'service': 'virustotal', 'available': True, 'error': f'status_{scan_resp.status_code}'}
        j = scan_resp.json()
        analysis_id = j.get('data', {}).get('id')
        if not analysis_id:
            return {'service': 'virustotal', 'available': True, 'error': 'no_analysis_id'}

        # Poll analysis (quick/simple): GET /api/v3/analyses/{id}
        analysis_url = f'https://www.virustotal.com/api/v3/analyses/{analysis_id}'
        for _ in range(6):
            time.sleep(1)
            aresp = requests.get(analysis_url, headers=headers, timeout=timeout)
            if aresp.status_code == 200:
                aj = aresp.json()
                stats = aj.get('data', {}).get('attributes', {}).get('stats', {})
                malicious = stats.get('malicious', 0)
                suspicious = stats.get('suspicious', 0)
                return {
                    'service': 'virustotal',
                    'available': True,
                    'malicious_count': malicious,
                    'suspicious_count': suspicious,
                    'raw': aj
                }
        return {'service': 'virustotal', 'available': True, 'error': 'timeout_waiting_analysis'}
    except Exception as e:
        return {'service': 'virustotal', 'available': True, 'error': str(e)}


def analyze_url(url, use_virustotal=True):
    """Analyze a single URL with heuristics and optional VirusTotal check.

    Returns a dict with heuristics and any external verdicts.
    """
    parsed = urlparse(url)
    netloc = parsed.netloc.lower()
    domain = netloc.split(':')[0]

    reasons = []
    details = {
        'url': url,
        'domain': domain,
        'is_ip': False,
        'is_shortened': False,
        'has_punycode': False,
        'suspicious_tld': False,
        'virustotal': None,
        'summary': 'unknown'
    }

    # Heuristic checks
    if _is_ip_based(domain):
        details['is_ip'] = True
        reasons.append('URL uses raw IP address')

    if domain in SHORTENER_DOMAINS:
        details['is_shortened'] = True
        reasons.append('URL is a shortened link')

    if 'xn--' in domain:
        details['has_punycode'] = True
        reasons.append('Domain uses punycode (possible homograph)')

    tld = _get_tld(domain)
    if tld in SUSPICIOUS_TLDS:
        details['suspicious_tld'] = True
        reasons.append(f'Unusual TLD {tld}')

    # Numeric-heavy domains (e.g., 0-9 prevalence)
    digits = sum(c.isdigit() for c in domain)
    if digits > 3:
        reasons.append('Domain contains many digits')

    # External API check (VirusTotal) if requested
    if use_virustotal:
        api_key = os.environ.get('VIRUSTOTAL_API_KEY')
        vt = _call_virustotal(url, api_key)
        details['virustotal'] = vt
        if isinstance(vt, dict) and vt.get('available') and vt.get('malicious_count', 0) > 0:
            reasons.append('VirusTotal reports malicious detections')

    # Final summary heuristics
    if reasons:
        details['summary'] = 'suspicious: ' + '; '.join(reasons)
    else:
        details['summary'] = 'no obvious heuristics triggered'

    return details


def analyze_urls_in_text(text, use_virustotal=True):
    urls = extract_urls(text)
    return [analyze_url(u, use_virustotal=use_virustotal) for u in urls]

def analyze_html_links(html_content):
    """
    Analyzes anchor tags in HTML content to find misleading links.
    """
    if not html_content:
        return []

    soup = BeautifulSoup(html_content, 'html.parser')
    links = soup.find_all('a')
    misleading_links = []

    for link in links:
        href = link.get('href')
        text = link.get_text().strip()

        if href and text:
            # Simple check: if link text looks like a domain, but href is different
            # This is a basic heuristic.
            text_domain_match = re.search(r'([a-zA-Z0-9-]+\.[a-zA-Z]{2,})', text)
            if text_domain_match:
                text_domain = text_domain_match.group(1).lower()
                try:
                    href_domain = urlparse(href).netloc.lower()
                    if href_domain and text_domain not in href_domain:
                        misleading_links.append({
                            'text': text,
                            'href': href,
                            'summary': f"Link text says '{text_domain}' but goes to '{href_domain}'."
                        })
                except Exception:
                    pass # Ignore parsing errors on href

    return misleading_links

def check_domain_reputation(domain):
    """Simple domain reputation check based on common patterns."""
    suspicious_indicators = [
        'suspicious' if any(char.isdigit() for char in domain) and len([char for char in domain if char.isdigit()]) > 2 else None,
        'suspicious' if '-' in domain and domain.count('-') > 1 else None,
        'suspicious' if len(domain) > 20 else None,
        'benign' if domain in ['google.com', 'microsoft.com', 'apple.com', 'amazon.com'] else None
    ]
    return [ind for ind in suspicious_indicators if ind]

def check_for_urgency(text):
    """
    Checks for common urgency-inducing phrases in text.
    """
    urgency_keywords = [
        'urgent', 'action required', 'immediate', 'account suspended',
        'verify your account', 'security alert', 'password expires',
        'limited time', 'offer expires'
    ]
    found_keywords = []
    for keyword in urgency_keywords:
        if keyword in text.lower():
            found_keywords.append(keyword)
    return found_keywords
