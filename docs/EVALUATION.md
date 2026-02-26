# Perfect Web Clone Skill — Full Evaluation & Comparison

**Date:** 2026-02-23
**Compared Against:** https://github.com/ericshang98/perfect-web-clone-skill (original)
**Local Fork:** CodeCompleteMedia/perfect-web-clone-skill
**Local Branch:** `security/fix-critical-vulnerabilities`

---

## Source Repos

| | Original | Local Fork |
|--|----------|------------|
| **Repo** | `ericshang98/perfect-web-clone-skill` | `CodeCompleteMedia/perfect-web-clone-skill` |
| **Branch** | `main` (only branch) | `security/fix-critical-vulnerabilities` |
| **Commits** | 3 | 4 (3 original + 1 security patch) |
| **Files** | 13 | 19 (+6 new files) |
| **Tests** | None | 67+ test cases |
| **Security** | None | 3 vulnerability classes patched |

---

## Project Overview

| Metric | Value |
|--------|-------|
| **Total Code** | ~4,400 lines production + ~750 lines tests |
| **Files** | 19 tracked files across 4 directories |
| **Author** | Nexting.ai (original), CodeCompleteMedia (security patch) |
| **License** | MIT |

---

## Architecture — 5-Phase Pipeline

The skill is a Claude Code instruction set (SKILL.md) backed by Python scripts. It does not run as a standalone app — it teaches Claude Code a workflow.

```
URL → [Extract] → [Sanitize] → [Chunk] → [Generate (parallel)] → [Assemble]
        Phase 2     Phase 2.5    Phase 3      Phase 4                Phase 5
```

---

## What the Fork Has Already Changed

### New Files Added (6)

| File | Purpose |
|------|---------|
| `scripts/sanitize.py` (172 lines) | Strips hidden elements, comments, scripts, malicious attributes |
| `tests/conftest.py` (62 lines) | Pytest fixtures for security testing |
| `tests/test_c1_prompt_injection.py` (313 lines) | Indirect prompt injection tests |
| `tests/test_c2_command_injection.py` (183 lines) | Command injection via URL tests |
| `tests/test_c3_ssrf.py` (246 lines) | SSRF vulnerability tests |
| `.gitignore` (21 lines) | Python/IDE/OS artifact exclusions |

### Modified Files (5)

| File | Change |
|------|--------|
| `scripts/extract_page.py` | Added `validate_url()` function (~102 new lines) — blocks shell metacharacters, private IPs, cloud metadata, non-HTTP schemes, IPv6-mapped bypass |
| `SKILL.md` | Added Phase 2.5 (sanitization), Phase 4.5 (output validation), single-quoted URLs, trust boundary block in subagent prompt. Added framework placeholder system with substitution table, 5 framework-specific Phase 5 assembly sections, SvelteKit and Vanilla HTML to tech stacks. |
| `docs/CODE_GENERATION.md` | Added SvelteKit and Vanilla HTML component templates, `class` vs `className` note, framework-specific image handling, framework-conditional output requirements, framework-syntax quality checklist items. |
| `README.md` | Added SvelteKit and Vanilla HTML to header, usage table, supported frameworks table, technical details, and project structure diagrams. |
| `README_CN.md` | Mirrored all README.md changes with Chinese translations. |

### Unchanged Files (8)

All original files carried over as-is:
- `LICENSE`
- `docs/EXTRACTION.md`, `docs/CHUNKING.md`
- `scripts/chunk_content.py`, `scripts/requirements.txt`, `scripts/setup.sh`

---

## Feature Set Breakdown

### 1. Page Extraction (`extract_page.py` — 684 lines) — FULLY IMPLEMENTED

| Feature | Status | Notes |
|---------|--------|-------|
| Playwright browser automation | Done | Chromium headless |
| Full DOM tree traversal | Done | Recursive with max_depth param |
| 30+ computed CSS properties per element | Done | Colors, fonts, spacing, borders, shadows, etc. |
| Full-page + viewport screenshots | Done | Base64 encoded |
| CSS variables extraction | Done | Custom properties from `:root` |
| Animation/transition capture | Done | Keyframes, transition properties |
| Media query extraction | Done | Responsive breakpoints |
| Lazy-load scroll triggering | Done | Auto-scrolls page, max 50 scrolls |
| Theme detection (light/dark) | Done | Detects color-scheme preferences |
| Asset inventory (images, fonts, scripts, stylesheets) | Done | With deduplication |
| Style summary statistics | Done | Top 20 colors, fonts, sizes |
| CLI with configurable viewport, wait time, depth | Done | Full argparse interface |

### 2. Content Sanitization (`sanitize.py` — 172 lines) — FULLY IMPLEMENTED

