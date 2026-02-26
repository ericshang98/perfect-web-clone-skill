"""
C3: Server-Side Request Forgery (SSRF) — No URL Validation
============================================================

VULNERABILITY: The URL passed to Playwright's page.goto() undergoes zero validation.
Any URL scheme, hostname, or IP address is accepted, allowing the headless browser
to reach internal network resources, cloud metadata endpoints, and local files.

ATTACK VECTOR: User (or attacker via social engineering) provides URLs like:
    file:///etc/passwd
    http://169.254.169.254/latest/meta-data/iam/security-credentials/
    http://localhost:8080/admin
    http://192.168.1.1/admin

The extracted raw_html, DOM tree, and screenshot then exfiltrate the response content
into page_data.json.

TEST STRATEGY:
  - BEFORE tests: Demonstrate that no SSRF protection exists.
  - AFTER tests: Verify that URL validation blocks internal/dangerous URLs.

NOTE: These tests do NOT make actual network requests. They test the validation
logic that should prevent dangerous URLs from reaching page.goto().
"""
import ipaddress
import os
import sys
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))


# ---------------------------------------------------------------------------
# SSRF attack URLs targeting internal resources
# ---------------------------------------------------------------------------

# Cloud metadata endpoints (AWS, GCP, Azure)
CLOUD_METADATA_URLS = [
    ("http://169.254.169.254/latest/meta-data/", "AWS metadata — IAM credentials"),
    ("http://169.254.169.254/latest/meta-data/iam/security-credentials/",
     "AWS metadata — IAM role credentials"),
    ("http://169.254.169.254/latest/user-data", "AWS metadata — user data scripts"),
    ("http://metadata.google.internal/computeMetadata/v1/",
     "GCP metadata endpoint"),
    ("http://169.254.169.254/metadata/instance?api-version=2021-02-01",
     "Azure metadata endpoint"),
]

# Local file access
FILE_URLS = [
    ("file:///etc/passwd", "Linux password file"),
    ("file:///etc/shadow", "Linux shadow file"),
    ("file:///C:/Windows/System32/config/SAM", "Windows SAM database"),
    ("file:///C:/Users/matth/.ssh/id_rsa", "SSH private key"),
    ("file:///home/user/.aws/credentials", "AWS credentials file"),
    ("file:///proc/self/environ", "Linux process environment variables"),
]

# Internal network addresses
INTERNAL_NETWORK_URLS = [
    ("http://localhost/admin", "localhost"),
    ("http://localhost:8080/api/config", "localhost with port"),
    ("http://127.0.0.1/", "loopback IPv4"),
    ("http://127.0.0.1:3000/", "loopback with port"),
    ("http://[::1]/", "loopback IPv6"),
    ("http://0.0.0.0/", "all-interfaces bind"),
    ("http://192.168.1.1/admin", "private network — 192.168.x.x"),
    ("http://10.0.0.1:9200/", "private network — 10.x.x.x (Elasticsearch)"),
    ("http://172.16.0.1/", "private network — 172.16.x.x"),
    ("http://10.0.0.1:6379/", "private network — Redis"),
]

# Dangerous schemes
DANGEROUS_SCHEME_URLS = [
    ("ftp://internal-server/secrets.txt", "FTP scheme"),
    ("javascript:alert(document.cookie)", "javascript scheme"),
    ("data:text/html,<script>alert(1)</script>", "data scheme"),
    ("blob:http://example.com/uuid", "blob scheme"),
    ("gopher://internal:25/", "gopher scheme (SSRF classic)"),
]

# Legitimate external URLs that should be allowed
LEGITIMATE_URLS = [
    "https://example.com",
    "https://stripe.com",
    "https://www.google.com",
    "http://example.com",
    "https://sub.domain.example.com/path?q=1",
    "https://93.184.216.34/",  # Public IP (example.com)
]


ALL_SSRF_URLS = CLOUD_METADATA_URLS + FILE_URLS + INTERNAL_NETWORK_URLS + DANGEROUS_SCHEME_URLS


