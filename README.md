# Perfect Web Clone

<div align="center">

**AI-Powered Webpage Cloning - One Command, Pixel-Perfect Replication**

English | [中文](README_CN.md)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-8A2BE2)](https://claude.ai)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-3776AB.svg)](https://python.org)
[![Playwright](https://img.shields.io/badge/Playwright-Powered-45ba4b.svg)](https://playwright.dev)

</div>

---

**Perfect Web Clone** is an open-source Claude Code Skill that transforms any webpage into production-ready React/Next.js/Vue code. It uses Playwright for extraction, a Three-Principle algorithm for intelligent chunking, and parallel agents for code generation.

> Created by [Nexting.ai](https://nexting.ai)

---

## Table of Contents

- [Features](#features)
- [How It Works - Complete Workflow](#how-it-works---complete-workflow)
  - [Phase 1: Environment Setup](#phase-1-environment-setup)
  - [Phase 2: Page Extraction](#phase-2-page-extraction)
  - [Phase 3: Intelligent Chunking](#phase-3-intelligent-chunking)
  - [Phase 4: Parallel Code Generation](#phase-4-parallel-code-generation)
  - [Phase 5: Project Assembly](#phase-5-project-assembly)
- [Quick Start](#quick-start)
  - [Method 1: Personal Global Installation](#method-1-personal-global-installation)
  - [Method 2: Project-Level Installation](#method-2-project-level-installation)
- [Usage Examples](#usage-examples)
- [The Three Principles](#the-three-principles)
  - [Principle 1: Mutual Exclusivity](#principle-1-mutual-exclusivity)
  - [Principle 2: Complete Coverage](#principle-2-complete-coverage)
  - [Principle 3: Size Control](#principle-3-size-control)
- [Parallelism Configuration](#parallelism-configuration)
- [Supported Tech Stacks](#supported-tech-stacks)
- [FAQ](#faq)
- [Advanced Documentation](#advanced-documentation)
- [About Nexting.ai](#about-nextingai)
- [Contributing](#contributing)
- [License](#license)

---

## Features

| Feature | Description |
|---------|-------------|
| **Pixel-Perfect Replication** | Faithfully recreates the original design with computed styles, colors, spacing, and typography |
| **Intelligent Chunking** | Three-principle algorithm ensures complete, non-overlapping, manageable sections |
| **Parallel Generation** | Multiple Claude agents work simultaneously for faster output |
| **30+ Data Types** | Extracts DOM, styles, animations, CSS variables, themes, hover states, and more |
| **Multi-Framework Support** | Next.js, React, Vue 3, or plain HTML output |
| **Theme Detection** | Automatically detects and preserves light/dark mode support |

---

## How It Works - Complete Workflow

This section provides a **detailed breakdown** of the entire cloning process.

```
User Input: URL
      │
      ▼
┌─────────────────────────────────────┐
│  Phase 1: Environment Setup         │  ← Check dependencies, install Playwright
└─────────────────────────────────────┘
      │
      ▼
┌─────────────────────────────────────┐
│  Phase 2: Page Extraction           │  ← Playwright captures DOM, styles, screenshots
└─────────────────────────────────────┘
      │
      ▼
┌─────────────────────────────────────┐
│  Phase 3: Intelligent Chunking      │  ← Three-principle algorithm splits page
└─────────────────────────────────────┘
      │
      ▼
┌─────────────────────────────────────┐
│  Phase 4: Parallel Code Generation  │  ← Multiple agents generate components
└─────────────────────────────────────┘
      │
      ▼
┌─────────────────────────────────────┐
│  Phase 5: Project Assembly          │  ← Combine into complete project
└─────────────────────────────────────┘
      │
      ▼
   npm run dev → View Result
```

---

### Phase 1: Environment Setup

**Goal**: Ensure all dependencies are installed and ready.

#### Step-by-Step

| Step | Command | What Happens |
|------|---------|--------------|
| 1.1 | `python --version` | Verify Python 3.8+ is installed |
| 1.2 | `python -c "from playwright.sync_api import sync_playwright"` | Check if Playwright is available |
| 1.3 | `pip install playwright beautifulsoup4` | Install Python dependencies (if needed) |
| 1.4 | `playwright install chromium` | Download Chromium browser for Playwright |

#### Troubleshooting

| Problem | Solution |
|---------|----------|
| "playwright not found" | Run `pip install playwright && playwright install chromium` |
| Permission denied on macOS | Use `pip install --user playwright` or create a virtual environment |
| Chromium download fails on Linux | Install system dependencies: `sudo apt-get install libnss3 libatk1.0-0 libatk-bridge2.0-0` |

---

### Phase 2: Page Extraction

**Goal**: Capture the complete webpage data using Playwright.

#### Command

```bash
python scripts/extract_page.py "<URL>" --output page_data.json
```

#### What Gets Extracted (30+ Data Types)

| Category | Data Item | Description |
|----------|-----------|-------------|
| **Page Metadata** | | |
| | `url` | The target URL |
| | `title` | Page title |
| | `viewport` | Browser viewport dimensions |
| | `page_dimensions` | Full page width and height |
| | `load_time_ms` | Page load time in milliseconds |
| **DOM Structure** | | |
| | `dom_tree` | Complete recursive tree of all elements |
| | `tag`, `id`, `classes` | Element identification |
| | `rect` | Bounding box (x, y, width, height) |
| | `children` | Nested child elements |
| **Computed Styles** | | |
| | Layout | `display`, `position`, `float`, `z_index` |
| | Flexbox | `flex_direction`, `justify_content`, `align_items`, `gap` |
| | Grid | `grid_template_columns`, `grid_template_rows` |
| | Dimensions | `width`, `height`, `min_width`, `max_width` |
| | Spacing | `margin`, `padding` (all sides) |
| | Visual | `background_color`, `background_image`, `color`, `border`, `border_radius`, `box_shadow`, `opacity` |
| | Typography | `font_family`, `font_size`, `font_weight`, `line_height`, `text_align` |
| | Transform | `transform` |
| **CSS Data** | | |
| | `variables` | CSS custom properties (e.g., `--primary: #3b82f6`) |
| | `animations` | @keyframes definitions |
| | `transitions` | Transition properties per selector |
| | `pseudo_elements` | ::before and ::after content |
| **Screenshots** | | |
| | `screenshot` | Viewport screenshot (base64 PNG) |
| | `full_page_screenshot` | Full scrollable page screenshot |
| **Theme Detection** | | |
| | `support` | "light", "dark", or "both" |
| | `current_mode` | Current active theme |
| | `has_significant_difference` | Whether themes are visually distinct |
| **Assets** | | |
| | `images` | All image URLs (img src and background-image) |
| | `fonts` | Web font URLs |
| | `scripts` | JavaScript file URLs |
| | `stylesheets` | CSS file URLs |
| **Interaction States** | | |
| | `hover_states` | Style changes on :hover |
| | `focus_states` | Style changes on :focus |

#### Command Options

| Option | Default | Description |
|--------|---------|-------------|
| `--output`, `-o` | `page_data.json` | Output file path |
| `--viewport` | `1920x1080` | Browser viewport size |
| `--wait` | `3000` | Wait time after load (ms) |
| `--full-screenshot` | `false` | Capture full page screenshot |
| `--download-images` | `false` | Download images locally |

#### Lazy Loading Handling

The extractor automatically scrolls through the entire page to trigger:
- Lazy-loaded images
- Infinite scroll content
- IntersectionObserver-based elements

---

### Phase 3: Intelligent Chunking

**Goal**: Split the page into independent, manageable sections following the Three Principles.

#### Command

```bash
python scripts/chunk_content.py page_data.json --output chunks/ --max-tokens 50000
```

#### The Three Principles

**Every chunk must satisfy ALL three principles:**

```
┌─────────────────────────────────────────────────────────────────┐
│  Principle 1: MUTUAL EXCLUSIVITY                                │
│  ─────────────────────────────────                              │
│  Chunks NEVER overlap. Each DOM region belongs to exactly       │
│  one chunk.                                                     │
│                                                                 │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐                      │
│  │ Chunk 1  │  │ Chunk 2  │  │ Chunk 3  │   ✓ No overlaps      │
│  └──────────┘  └──────────┘  └──────────┘                      │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│  Principle 2: COMPLETE COVERAGE                                 │
│  ───────────────────────────────                                │
│  All chunks combined = entire page. No content gaps.            │
│                                                                 │
│  Page Height: 5000px                                            │
│  Chunk 1: 0-800px    ┐                                         │
│  Chunk 2: 800-2000px │→ Total: 5000px ✓                        │
│  Chunk 3: 2000-3500px│                                          │
│  Chunk 4: 3500-5000px┘                                         │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│  Principle 3: SIZE CONTROL                                      │
│  ─────────────────────────                                      │
│  Each chunk < 50,000 tokens. Large sections auto-split.         │
│                                                                 │
│  Original: 200K tokens                                          │
│       ↓ Recursive split                                         │
│  ┌─────────┬─────────┬─────────┬─────────┐                     │
│  │  50K    │   50K   │   50K   │   50K   │  ✓ Manageable       │
│  └─────────┴─────────┴─────────┴─────────┘                     │
└─────────────────────────────────────────────────────────────────┘
```

#### Output Structure

```
chunks/
├── section_0_header.json       # Navigation/header
├── section_1_hero.json         # Hero section
├── section_2_features.json     # Features section
├── section_3_pricing.json      # Pricing section
├── section_4_testimonials.json # Testimonials
└── section_5_footer.json       # Footer
```

#### Each Chunk Contains

```json
{
  "id": "section-2",
  "name": "section_2",
  "selector": "section.features",
  "rect": {
    "x": 0, "y": 680, "width": 1920, "height": 800
  },
  "styles": {
    "background_color": "rgb(249, 250, 251)",
    "padding": "96px 0px"
  },
  "html": "<section class=\"features\">...</section>",
  "images": [
    {"src": "https://example.com/icon1.svg", "alt": "Feature 1"}
  ],
  "estimated_tokens": 2500
}
```

---

### Phase 4: Parallel Code Generation

**Goal**: Multiple Claude agents work simultaneously, each generating one component.

#### How It Works

```
┌───────────────────────────────────────────────────────────────────┐
│                     Claude Code (Orchestrator)                    │
│                              │                                    │
│         ┌────────────────────┼────────────────────┐              │
│         ▼          ▼         ▼         ▼          ▼              │
│    ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐   │
│    │ Agent 1 │ │ Agent 2 │ │ Agent 3 │ │ Agent 4 │ │ Agent 5 │   │
│    │ Header  │ │  Hero   │ │Features │ │ Pricing │ │ Footer  │   │
│    └────┬────┘ └────┬────┘ └────┬────┘ └────┬────┘ └────┬────┘   │
│         ▼          ▼         ▼         ▼          ▼              │
│    Header.tsx  Hero.tsx  Features.tsx Pricing.tsx Footer.tsx     │
└───────────────────────────────────────────────────────────────────┘
```

#### Data Received by Each Agent

| Field | Description |
|-------|-------------|
| `html` | The HTML fragment for this section |
| `styles` | Computed CSS styles |
| `rect` | Bounding box position and dimensions |
| `images` | List of images in this section |
| `estimated_tokens` | Content size estimate |

#### Agent Prompt Template

Each agent receives instructions like:

```
You are a frontend developer focused on pixel-perfect replication.

## Task
Implement the [Features] section of a webpage clone.

## Input Data
- Section HTML: [from chunks/section_2_features.json]
- Section Styles: [computed styles]
- Images: [image list with URLs]
- Bounding Box: [position info]

## Requirements
1. Pixel-Perfect: Replicate the exact visual design
2. Use Original URLs: Keep all image src as-is
3. Tailwind CSS: Use Tailwind utilities, inline styles only when necessary
4. Self-Contained: Component must work independently
5. Responsive: Implement reasonable breakpoints

## Output
Write a React/Next.js component to: src/components/Features.tsx
```

#### Generated Component Example

```tsx
// src/components/Features.tsx
import Image from 'next/image'

interface FeaturesProps {
  className?: string
}

export default function Features({ className = '' }: FeaturesProps) {
  const features = [
    {
      icon: 'https://example.com/icon1.svg',
      title: 'Fast Performance',
      description: 'Lightning-fast load times...'
    },
    // ... more features
  ]

  return (
    <section className={`py-24 bg-gray-50 ${className}`}>
      <div className="container mx-auto px-4">
        <h2 className="text-4xl font-bold text-center mb-16">Features</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {features.map((feature, i) => (
            <div key={i} className="p-6 bg-white rounded-xl shadow-sm">
              <img src={feature.icon} alt="" className="w-12 h-12 mb-4" />
              <h3 className="text-xl font-semibold mb-2">{feature.title}</h3>
              <p className="text-gray-600">{feature.description}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}
```

---

### Phase 5: Project Assembly

**Goal**: Combine all generated components into a complete, runnable project.

#### Generated File Structure

```
project/
├── src/
│   ├── app/
│   │   ├── page.tsx           # Main page importing all sections
│   │   ├── layout.tsx         # Root layout
│   │   └── globals.css        # Global styles
│   └── components/
│       ├── Header.tsx
│       ├── Hero.tsx
│       ├── Features.tsx
│       ├── Pricing.tsx
│       ├── Testimonials.tsx
│       └── Footer.tsx
├── tailwind.config.js
├── next.config.js
├── package.json
└── tsconfig.json
```

#### Main Page Assembly

```tsx
// src/app/page.tsx
import Header from '@/components/Header'
import Hero from '@/components/Hero'
import Features from '@/components/Features'
import Pricing from '@/components/Pricing'
import Testimonials from '@/components/Testimonials'
import Footer from '@/components/Footer'

export default function Home() {
  return (
    <main>
      <Header />
      <Hero />
      <Features />
      <Pricing />
      <Testimonials />
      <Footer />
    </main>
  )
}
```

#### Final Step

```bash
npm install && npm run dev
# Open http://localhost:3000
```

---

## Quick Start

### Method 1: Personal Global Installation

For personal use - available in all your projects:

```bash
# Step 1: Clone to Claude Code skills directory
git clone https://github.com/anthropics/perfect-web-clone-skill.git ~/.claude/skills/perfect-web-clone

# Step 2: Install Python dependencies
cd ~/.claude/skills/perfect-web-clone/scripts
pip install -r requirements.txt

# Step 3: Install Playwright browser
playwright install chromium

# Step 4: Restart Claude Code
# The skill will be automatically detected
```

### Method 2: Project-Level Installation

For team projects - available to all team members:

```bash
# Step 1: Clone to project directory
git clone https://github.com/anthropics/perfect-web-clone-skill.git .claude/skills/perfect-web-clone

# Step 2-4: Same as above
```

---

## Usage Examples

### Basic Usage

```
Clone https://stripe.com
```

### Specify Framework

```
Clone https://linear.app using React
```

```
Clone https://example.com with Vue
```

### Control Parallelism

```
Clone https://example.com with 5 parallel agents
```

```
Clone https://example.com as fast as possible
```

### Combine Options

```
Clone https://example.com using Next.js with 10 parallel agents
```

---

## The Three Principles

### Why Three Principles?

Without these principles, problems occur:

| Without Principle | Problem |
|-------------------|---------|
| No Mutual Exclusivity | Duplicate code, merge conflicts, overlapping components |
| No Complete Coverage | Missing sections, incomplete clones, visual gaps |
| No Size Control | Context overflow, agent failures, incomplete outputs |

### Principle 1: Mutual Exclusivity

**Rule**: Any two chunks MUST NOT share DOM regions.

**Implementation**:
- Calculate bounding box overlap for each section pair
- If overlap > 100px², keep the larger section, discard the other
- Validation ensures zero overlap in final output

**Benefit**: Each agent works on truly isolated content with no conflicts.

### Principle 2: Complete Coverage

**Rule**: All chunks combined = entire page (y=0 to y=pageHeight).

**Implementation**:
- Sort sections by Y coordinate (top to bottom)
- Detect gaps between adjacent sections
- Extend section boundaries to fill gaps
- Final coverage must equal 100%

**Benefit**: No content is lost. The clone is visually complete.

### Principle 3: Size Control

**Rule**: Each chunk < 50,000 tokens.

**Implementation**:
- Estimate tokens: `characters / 4`
- If section exceeds limit, recursively split into children
- Continue until all chunks are under threshold

**Benefit**: Each agent receives manageable context, ensuring reliable generation.

---

## Parallelism Configuration

| User Command | Agent Count | Use Case |
|--------------|-------------|----------|
| `"clone this page"` | 3 (default) | Balanced speed and resource usage |
| `"clone with N parallel"` | N | Precise control |
| `"clone as fast as possible"` | All sections | Maximum speed |
| `"clone one by one"` | 1 | Debugging, careful review |

---

## Supported Tech Stacks

| Framework | Styling | Command Example |
|-----------|---------|-----------------|
| Next.js (default) | Tailwind CSS | `Clone https://... using Next.js` |
| React | Tailwind CSS | `Clone https://... using React` |
| Vue 3 | Tailwind CSS | `Clone https://... with Vue` |
| HTML | Vanilla CSS | `Clone https://... as static HTML` |

---

## FAQ

### Playwright Installation Issues

**macOS:**
```bash
brew install chromium
playwright install chromium
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install chromium-browser
playwright install chromium
```

**Windows:**
```bash
playwright install chromium
```

### Page is too large (100+ sections)?

Use maximum parallelism:
```
Clone https://large-site.com as fast as possible
```

### Dynamic content not captured?

Increase wait time:
```bash
python scripts/extract_page.py "https://spa-site.com" --wait 5000
```

### Page requires authentication?

Currently not supported. Clone publicly accessible pages, or implement cookie injection in the extraction script.

### Images not loading in the clone?

For Next.js, add domain configuration:
```js
// next.config.js
module.exports = {
  images: {
    remotePatterns: [
      { protocol: 'https', hostname: '**' }
    ]
  }
}
```

---

## Advanced Documentation

| Document | Contents |
|----------|----------|
| [SKILL.md](SKILL.md) | Core skill instruction definition |
| [docs/EXTRACTION.md](docs/EXTRACTION.md) | Detailed 30+ data types extracted |
| [docs/CHUNKING.md](docs/CHUNKING.md) | Three-principle algorithm implementation |
| [docs/CODE_GENERATION.md](docs/CODE_GENERATION.md) | Component generation strategies |

---

## About Nexting.ai

**Perfect Web Clone** is an open-source Claude Code Skill created by [Nexting.ai](https://nexting.ai).

Want the complete visual experience?
- Real-time preview in browser
- Visual diff comparison
- One-click deployment
- Team collaboration

Visit [nexting.ai](https://nexting.ai) to try our full-featured AI web development platform.

---

## Contributing

Contributions are welcome!

1. Fork this repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## License

MIT License - Free for personal and commercial use.

---

<div align="center">

**If this project helps you, please give it a ⭐!**

[GitHub](https://github.com/anthropics/perfect-web-clone-skill) · [Nexting.ai](https://nexting.ai) · [Report Issues](https://github.com/anthropics/perfect-web-clone-skill/issues)

</div>
