# Perfect Web Clone

> Clone any webpage into pixel-perfect, production-ready code.

A Claude Code Skill that extracts web pages using Playwright, intelligently chunks content following the Three Principles, and generates React/Next.js/Vue components in parallel.

## Features

- **Pixel-Perfect Replication** - Faithfully recreates the original design
- **Intelligent Chunking** - Three-principle algorithm ensures completeness
- **Parallel Generation** - Multiple agents work simultaneously
- **Multi-Framework Support** - Next.js, React, Vue, and more
- **Full Data Extraction** - 30+ data types including CSS animations, themes, interactions

## Installation

### 1. Clone to your Claude Code skills directory

**For personal use (available in all projects):**
```bash
git clone https://github.com/anthropics/perfect-web-clone-skill.git ~/.claude/skills/perfect-web-clone
```

**For project use (available to team members):**
```bash
git clone https://github.com/anthropics/perfect-web-clone-skill.git .claude/skills/perfect-web-clone
```

### 2. Install Python dependencies

```bash
cd ~/.claude/skills/perfect-web-clone/scripts  # or .claude/skills/...
pip install -r requirements.txt
playwright install chromium
```

### 3. Restart Claude Code

The skill will be automatically detected.

## Usage

Simply tell Claude Code what you want to clone:

```
Clone https://stripe.com using Next.js
```

```
Replicate this landing page: https://linear.app with React and Tailwind
```

```
Clone https://example.com with 5 parallel agents for faster generation
```

## How It Works

```
┌─────────────────────────────────────────────────────────────┐
│  1. Page Extraction (Playwright)                            │
│     - DOM tree with computed styles                         │
│     - Full-page screenshot                                  │
│     - CSS variables, animations, transitions                │
│     - Theme detection (light/dark mode)                     │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  2. Intelligent Chunking (Three Principles)                 │
│     - Mutual Exclusivity: Chunks never overlap              │
│     - Complete Coverage: No content gaps                    │
│     - Size Control: Each chunk < 50K tokens                 │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  3. Parallel Code Generation                                │
│     ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐        │
│     │ Agent 1 │ │ Agent 2 │ │ Agent 3 │ │ Agent N │        │
│     │ Header  │ │  Hero   │ │Features │ │ Footer  │        │
│     └────┬────┘ └────┬────┘ └────┬────┘ └────┬────┘        │
│          ↓           ↓           ↓           ↓              │
│     Header.tsx  Hero.tsx  Features.tsx  Footer.tsx          │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  4. Project Assembly                                        │
│     - Generate main page importing all sections             │
│     - Configure Tailwind CSS                                │
│     - User runs: npm install && npm run dev                 │
└─────────────────────────────────────────────────────────────┘
```

## The Three Principles

### 1. Mutual Exclusivity
Chunks **never overlap**. Each section of the page is handled by exactly one agent with no conflicts.

### 2. Complete Coverage
All chunks combined equal the **entire page**. No content is lost or skipped.

### 3. Size Control
Each chunk is **smaller than 50,000 tokens**. Large sections are automatically split into manageable pieces.

## Parallelism Options

| Command | Behavior |
|---------|----------|
| "clone this page" | Default: 3 parallel agents |
| "clone with 5 parallel" | Exactly 5 agents |
| "clone as fast as possible" | All sections in parallel |
| "clone one by one" | Sequential (1 agent) |

## Supported Tech Stacks

| Framework | Styling | Notes |
|-----------|---------|-------|
| Next.js | Tailwind CSS | Default, recommended |
| React | Tailwind CSS | Create React App |
| Vue 3 | Tailwind CSS | Composition API |
| HTML | Vanilla CSS | Static sites |

## Documentation

- [SKILL.md](SKILL.md) - Main skill instructions
- [docs/EXTRACTION.md](docs/EXTRACTION.md) - Page extraction details
- [docs/CHUNKING.md](docs/CHUNKING.md) - Three principles algorithm
- [docs/CODE_GENERATION.md](docs/CODE_GENERATION.md) - Component generation guide

## Requirements

- Python 3.8+
- Node.js 18+
- Claude Code

## About

**Perfect Web Clone** is an open-source Claude Code Skill created by [Nexting.ai](https://nexting.ai).

For a complete visual experience with:
- Real-time preview in browser
- Visual diff comparison
- One-click deployment
- Team collaboration

Visit [nexting.ai](https://nexting.ai) to try our full-featured AI web development platform.

## License

MIT License - Free for personal and commercial use.

## Contributing

Contributions are welcome! Please read our contributing guidelines before submitting a PR.

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Support

- [GitHub Issues](https://github.com/anthropics/perfect-web-clone-skill/issues)
- [Nexting.ai Discord](https://discord.gg/nexting)
