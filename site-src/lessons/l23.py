REL_YML = '''name: Release

on:
  push:
    tags: ['v*.*.*']

permissions:
  contents: write

env:
  BOARD_URL: https://files.seeedstudio.com/arduino/package_seeeduino_boards_index.json
  FQBN: Seeeduino:nrf52:xiaonRF52840Sense

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install adafruit-nrfutil
      - uses: arduino/setup-arduino-cli@v2
      - run: |
          arduino-cli core update-index --additional-urls "$BOARD_URL"
          arduino-cli core install Seeeduino:nrf52 --additional-urls "$BOARD_URL"
      - name: Stamp version
        run: echo "#define FW_VERSION \\"${GITHUB_REF_NAME}\\"" > firmware/src/version.h
      - name: Compile
        run: arduino-cli compile --fqbn "$FQBN" --additional-urls "$BOARD_URL" --output-dir out firmware
      - uses: softprops/action-gh-release@v2
        with:
          files: |
            out/*.hex
            out/*.zip
          generate_release_notes: true'''

lesson('23', 'C', T('CD: release firmware อัตโนมัติด้วย tag', 'CD: automatic firmware releases from tags'), 30, T('บอร์ด + คอมพิวเตอร์', 'Board + computer'), goal(T('push tag แล้วได้ GitHub Release ที่มีไฟล์ firmware และเลขเวอร์ชันฝังในตัว แล้วแฟลชไฟล์นั้นลงบอร์ดได้', 'Push a tag, get a GitHub Release with the firmware files and the version number built in, and flash that file onto the board'))
   + fig(SVG_REL, T('จาก tag ถึงไฟล์ที่ QA ดาวน์โหลดไปแฟลช', 'From a tag to the file QA downloads and flashes')) + T('''
<p>CD (Continuous Delivery) คือการส่งมอบไฟล์ที่พร้อมใช้งานโดยอัตโนมัติ workflow ในบทนี้ทำงานเมื่อ push <b>tag</b> ที่ขึ้นต้นด้วย <code class="il">v</code> เช่น <code class="il">v0.1.0</code> มันจะสร้างไฟล์ <code class="il">version.h</code> จากชื่อ tag, compile firmware แล้วสร้างหน้า GitHub Release พร้อมแนบไฟล์ให้ดาวน์โหลด</p>
<p>บทนี้พิสูจน์ว่าไฟล์ที่ลงบอร์ดสร้างจาก tag โดยเครื่อง CI ไม่ใช่จากเครื่องใครคนหนึ่ง และ firmware บอกเวอร์ชันของตัวเองได้</p>
<h3>ขั้นที่ 1: เพิ่ม workflow release</h3>
<p>main ถูกตั้งกฎให้รับการเปลี่ยนแปลงผ่าน PR เท่านั้น (บท 18) จึงต้องเพิ่มไฟล์นี้ผ่าน PR เหมือนเดิม สร้างไฟล์ <code class="il">.github/workflows/release.yml</code> ด้วยเนื้อหาข้างล่าง แล้วรันคำสั่งชุดถัดไป</p>
''', '''
<p>CD (Continuous Delivery) means delivering ready-to-use files automatically. The workflow in this lesson runs when you push a <b>tag</b> starting with <code class="il">v</code>, such as <code class="il">v0.1.0</code>. It writes <code class="il">version.h</code> from the tag name, compiles the firmware, and creates a GitHub Release page with the files attached for download.</p>
<p>This lesson proves that the file on the board was built from a tag by the CI machine, not on someone's PC, and that the firmware can report its own version.</p>
<h3>Step 1: Add the release workflow</h3>
<p>main only accepts changes through PRs (lesson 18), so add this file through a PR as before. Create <code class="il">.github/workflows/release.yml</code> with the content below, then run the next set of commands.</p>
''') + code(REL_YML, '.github/workflows/release.yml') + T('''
<p>ส่วนที่ต่างจาก <code class="il">ci.yml</code>:</p>
<ul>
<li><code class="il">tags: ['v*.*.*']</code> รันเฉพาะเมื่อ push tag ที่มีรูปแบบ v ตามด้วยตัวเลข 3 ชุด เช่น <code class="il">v0.1.0</code> ไม่รันตอน push code ปกติ</li>
<li><code class="il">permissions: contents: write</code> ให้สิทธิ์ workflow เขียนลง repo ได้ เพราะต้องสร้างหน้า Release (ดูคำถามข้อสอง)</li>
<li><i>Stamp version</i> เขียนไฟล์ <code class="il">firmware/src/version.h</code> หนึ่งบรรทัดคือ <code class="il">#define FW_VERSION "v0.1.0"</code> โดย <code class="il">GITHUB_REF_NAME</code> คือชื่อ tag ที่ push มา บรรทัด <code class="il">#if __has_include("src/version.h")</code> ใน firmware.ino (บท 13–14) จะเจอไฟล์นี้และใช้ค่าแทน <code class="il">"dev"</code></li>
<li><code class="il">action-gh-release</code> สร้างหน้า Release แนบไฟล์ .hex และ .zip ส่วน <code class="il">generate_release_notes</code> เขียนรายการสิ่งที่เปลี่ยนจากชื่อ PR ให้เอง</li>
</ul>
''', '''
<p>What differs from <code class="il">ci.yml</code>:</p>
<ul>
<li><code class="il">tags: ['v*.*.*']</code>: runs only when you push a tag shaped like v plus three numbers, e.g. <code class="il">v0.1.0</code>, not on ordinary code pushes.</li>
<li><code class="il">permissions: contents: write</code>: lets the workflow write to the repo, which creating a Release page needs (see the second question).</li>
<li><i>Stamp version</i> writes <code class="il">firmware/src/version.h</code> with one line, <code class="il">#define FW_VERSION "v0.1.0"</code>; <code class="il">GITHUB_REF_NAME</code> is the name of the pushed tag. The <code class="il">#if __has_include("src/version.h")</code> line in firmware.ino (lessons 13–14) finds this file and uses it instead of <code class="il">"dev"</code>.</li>
<li><code class="il">action-gh-release</code> creates the Release page with the .hex and .zip attached; <code class="il">generate_release_notes</code> writes the list of changes from your PR titles.</li>
</ul>
''') + code('''git switch -c ci/release
git add .github/workflows/release.yml
git commit -m "ci: release firmware on version tag"
git push -u origin ci/release
gh pr create --fill
gh pr checks --watch
gh pr merge --squash --delete-branch
git switch main
git pull''', 'Git Bash') + T('''
<h3>ขั้นที่ 2: ติด tag แล้ว push</h3>
<p>tag คือป้ายชื่อที่ติดไว้กับ commit หนึ่ง ใช้บอกว่า commit นี้คือเวอร์ชันอะไร การ push tag ไม่ต้องผ่าน PR หลัง push ให้เปิดแท็บ <b>Actions</b> ดู workflow <i>Release</i> ทำงาน เมื่อเสร็จจะมีหน้า Release ใหม่ (<code class="il">gh release view --web</code>)</p>''', '''
<h3>Step 2: Tag and push</h3>
<p>A tag is a label attached to one commit, saying which version it is. Pushing a tag does not need a PR. After the push, open the <b>Actions</b> tab and watch the <i>Release</i> workflow run. When it finishes there is a new Release page (<code class="il">gh release view --web</code>).</p>''') + code('''git tag -a v0.1.0 -m "first release: scheduler, debounce, moving average"
git push origin v0.1.0
gh release view --web''', 'Git Bash') + T('''
<h3>ขั้นที่ 3: แฟลชไฟล์จาก Release ลงบอร์ด</h3>
<p>บอร์ด XIAO nRF52840 รับ firmware ผ่าน bootloader ด้วยไฟล์ <code class="il">.zip</code> ที่เรียกว่า DFU package (DFU = Device Firmware Update คือการส่ง firmware ใหม่ให้ bootloader เขียนลง flash ตามบท 01) ไม่ใช่ไฟล์ .hex โดยตรง Arduino IDE ทำขั้นนี้ให้ทุกครั้งที่กด Upload ส่วนไฟล์จาก Release ต้องใช้เครื่องมือ <code class="il">adafruit-nrfutil</code></p>
<ol>
<li>ถ้ายังไม่มี Python ให้ติดตั้งก่อน (คำสั่งแรกข้างล่าง ใน PowerShell) แล้วปิด terminal เปิดใหม่ จากนั้นติดตั้ง <code class="il">adafruit-nrfutil</code> ด้วย pip</li>
<li>ใน Git Bash ดาวน์โหลดไฟล์ <code class="il">.zip</code> จาก Release (ชื่อประมาณ <code class="il">firmware.ino.zip</code>)</li>
<li>กดปุ่ม reset บนบอร์ด 2 ครั้งเร็ว ๆ ให้เข้า bootloader แล้วดูเลขพอร์ตใน Arduino IDE ที่ <b>Tools → Port</b> (เช่น COM5)</li>
<li>รันคำสั่ง <code class="il">adafruit-nrfutil</code> โดยเปลี่ยน <code class="il">COM5</code> เป็นพอร์ตของคุณ รอจนขึ้นว่า Device programmed</li>
<li>เปิด Serial Monitor (115200 baud) แล้วกด reset 1 ครั้ง ต้องเห็น <code class="il">fw v0.1.0</code> (ถ้า build จาก IDE ในเครื่องจะเห็น <code class="il">fw dev</code>)</li>
</ol>''', '''
<h3>Step 3: Flash the Release file onto the board</h3>
<p>The XIAO nRF52840 takes firmware through its bootloader as a <code class="il">.zip</code> called a DFU package (DFU = Device Firmware Update: sending new firmware for the bootloader to write into flash, lesson 01), not as a raw .hex. Arduino IDE does this for you on every Upload; for a file from a Release you use the <code class="il">adafruit-nrfutil</code> tool.</p>
<ol>
<li>If you do not have Python yet, install it first (the first command below, in PowerShell), close the terminal and open it again. Then install <code class="il">adafruit-nrfutil</code> with pip.</li>
<li>In Git Bash, download the <code class="il">.zip</code> from the Release (named something like <code class="il">firmware.ino.zip</code>).</li>
<li>Double-press the reset button on the board to enter the bootloader, and check the port number in Arduino IDE under <b>Tools → Port</b> (e.g. COM5).</li>
<li>Run the <code class="il">adafruit-nrfutil</code> command with <code class="il">COM5</code> replaced by your port, and wait for "Device programmed".</li>
<li>Open Serial Monitor (115200 baud) and press reset once. You should see <code class="il">fw v0.1.0</code> (a build from your local IDE shows <code class="il">fw dev</code>).</li>
</ol>''') + code('''winget install -e --id Python.Python.3.12
pip install adafruit-nrfutil''', 'PowerShell') + code('''gh release download v0.1.0 --pattern "*.zip"
adafruit-nrfutil --verbose dfu serial --package firmware.ino.zip -p COM5 -b 115200 --singlebank''', 'Git Bash') + T('''
<p>ผลนี้บอกอะไร: เห็น <code class="il">fw v0.1.0</code> แทน <code class="il">fw dev</code> แปลว่า firmware บนบอร์ดคือไฟล์ที่ CI build จาก tag นั้นจริง เรียกว่า <b>traceability</b>: รู้เสมอว่าบอร์ดตัวไหนรัน firmware เวอร์ชันไหน และย้อนไปดูโค้ดของเวอร์ชันนั้นได้จาก tag</p>
<p class="note">ตั้งเลขเวอร์ชันแบบ SemVer: MAJOR.MINOR.PATCH แก้บั๊กเพิ่ม PATCH, เพิ่มฟีเจอร์ที่ยังใช้กับของเดิมได้เพิ่ม MINOR, เปลี่ยนแบบที่ของเดิมใช้ไม่ได้ (เช่น เปลี่ยนรูปแบบคำสั่ง Serial) เพิ่ม MAJOR</p>
''', '''
<p>What this tells you: seeing <code class="il">fw v0.1.0</code> instead of <code class="il">fw dev</code> means the firmware on the board really is the file CI built from that tag. This is <b>traceability</b>: you always know which firmware version each board runs, and the tag takes you back to that version's code.</p>
<p class="note">Number versions with SemVer: MAJOR.MINOR.PATCH. A bug fix bumps PATCH, a feature that still works with the old version bumps MINOR, and a change the old version cannot handle (e.g. a new Serial command format) bumps MAJOR.</p>
''') + qa([(T('ทำไมสร้าง version.h ใน CI แทนเขียนเลขเวอร์ชันในโค้ด?', 'Why generate version.h in CI instead of writing the version in the code?'),
           T('ให้ tag เป็นแหล่งความจริงแหล่งเดียว ลืมแก้เลขไม่ได้ และ build ในเครื่องจะติด "dev" ชัดเจนว่าไม่ใช่ของ release', 'The tag becomes the single source of truth, so you cannot forget to bump the number, and local builds say "dev", clearly not a release.')),
          (T('permissions: contents: write จำเป็นไหม?', 'Is permissions: contents: write required?'),
           T('จำเป็น workflow ใช้ GITHUB_TOKEN (กุญแจชั่วคราวที่ GitHub ออกให้ทุกครั้งที่รัน) ซึ่งในหลาย repo อ่านได้อย่างเดียวเป็นค่าเริ่มต้น การสร้าง Release ต้องได้สิทธิ์เขียน', 'Yes. The workflow uses GITHUB_TOKEN (a temporary key GitHub issues for every run), which is read-only by default in many repos, and creating a Release needs write access.'))]))
