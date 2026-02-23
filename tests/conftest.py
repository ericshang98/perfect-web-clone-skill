"""Shared fixtures for security tests."""
import json
import os
import pytest

FIXTURES_DIR = os.path.join(os.path.dirname(__file__), "fixtures")


@pytest.fixture
def fixtures_dir():
    return FIXTURES_DIR


@pytest.fixture
def make_page_data():
    """Factory fixture to create page_data dicts with custom raw_html and DOM trees."""

    def _make(raw_html="", dom_tree=None, page_width=1920, page_height=1080):
        if dom_tree is None:
            dom_tree = {
                "tag": "body",
                "id": None,
                "classes": [],
                "rect": {
                    "x": 0, "y": 0, "width": page_width, "height": page_height,
                    "top": 0, "bottom": page_height, "left": 0, "right": page_width,
                },
                "styles": {},
                "text_content": "",
                "inner_html_length": len(raw_html),
                "attributes": {},
                "is_visible": True,
                "is_interactive": False,
                "children": [],
                "children_count": 0,
                "xpath": "/body",
            }
        return {
            "success": True,
            "url": "https://example.com",
            "extracted_at": "2026-01-01T00:00:00",
            "metadata": {
                "url": "https://example.com",
                "title": "Test Page",
                "viewport_width": 1920,
                "viewport_height": 1080,
                "page_width": page_width,
                "page_height": page_height,
                "total_elements": 1,
                "max_depth": 1,
                "load_time_ms": 100,
            },
            "dom_tree": dom_tree,
            "style_summary": {},
            "assets": {"images": [], "scripts": [], "stylesheets": [], "fonts": []},
            "screenshot": "",
            "raw_html": raw_html,
            "css_data": {"variables": [], "animations": [], "transitions": [], "media_queries": {}},
        }

    return _make
