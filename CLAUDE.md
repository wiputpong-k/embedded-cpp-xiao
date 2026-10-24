# embedded-cpp-xiao

Bilingual (Thai/English) course page: embedded C++ (vs C) on Seeed XIAO nRF52840, plus Git, GitHub and CI/CD.
Published with GitHub Pages from `main` (root): a home page plus one page per lesson. Thai at `index.html` and `lesson/NN/`, English under `en/`, shared `assets/style.css` and `assets/app.js`.
https://wiputpong-k.github.io/embedded-cpp-xiao/ (EN: `/en/`)

## Source of truth

- **Never edit `index.html`, `lesson/`, `en/` or `assets/` at the repo root by hand.** They are generated. Edit `site-src/` and rebuild.
- `site-src/lessons/lNN.py` — one file per lesson (25 lessons, `00`–`24`), each with one `lesson(...)` call. `build.py` runs them in file order with its helpers in scope; a lesson may define constants that a later lesson reuses (e.g. `LED_CLASS` in `l04.py`, `FW_HEAD` in `l13.py`, `CI_HOST` in `l21.py`).
- `site-src/build.py` — helpers (`T`, `tr`, `code`, `fig`, `goal`, `vs`, `qa`, `iv`), SVG diagrams (`SVG_*`, `flow(...)`), module names and the page templates (home, lesson pages, search index). Each run builds every page once per language (`LANG` = `th`, `en`) into `site-src/pages/`.
- `site-src/style.css` — design tokens on `:root` with dark-mode overrides; use tokens, never literal colors.
- `site-src/app.js` — progress (localStorage key `xiao-cpp-done-v2`, wrapped in try/catch, shared by both languages), last opened lesson, home search and continue button, copy buttons, and the language switch, which keeps the section on screen.
- `site-src/hw/` — C++ code shown in lessons 07, 10 and 19 (`Debouncer.h`, `RingBuffer.h`, `test_main.cpp`). `build.py` embeds these files directly, so lesson code and tested code stay identical.

## Workflow

1. `git pull` first (the owner works from two computers and from Claude chat).
2. Edit files in `site-src/`.
3. If `site-src/hw/` changed, run the host tests (must print `ALL TESTS PASSED`):
   ```
   cd site-src
   g++ -std=c++17 -Wall -Wextra -Werror -Ihw/firmware/src hw/test/test_main.cpp -o test_runner && ./test_runner
   ```
4. Rebuild and copy the site:
   - Linux/macOS: `cd site-src && python3 build.py && cp -r pages/* ../`
   - Windows (PowerShell): `cd site-src; python build.py; Copy-Item pages\* .. -Recurse -Force`
5. Preview with a local server (links between pages need one): `python -m http.server 8765 -d site-src/pages`, then open http://localhost:8765/. Check the changed lesson in both languages, in light and dark mode and at phone width.
6. Commit with Conventional Commits (`feat:`, `fix:`, `docs:`, `style:`, `chore:`), one topic per commit, then push. Pages redeploys in 1–2 minutes.

Generated files (`site-src/pages/`, `test_runner`) are gitignored. Do not commit them. The copies at the repo root are committed, because Pages serves them.

## Content conventions

- Every user-visible string is written as `T('ไทย', 'English')`. Thai is the source; if the English is missing, the English page shows the Thai text. When you change the Thai, update the English in the same commit.
- Thai prose keeps code, identifiers and technical terms in English. Code blocks and SVG labels may stay shared when they contain no Thai.
- Thai inside shared code or hand-drawn SVGs is swapped with `tr(s, {'ไทย': 'English'})` (`code(..., en={...})` for code blocks; the SVG block sits just above `# lessons`). `tr()` fails the build if a Thai fragment no longer matches, so update the mapping when you edit that text. Keep English SVG labels inside the `viewBox`.
- Each lesson: `goal(...)` → concept (+ `vs(C, C++)` when comparing) → `fig(svg, caption)` → Hands-on `code(...)` → `qa([...])` → optional `iv(...)` "In practice" note (how the topic shows up in real firmware work; keep job-application and interview framing out of the course). Target 20–30 minutes; split a lesson rather than go over 30. Write hands-on steps so a beginner can follow them: where to download, which menu to click, and how to check it worked.
- Keep lessons cumulative: later lessons (13–14, 15, 19–23) reuse files from earlier ones. Check downstream lessons when renaming files, pins or APIs. When adding, removing or renumbering lessons, update every "บท NN" / "lesson NN" reference.
- Hardware assumptions: XIAO nRF52840 (Sense), Seeed nRF52 non-mbed core, 3.3 V GPIO, on-board RGB LED is active-LOW, D0 = pot, D1 = button to GND (INPUT_PULLUP), D2 = external LED via 1 kΩ.
- Wrap any title or text inserted into HTML with `html.escape(...)`.
- Third-party images (e.g. Seeed board photos and pinouts): use `photo(...)`, which links the image from its original URL with a visible source credit. Do not copy third-party image files into the repo. The owner's own photos may live in the repo.
- SVG diagrams: use the existing classes (`b`, `ba`, `bm`, `ln`, `la`, `w`, `tt`, `sub`, `m`, `acc`) so they follow the theme; keep everything inside the `viewBox`.
- The author section uses a neutral example name in code (`"Your Name"`); do not add personal email, phone or employer details.

## Communication

The owner (Ake) prefers concise, direct answers. Reply in Thai when he writes in Thai.
