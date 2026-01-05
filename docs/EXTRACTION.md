# Page Extraction Guide

The extraction phase captures everything needed to perfectly replicate a webpage.

## Overview

The `extract_page.py` script uses Playwright to:
1. Load the page in a headless browser
2. Scroll to trigger lazy loading
3. Extract 30+ types of data
4. Save results to JSON

## Data Types Extracted

### 1. Page Metadata
```json
{
  "url": "https://example.com",
  "title": "Page Title",
  "viewport": {"width": 1920, "height": 1080},
  "page_dimensions": {"width": 1920, "height": 5400},
  "total_elements": 1250,
  "max_depth": 15,
  "load_time_ms": 2340
}
```

### 2. DOM Tree Structure

Complete recursive tree of all elements:
```json
{
  "tag": "div",
  "id": "hero-section",
  "classes": ["hero", "bg-gradient"],
  "rect": {"x": 0, "y": 80, "width": 1920, "height": 600},
  "styles": {
    "display": "flex",
    "flex_direction": "column",
    "justify_content": "center",
    "background_color": "rgb(59, 130, 246)",
    "padding": "64px 32px"
  },
  "text_content": "Welcome to our platform",
  "attributes": {"data-section": "hero"},
  "children": [...]
}
```

**Extracted Style Properties** (30+):
- Layout: `display`, `position`, `float`
- Flexbox: `flex_direction`, `justify_content`, `align_items`, `gap`
- Grid: `grid_template_columns`, `grid_template_rows`
- Dimensions: `width`, `height`, `min_width`, `max_width`
- Spacing: `margin`, `padding` (all sides)
- Positioning: `top`, `right`, `bottom`, `left`, `z_index`
- Visual: `background_color`, `background_image`, `color`, `border`, `border_radius`, `box_shadow`, `opacity`
- Typography: `font_family`, `font_size`, `font_weight`, `line_height`, `text_align`
- Transform: `transform`

### 3. Screenshots

```json
{
  "screenshot": "base64_encoded_png...",
  "full_page_screenshot": "base64_encoded_png..."
}
```

- **Viewport screenshot**: What users see immediately
- **Full page screenshot**: Entire scrollable page

### 4. CSS Data

#### CSS Variables
```json
{
  "variables": [
    {"name": "--primary", "value": "#3b82f6", "scope": ":root"},
    {"name": "--background", "value": "#ffffff", "scope": ":root"},
    {"name": "--foreground", "value": "#000000", "scope": ":root"}
  ]
}
```

#### Animations (@keyframes)
```json
{
  "animations": [
    {
      "name": "fadeIn",
      "keyframes": [
        {"offset": "0%", "styles": {"opacity": "0"}},
        {"offset": "100%", "styles": {"opacity": "1"}}
      ]
    }
  ]
}
```

#### Transitions
```json
{
  "transitions": [
    {
      "selector": "button.primary",
      "property": "all",
      "duration": "0.3s",
      "timing_function": "ease-in-out"
    }
  ]
}
```

#### Pseudo Elements
```json
{
  "pseudo_elements": [
    {
      "selector": ".card",
      "pseudo": "::before",
      "styles": {"content": "''", "position": "absolute"},
      "content": "''"
    }
  ]
}
```

### 5. Theme Detection

Automatically detects light/dark mode support:
```json
{
  "theme_detection": {
    "support": "both",
    "current_mode": "light",
    "has_significant_difference": true,
    "detection_method": "style_comparison",
    "css_variables_diff_count": 15,
    "color_diff_count": 8
  }
}
```

If dark mode is supported, both theme variants are extracted.

### 6. Assets

#### Images
```json
{
  "images": [
    {"url": "https://example.com/hero.jpg", "type": "image"},
    {"url": "https://example.com/bg.png", "type": "background-image"}
  ]
}
```

#### Fonts
```json
{
  "fonts": [
    {"url": "https://fonts.gstatic.com/s/inter/v12/xxx.woff2", "type": "font"}
  ]
}
```

#### Scripts & Stylesheets
```json
{
  "scripts": [{"url": "https://example.com/main.js"}],
  "stylesheets": [{"url": "https://example.com/styles.css"}]
}
```

### 7. Interaction States

Captures hover/focus styles:
```json
{
  "hover_states": [
    {
      "selector": "button.primary",
      "state": "hover",
      "styles": {
        "backgroundColor": "rgb(29, 78, 216)",
        "transform": "translateY(-2px)"
      }
    }
  ]
}
```

### 8. Raw HTML

Complete page HTML source:
```json
{
  "raw_html": "<!DOCTYPE html><html>..."
}
```

---

## Usage

### Basic Extraction
```bash
python scripts/extract_page.py "https://example.com" --output page_data.json
```

### With Options
```bash
python scripts/extract_page.py "https://example.com" \
  --output page_data.json \
  --viewport 1920x1080 \
  --wait 3000 \
  --full-screenshot \
  --download-images
```

### Options

| Option | Default | Description |
|--------|---------|-------------|
| `--output`, `-o` | `page_data.json` | Output file path |
| `--viewport` | `1920x1080` | Browser viewport size |
| `--wait` | `3000` | Wait time after load (ms) |
| `--full-screenshot` | `false` | Capture full page screenshot |
| `--download-images` | `false` | Download images locally |
| `--max-depth` | `20` | Maximum DOM traversal depth |
| `--include-hidden` | `false` | Include hidden elements |

---

## Lazy Loading Handling

The extractor automatically scrolls the page to trigger lazy-loaded content:

```python
async def scroll_to_load_lazy_content(page):
    viewport_height = page.viewport_size['height']
    scroll_position = 0

    while scroll_position < page_height:
        await page.evaluate(f'window.scrollTo(0, {scroll_position})')
        await asyncio.sleep(0.3)  # Wait for content to load
        scroll_position += viewport_height

    # Return to top
    await page.evaluate('window.scrollTo(0, 0)')
```

This ensures:
- Infinite scroll content is captured
- Lazy-loaded images are rendered
- IntersectionObserver-based content is triggered

---

## Output File Structure

```json
{
  "success": true,
  "message": "Extraction complete",
  "metadata": {...},
  "screenshot": "base64...",
  "full_page_screenshot": "base64...",
  "dom_tree": {...},
  "style_summary": {...},
  "assets": {...},
  "raw_html": "...",
  "css_data": {...},
  "interaction_data": {...},
  "theme_detection": {...}
}
```

---

## Performance Tips

### For Fast Sites
```bash
python scripts/extract_page.py "https://fast-site.com" --wait 1000
```

### For Slow/Heavy Sites
```bash
python scripts/extract_page.py "https://heavy-site.com" --wait 5000
```

### For SPAs (Single Page Apps)
```bash
python scripts/extract_page.py "https://spa-site.com" --wait 5000 --wait-for-selector ".main-content"
```

---

## Troubleshooting

### "Playwright not found"
```bash
pip install playwright
playwright install chromium
```

### "Timeout waiting for page"
Increase wait time:
```bash
python scripts/extract_page.py "https://slow-site.com" --wait 10000
```

### "Cannot access cross-origin stylesheets"
This is expected for external CSS. The extractor captures computed styles instead.

### "Page requires authentication"
Currently not supported. Consider extracting a public page or implementing cookie injection.
