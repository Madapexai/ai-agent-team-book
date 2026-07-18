# Changelog

## [v1.1.3] - 2026-07-18

### Fixed (content editorial review — see REVIEW.md)
- **Terminology unified**: all `Subagents` / `Subagent` / `sub-Agent` / `SubAgent` variants across `zh/*.md` and `en/*.md` normalized to `Sub-Agent` / `Sub-Agents`
- **ch01**: resolved Boris Cherny event date contradiction (was "June 2026" vs "same month May 20"); both events now May 2026
- **ch03**: unified the two cost diagrams' inference-model price to `$0.15–$0.90/M tokens` (was 10× off) and moved the second diagram into the body
- **ch12**: softened "models never changed" → "model family / routing strategy never changed" (reconciles with ch13 multi-model routing); aligned Skill-promotion threshold (3→5) and dream-trigger time (midnight→2 a.m.) with the rest of the book
- **ch13**: clarified the `$847` cost breakdown is the post-incident baseline (the `$312.44` qclaw loop is one-off, not in the breakdown); clarified 43% (monthly) vs 62% (weekly) budget-remaining; fixed a bash loop bug (`kai kai_cost rex rex_cost max max_cost` → `kai rex max`); noted Rex's `$5` vs `$15` daily cap
- **ch15**: fixed a reversed core thesis in the English edition ("Spend time, not money" → "Spend money, not time"); aligned human-cost figure to ¥3,200 (≈$444) and the ROI printout with the comparison table
- **ch16**: aligned the chapter summary with the body's actual fix (strict System Prompt isolation, not "Inspector + honeypot")
- **ch17 / ch20**: fixed chapter summaries that contradicted the body (protocol layers; evolution bottlenecks)
- **ch21**: corrected "5 main + 5 sub" → "4 main + 6 sub" to match the YAML; aligned `total_monthly_cap` to 1500 with a clarifying comment; fixed Boris Cherny title (CEO→Chief Product Officer), the "Chapter 17"→"Chapter 20" cross-reference, the single-Agent cost range ($50–$500), and filled the empty closing summary
- **ch08 / ch09**: fixed handoff status `merged`→`committed` (not in the enum); made the check-in scan `grep`/`date` commands cross-platform and case-consistent
- **ch10**: renamed the Inspector's self-name `Monitor`→`Inspector` to avoid colliding with ch21's Monitor agent
- **Preface**: "Old K / Mini M" → `Kai` / `Max`
- **Corrupted image alt text** in `zh/02, 04, 06, 07, 08, 12, 16, 20, 21` rewritten (placeholder commas, `addCriterion` template residue, truncated text)

## [v1.1.2] - 2026-07-18

### Fixed
- Corrected Chapter 13 cost figures in `zh/13.md`, `en/13.md`, and the four cost/budget SVGs (`zh_13_1`, `en_13_1`, `zh_13_2`, `en_13_2`): the original alt text showed a garbled `$5000` budget that conflicted with its own math (57% used / `$212.70` remaining ⇒ a `$500` budget). All now use the internally consistent **monthly budget of `$500`** (used 57% / `$287.30`, remaining `$212.70`), keeping the per-Agent total of `$847` intact
- Rebuilt the Chapter 21 vision diagram (`zh_21_1`, `en_21_1`), which was previously drawn from a garbled alt, into the accurate "Infinite Employee" paradigm: ~`$1,500`/month API cost for 5 main + 5 sub Agents, i.e. one person running a 10-person team at the cost of ≈2 employees
- Fixed an unescaped `&` in `en_13_2.svg` so it parses as valid XML and renders on GitHub

## [v1.1.1] - 2026-07-18

### Fixed
- Removed all 80 Feishu internal image links (`internal-api-drive-stream.feishu.cn`) from `zh/*.md` and `en/*.md` — they required auth and expired, so they rendered as broken images on GitHub
- Converted `assets/banner.png` (was actually JPEG bytes in a `.png` file) to a valid PNG so the hero banner renders correctly on GitHub

## [v1.1.0] - 2026-07-18

### Added
- **Full English version (`en/`)** — all 21 chapters + preface translated, attracting an international audience
- Revamped bilingual README (`README.md` English / `README_zh.md` Chinese) with hero banner, maturity-roadmap, bilingual chapter index, star CTA, and contributing section
- Two-language chapter table linking every chapter to both `zh/` and `en/` versions

### Changed
- Rewrote both README files for clarity and appeal (why / what you'll learn / who it's for / 21-day L0→L3 path)

## [v1.0.0] - 2026-07-12

### Added
- 21 chapters of practical AI Agent team management handbook
- Chinese version (zh/) with 22 files (preface + 21 chapters)
- Bilingual README (English + Chinese)
- MIT License
- GitHub Topics and Discussions enabled
- Banner image and visual README design

### Book Series
- Part of MindApex book series (3 books total)
