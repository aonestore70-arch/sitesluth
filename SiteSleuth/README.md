# SiteSleuth (prototype)

A small, read-only security-review helper for websites you own or have explicit permission to assess. It is intentionally **not** an exploit scanner. It does not crawl pages, submit forms, guess passwords, fuzz endpoints, test access controls, run payloads, or attempt to bypass protections.

## Local dashboard demo

Requires Python 3.10+; no third-party packages. From this directory, run:

```bash
python -m http.server 8765 --bind 127.0.0.1
```

Then open http://127.0.0.1:8765/ in your browser. The dashboard loads `demo_data.json`, a fictional sample report. It makes no requests to any real target. Stop the server with Ctrl+C. The binding is loopback-only, so it is not exposed to your network.

## CLI review

The original CLI checks remain available:

```bash
python sitesleuth.py https://your-site.example
python sitesleuth.py --source path/to/your-own-file.js
python -m unittest discover -s tests -v
```

The URL mode makes a single ordinary request to the supplied public homepage and checks response headers. Private, loopback, link-local, and other non-public IP addresses are blocked after DNS resolution to reduce SSRF risk. Do not use against systems without permission. The source mode reads one local file and reports line numbers without printing possible secret values.

## Current checks

### Public homepage response
- HTTPS URL usage (only HTTPS-specific check: the URL must be explicitly supplied as http(s); no certificate-chain audit).
- Presence/absence of HSTS, CSP, X-Content-Type-Options, X-Frame-Options, Referrer-Policy, and Permissions-Policy.
- Flags CSP values containing `unsafe-inline` or `unsafe-eval` as an informational review item.

Missing headers are **hardening recommendations**, not confirmed vulnerabilities. Header review says nothing by itself about whether the application has exploitable flaws.

### Local source text
- Heuristic secret-like patterns (AWS access-key shape, generic credential assignments, Stripe-style live secret prefix, private-key marker). Evidence redacts values; rotate any genuine exposed credential immediately.
- Potentially dangerous browser sinks (`innerHTML`, `document.write`) and dynamic execution (`eval`, `new Function`). These are code-review leads: exploitability depends on whether untrusted input can reach them and the surrounding protections.

## Important limitations

This prototype does **not** detect or prove: broken access control/IDOR, authentication or session weaknesses, SQL/command injection, stored/reflected/DOM XSS, CSRF, unsafe uploads, API authorization, database/RLS mistakes, dependency CVEs, exposed backups, server-side secrets, cloud misconfiguration, rate-limit/business-logic flaws, or AI prompt injection/data leakage/tool authorization. Many require source code, architecture/configuration access, authenticated test accounts, dependency manifests, or explicitly scoped tests. Do not interpret “no findings” as “secure.” False positives and false negatives are expected.

Never test other people's websites with intrusive techniques. For deeper DAST, obtain written authorization, specify exact domains and accounts, agree on rate limits and excluded actions, use a staging environment where possible, and use established tools under the owner's supervision. Do not test payments, destructive actions, real user data, or production AI agents without explicit scope and safeguards.

## Safe development roadmap

A responsible next version could add: (1) local directory/repository scanning with secret redaction; (2) lockfile-based dependency audit using official package-manager advisory data; (3) passive HTML analysis of the supplied page for mixed content, insecure form actions, and risky third-party scripts; (4) optional owner-provided API/OpenAPI review; (5) a report with severity, evidence, confidence, and remediation. Authenticated authorization testing, payload-based injection testing, and AI red-team testing should remain separately gated to a documented owner-approved staging scope.

## Severity and reporting

The prototype assigns heuristic labels, not CVSS ratings. A finding must be validated by a qualified reviewer before being represented to a client as a vulnerability. The report should identify the exact tested URL/file and time, evidence, limitations, and remediation. Do not claim the site is “hackable” based solely on absent headers or a code-pattern match.
