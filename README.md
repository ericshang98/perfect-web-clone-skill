# Perfect Web Clone Skill

A skill for cloning a live webpage into a measured Vite + React project.

This repository is the **playbook**. The measured core (extract / plan / gates)
lives in [Perfect-Web-Clone](https://github.com/ericshang98/Perfect-Web-Clone).

English | [中文](README_CN.md)

## Install

```bash
pip install "git+https://github.com/ericshang98/Perfect-Web-Clone.git"
playwright install chromium
```

### Claude Code

```bash
mkdir -p ~/.claude/skills/perfect-web-clone
cp SKILL.md ~/.claude/skills/perfect-web-clone/
```

Or clone this repo into `~/.claude/skills/perfect-web-clone`.

### DeepSeek Harness

```bash
npx @deepseek-ai/dsh web
dsh plugin --profile web add github:ericshang98/Perfect-Web-Clone
```

Then: `clone https://example.com`

## What this is not

This is not the January 2026 two-script extractor. Pixel-perfect is a gate
table (fingerprints, weight, per-section SSIM), not a prompt. The old
`scripts/extract_page.py` path is retired.

## License

MIT
