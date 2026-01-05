# Perfect Web Clone Skill

<div align="center">

**A Claude Code Skill for Cloning Any Webpage**

English | [中文](README_CN.md)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Claude Code Skill](https://img.shields.io/badge/Claude%20Code-Skill-8A2BE2)](https://claude.ai)

</div>

---

A Claude Code Skill that clones any webpage into pixel-perfect, production-ready React/Next.js/Vue code.

> Created by [Nexting.ai](https://nexting.ai)

---

## What is This?

This is a **Skill** for Claude Code - a set of instructions that teaches Claude Code how to clone webpages. Once installed, you can simply tell Claude Code:

```
Clone https://stripe.com
```

And it will automatically:
1. Extract the page using Playwright
2. Split it into manageable chunks
3. Generate React/Next.js/Vue components in parallel
4. Assemble a complete runnable project

**You don't need to run any scripts manually** - Claude Code handles everything.

---

## Installation

### Option 1: Personal Installation (All Projects)

```bash
# Clone to your Claude Code skills directory
git clone https://github.com/anthropics/perfect-web-clone-skill.git ~/.claude/skills/perfect-web-clone

# Install dependencies
cd ~/.claude/skills/perfect-web-clone/scripts
pip install -r requirements.txt
playwright install chromium
```

### Option 2: Project Installation (Team Sharing)

```bash
# Clone to your project
git clone https://github.com/anthropics/perfect-web-clone-skill.git .claude/skills/perfect-web-clone

# Install dependencies (same as above)
```

Restart Claude Code. The skill will be automatically detected.

---

## Usage

Just tell Claude Code what you want in natural language:

| What You Say | What Happens |
|--------------|--------------|
| `Clone https://stripe.com` | Clone with Next.js (default) |
| `Clone https://linear.app using React` | Clone with React |
| `Clone https://example.com with Vue` | Clone with Vue 3 |
| `Clone https://example.com with 5 parallel agents` | Faster with more agents |
| `Clone https://example.com as fast as possible` | Maximum parallelism |

After cloning, run:
```bash
npm install && npm run dev
```

---

## What Gets Cloned

| Aspect | Coverage |
|--------|----------|
| **Layout** | Flexbox, Grid, positioning |
| **Styling** | Colors, typography, spacing, shadows, borders |
| **Images** | All images with original URLs |
| **Animations** | CSS animations, transitions, hover effects |
| **Theme** | Light/dark mode detection |
| **Responsiveness** | Breakpoints preserved |

---

## How It Works (Overview)

```
Your command: "Clone https://example.com"
                    ↓
    ┌───────────────────────────────┐
    │  1. Extract page (Playwright) │
    │  2. Split into sections       │
    │  3. Generate components       │  ← Claude Code does all this
    │  4. Assemble project          │
    └───────────────────────────────┘
                    ↓
         Ready-to-run project
```

The skill uses:
- **Playwright** to capture DOM, styles, screenshots
- **Three Principles** chunking algorithm (no overlap, complete coverage, size control)
- **Parallel agents** for faster code generation

For technical details, see [How It Works](#how-it-works-technical-details).

---

## Supported Frameworks

| Framework | Styling | Command |
|-----------|---------|---------|
| Next.js (default) | Tailwind CSS | `Clone https://...` |
| React | Tailwind CSS | `Clone https://... using React` |
| Vue 3 | Tailwind CSS | `Clone https://... with Vue` |
| HTML | Vanilla CSS | `Clone https://... as static HTML` |

---

## Requirements

- Claude Code
- Python 3.8+
- Node.js 18+

---

## Troubleshooting

### Playwright not found
```bash
pip install playwright && playwright install chromium
```

### Page not fully captured (SPA/dynamic content)
Tell Claude Code:
```
Clone https://example.com, wait 5 seconds for content to load
```

### Images not loading in Next.js
Add to `next.config.js`:
```js
module.exports = {
  images: {
    remotePatterns: [{ protocol: 'https', hostname: '**' }]
  }
}
```

---

## How It Works (Technical Details)

<details>
<summary>Click to expand</summary>

### Phase 1: Page Extraction

The skill uses Playwright to capture:
- Complete DOM tree with computed styles
- Full-page screenshot
- CSS variables, animations, transitions
- Theme detection (light/dark mode)
- All images and assets

### Phase 2: Intelligent Chunking

The page is split following **Three Principles**:

1. **Mutual Exclusivity** - Chunks never overlap
2. **Complete Coverage** - All chunks combined = entire page
3. **Size Control** - Each chunk < 50K tokens

### Phase 3: Parallel Code Generation

Multiple Claude agents work simultaneously:
- Each agent receives one section
- Generates a self-contained React/Vue component
- Uses Tailwind CSS for styling

### Phase 4: Project Assembly

All components are combined into:
```
project/
├── src/components/   # Generated components
├── src/app/page.tsx  # Main page
├── tailwind.config.js
└── package.json
```

For more details:
- [docs/EXTRACTION.md](docs/EXTRACTION.md)
- [docs/CHUNKING.md](docs/CHUNKING.md)
- [docs/CODE_GENERATION.md](docs/CODE_GENERATION.md)

</details>

---

## About Nexting.ai

**Perfect Web Clone** is an open-source Claude Code Skill by [Nexting.ai](https://nexting.ai).

Want a visual experience with real-time preview, diff comparison, and one-click deployment? Visit [nexting.ai](https://nexting.ai).

---

## License

MIT License

---

<div align="center">

**If this helps you, give it a ⭐!**

[Nexting.ai](https://nexting.ai) · [Report Issues](https://github.com/anthropics/perfect-web-clone-skill/issues)

</div>
