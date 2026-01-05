# Intelligent Chunking Algorithm

The chunking algorithm is the core of Perfect Web Clone. It transforms a complex webpage into independent, manageable sections that can be processed in parallel.

## The Three Principles

### Principle 1: Mutual Exclusivity (No Overlap)

**Definition**: Any two chunks MUST NOT share DOM regions.

**Why It Matters**:
- Prevents duplicate code generation
- Eliminates merge conflicts when assembling
- Each subagent works on truly isolated content

**Implementation**:
```
For each pair of sections (A, B):
  1. Calculate bounding box overlap:
     overlap_left = max(A.left, B.left)
     overlap_right = min(A.right, B.right)
     overlap_top = max(A.top, B.top)
     overlap_bottom = min(A.bottom, B.bottom)

  2. If overlap area > threshold:
     - Keep the section with more content (higher token count)
     - Discard the other
```

**Validation**:
```python
def validate_no_overlap(sections):
    for i, s1 in enumerate(sections):
        for j, s2 in enumerate(sections):
            if i >= j:
                continue
            overlap = calculate_overlap(s1.rect, s2.rect)
            if overlap > 100:  # 100px² threshold
                raise ValidationError(f"Sections {i} and {j} overlap")
```

---

### Principle 2: Complete Coverage (No Gaps)

**Definition**: All chunks combined must equal the entire page (y=0 to y=pageHeight).

**Why It Matters**:
- No content is lost
- The cloned page is visually complete
- Users see exactly what they asked to clone

**Implementation**:
```
1. Sort sections by Y coordinate (top to bottom)

2. Handle top gap:
   if first_section.top > 0:
     first_section.top = 0  # Extend to page top

3. Handle middle gaps:
   for each adjacent pair (prev, current):
     gap = current.top - prev.bottom
     if gap > threshold:
       # Split gap between sections
       midpoint = prev.bottom + gap/2
       prev.bottom = midpoint
       current.top = midpoint

4. Handle bottom gap:
   if last_section.bottom < page_height:
     last_section.bottom = page_height  # Extend to page bottom
```

**Key Decision**: We extend existing sections rather than creating empty "gap sections" because:
- Empty sections have no content to generate
- Extending maintains semantic coherence
- Simpler output for subagents

---

### Principle 3: Size Control (< 50K Tokens)

**Definition**: Each chunk must be smaller than 50,000 tokens (~200,000 characters).

**Why It Matters**:
- Fits within Claude's context window
- Prevents subagent overload
- Enables efficient parallel processing

**Implementation**:
```
function split_if_too_large(section):
    tokens = estimate_tokens(section)  # chars / 4

    if tokens <= 50000:
        return [section]

    # Need to split - use children
    children = section.children
    if not children:
        # Cannot split further, keep as-is (with warning)
        return [section]

    # Recursively process children
    result = []
    for child in children:
        if is_valid_section(child):
            result.extend(split_if_too_large(child))

    return result if result else [section]
```

**Token Estimation**:
```python
def estimate_tokens(section):
    # Rough estimate: 1 token ≈ 4 characters
    return section.inner_html_length // 4
```

---

## Section Detection

### Container Tags (Traverse Into)
```python
CONTAINER_TAGS = {'body', 'main', 'div', 'section', 'article'}
```
These are traversed to find meaningful sections inside.

### Skip Tags (Ignore)
```python
SKIP_TAGS = {'script', 'style', 'head', 'meta', 'link', 'noscript', 'svg', 'path', 'br', 'hr'}
```
These have no visual content and are skipped.

### Minimum Section Size
```python
MIN_SECTION_HEIGHT = 50      # pixels
MIN_SECTION_WIDTH_RATIO = 0.2  # 20% of page width
MIN_SECTION_TOKENS = 50      # minimum content
```
Sections smaller than this are merged with neighbors.

---

## Handling Horizontal Layouts

Modern pages often have side-by-side elements (e.g., two-column layouts, card grids).

**Detection**:
```
Two sections are "horizontal neighbors" if:
  vertical_overlap / min_height > 0.3  (30% overlap)
```

**Ordering**:
```
1. Group sections by vertical position (rows)
2. Within each row, sort left-to-right
3. Process rows top-to-bottom
```

**Result**: A grid of cards becomes `section_1`, `section_2`, `section_3`... in reading order.

---

## Output Format

Each chunk is saved as a JSON file:

```json
{
  "id": "section-1",
  "name": "section_1",
  "type": "section",
  "selector": "header.main-nav",
  "rect": {
    "x": 0,
    "y": 0,
    "width": 1920,
    "height": 80,
    "top": 0,
    "bottom": 80,
    "left": 0,
    "right": 1920
  },
  "styles": {
    "background_color": "rgb(255, 255, 255)",
    "color": "rgb(0, 0, 0)",
    "padding": "16px 24px"
  },
  "html": "<header class=\"main-nav\">...</header>",
  "images": [
    {"src": "https://example.com/logo.png", "alt": "Logo"}
  ],
  "links": [
    {"href": "/about", "text": "About"}
  ],
  "estimated_tokens": 1250
}
```

---

## Validation Report

After chunking, a validation report is generated:

```json
{
  "principles_met": true,
  "section_count": 12,
  "errors": [],
  "warnings": [
    "Low coverage: 85% of page area"
  ],
  "stats": {
    "total_tokens": 45000,
    "avg_tokens_per_section": 3750,
    "max_tokens": 8500,
    "min_tokens": 120
  }
}
```

---

## Algorithm Pseudocode

```python
def chunk_page(dom_tree, page_width, page_height):
    # Step 1: Extract raw sections from DOM
    sections = extract_sections_recursive(dom_tree)

    # Step 2: Split large sections (Principle 3)
    sections = split_large_sections(sections, max_tokens=50000)

    # Step 3: Handle horizontal layouts
    sections = handle_horizontal_layout(sections)

    # Step 4: Remove overlaps (Principle 1)
    sections = remove_overlaps(sections)

    # Step 5: Fill gaps (Principle 2)
    sections = merge_gaps(sections, page_height)

    # Step 6: Validate
    validation = validate_three_principles(sections)

    # Step 7: Uniform naming
    for i, section in enumerate(sections):
        section.name = f"section_{i + 1}"

    return sections, validation
```

---

## Performance

| Page Complexity | Sections | Chunking Time |
|-----------------|----------|---------------|
| Simple landing | 5-10 | < 1s |
| Corporate site | 15-30 | 1-2s |
| E-commerce | 30-50 | 2-3s |
| Complex SaaS | 50-100 | 3-5s |

The algorithm is O(n log n) where n is the number of DOM nodes.
