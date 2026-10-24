CI_ON = '''name: CI

on:
  push:
    branches: [main]
  pull_request:
'''
CI_ENV = '''
env:
  BOARD_URL: https://files.seeedstudio.com/arduino/package_seeeduino_boards_index.json
  FQBN: Seeeduino:nrf52:xiaonRF52840Sense   # ใช้ค่าที่ได้จาก board listall
'''
CI_HOST = '''
jobs:
  host-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Build tests
        run: g++ -std=c++17 -Wall -Wextra -Werror -Ifirmware/src test/test_main.cpp -o test_runner
      - name: Run tests
        run: ./test_runner
      - name: Static analysis
        run: |
          sudo apt-get update && sudo apt-get install -y cppcheck
          cppcheck --error-exitcode=1 --enable=warning,performance --std=c++17 -Ifirmware/src test/test_main.cpp
'''
CI_BUILD = '''
  build-firmware:
    needs: host-tests
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install adafruit-nrfutil   # core ใช้ตอนแพ็ก .zip บน Linux
      - uses: arduino/setup-arduino-cli@v2
      - name: Install board core
        run: |
          arduino-cli core update-index --additional-urls "$BOARD_URL"
          arduino-cli core install Seeeduino:nrf52 --additional-urls "$BOARD_URL"
      - name: Compile
        run: arduino-cli compile --fqbn "$FQBN" --additional-urls "$BOARD_URL" --output-dir out firmware
      - uses: actions/upload-artifact@v4
        with:
          name: firmware
          path: out/'''
CI_EN = {'# ใช้ค่าที่ได้จาก board listall': '# use the value from board listall', '# core ใช้ตอนแพ็ก .zip บน Linux': '# the core needs it to package the .zip on Linux'}

