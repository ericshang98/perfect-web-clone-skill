#!/usr/bin/env python3
"""
Perfect Web Clone - Content Chunker
Intelligently splits page content into independent sections following the Three Principles.

Three Principles:
1. Mutual Exclusivity - Chunks NEVER overlap
2. Complete Coverage - All chunks combined = entire page (no gaps)
3. Size Control - Each chunk < 50,000 tokens

Usage:
    python chunk_content.py <page_data.json> [options]

Options:
    --output, -o        Output directory (default: chunks/)
    --max-tokens        Maximum tokens per chunk (default: 50000)
    --min-tokens        Minimum tokens per chunk (default: 50)

Example:
    python chunk_content.py page_data.json -o chunks/ --max-tokens 50000
"""

import argparse
import json
import logging
import os
import re
import sys
from typing import Dict, List, Any, Optional, Tuple

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class ContentChunker:
    """
    Intelligent content chunker implementing the Three Principles.
    """

    # Token limits
    MAX_TOKENS = 50000  # ~200,000 characters
    MIN_TOKENS = 50

    # Size thresholds
    MIN_SECTION_HEIGHT = 50  # pixels
    MIN_SECTION_WIDTH_RATIO = 0.2  # 20% of page width

    # Tags to skip
    SKIP_TAGS = {'script', 'style', 'head', 'meta', 'link', 'noscript', 'svg', 'path', 'br', 'hr'}

    # Horizontal overlap threshold for detecting side-by-side elements
    HORIZONTAL_OVERLAP_THRESHOLD = 0.3

    def __init__(self, max_tokens: int = 50000, min_tokens: int = 50):
        self.max_tokens = max_tokens
        self.min_tokens = min_tokens
        self.page_width = 0
        self.page_height = 0
        self.raw_html = ""

    def chunk(self, page_data: Dict) -> Tuple[List[Dict], Dict]:
        """
        Main chunking method.

        Args:
            page_data: Extracted page data from extract_page.py

        Returns:
            Tuple of (sections list, validation report)
        """
        # Get page dimensions
        metadata = page_data.get('metadata', {})
        self.page_width = metadata.get('page_width', 1920)
        self.page_height = metadata.get('page_height', 1080)
        self.raw_html = page_data.get('raw_html', '')

        dom_tree = page_data.get('dom_tree')
        if not dom_tree:
            logger.error("No DOM tree found in page data")
            return [], {'errors': ['No DOM tree found'], 'principles_met': False}

        logger.info(f"Page dimensions: {self.page_width}x{self.page_height}")

        # Step 1: Extract raw sections from DOM tree
        sections = self._extract_sections_recursive(dom_tree)
        logger.info(f"Step 1: Extracted {len(sections)} raw sections")

        # Step 2: Split large sections (Principle 3)
        sections = self._split_large_sections(sections)
        logger.info(f"Step 2: After splitting: {len(sections)} sections")

        # Step 3: Handle horizontal layouts
        sections = self._handle_horizontal_layout(sections)
        logger.info(f"Step 3: After horizontal handling: {len(sections)} sections")

        # Step 4: Remove overlaps (Principle 1)
        sections = self._remove_overlaps(sections)
        logger.info(f"Step 4: After removing overlaps: {len(sections)} sections")

        # Step 5: Merge gaps (Principle 2)
        sections = self._merge_gaps(sections)
        logger.info(f"Step 5: After merging gaps: {len(sections)} sections")

        # Step 6: Validate Three Principles
        validation = self._validate_three_principles(sections)
        logger.info(f"Step 6: Validation complete - principles_met: {validation['principles_met']}")

        # Step 7: Finalize sections with HTML content
        sections = self._finalize_sections(sections)
        logger.info(f"Step 7: Finalized {len(sections)} sections")

        return sections, validation

    def _extract_sections_recursive(self, dom_tree: Dict) -> List[Dict]:
        """Extract sections from DOM tree."""
        sections = []
        min_width = self.page_width * self.MIN_SECTION_WIDTH_RATIO

        def estimate_tokens(node: Dict) -> int:
            return node.get('inner_html_length', 0) // 4

        def is_valid_section(node: Dict) -> bool:
            tag = node.get('tag', '').lower()
            if tag in self.SKIP_TAGS:
                return False

            rect = node.get('rect', {})
            if rect.get('height', 0) < self.MIN_SECTION_HEIGHT:
                return False

            tokens = estimate_tokens(node)
            if rect.get('width', 0) < min_width and tokens < 1000:
                return False

            return True

        def create_section(node: Dict) -> Dict:
            rect = node.get('rect', {})
            styles = node.get('styles', {})

            return {
                'tag': node.get('tag', 'div'),
                'id': node.get('id'),
                'classes': node.get('classes', []),
                'selector': self._generate_selector(node),
                'type': 'section',
                'rect': {
                    'x': rect.get('x', 0),
                    'y': rect.get('y', 0),
                    'width': rect.get('width', 0),
                    'height': rect.get('height', 0),
                    'top': rect.get('top', 0),
                    'bottom': rect.get('bottom', 0),
                    'left': rect.get('left', 0),
                    'right': rect.get('right', 0),
                },
                'styles': {
                    'background_color': styles.get('background_color'),
                    'background_image': styles.get('background_image'),
                    'color': styles.get('color'),
                    'padding': styles.get('padding'),
                },
                'inner_html_length': node.get('inner_html_length', 0),
                'estimated_tokens': estimate_tokens(node),
                'children_count': node.get('children_count', 0),
                'children': node.get('children', []),
            }

        def extract_from_node(node: Dict, depth: int = 0) -> List[Dict]:
            result = []
            tag = node.get('tag', '').lower()

            if tag in self.SKIP_TAGS:
                return result

            if not is_valid_section(node):
                for child in node.get('children', []):
                    result.extend(extract_from_node(child, depth + 1))
                return result

            tokens = estimate_tokens(node)
            if tokens < self.min_tokens:
                return result

            result.append(create_section(node))
            return result

        def find_main_content(node: Dict) -> List[Dict]:
            tag = node.get('tag', '').lower()

            if tag in ['html', 'body']:
                result = []
                for child in node.get('children', []):
                    result.extend(find_main_content(child))
                return result

            if tag == 'div':
                rect = node.get('rect', {})
                if (rect.get('width', 0) >= self.page_width * 0.9 and
                    rect.get('height', 0) >= self.page_height * 0.9):
                    result = []
                    for child in node.get('children', []):
                        result.extend(find_main_content(child))
                    if result:
                        return result

            return [node]

        main_nodes = find_main_content(dom_tree)
        for node in main_nodes:
            sections.extend(extract_from_node(node))

        return sections

    def _generate_selector(self, node: Dict) -> str:
        """Generate CSS selector for node."""
        if node.get('id'):
            return f"#{node['id']}"

        selector = node.get('tag', 'div').lower()
        classes = node.get('classes', [])

        if classes:
            for cls in classes:
                if cls and not cls[0].isdigit() and not cls.startswith('-'):
                    selector += f".{cls}"
                    break

        return selector

    def _split_large_sections(self, sections: List[Dict]) -> List[Dict]:
        """Split sections that exceed max tokens (Principle 3)."""
        result = []

        def split_section(section: Dict) -> List[Dict]:
            tokens = section.get('estimated_tokens', 0)

            if tokens <= self.max_tokens:
                return [section]

            children = section.get('children', [])
            if not children:
                logger.warning(f"Cannot split section with {tokens} tokens (no children)")
                return [section]

            child_sections = []
            for child in children:
                tag = child.get('tag', '').lower()
                if tag in self.SKIP_TAGS:
                    continue

                rect = child.get('rect', {})
                if rect.get('height', 0) < self.MIN_SECTION_HEIGHT:
                    continue

                child_tokens = child.get('inner_html_length', 0) // 4
                if child_tokens < self.min_tokens:
                    continue

                child_section = {
                    'tag': child.get('tag', 'div'),
                    'id': child.get('id'),
                    'classes': child.get('classes', []),
                    'selector': self._generate_selector(child),
                    'type': 'section',
                    'rect': {
                        'x': rect.get('x', 0),
                        'y': rect.get('y', 0),
                        'width': rect.get('width', 0),
                        'height': rect.get('height', 0),
                        'top': rect.get('top', 0),
                        'bottom': rect.get('bottom', 0),
                        'left': rect.get('left', 0),
                        'right': rect.get('right', 0),
                    },
                    'styles': child.get('styles', {}),
                    'inner_html_length': child.get('inner_html_length', 0),
                    'estimated_tokens': child_tokens,
                    'children_count': child.get('children_count', 0),
                    'children': child.get('children', []),
                }

                child_sections.extend(split_section(child_section))

            return child_sections if child_sections else [section]

        for section in sections:
            result.extend(split_section(section))

        return result

    def _handle_horizontal_layout(self, sections: List[Dict]) -> List[Dict]:
        """Handle side-by-side elements (e.g., card grids)."""
        if len(sections) <= 1:
            return sections

        sections.sort(key=lambda s: (s['rect']['y'], s['rect']['x']))

        groups = []
        current_group = [sections[0]]

        for i in range(1, len(sections)):
            current = sections[i]
            prev = current_group[-1]

            overlap_top = max(current['rect']['top'], prev['rect']['top'])
            overlap_bottom = min(current['rect']['bottom'], prev['rect']['bottom'])
            overlap_height = max(0, overlap_bottom - overlap_top)

            current_height = current['rect']['bottom'] - current['rect']['top']
            prev_height = prev['rect']['bottom'] - prev['rect']['top']
            min_height = min(current_height, prev_height)

            if min_height > 0 and overlap_height / min_height > self.HORIZONTAL_OVERLAP_THRESHOLD:
                current_group.append(current)
            else:
                groups.append(current_group)
                current_group = [current]

        groups.append(current_group)

        result = []
        for group in groups:
            group.sort(key=lambda s: s['rect']['x'])
            result.extend(group)

        return result

    def _remove_overlaps(self, sections: List[Dict]) -> List[Dict]:
        """Remove overlapping sections, keeping the one with more content (Principle 1)."""
        if len(sections) <= 1:
            return sections

        kept = []

        for section in sections:
            s_rect = section['rect']
            s_area = s_rect['width'] * s_rect['height']

            is_redundant = False
            remove_existing = None

            for k in kept:
                k_rect = k['rect']

                overlap_left = max(s_rect['left'], k_rect['left'])
                overlap_right = min(s_rect['right'], k_rect['right'])
                overlap_top = max(s_rect['top'], k_rect['top'])
                overlap_bottom = min(s_rect['bottom'], k_rect['bottom'])

                overlap_width = max(0, overlap_right - overlap_left)
                overlap_height = max(0, overlap_bottom - overlap_top)
                overlap_area = overlap_width * overlap_height

                min_area = min(s_area, k_rect['width'] * k_rect['height'])
                if min_area > 0 and overlap_area / min_area > 0.5:
                    if section['estimated_tokens'] > k['estimated_tokens']:
                        remove_existing = k
                        break
                    else:
                        is_redundant = True
                        break

            if remove_existing:
                kept.remove(remove_existing)
                kept.append(section)
            elif not is_redundant:
                kept.append(section)

        return kept

    def _merge_gaps(self, sections: List[Dict]) -> List[Dict]:
        """Extend sections to fill gaps (Principle 2)."""
        if not sections:
            return sections

        sections.sort(key=lambda s: s['rect']['y'])

        gap_threshold = 30

        # Handle top gap
        first = sections[0]
        if first['rect']['top'] > gap_threshold:
            first['rect']['top'] = 0
            first['rect']['y'] = 0
            first['rect']['height'] = first['rect']['bottom']

        # Handle middle gaps
        for i in range(1, len(sections)):
            prev = sections[i - 1]
            current = sections[i]

            gap = current['rect']['top'] - prev['rect']['bottom']
            if gap > gap_threshold:
                midpoint = prev['rect']['bottom'] + gap / 2
                prev['rect']['bottom'] = midpoint
                prev['rect']['height'] = prev['rect']['bottom'] - prev['rect']['top']
                current['rect']['top'] = midpoint
                current['rect']['y'] = midpoint
                current['rect']['height'] = current['rect']['bottom'] - current['rect']['top']

        # Handle bottom gap
        last = sections[-1]
        if self.page_height - last['rect']['bottom'] > gap_threshold:
            last['rect']['bottom'] = self.page_height
            last['rect']['height'] = last['rect']['bottom'] - last['rect']['top']

        return sections

    def _validate_three_principles(self, sections: List[Dict]) -> Dict:
        """Validate the Three Principles."""
        errors = []
        warnings = []

        # Principle 1: Check overlaps
        for i, s1 in enumerate(sections):
            for j, s2 in enumerate(sections):
                if i >= j:
                    continue

                overlap_left = max(s1['rect']['left'], s2['rect']['left'])
                overlap_right = min(s1['rect']['right'], s2['rect']['right'])
                overlap_top = max(s1['rect']['top'], s2['rect']['top'])
                overlap_bottom = min(s1['rect']['bottom'], s2['rect']['bottom'])

                if overlap_left < overlap_right and overlap_top < overlap_bottom:
                    overlap_area = (overlap_right - overlap_left) * (overlap_bottom - overlap_top)
                    if overlap_area > 100:
                        warnings.append(f"Overlap: section {i+1} and {j+1} ({overlap_area:.0f}px²)")

        # Principle 2: Check coverage
        if sections:
            total_coverage = sum(s['rect']['width'] * s['rect']['height'] for s in sections)
            page_area = self.page_width * self.page_height
            coverage_ratio = total_coverage / page_area if page_area > 0 else 0

            if coverage_ratio < 0.8:
                warnings.append(f"Low coverage: {coverage_ratio*100:.1f}% of page")

        # Principle 3: Check token limits
        for i, s in enumerate(sections):
            tokens = s.get('estimated_tokens', 0)
            if tokens > self.max_tokens:
                errors.append(f"Section {i+1} exceeds {self.max_tokens} tokens: {tokens}")

        # Stats
        token_counts = [s.get('estimated_tokens', 0) for s in sections]
        stats = {
            'total_sections': len(sections),
            'total_tokens': sum(token_counts),
            'avg_tokens': sum(token_counts) // len(sections) if sections else 0,
            'max_tokens': max(token_counts) if token_counts else 0,
            'min_tokens': min(token_counts) if token_counts else 0,
        }

        return {
            'errors': errors,
            'warnings': warnings,
            'principles_met': len(errors) == 0,
            'stats': stats
        }

    def _finalize_sections(self, sections: List[Dict]) -> List[Dict]:
        """Finalize sections with HTML content and sequential naming."""
        sections.sort(key=lambda s: (s['rect']['y'], s['rect']['x']))

        finalized = []
        for idx, section in enumerate(sections):
            # Extract HTML from raw_html if available
            html = self._extract_html_for_section(section)

            finalized.append({
                'id': f'section-{idx + 1}',
                'name': f'section_{idx + 1}',
                'type': 'section',
                'selector': section['selector'],
                'rect': section['rect'],
                'styles': section.get('styles', {}),
                'html': html,
                'estimated_tokens': len(html) // 4 if html else section.get('estimated_tokens', 0),
                'images': self._extract_images_from_html(html),
                'links': self._extract_links_from_html(html),
            })

        return finalized

    def _extract_html_for_section(self, section: Dict) -> str:
        """Extract HTML content for a section from raw HTML."""
        if not self.raw_html:
            return ""

        selector = section.get('selector', '')
        tag = section.get('tag', 'div')
        element_id = section.get('id')
        classes = section.get('classes', [])

        # Strategy 1: Search by ID
        if element_id:
            pattern = f'<{tag}[^>]*id=["\']?{re.escape(element_id)}["\']?[^>]*>'
            match = re.search(pattern, self.raw_html, re.IGNORECASE)
            if match:
                start = match.start()
                end = self._find_closing_tag(self.raw_html, start, tag)
                if end > start:
                    return self.raw_html[start:end]

        # Strategy 2: Search by class
        if classes and classes[0]:
            first_class = classes[0]
            if not first_class[0].isdigit():
                pattern = f'<{tag}[^>]*class=["\'][^"\']*{re.escape(first_class)}[^"\']*["\'][^>]*>'
                match = re.search(pattern, self.raw_html, re.IGNORECASE)
                if match:
                    start = match.start()
                    end = self._find_closing_tag(self.raw_html, start, tag)
                    if end > start:
                        return self.raw_html[start:end]

        return ""

    def _find_closing_tag(self, html: str, start: int, tag: str) -> int:
        """Find the matching closing tag position."""
        open_tag = f'<{tag}'
        close_tag = f'</{tag}>'

        depth = 0
        pos = start

        while pos < len(html):
            next_open = html.lower().find(open_tag.lower(), pos)
            next_close = html.lower().find(close_tag.lower(), pos)

            if next_close == -1:
                return len(html)

            if next_open != -1 and next_open < next_close:
                depth += 1
                pos = next_open + len(open_tag)
            else:
                if depth == 0:
                    return next_close + len(close_tag)
                depth -= 1
                pos = next_close + len(close_tag)

        return len(html)

    def _extract_images_from_html(self, html: str) -> List[Dict]:
        """Extract images from HTML."""
        images = []
        pattern = r'<img[^>]*src=["\']([^"\']+)["\'][^>]*(?:alt=["\']([^"\']*)["\'])?[^>]*>'

        for match in re.finditer(pattern, html, re.IGNORECASE):
            images.append({
                'src': match.group(1),
                'alt': match.group(2) or ''
            })

        return images[:20]  # Limit to 20

    def _extract_links_from_html(self, html: str) -> List[Dict]:
        """Extract links from HTML."""
        links = []
        pattern = r'<a[^>]*href=["\']([^"\']+)["\'][^>]*>([^<]*)</a>'

        for match in re.finditer(pattern, html, re.IGNORECASE):
            links.append({
                'href': match.group(1),
                'text': match.group(2).strip()
            })

        return links[:20]  # Limit to 20


