---
name: perfect-web-clone
description: >-
  Reproduce a live website from its URL as a clean, deployable Vite + React
  project: capture source evidence, plan the full page, author every section,
  build, compare, repair, and hand the measured result to the user for review.
  Use when the user asks to clone, copy, reproduce, replicate, rebuild, or 复刻
  a website, including a request that is only an action and a URL.
---

# Perfect Web Clone

Install the measured core from the product repo first:

https://github.com/ericshang98/Perfect-Web-Clone

```bash
pip install "git+https://github.com/ericshang98/Perfect-Web-Clone.git"
playwright install chromium
```

The current agent is the harness runtime. `pwc` is the deterministic hands and
eyes. It never calls a model. You understand the evidence, author code, and
repair the worst section.

One request such as `clone https://example.com` authorizes the whole local
reproduction. Deployment is never implicit.

## Contract

1. Capture, plan, author, build, verify, repair, and hand off as one task.
2. Inspect every `ok` flag. Never invent a tool result.
3. Refuse to plan from an incomplete capture.
4. Reproduce every planned section. Do not stop after the viewport.
5. A similar but inert control fails.
6. Run gates in order. A downstream score cannot override an upstream failure.
7. Repair the smallest owning component, rebuild, re-run affected gates.
8. Never hide a red gate.
9. End only in `ready_for_user_review` or `failed_with_residuals`.

## Commands

```bash
pwc extract <url>
pwc plan <source_id>
pwc assemble <source_id>
pwc build
pwc fingerprints <dist_dir>
pwc weight <dist_dir>
pwc score --ref <reference.png> --cand <clone.png>
```

Every command prints JSON.

## Workflow

1. `pwc extract <url>` — require `ok` and `capture_integrity.status == "passed"`.
2. `pwc plan <source_id>` — author every listed section as clean React.
3. `pwc assemble <source_id>` then `pwc build`.
4. `pwc fingerprints dist/` and `pwc weight dist/`.
5. Screenshot the clone and `pwc score --ref ... --cand ...`.
6. Repair the worst section, rebuild, re-measure. Cap five attempts per state.
7. Hand the local review URL to the user. Never say pixel-perfect or accepted.

If the classifier reports WebGL / canvas / scroll choreography, keep that as a
residual. Content still clones; the runtime-drawn look may not.