| Feature | Status | Notes |
|---------|--------|-------|
| Strip HTML comments | Done | Prevents hidden instruction injection |
| Strip `<script>` tag contents | Done | Removes executable code |
| Strip `<style>` tag contents | Done | Removes CSS-based hiding tricks |
| Strip hidden elements (`display:none`, etc.) | Done | 3 hidden patterns detected |
| Sanitize `alt`/`title` attributes | Done | Truncates >200 chars, blocks instruction phrases |
| Instruction phrase detection | Done | 10+ patterns (e.g. "ignore instructions", "system override", `eval(`) |

### 3. Intelligent Chunking (`chunk_content.py` — 643 lines) — FULLY IMPLEMENTED

| Feature | Status | Notes |
|---------|--------|-------|
| **Principle 1: Mutual Exclusivity** | Done | Overlap detection + removal (>50% area threshold) |
| **Principle 2: Complete Coverage** | Done | Gap filling (30px threshold), extends to page edges |
| **Principle 3: Size Control** | Done | Max 50K tokens per chunk, recursive splitting |
| Section detection from DOM | Done | Recursive traversal, tag filtering |
| Horizontal layout handling | Done | Detects grids/cards, groups by 30% vertical overlap |
| CSS selector generation | Done | ID-first, then class-based |
| HTML extraction per section | Done | Regex-based with depth-tracking for closing tags |
| Image/link extraction per section | Done | Max 20 each per section |
| Validation report generation | Done | `_validation.json` with errors, warnings, stats |
| CLI with configurable token limits | Done | Full argparse interface |

### 4. Parallel Code Generation (SKILL.md instructions only) — DOCUMENTED, NOT SCRIPTED

| Feature | Status | Notes |
|---------|--------|-------|
| Spawn parallel Task subagents | Instruction only | Claude Code follows SKILL.md guidance |
| Security trust boundary in subagent prompt | Documented | Template blocks file access, network calls, eval |
| Framework selection (Next.js/React/Vue/SvelteKit/HTML) | Documented | User specifies via natural language; placeholder substitution table in SKILL.md |
| Tailwind CSS styling | Documented | Preferred, with inline fallback |
| Responsive breakpoints | Documented | sm/md/lg/xl/2xl in template |
| Natural language parallelism control | Documented | "fastest" / number / default 3-5 agents |

### 5. Output Validation (SKILL.md instructions only) — DOCUMENTED, NOT SCRIPTED

| Feature | Status | Notes |
|---------|--------|-------|
| Verify files only in `src/components/` | Instruction only | No automated scanner |
| Scan for `process.env`, `eval(`, `exec(`, etc. | Instruction only | Claude Code does manual scan |
| Reject suspicious components | Instruction only | Warning + exclusion |

### 6. Project Assembly (SKILL.md instructions only) — DOCUMENTED, NOT SCRIPTED

| Feature | Status | Notes |
|---------|--------|-------|
| Create main page importing all sections | Instruction only | Template in SKILL.md |
| Ensure `package.json` dependencies | Instruction only | React, Next.js, Tailwind |
| Create `tailwind.config.js` | Instruction only | If not exists |
| User prompted to `npm install && npm run dev` | Instruction only | Final step |

---

## Security Posture — 3 Vulnerability Classes Patched

