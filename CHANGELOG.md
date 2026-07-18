# Changelog

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
