# embedded-cpp-xiao

Bilingual (Thai/English) course page: embedded C++ (vs C) on Seeed XIAO nRF52840, plus Git, GitHub and CI/CD.
Published with GitHub Pages from `main` (root): Thai at `index.html`, English at `en/index.html`.
https://wiputpong-k.github.io/embedded-cpp-xiao/ (EN: `/en/`)

## Source of truth

- **Never edit `index.html` or `en/index.html` by hand.** They are generated. Edit `site-src/` and rebuild.
- `site-src/build.py` — all lesson content (`lesson(...)` calls), SVG diagrams (`SVG_*`, `flow(...)`) and the page template. Each run builds the page once per language (`LANG` = `th`, `en`).
- `site-src/style.css` — design tokens on `:root` with dark-mode overrides; use tokens, never literal colors.
- `site-src/app.js` — progress checkboxes (localStorage, wrapped in try/catch, shared by both languages) and the language switch, which keeps the lesson on screen.
- `site-src/hw/` — C++ code shown in lessons 6, 8 and 15 (`Debouncer.h`, `RingBuffer.h`, `test_main.cpp`). `build.py` embeds these files directly, so lesson code and tested code stay identical.

## Workflow

1. `git pull` first (the owner works from two computers and from Claude chat).
2. Edit files in `site-src/`.
3. If `site-src/hw/` changed, run the host tests (must print `ALL TESTS PASSED`):
   ```
   cd site-src
   g++ -std=c++17 -Wall -Wextra -Werror -Ihw/firmware/src hw/test/test_main.cpp -o test_runner && ./test_runner
   ```
4. Rebuild and copy both pages:
   - Linux/macOS: `cd site-src && python3 build.py && cp -r pages/* ../`
   - Windows (PowerShell): `cd site-src; python build.py; Copy-Item pages\* .. -Recurse -Force`
5. Open `index.html` and `en/index.html` in a browser and check the changed lesson in both languages, in light and dark mode and at phone width.
6. Commit with Conventional Commits (`feat:`, `fix:`, `docs:`, `style:`, `chore:`), one topic per commit, then push. Pages redeploys in 1–2 minutes.

Generated files (`site-src/pages/`, `site-src/course*.html`, `test_runner`) are gitignored. Do not commit them.

## Content conventions

- Every user-visible string is written as `T('ไทย', 'English')`. Thai is the source; if the English is missing, the English page shows the Thai text. When you change the Thai, update the English in the same commit.
- Thai prose keeps code, identifiers and technical terms in English. Code blocks and SVG labels may stay shared when they contain no Thai.
- Remove the "translation is in progress" note in the page template once every lesson has English.
- Each lesson: `goal(...)` → concept (+ `vs(C, C++)` when comparing) → `fig(svg, caption)` → Hands-on `code(...)` → `qa([...])` → optional `iv(...)` interview note. Target 20–30 minutes.
- Keep lessons cumulative: later lessons (11, 15–17) reuse files from earlier ones. Check downstream lessons when renaming files, pins or APIs.
- Hardware assumptions: XIAO nRF52840 (Sense), Seeed nRF52 non-mbed core, 3.3 V GPIO, on-board RGB LED is active-LOW, D0 = pot, D1 = button to GND (INPUT_PULLUP), D2 = external LED via 1 kΩ.
- Wrap any title or text inserted into HTML with `html.escape(...)`.
- SVG diagrams: use the existing classes (`b`, `ba`, `bm`, `ln`, `la`, `w`, `tt`, `sub`, `m`, `acc`) so they follow the theme; keep everything inside the `viewBox`.
- The author section uses a neutral example name in code (`"Your Name"`); do not add personal email, phone or employer details.

## Communication

The owner (Ake) prefers concise, direct answers. Reply in Thai when he writes in Thai.
