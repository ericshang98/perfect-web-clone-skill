#!/usr/bin/env python3
"""
Perfect Web Clone - Content Sanitizer
Strips potentially dangerous content from extracted page data before chunking.

Addresses C1 (Indirect Prompt Injection): malicious webpages can embed hidden
instructions in HTML comments, <script> tags, and attribute values.  This module
removes those vectors so that downstream subagent prompts never see
attacker-controlled instructions.

DESIGN PRINCIPLE: Be surgical, not scorched-earth.  <style> tags and hidden
elements carry critical visual information (fonts, colors, layouts, responsive
breakpoints) that subagents need for pixel-perfect replication.  Only strip
content that is a genuine injection vector and has no visual value.

Usage (standalone):
    python sanitize.py page_data.json --output page_data_sanitized.json

Usage (as library):
    from sanitize import sanitize_page_data
    clean = sanitize_page_data(page_data_dict)
"""

import argparse
import json
import logging
import re
import sys
from typing import Dict

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def sanitize_page_data(page_data: Dict) -> Dict:
    """
    Return a sanitized copy of *page_data*.

    What gets stripped from ``raw_html``:
      1. HTML comments  (``<!-- ... -->``) — can hide injected instructions
      2. ``<script>`` tag contents — executable code, real injection vector
         (the DOM extractor already captures the *rendered* result of scripts)
      3. Prompt-injection phrases inside CSS ``content:`` property values
      4. Suspiciously long or instruction-like ``alt`` / ``title`` attributes

    What is deliberately PRESERVED:
      - ``<style>`` tags — contain fonts, colors, layouts, variables, media
        queries essential for visual fidelity
      - Hidden elements (``display:none``, etc.) — used for responsive layouts,
        mobile menus, dropdowns, and accessibility
    """
    out = dict(page_data)
    raw = out.get('raw_html', '')
    if raw:
        raw = _strip_comments(raw)
        raw = _strip_tag_contents(raw, 'script')
        raw = _sanitize_style_contents(raw)
        raw = _sanitize_attributes(raw)
        out['raw_html'] = raw
    return out


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _strip_comments(html: str) -> str:
    """Remove all HTML comments."""
    return re.sub(r'<!--.*?-->', '', html, flags=re.DOTALL)


def _strip_tag_contents(html: str, tag: str) -> str:
    """Remove everything between <tag …> and </tag>, keeping no trace."""
    pattern = rf'<{tag}\b[^>]*>.*?</{tag}\s*>'
    return re.sub(pattern, '', html, flags=re.DOTALL | re.IGNORECASE)


# ---------------------------------------------------------------------------
# Surgical <style> sanitization — preserve CSS, scrub injection attempts
# ---------------------------------------------------------------------------

# Matches CSS content: "..." or content: '...' property values, which are the
# only place inside a stylesheet where arbitrary attacker-controlled text can
# appear and potentially be seen by the LLM.
_CSS_CONTENT_PROP_RE = re.compile(
    r'(content\s*:\s*)'           # property name + colon
    r'(["\'])'                    # opening quote
    r'(.*?)'                      # value
    r'(\2)',                       # matching closing quote
    re.DOTALL | re.IGNORECASE,
)

# Reuse the same injection-phrase detector for CSS content values.
_INJECTION_PHRASES = re.compile(
    r'(?:ignore\s+(?:all\s+)?(?:previous\s+)?instructions|'
    r'system\s*(?:override|instruction|prompt)|'
    r'you\s+are\s+no\s+longer|'
    r'do\s+not\s+generate|'
    r'instead\s*[:,]\s*(?:read|write|execute|create|add|run|curl|fetch|import)|'
    r'(?:child_process|process\.env|require\s*\(|eval\s*\(|exec\s*\())',
    re.IGNORECASE,
)


def _sanitize_style_contents(html: str) -> str:
    """Sanitize CSS content inside <style> tags without removing the styles.

    Only scrubs ``content: "..."`` property values that contain
    prompt-injection phrases.  All other CSS (fonts, colors, layouts,
    variables, media queries, keyframes) passes through untouched.
    """
    def _sanitize_single_style(m: re.Match) -> str:
        open_tag = m.group(1)
        css_body = m.group(2)
        close_tag = m.group(3)

        # Scrub suspicious content: property values within this <style> block
        css_body = _CSS_CONTENT_PROP_RE.sub(_scrub_css_content_value, css_body)
        return f'{open_tag}{css_body}{close_tag}'

    # Match <style ...>...</style> and process each block
    return re.sub(
        r'(<style\b[^>]*>)(.*?)(</style\s*>)',
        _sanitize_single_style,
        html,
        flags=re.DOTALL | re.IGNORECASE,
    )


def _scrub_css_content_value(m: re.Match) -> str:
    """Replace a CSS content value if it contains injection phrases."""
    prop = m.group(1)
    open_quote = m.group(2)
    value = m.group(3)
    close_quote = m.group(4)

    if _INJECTION_PHRASES.search(value):
        return f'{prop}{open_quote}{close_quote}'
    return m.group(0)


# ---------------------------------------------------------------------------
# Attribute sanitization
# ---------------------------------------------------------------------------

# Attributes whose values should be length-limited and scrubbed for
# instruction-like content.
_SUSPICIOUS_ATTR_RE = re.compile(
    r'(\b(?:alt|title)\s*=\s*["\'])'   # attribute opener
    r'([^"\']*)'                        # attribute value
    r'(["\'])',                          # closing quote
    re.IGNORECASE,
)

_MAX_ATTR_LENGTH = 200  # characters


def _sanitize_attributes(html: str) -> str:
    """Truncate / scrub alt and title attributes that look like injections."""

    def _replace(m: re.Match) -> str:
        opener = m.group(1)
        value = m.group(2)
        closer = m.group(3)

        # If the value contains instruction-like phrasing, blank it entirely.
        if _INJECTION_PHRASES.search(value):
            return f'{opener}{closer}'

        # Truncate overly long values (legitimate alt text is rarely >200 chars).
        if len(value) > _MAX_ATTR_LENGTH:
            value = value[:_MAX_ATTR_LENGTH]

        return f'{opener}{value}{closer}'

    return _SUSPICIOUS_ATTR_RE.sub(_replace, html)


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description='Sanitize extracted page data before chunking (security layer)',
    )
    parser.add_argument('input', help='Input page_data.json file')
    parser.add_argument('--output', '-o', default=None,
                        help='Output file (default: overwrite input)')
    args = parser.parse_args()

    try:
        with open(args.input, 'r', encoding='utf-8') as f:
            page_data = json.load(f)
    except Exception as e:
        logger.error(f"Failed to load: {e}")
        sys.exit(1)

    sanitized = sanitize_page_data(page_data)

    output_path = args.output or args.input
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(sanitized, f, indent=2, ensure_ascii=False)

    logger.info(f"Sanitized page data written to {output_path}")


if __name__ == '__main__':
    main()