| Vulnerability | Mitigation | Tests |
|---------------|------------|-------|
| **C1: Indirect Prompt Injection** | `sanitize.py` strips hidden content, comments, malicious attributes | 9 tests (313 lines) |
| **C2: Command Injection via URL** | `validate_url()` rejects shell metacharacters (`$`, `` ` ``, `;`, `|`, `&`, etc.) | 11 tests (183 lines) |
| **C3: SSRF** | Blocks private IPs, cloud metadata (AWS/GCP/Azure), non-HTTP schemes, IPv6-mapped bypass | 13 tests (246 lines) |

Defense-in-depth: URL validated in both `main()` and `extract()`.

### Original Repo Vulnerabilities (unpatched on upstream `main`)

1. **No URL validation** — any URL (including `file://`, private IPs, cloud metadata) goes straight to Playwright
2. **Double-quoted URLs** in SKILL.md shell commands — allows `$()` command injection
3. **No content sanitization** — malicious webpage content flows directly into subagent prompts
4. **No `.gitignore`**
5. **No tests of any kind**

---

## What Has NOT Been Implemented Yet

### High Priority — Functional Gaps

| # | Feature | Where Referenced | Current State |
|---|---------|-----------------|---------------|
| 1 | **Phase 4: Code generation script** | SKILL.md Phase 4 | No `scripts/generate_code.py` — relies entirely on SKILL.md prose for Claude Code to follow. No automation, no error recovery, no retry logic. |
| 2 | **Phase 4.5: Output validation script** | SKILL.md Phase 4.5 | No `scripts/validate_output.py` — the scan for `process.env`, `eval(`, `exec(`, `fetch(` is a manual checklist, not an automated scanner. |
| 3 | **Phase 5: Project assembly script** | SKILL.md Phase 5 | No `scripts/assemble_project.py` — scaffold creation (package.json, tailwind.config, main page) is left entirely to Claude Code's judgment. |
| 4 | **End-to-end integration tests** | Implied by test suite | No test runs the full pipeline: extract → sanitize → chunk → generate → assemble. Only unit-level security tests exist. |
| 5 | **Chunking correctness tests** | Implied | Zero tests for `chunk_content.py` — no validation that the Three Principles actually hold on real-world HTML. |
| 6 | **Extraction output tests** | Implied | Zero tests for `extract_page.py` output format/correctness (only URL validation is tested). |

### Medium Priority — Security Gaps

| # | Feature | Where Referenced | Current State |
|---|---------|-----------------|---------------|
| 7 | **Open redirect / DNS rebinding protection** | `tests/test_c3_ssrf.py` line noting "redirect limitation" | `validate_url()` checks the initial URL but does NOT follow redirects. A site could redirect to `http://169.254.169.254/`. Playwright follows redirects by default. |
| 8 | **Automated output scanning** | SKILL.md Phase 4.5 | The checklist says to scan `.tsx` files for dangerous patterns, but there's no script or regex scanner. If Claude Code misses one, it ships. |
| 9 | **Subagent file-write scope enforcement** | SKILL.md Phase 4 | The prompt *tells* subagents to only write in `src/components/`, but nothing *prevents* them from writing elsewhere. No filesystem sandbox. |
| 10 | **Content-Security-Policy / sandbox headers** | Not referenced | Generated projects have no CSP or security headers. Cloned pages could contain XSS vectors in the replicated HTML. |

### Low Priority — Quality & Completeness

| # | Feature | Where Referenced | Current State |
|---|---------|-----------------|---------------|
| 11 | **beautifulsoup4 is unused** | `requirements.txt` | Listed as dependency, imported nowhere. `chunk_content.py` uses regex-based HTML parsing instead. Either use it or remove it. |
| 12 | **aiohttp is unused** | `requirements.txt` | Listed as optional dependency, imported nowhere in any script. |
| 13 | **HTML and SvelteKit framework support** | README.md framework table | IMPLEMENTED — Full templates in `CODE_GENERATION.md`, subagent prompt placeholders and assembly instructions in `SKILL.md`, and documentation in both READMEs for Vanilla HTML (Tailwind CDN or hand-written CSS) and SvelteKit (Svelte 5 runes, `@tailwindcss/vite`). |
| 14 | **Vue 3 generation template completeness** | `docs/CODE_GENERATION.md` | Vue template is documented but less detailed than the React/Next.js template. Vue-specific assembly instructions now added in SKILL.md Phase 5. |
| 15 | **Security branch not merged** | Git state | The `security/fix-critical-vulnerabilities` branch has an open PR (#1) against the original repo but has not been merged. Local `main` has none of the security patches. |
| 16 | **No CI/CD pipeline** | Not referenced | No GitHub Actions, no automated test runner, no lint checks. Tests exist but nothing runs them automatically. |
| 17 | **No `pyproject.toml` or package metadata** | Not referenced | No standard Python packaging. Can't `pip install` the skill or version it properly. |
| 18 | **Error recovery in chunking** | `chunk_content.py` | If a section can't be split below `max_tokens`, it logs a warning and returns the oversized section as-is. No fallback strategy. |
| 19 | **Screenshot comparison / visual diff** | README mentions Nexting.ai has this | No built-in visual regression testing. No way to verify the clone looks correct programmatically. |
| 20 | **Dynamic SPA handling** | `docs/EXTRACTION.md` troubleshooting | The `--wait` flag is a blunt instrument. No route-based SPA extraction, no click-to-reveal, no JavaScript execution tracking. |

---

## Summary Scorecard

| Category | Score | Notes |
|----------|-------|-------|
| **Extraction (Phase 2)** | 95% | Fully built, tested for security, only missing redirect protection |
| **Sanitization (Phase 2.5)** | 90% | Fully built, tested, but only strips `raw_html` (not DOM tree nodes directly) |
| **Chunking (Phase 3)** | 80% | Fully built, zero tests for correctness, oversized fallback is weak |
| **Code Generation (Phase 4)** | 20% | Prompt template only — no script, no automation, no retry |
| **Output Validation (Phase 4.5)** | 10% | Checklist in docs — no scanner, no enforcement |
| **Project Assembly (Phase 5)** | 10% | Template in docs — no scaffold script, no framework-specific logic |
| **Test Coverage** | 40% | Strong security tests, zero functional/integration tests |
| **CI/CD** | 0% | Nothing |
| **Documentation** | 95% | Thorough across 4 guides + 2 READMEs |

---

## Key Takeaway

The extraction pipeline (Phases 2–3) is production-quality code. Everything after chunking (Phases 4–5) is documentation pretending to be implementation — it works only because Claude Code is good at following instructions, not because there's actual software enforcing it. The 20 items above are what stands between this skill and a robust, reliable tool.