def main():
    parser = argparse.ArgumentParser(description='Chunk page content following Three Principles')
    parser.add_argument('input', help='Input page_data.json file')
    parser.add_argument('--output', '-o', default='chunks', help='Output directory')
    parser.add_argument('--max-tokens', type=int, default=50000, help='Maximum tokens per chunk')
    parser.add_argument('--min-tokens', type=int, default=50, help='Minimum tokens per chunk')

    args = parser.parse_args()

    # Load page data
    logger.info(f"Loading page data from {args.input}")
    try:
        with open(args.input, 'r', encoding='utf-8') as f:
            page_data = json.load(f)
    except Exception as e:
        logger.error(f"Failed to load page data: {e}")
        sys.exit(1)

    if not page_data.get('success'):
        logger.error("Page data indicates extraction failed")
        sys.exit(1)

    # Create chunker and process
    chunker = ContentChunker(max_tokens=args.max_tokens, min_tokens=args.min_tokens)
    sections, validation = chunker.chunk(page_data)

    # Create output directory
    os.makedirs(args.output, exist_ok=True)

    # Save each section
    for section in sections:
        output_file = os.path.join(args.output, f"{section['name']}.json")
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(section, f, indent=2, ensure_ascii=False)
        logger.info(f"Saved {section['name']} ({section['estimated_tokens']} tokens)")

    # Save validation report
    validation_file = os.path.join(args.output, '_validation.json')
    with open(validation_file, 'w', encoding='utf-8') as f:
        json.dump(validation, f, indent=2)

    # Summary
    logger.info("=" * 50)
    logger.info("Chunking Complete!")
    logger.info(f"  Total sections: {len(sections)}")
    logger.info(f"  Output directory: {args.output}")
    logger.info(f"  Principles met: {validation['principles_met']}")

    if validation['stats']:
        stats = validation['stats']
        logger.info(f"  Total tokens: {stats['total_tokens']}")
        logger.info(f"  Average tokens/section: {stats['avg_tokens']}")
        logger.info(f"  Max tokens: {stats['max_tokens']}")

    if validation['warnings']:
        logger.warning(f"  Warnings: {len(validation['warnings'])}")
        for w in validation['warnings']:
            logger.warning(f"    - {w}")

    if validation['errors']:
        logger.error(f"  Errors: {len(validation['errors'])}")
        for e in validation['errors']:
            logger.error(f"    - {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
