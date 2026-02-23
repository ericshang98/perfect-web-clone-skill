#!/usr/bin/env python3
"""
Perfect Web Clone - Content Sanitizer
Strips potentially dangerous content from extracted page data before chunking.

Addresses C1 (Indirect Prompt Injection): malicious webpages can embed hidden
instructions in HTML comments, <script> tags, display:none elements, and
attribute values.  This module removes those vectors so that downstream
subagent prompts never see attacker-controlled instructions.

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
      1. HTML comments  (``<!-- ... -->``)
      2. ``<script>`` tag contents
      3. ``<style>``  tag contents
      4. Content inside elements with ``display:none``, ``visibility:hidden``,
         or ``position:absolute; left:-9999`` (common injection hiding patterns)
      5. Suspiciously long or instruction-like ``alt`` / ``title`` attributes

    The returned dict is a shallow copy — only ``raw_html`` is replaced.
    """
    out = dict(page_data)
    raw = out.get('raw_html', '')
    if raw:
        raw = _strip_comments(raw)
        raw = _strip_tag_contents(raw, 'script')
        raw = _strip_tag_contents(raw, 'style')
        raw = _strip_hidden_elements(raw)
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


_HIDDEN_PATTERNS = [
    # display:none (with optional surrounding whitespace / quotes)
    re.compile(
        r'<([a-z]\w*)\b([^>]*?(?:display\s*:\s*none|'
        r'visibility\s*:\s*hidden|'
        r'position\s*:\s*absolute[^"\']*left\s*:\s*-\d{4,})[^>]*)>'
        r'(.*?)'
        r'</\1\s*>',
        re.DOTALL | re.IGNORECASE,
    ),
]


def _strip_hidden_elements(html: str) -> str:
    """Remove elements whose inline style makes them invisible.

    Targets the three most common injection-hiding patterns:
      - style="display:none"
      - style="visibility:hidden"
      - style="position:absolute; left:-9999px"
    """
    for pat in _HIDDEN_PATTERNS:
        html = pat.sub('', html)
    return html


# Attributes whose values should be length-limited and scrubbed for
# instruction-like content.
_SUSPICIOUS_ATTR_RE = re.compile(
    r'(\b(?:alt|title)\s*=\s*["\'])'   # attribute opener
    r'([^"\']*)'                        # attribute value
    r'(["\'])',                          # closing quote
    re.IGNORECASE,
)

# Phrases that look like prompt-injection instructions inside attribute values.
_INSTRUCTION_PHRASES = re.compile(
    r'(?:ignore\s+(?:all\s+)?(?:previous\s+)?instructions|'
    r'system\s*(?:override|instruction|prompt)|'
    r'you\s+are\s+no\s+longer|'
    r'do\s+not\s+generate|'
    r'instead\s*[:,]\s*(?:read|write|execute|create|add|run|curl|fetch|import)|'
    r'(?:child_process|process\.env|require\s*\(|eval\s*\(|exec\s*\())',
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
        if _INSTRUCTION_PHRASES.search(value):
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
