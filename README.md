# Perfect Web Clone Skill

Clone any webpage into a **pixel-perfect**, measured Vite + React project.

This repository is the **playbook**. Capture, sectioning, and scoring live in
[Perfect-Web-Clone](https://github.com/ericshang98/Perfect-Web-Clone).

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

Then: `clone https://example.com`

The same `pwc` CLI works from Codex or any coding agent that can run shell commands.

## What this is

Pixel-perfect is a gate table (fingerprints, weight, per-section visual score),
not a prompt. The agent writes clean React; the core measures the replica
against the original and repairs the worst section.

## License

MIT