lesson('21', 'C', T('CI 1: รัน test อัตโนมัติด้วย GitHub Actions', 'CI 1: run tests automatically with GitHub Actions'), 30, PC, goal(T('ทุก push และทุก PR ถูก test อัตโนมัติบนเซิร์ฟเวอร์ของ GitHub', 'Every push and every PR is tested automatically on GitHub\'s servers')) + T('''
<p>CI (Continuous Integration) คือการให้เครื่องตรวจโค้ดทุกครั้งที่มีการเปลี่ยนแปลง GitHub Actions อ่านไฟล์ workflow (เขียนด้วย YAML) ในโฟลเดอร์ <code class="il">.github/workflows/</code> แล้วเปิดเครื่อง Linux ชั่วคราว (runner) มารันคำสั่งตามนั้น บทนี้เริ่มจาก job เดียวคือ <code class="il">host-tests</code> ที่รัน test จากบท 19–20 บทหน้าจะเพิ่ม job compile firmware</p>
''', '''
<p>CI (Continuous Integration) means a machine checks the code on every change. GitHub Actions reads workflow files (written in YAML) in <code class="il">.github/workflows/</code>, starts a temporary Linux machine (a runner) and runs the commands in them. This lesson starts with one job, <code class="il">host-tests</code>, which runs the tests from lessons 19–20. The next lesson adds a job that compiles the firmware.</p>
''') + fig(SVG_CI, T('workflow 2 job: test ก่อน ผ่านแล้วค่อย build (บทนี้ทำ job แรก)', 'A 2-job workflow: test first, build only after the tests pass (this lesson covers the first job)')) + T('''
<h3>Hands-on</h3>
<ol>
<li>ใน Git Bash เข้าไปที่ repo สร้าง branch ใหม่ และสร้างโฟลเดอร์ <code class="il">.github/workflows</code> (3 บรรทัดแรกของชุดคำสั่งข้างล่าง)</li>
<li>รัน <code class="il">notepad .github/workflows/ci.yml</code> วางเนื้อหา <code class="il">ci.yml</code> ข้างล่าง แล้วบันทึก YAML นับการเว้นวรรคเป็นโครงสร้าง ต้องใช้ space ห้ามใช้ Tab และระยะย่อหน้าต้องตรงตามตัวอย่าง</li>
<li>commit, push แล้วเปิด PR จากนั้นรัน <code class="il">gh pr checks --watch</code> เพื่อดูสถานะ job แบบ live</li>
<li>เปิดหน้า PR บนเว็บ แท็บ <b>Checks</b> หรือแท็บ <b>Actions</b> ของ repo คลิกที่ job <code class="il">host-tests</code> แล้วคลิกแต่ละ step เพื่อดู log</li>
<li>เมื่อเป็นสีเขียวแล้ว merge PR นี้ (<code class="il">gh pr merge --squash --delete-branch</code>)</li>
</ol>''', '''
<h3>Hands-on</h3>
<ol>
<li>In Git Bash, go into the repo, create a new branch and create the <code class="il">.github/workflows</code> folder (the first 3 lines below).</li>
<li>Run <code class="il">notepad .github/workflows/ci.yml</code>, paste the <code class="il">ci.yml</code> content below and save. YAML uses indentation as structure: use spaces, never Tab, and keep the indentation exactly as shown.</li>
<li>Commit, push and open a PR, then run <code class="il">gh pr checks --watch</code> to watch the job status live.</li>
<li>Open the PR on the web, go to the <b>Checks</b> tab (or the repo's <b>Actions</b> tab), click the <code class="il">host-tests</code> job and click each step to read its log.</li>
<li>When it is green, merge the PR (<code class="il">gh pr merge --squash --delete-branch</code>).</li>
</ol>''') + code('''cd ~/xiao-embedded-cpp
git switch -c ci/host-tests
mkdir -p .github/workflows
# วาง ci.yml แล้วบันทึก จากนั้น:
git add .github/
git commit -m "ci: run host tests on every push and PR"
git push -u origin ci/host-tests
gh pr create --fill
gh pr checks --watch        # ดูสถานะ job แบบ live''', 'Git Bash', en={'# วาง ci.yml แล้วบันทึก จากนั้น:': '# paste ci.yml and save, then:', '# ดูสถานะ job แบบ live': '# watch job status live'})
   + code(CI_ON + CI_HOST, '.github/workflows/ci.yml') + T('''
<h3>ลองทำให้ CI แดง</h3>
<p>สร้าง branch ใหม่ แก้ <code class="il">&gt;=</code> ใน Debouncer.h เป็น <code class="il">&gt;</code> แบบบท 20 แล้ว push และเปิด PR หน้า PR จะขึ้นกากบาทสีแดง คลิกดู log ของ step <i>Run tests</i> จะเห็นบรรทัด FAIL เดียวกับที่เห็นในเครื่อง จากนั้นปิด PR นี้ทิ้งด้วย <code class="il">gh pr close --delete-branch</code></p>
''', '''
<h3>Make CI fail on purpose</h3>
<p>Create a new branch, change <code class="il">&gt;=</code> to <code class="il">&gt;</code> in Debouncer.h as in lesson 20, push and open a PR. The PR shows a red cross; open the log of the <i>Run tests</i> step and you see the same FAIL line you saw locally. Then close that PR with <code class="il">gh pr close --delete-branch</code>.</p>
''') + qa([(T('runner ของ GitHub เป็น Linux แต่เครื่องเราเป็น Windows ทำไม test ยังได้ผลเหมือนกัน?', 'The GitHub runner is Linux and your PC is Windows. Why do the tests give the same result?'),
           T('เพราะโค้ดที่ test เป็น C++ มาตรฐานล้วน ไม่ขึ้นกับระบบปฏิบัติการหรือฮาร์ดแวร์ นี่คืออีกประโยชน์ของการแยก logic ออกจากฮาร์ดแวร์ในบท 19', 'Because the code under test is plain standard C++ that does not depend on the OS or hardware. That is another benefit of separating logic from hardware in lesson 19.')),
          (T('ทำไม job ถึงขึ้นสีแดงเมื่อ test fail?', 'Why does the job turn red when a test fails?'),
           T('./test_runner คืน exit code 1 เมื่อมี CHECK ไม่ผ่าน GitHub Actions ถือว่า step ที่คืนค่าไม่เป็น 0 คือ fail และหยุด job ทันที', './test_runner returns exit code 1 when any CHECK fails. GitHub Actions treats any step that returns non-zero as failed and stops the job.'))]))
