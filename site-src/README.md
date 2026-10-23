# site-src

Source used to generate `../index.html` (the course page on GitHub Pages).

- `build.py` — lesson content, diagrams (SVG) and page template
- `style.css`, `app.js` — page styles and progress-tracking script
- `hw/` — code embedded in the lessons; compiled and tested on host

Rebuild:

    python3 build.py              # writes course.html and pages/index.html
    cp pages/index.html ../index.html

Verify the embedded code:

    g++ -std=c++17 -Wall -Wextra -Werror -Ihw/firmware/src hw/test/test_main.cpp -o test_runner && ./test_runner
