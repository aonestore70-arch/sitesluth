"""SiteSleuth: safe, non-invasive website security review helper."""
import ipaddress
import re
import socket
from urllib.parse import urlparse

HEADERS = {
    'strict-transport-security': ('HDR-HSTS', 'HSTS absent', 'Enable HSTS after confirming HTTPS works across all intended subdomains.'),
    'content-security-policy': ('HDR-CSP', 'CSP absent', 'Define a restrictive CSP; avoid unsafe-inline/unsafe-eval where feasible.'),
    'x-content-type-options': ('HDR-NOSNIFF', 'X-Content-Type-Options absent', 'Set X-Content-Type-Options: nosniff.'),
    'x-frame-options': ('HDR-FRAME', 'Clickjacking header absent', 'Set frame-ancestors in CSP; optionally X-Frame-Options for legacy clients.'),
    'referrer-policy': ('HDR-REFERRER', 'Referrer-Policy absent', 'Set a privacy-conscious Referrer-Policy such as strict-origin-when-cross-origin.'),
    'permissions-policy': ('HDR-PERMISSIONS', 'Permissions-Policy absent', 'Disable browser features the site does not need.'),
}

def validate_public_url(url):
    p = urlparse(url)
    if p.scheme not in ('http', 'https') or not p.hostname or p.username or p.password:
        raise ValueError('Enter an http(s) URL without embedded credentials.')
    try:
        records = socket.getaddrinfo(p.hostname, p.port or (443 if p.scheme == 'https' else 80), type=socket.SOCK_STREAM)
    except OSError as e:
        raise ValueError(f'Could not resolve host: {e}')
    for rec in records:
        ip = ipaddress.ip_address(rec[4][0])
        if not ip.is_global:
            raise ValueError('Only publicly routable hosts are allowed; private/local targets are blocked.')
    return url

def analyze_headers(headers):
    normalized = {k.lower(): v for k, v in headers.items()}
    findings=[]
    for key,(fid,title,fix) in HEADERS.items():
        value=normalized.get(key)
        if not value:
            findings.append({'id':fid,'severity':'Low','title':title,'evidence':'Header not present on the checked response.','fix':fix})
        elif key == 'content-security-policy' and ('unsafe-inline' in value or 'unsafe-eval' in value):
            findings.append({'id':'HDR-CSP-WEAK','severity':'Info','title':'CSP contains unsafe allowances','evidence':'CSP includes unsafe-inline and/or unsafe-eval.','fix':'Use nonces/hashes and remove unsafe allowances where practical; test carefully.'})
    return findings

SECRET_PATTERNS=[re.compile(p,re.I) for p in [r'(?<![A-Za-z0-9])(?:AKIA[0-9A-Z]{16})(?![A-Za-z0-9])',r'(?:api[_-]?key|secret|password|passwd|token)\s*[:=]\s*[\'\"][^\'\"]{12,}[\'\"]',r'sk_live_[A-Za-z0-9]{12,}',r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----']]

def scan_text(text):
    findings=[]
    for i,line in enumerate(text.splitlines(),1):
        if any(p.search(line) for p in SECRET_PATTERNS):
            findings.append({'id':'SRC-SECRET','severity':'High','title':'Possible hardcoded secret','evidence':f'Line {i}: secret-like pattern; value redacted.','fix':'Revoke/rotate exposed credentials, remove from history, and use a secrets manager/environment injection.'})
        if re.search(r'\.innerHTML\s*=|document\.write\s*\(',line):
            findings.append({'id':'SRC-XSS-SINK','severity':'Medium','title':'Potential unsafe DOM sink','evidence':f'Line {i}: innerHTML/document.write use; exploitability depends on data flow.','fix':'Prefer textContent or safe templating; sanitize and context-encode untrusted data.'})
        if re.search(r'eval\s*\(|new Function\s*\(',line):
            findings.append({'id':'SRC-DYNAMIC-CODE','severity':'Medium','title':'Dynamic code execution pattern','evidence':f'Line {i}: eval/new Function pattern; review data source and necessity.','fix':'Remove dynamic execution or replace with explicit safe parsing/dispatch.'})
    return findings

if __name__ == '__main__':
    import argparse, json, urllib.request
    ap=argparse.ArgumentParser(description='Passive public homepage header review; local source audit.')
    ap.add_argument('url',nargs='?',help='public http(s) homepage URL')
    ap.add_argument('--source',help='local source file to inspect (read-only)')
    args=ap.parse_args(); report={'scope':'passive checks only','findings':[],'notes':[]}
    if args.url:
        validate_public_url(args.url)
        req=urllib.request.Request(args.url,headers={'User-Agent':'SiteSleuth/0.1 (passive security configuration review)'})
        try:
            with urllib.request.urlopen(req,timeout=12) as res:
                report['url']=res.geturl(); report['http_status']=res.status
                report['findings']+=analyze_headers(dict(res.headers.items()))
                report['notes'].append('Only the requested page response headers were checked; no crawling or payload testing.')
        except Exception as e: report['notes'].append(f'Page request failed or was blocked: {e}')
    if args.source:
        with open(args.source,'r',encoding='utf-8',errors='replace') as f: report['findings']+=scan_text(f.read())
    print(json.dumps(report,indent=2))