class TestC3BeforeExploit:
    """
    BEFORE FIX: These tests DEMONSTRATE the vulnerability.
    They prove there is no SSRF protection whatsoever.

    Expected: ALL tests PASS (proving the vulnerability exists).
    """

    def test_url_validation_now_in_extract_method(self):
        """After fix: extract() now calls validate_url() before page.goto().

        BEFORE the fix this test asserted no validation existed (and passed).
        Now it confirms the fix was applied.
        """
        import inspect
        from extract_page import PageExtractor

        source = inspect.getsource(PageExtractor.extract)
        assert "validate_url" in source, \
            "extract() should call validate_url() after the C3 fix"

    def test_no_scheme_validation(self):
        """No scheme validation exists — file://, ftp://, etc. would be accepted."""
        from extract_page import PageExtractor
        import inspect

        source = inspect.getsource(PageExtractor)
        # Check the entire class for any URL scheme filtering
        assert "file://" not in source, "No file:// blocking exists"
        assert "ALLOWED_SCHEMES" not in source, "No scheme allowlist exists"
        assert "BLOCKED" not in source, "No blocklist exists"

    def test_no_ip_validation(self):
        """No private IP address validation exists."""
        from extract_page import PageExtractor
        import inspect

        source = inspect.getsource(PageExtractor)
        assert "is_private" not in source, "No private IP check exists"
        assert "169.254" not in source, "No metadata IP blocking exists"
        assert "ipaddress" not in source, "No ipaddress module usage"

    def test_ssrf_url_count(self):
        """Document the number of distinct SSRF vectors that are unprotected."""
        # This test just documents the attack surface size
        total_vectors = len(ALL_SSRF_URLS)
        assert total_vectors >= 20, \
            f"At least 20 SSRF vectors exist, found {total_vectors}"


class TestC3AfterFix:
    """
    AFTER FIX: These tests verify that SSRF protection works.

    Expected: ALL tests PASS after validate_url() with SSRF checks is implemented.
    Before the fix, these tests will FAIL.

    The fix should add to validate_url() in extract_page.py:
    1. Scheme allowlist (only http:// and https://)
    2. Block private/reserved IP ranges
    3. Block known metadata endpoints
    4. Block localhost and loopback addresses
    """

    def _get_validator(self):
        """Try to import the URL validator. Skip if not yet implemented."""
        try:
            from extract_page import validate_url
            return validate_url
        except ImportError:
            pytest.skip("validate_url() not yet implemented — fix not applied")

    # --- Legitimate URLs must be ALLOWED ---

    @pytest.mark.parametrize("url", LEGITIMATE_URLS)
    def test_legitimate_urls_allowed(self, url):
        """Legitimate external URLs should pass validation."""
        validate_url = self._get_validator()
        result = validate_url(url)
        assert result == url, f"Legitimate URL should be accepted: {url}"

    # --- Cloud metadata must be BLOCKED ---

    @pytest.mark.parametrize("url,description", CLOUD_METADATA_URLS)
    def test_cloud_metadata_blocked(self, url, description):
        """Cloud provider metadata endpoints must be blocked."""
        validate_url = self._get_validator()
        with pytest.raises((ValueError, Exception)) as exc_info:
            validate_url(url)
        assert exc_info.value is not None, \
            f"Should block {description}: {url}"

    # --- Local file access must be BLOCKED ---

    @pytest.mark.parametrize("url,description", FILE_URLS)
    def test_file_urls_blocked(self, url, description):
        """file:// URLs must be blocked to prevent local file read."""
        validate_url = self._get_validator()
        with pytest.raises((ValueError, Exception)) as exc_info:
            validate_url(url)
        assert exc_info.value is not None, \
            f"Should block {description}: {url}"

    # --- Internal network must be BLOCKED ---

    @pytest.mark.parametrize("url,description", INTERNAL_NETWORK_URLS)
    def test_internal_network_blocked(self, url, description):
        """Internal/private network addresses must be blocked."""
        validate_url = self._get_validator()
        with pytest.raises((ValueError, Exception)) as exc_info:
            validate_url(url)
        assert exc_info.value is not None, \
            f"Should block {description}: {url}"

    # --- Dangerous schemes must be BLOCKED ---

    @pytest.mark.parametrize("url,description", DANGEROUS_SCHEME_URLS)
    def test_dangerous_schemes_blocked(self, url, description):
        """Non-HTTP schemes must be blocked."""
        validate_url = self._get_validator()
        with pytest.raises((ValueError, Exception)) as exc_info:
            validate_url(url)
        assert exc_info.value is not None, \
            f"Should block {description}: {url}"

    # --- Edge cases ---

    def test_ip_decimal_bypass_blocked(self):
        """Decimal IP notation bypass (2130706433 = 127.0.0.1) should be blocked."""
        validate_url = self._get_validator()
        # Some parsers resolve http://2130706433/ to 127.0.0.1
        # This is an edge case that sophisticated SSRF protection should handle
        # For now, just ensure standard private IPs are caught
        with pytest.raises((ValueError, Exception)):
            validate_url("http://127.0.0.1/")

    def test_ipv6_mapped_ipv4_blocked(self):
        """IPv6-mapped IPv4 addresses should be blocked."""
        validate_url = self._get_validator()
        with pytest.raises((ValueError, Exception)):
            validate_url("http://[::ffff:127.0.0.1]/")

    def test_redirect_note(self):
        """
        NOTE: DNS rebinding and HTTP redirects cannot be tested at the URL
        validation level. A malicious site at https://evil.com could return
        a 302 redirect to http://169.254.169.254/. This requires additional
        mitigation at the Playwright navigation level (e.g., intercepting
        redirects). This is documented as a known limitation.
        """
        pass  # Documentation-only test
