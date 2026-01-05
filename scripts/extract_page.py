#!/usr/bin/env python3
"""
Perfect Web Clone - Page Extractor
Extracts complete page data using Playwright for pixel-perfect cloning.

Usage:
    python extract_page.py <URL> [options]

Options:
    --output, -o        Output file path (default: page_data.json)
    --viewport          Viewport size WxH (default: 1920x1080)
    --wait              Wait time after load in ms (default: 3000)
    --full-screenshot   Capture full page screenshot
    --max-depth         Maximum DOM traversal depth (default: 20)

Example:
    python extract_page.py "https://example.com" -o page_data.json --viewport 1920x1080
"""

import asyncio
import argparse
import base64
import json
import logging
import sys
from datetime import datetime
from typing import Dict, Any, List, Optional
from urllib.parse import urljoin, urlparse

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class PageExtractor:
    """
    Playwright-based page extractor.
    Extracts DOM, styles, screenshots, and assets from any webpage.
    """

    # Style properties to extract
    STYLE_PROPS = [
        'display', 'position', 'float',
        'flexDirection', 'flexWrap', 'justifyContent', 'alignItems', 'alignContent', 'gap',
        'gridTemplateColumns', 'gridTemplateRows', 'gridColumn', 'gridRow',
        'width', 'height', 'minWidth', 'minHeight', 'maxWidth', 'maxHeight',
        'margin', 'marginTop', 'marginRight', 'marginBottom', 'marginLeft',
        'padding', 'paddingTop', 'paddingRight', 'paddingBottom', 'paddingLeft',
        'top', 'right', 'bottom', 'left', 'zIndex',
        'backgroundColor', 'backgroundImage', 'color', 'border', 'borderRadius',
        'boxShadow', 'opacity', 'overflow', 'visibility',
        'fontFamily', 'fontSize', 'fontWeight', 'lineHeight', 'textAlign',
        'transform'
    ]

    def __init__(self, viewport_width: int = 1920, viewport_height: int = 1080):
        self.viewport_width = viewport_width
        self.viewport_height = viewport_height
        self._browser = None
        self._playwright = None

    async def __aenter__(self):
        from playwright.async_api import async_playwright
        self._playwright = await async_playwright().start()
        self._browser = await self._playwright.chromium.launch(
            headless=True,
            args=['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage']
        )
        return self

    async def __aexit__(self, *args):
        if self._browser:
            await self._browser.close()
        if self._playwright:
            await self._playwright.stop()

    async def extract(self, url: str, wait_time: int = 3000, max_depth: int = 20,
                      full_screenshot: bool = False) -> Dict[str, Any]:
        """
        Extract complete page data.

        Args:
            url: Target URL
            wait_time: Wait time after page load (ms)
            max_depth: Maximum DOM traversal depth
            full_screenshot: Whether to capture full page screenshot

        Returns:
            Dict containing all extracted data
        """
        start_time = datetime.now()

        page = await self._browser.new_page(
            viewport={'width': self.viewport_width, 'height': self.viewport_height}
        )

        try:
            logger.info(f"Loading page: {url}")
            await page.goto(url, wait_until='load', timeout=60000)
            await asyncio.sleep(wait_time / 1000)

            # Scroll to load lazy content
            await self._scroll_page(page)

            load_time_ms = int((datetime.now() - start_time).total_seconds() * 1000)

            # Extract all data in parallel
            logger.info("Extracting page data...")

            results = await asyncio.gather(
                self._extract_metadata(page, url, load_time_ms),
                self._extract_dom_tree(page, max_depth),
                self._extract_assets(page),
                self._take_screenshot(page, full_page=full_screenshot),
                self._get_raw_html(page),
                self._extract_css_data(page),
                return_exceptions=True
            )

            # Parse results
            metadata = results[0] if not isinstance(results[0], Exception) else None
            dom_tree = results[1] if not isinstance(results[1], Exception) else None
            assets = results[2] if not isinstance(results[2], Exception) else None
            screenshot = results[3] if not isinstance(results[3], Exception) else None
            raw_html = results[4] if not isinstance(results[4], Exception) else None
            css_data = results[5] if not isinstance(results[5], Exception) else None

            # Compute style summary from DOM tree
            style_summary = self._compute_style_summary(dom_tree) if dom_tree else None

            # Log any errors
            for i, result in enumerate(results):
                if isinstance(result, Exception):
                    logger.error(f"Extraction task {i} failed: {result}")

            return {
                'success': True,
                'url': url,
                'extracted_at': datetime.now().isoformat(),
                'metadata': metadata,
                'dom_tree': dom_tree,
                'style_summary': style_summary,
                'assets': assets,
                'screenshot': screenshot,
                'raw_html': raw_html,
                'css_data': css_data
            }

        except Exception as e:
            logger.error(f"Extraction failed: {e}")
            return {
                'success': False,
                'url': url,
                'error': str(e)
            }
        finally:
            await page.close()

    async def _scroll_page(self, page, max_scrolls: int = 50, scroll_delay: float = 0.3):
        """Scroll page to trigger lazy loading."""
        try:
            dimensions = await page.evaluate('''() => ({
                viewportHeight: window.innerHeight,
                scrollHeight: document.body.scrollHeight
            })''')

            viewport_height = dimensions['viewportHeight']
            current_position = 0
            scroll_count = 0
            last_height = dimensions['scrollHeight']

            while scroll_count < max_scrolls:
                current_position += viewport_height
                await page.evaluate(f'window.scrollTo(0, {current_position})')
                await asyncio.sleep(scroll_delay)

                new_height = await page.evaluate('document.body.scrollHeight')
                scroll_count += 1

                if current_position >= new_height:
                    if new_height <= last_height:
                        break
                    last_height = new_height

            # Return to top
            await page.evaluate('window.scrollTo(0, 0)')
            await asyncio.sleep(0.5)

        except Exception as e:
            logger.warning(f"Scroll failed: {e}")
            try:
                await page.evaluate('window.scrollTo(0, 0)')
            except:
                pass

    async def _extract_metadata(self, page, url: str, load_time_ms: int) -> Dict:
        """Extract page metadata."""
        page_info = await page.evaluate('''() => ({
            title: document.title,
            viewportWidth: window.innerWidth,
            viewportHeight: window.innerHeight,
            pageWidth: document.documentElement.scrollWidth,
            pageHeight: document.documentElement.scrollHeight,
            totalElements: document.querySelectorAll('*').length
        })''')

        max_depth = await page.evaluate('''() => {
            function getDepth(element, currentDepth) {
                if (!element.children || element.children.length === 0) return currentDepth;
                let maxChildDepth = currentDepth;
                for (const child of element.children) {
                    const childDepth = getDepth(child, currentDepth + 1);
                    if (childDepth > maxChildDepth) maxChildDepth = childDepth;
                }
                return maxChildDepth;
            }
            return getDepth(document.body, 1);
        }''')

        return {
            'url': url,
            'title': page_info['title'],
            'viewport_width': page_info['viewportWidth'],
            'viewport_height': page_info['viewportHeight'],
            'page_width': page_info['pageWidth'],
            'page_height': page_info['pageHeight'],
            'total_elements': page_info['totalElements'],
            'max_depth': max_depth,
            'load_time_ms': load_time_ms
        }

    async def _extract_dom_tree(self, page, max_depth: int) -> Dict:
        """Extract complete DOM tree with styles."""
        dom_data = await page.evaluate('''(params) => {
            const { maxDepth } = params;

            const STYLE_PROPS = [
                'display', 'position', 'float',
                'flexDirection', 'flexWrap', 'justifyContent', 'alignItems', 'alignContent', 'gap',
                'gridTemplateColumns', 'gridTemplateRows', 'gridColumn', 'gridRow',
                'width', 'height', 'minWidth', 'minHeight', 'maxWidth', 'maxHeight',
                'margin', 'marginTop', 'marginRight', 'marginBottom', 'marginLeft',
                'padding', 'paddingTop', 'paddingRight', 'paddingBottom', 'paddingLeft',
                'top', 'right', 'bottom', 'left', 'zIndex',
                'backgroundColor', 'backgroundImage', 'color', 'border', 'borderRadius',
                'boxShadow', 'opacity', 'overflow', 'visibility',
                'fontFamily', 'fontSize', 'fontWeight', 'lineHeight', 'textAlign',
                'transform'
            ];

            const INTERACTIVE_TAGS = ['A', 'BUTTON', 'INPUT', 'SELECT', 'TEXTAREA'];
            const IMPORTANT_ATTRS = ['href', 'src', 'alt', 'title', 'type', 'name', 'placeholder', 'role'];

            function camelToSnake(str) {
                return str.replace(/([a-z])([A-Z])/g, '$1_$2').toLowerCase();
            }

            function isVisible(el, styles) {
                if (styles.display === 'none' || styles.visibility === 'hidden' || styles.opacity === '0') {
                    return false;
                }
                const rect = el.getBoundingClientRect();
                return rect.width > 0 && rect.height > 0;
            }

            function getDirectText(el) {
                let text = '';
                for (const node of el.childNodes) {
                    if (node.nodeType === Node.TEXT_NODE) {
                        text += node.textContent;
                    }
                }
                return text.trim().slice(0, 200);
            }

            function extractElement(el, depth, path) {
                if (depth > maxDepth) return null;

                const styles = window.getComputedStyle(el);
                const visible = isVisible(el, styles);
                const rect = el.getBoundingClientRect();

                const styleObj = {};
                for (const prop of STYLE_PROPS) {
                    const value = styles[prop];
                    if (value && value !== 'none' && value !== 'normal' && value !== 'auto' && value !== '0px') {
                        styleObj[camelToSnake(prop)] = value;
                    }
                }

                const attrs = {};
                for (const attrName of IMPORTANT_ATTRS) {
                    if (el.hasAttribute(attrName)) {
                        attrs[attrName] = el.getAttribute(attrName);
                    }
                }

                const children = [];
                let childIndex = 0;
                for (const child of el.children) {
                    const childInfo = extractElement(child, depth + 1, path + '/' + child.tagName.toLowerCase() + '[' + childIndex + ']');
                    if (childInfo) children.push(childInfo);
                    childIndex++;
                }

                return {
                    tag: el.tagName.toLowerCase(),
                    id: el.id || null,
                    classes: el.className && typeof el.className === 'string' ? el.className.trim().split(/\\s+/).filter(c => c) : [],
                    rect: {
                        x: rect.x, y: rect.y, width: rect.width, height: rect.height,
                        top: rect.top, right: rect.right, bottom: rect.bottom, left: rect.left
                    },
                    styles: styleObj,
                    text_content: getDirectText(el),
                    inner_html_length: el.innerHTML.length,
                    attributes: attrs,
                    is_visible: visible,
                    is_interactive: INTERACTIVE_TAGS.includes(el.tagName),
                    children: children,
                    children_count: el.children.length,
                    xpath: path
                };
            }

            return extractElement(document.body, 1, '/body');
        }''', {'maxDepth': max_depth})

        return dom_data

    async def _extract_assets(self, page) -> Dict:
        """Extract all page assets (images, scripts, stylesheets, fonts)."""
        assets_data = await page.evaluate('''() => {
            const result = { images: [], scripts: [], stylesheets: [], fonts: [] };

            // Images (including background images)
            document.querySelectorAll('img').forEach(img => {
                if (img.src) result.images.push({ url: img.src, type: 'image', alt: img.alt || '' });
            });

            document.querySelectorAll('*').forEach(el => {
                const bg = window.getComputedStyle(el).backgroundImage;
                if (bg && bg !== 'none' && bg.includes('url(')) {
                    const match = bg.match(/url\\(["']?([^"')]+)["']?\\)/);
                    if (match && match[1]) {
                        result.images.push({ url: match[1], type: 'background-image' });
                    }
                }
            });

            // Scripts
            document.querySelectorAll('script[src]').forEach(script => {
                result.scripts.push({ url: script.src, type: 'script' });
            });

            // Stylesheets
            document.querySelectorAll('link[rel="stylesheet"]').forEach(link => {
                result.stylesheets.push({ url: link.href, type: 'stylesheet' });
            });

            // Fonts
            for (const sheet of document.styleSheets) {
                try {
                    for (const rule of sheet.cssRules || []) {
                        if (rule instanceof CSSFontFaceRule) {
                            const src = rule.style.getPropertyValue('src');
                            const urlMatch = src.match(/url\\(["']?([^"')]+)["']?\\)/);
                            if (urlMatch && urlMatch[1]) {
                                result.fonts.push({ url: urlMatch[1], type: 'font' });
                            }
                        }
                    }
                } catch (e) {}
            }

            return result;
        }''')

        # Deduplicate
        def dedupe(items):
            seen = set()
            result = []
            for item in items:
                if item['url'] not in seen:
                    seen.add(item['url'])
                    result.append(item)
            return result

        return {
            'images': dedupe(assets_data['images']),
            'scripts': dedupe(assets_data['scripts']),
            'stylesheets': dedupe(assets_data['stylesheets']),
            'fonts': dedupe(assets_data['fonts']),
            'total_images': len(assets_data['images']),
            'total_scripts': len(assets_data['scripts']),
            'total_stylesheets': len(assets_data['stylesheets']),
            'total_fonts': len(assets_data['fonts'])
        }

    async def _take_screenshot(self, page, full_page: bool = True) -> str:
        """Take page screenshot and return base64 encoded."""
        screenshot_bytes = await page.screenshot(type='png', full_page=full_page)
        return base64.b64encode(screenshot_bytes).decode('utf-8')

    async def _get_raw_html(self, page) -> str:
        """Get complete page HTML."""
        return await page.content()

    async def _extract_css_data(self, page) -> Dict:
        """Extract CSS variables, animations, and transitions."""
        css_data = await page.evaluate('''() => {
            const result = {
                variables: [],
                animations: [],
                transitions: [],
                media_queries: {}
            };

            // CSS Variables from :root
            for (const sheet of document.styleSheets) {
                try {
                    for (const rule of sheet.cssRules || []) {
                        if (rule instanceof CSSStyleRule && rule.selectorText === ':root') {
                            for (let i = 0; i < rule.style.length; i++) {
                                const prop = rule.style[i];
                                if (prop.startsWith('--')) {
                                    result.variables.push({
                                        name: prop,
                                        value: rule.style.getPropertyValue(prop).trim()
                                    });
                                }
                            }
                        }

                        // @keyframes
                        if (rule instanceof CSSKeyframesRule) {
                            const keyframes = [];
                            for (const kf of rule.cssRules) {
                                keyframes.push({
                                    offset: kf.keyText,
                                    styles: kf.style.cssText
                                });
                            }
                            result.animations.push({ name: rule.name, keyframes: keyframes });
                        }

                        // @media
                        if (rule instanceof CSSMediaRule) {
                            result.media_queries[rule.conditionText] = rule.cssText.slice(0, 500);
                        }
                    }
                } catch (e) {}
            }

            // Transitions
            const seen = new Set();
            document.querySelectorAll('*').forEach(el => {
                const styles = getComputedStyle(el);
                const transitionProp = styles.transitionProperty;
                const transitionDur = styles.transitionDuration;

                if (transitionProp && transitionProp !== 'none' && transitionDur !== '0s') {
                    const selector = el.id ? `#${el.id}` :
                        (el.className && typeof el.className === 'string' ?
                            el.tagName.toLowerCase() + '.' + el.className.split(' ')[0] :
                            el.tagName.toLowerCase());

                    const key = selector + '_' + transitionProp;
                    if (!seen.has(key)) {
                        seen.add(key);
                        result.transitions.push({
                            selector: selector,
                            property: transitionProp,
                            duration: transitionDur,
                            timing_function: styles.transitionTimingFunction
                        });
                    }
                }
            });

            return result;
        }''')

        return css_data

    def _compute_style_summary(self, dom_tree: Dict) -> Dict:
        """Compute style statistics from DOM tree."""
        summary = {
            'colors': {},
            'background_colors': {},
            'font_families': {},
            'font_sizes': {},
            'display_types': {},
            'position_types': {}
        }

        def traverse(element):
            if not element:
                return

            styles = element.get('styles', {})

            if styles.get('color'):
                summary['colors'][styles['color']] = summary['colors'].get(styles['color'], 0) + 1
            if styles.get('background_color'):
                summary['background_colors'][styles['background_color']] = \
                    summary['background_colors'].get(styles['background_color'], 0) + 1
            if styles.get('font_family'):
                summary['font_families'][styles['font_family']] = \
                    summary['font_families'].get(styles['font_family'], 0) + 1
            if styles.get('font_size'):
                summary['font_sizes'][styles['font_size']] = \
                    summary['font_sizes'].get(styles['font_size'], 0) + 1
            if styles.get('display'):
                summary['display_types'][styles['display']] = \
                    summary['display_types'].get(styles['display'], 0) + 1
            if styles.get('position'):
                summary['position_types'][styles['position']] = \
                    summary['position_types'].get(styles['position'], 0) + 1

            for child in element.get('children', []):
                traverse(child)

        traverse(dom_tree)

        # Sort and limit to top 20
        for key in summary:
            sorted_items = sorted(summary[key].items(), key=lambda x: x[1], reverse=True)[:20]
            summary[key] = dict(sorted_items)

        return summary


