# Perfect Web Clone Skill

**This is the pixel-perfect cloning harness.** One request — `clone https://example.com` — and the current coding agent must capture, plan, author, build, measure, repair, and hand the result to you.

English | [中文](README_CN.md)

The skill is the product. [`SKILL.md`](SKILL.md) is the contract:

- The agent is the runtime
- [`pwc`](https://github.com/ericshang98/Perfect-Web-Clone) is the hands and eyes (never calls a model)
- Pixel-perfect is a gate table: capture integrity, complete structure, real interactions, fingerprints, weight, per-section visual score
- A similar but inert control fails
- The run ends only in `ready_for_user_review` or `failed_with_residuals`

The measured core lives in [Perfect-Web-Clone](https://github.com/ericshang98/Perfect-Web-Clone).

## Install

```bash
pip install "git+https://github.com/ericshang98/Perfect-Web-Clone.git"
playwright install chromium

mkdir -p ~/.claude/skills/perfect-web-clone/references
cp SKILL.md ~/.claude/skills/perfect-web-clone/
cp references/harness-contract.md ~/.claude/skills/perfect-web-clone/references/
```

Or clone this repo into `~/.claude/skills/perfect-web-clone`.

Then: `clone https://example.com`

Codex and other coding agents that can run `pwc` load the same `SKILL.md`.

## License

MIT
