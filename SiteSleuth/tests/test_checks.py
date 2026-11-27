import unittest
from sitesleuth import analyze_headers, scan_text, validate_public_url

class ChecksTests(unittest.TestCase):
    def test_missing_security_headers_are_informational_gaps(self):
        findings = analyze_headers({})
        self.assertTrue(any(f['id'] == 'HDR-HSTS' for f in findings))
        self.assertEqual({f['severity'] for f in findings}, {'Low'})

    def test_flags_private_ip_target(self):
        with self.assertRaises(ValueError):
            validate_public_url('http://127.0.0.1/admin')

    def test_detects_secret_and_unsafe_sink_patterns(self):
        findings = scan_text('const api_key = "sk_live_123456789012345"; el.innerHTML = input;')
        ids = {f['id'] for f in findings}
        self.assertIn('SRC-SECRET', ids)
        self.assertIn('SRC-XSS-SINK', ids)

if __name__ == '__main__':
    unittest.main()