async def main():
    parser = argparse.ArgumentParser(description='Extract webpage data for cloning')
    parser.add_argument('url', help='URL to extract')
    parser.add_argument('--output', '-o', default='page_data.json', help='Output file path')
    parser.add_argument('--viewport', default='1920x1080', help='Viewport size WxH')
    parser.add_argument('--wait', type=int, default=3000, help='Wait time after load (ms)')
    parser.add_argument('--full-screenshot', action='store_true', help='Capture full page screenshot')
    parser.add_argument('--max-depth', type=int, default=20, help='Maximum DOM traversal depth')

    args = parser.parse_args()

    # Parse viewport
    try:
        width, height = map(int, args.viewport.split('x'))
    except:
        width, height = 1920, 1080
        logger.warning(f"Invalid viewport format, using default {width}x{height}")

    logger.info(f"Starting extraction: {args.url}")
    logger.info(f"Viewport: {width}x{height}, Wait: {args.wait}ms")

    async with PageExtractor(viewport_width=width, viewport_height=height) as extractor:
        result = await extractor.extract(
            url=args.url,
            wait_time=args.wait,
            max_depth=args.max_depth,
            full_screenshot=args.full_screenshot
        )

    # Save result
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    if result['success']:
        logger.info(f"Extraction complete! Saved to {args.output}")
        if result.get('metadata'):
            logger.info(f"  - Page title: {result['metadata'].get('title', 'N/A')}")
            logger.info(f"  - Page size: {result['metadata'].get('page_width')}x{result['metadata'].get('page_height')}")
            logger.info(f"  - Total elements: {result['metadata'].get('total_elements')}")
        if result.get('assets'):
            logger.info(f"  - Images: {result['assets'].get('total_images', 0)}")
    else:
        logger.error(f"Extraction failed: {result.get('error')}")
        sys.exit(1)


if __name__ == '__main__':
    asyncio.run(main())
