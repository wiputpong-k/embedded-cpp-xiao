lesson('22', 'C', T('CI 2: compile firmware ใน CI', 'CI 2: compile the firmware in CI'), 30, PC, goal(T('เพิ่ม job ที่ compile firmware ทุกครั้งหลัง test ผ่าน และบังคับให้ PR ต้องผ่าน CI ก่อน merge', 'Add a job that compiles the firmware after the tests pass, and require PRs to pass CI before merging')) + T('''
<h3>ขั้นที่ 1: หาค่า FQBN ด้วย arduino-cli</h3>
<p>CI ไม่มี Arduino IDE ให้กด จึงใช้ arduino-cli ซึ่งเป็น Arduino แบบสั่งงานด้วยคำสั่งพิมพ์ ต้องบอกชื่อเต็มของบอร์ด (FQBN) ให้ถูก วิธีที่แน่นอนที่สุดคือถาม arduino-cli ในเครื่องเอง</p>
<ol>
<li>เปิดหน้า <a href="https://github.com/arduino/arduino-cli/releases">github.com/arduino/arduino-cli/releases</a> แล้วดาวน์โหลดไฟล์ที่ลงท้ายด้วย <code class="il">Windows_64bit.zip</code> ของเวอร์ชันล่าสุด</li>
<li>แตกไฟล์ zip ไว้ในโฟลเดอร์ที่หาง่าย เช่น <code class="il">C:\\tools\\arduino-cli</code></li>
<li>เปิดโฟลเดอร์นั้นใน File Explorer คลิกขวาที่พื้นที่ว่าง แล้วเลือก <b>Open in Terminal</b> (เปิด PowerShell)</li>
<li>รันคำสั่งข้างล่างทีละบรรทัด คำสั่งสุดท้ายจะแสดงชื่อบอร์ดพร้อม FQBN เช่น <code class="il">Seeeduino:nrf52:xiaonRF52840Sense</code></li>
</ol>''', '''
<h3>Step 1: Find the FQBN with arduino-cli</h3>
<p>CI has no Arduino IDE to click, so it uses arduino-cli, Arduino driven by typed commands. It needs the board's full name (FQBN), and the surest way to get it right is to ask arduino-cli on your own machine.</p>
<ol>
<li>Open <a href="https://github.com/arduino/arduino-cli/releases">github.com/arduino/arduino-cli/releases</a> and download the file ending in <code class="il">Windows_64bit.zip</code> from the latest release.</li>
<li>Extract the zip into a folder that is easy to find, e.g. <code class="il">C:\\tools\\arduino-cli</code>.</li>
<li>Open that folder in File Explorer, right-click an empty area and choose <b>Open in Terminal</b> (this opens PowerShell).</li>
<li>Run the commands below one line at a time. The last one lists the boards with their FQBN, e.g. <code class="il">Seeeduino:nrf52:xiaonRF52840Sense</code>.</li>
</ol>''') + code(f'''.\\arduino-cli.exe core update-index --additional-urls {SEEED_URL}
.\\arduino-cli.exe core install Seeeduino:nrf52 --additional-urls {SEEED_URL}
.\\arduino-cli.exe board listall xiao''', 'PowerShell') + T('''
<h3>ขั้นที่ 2: เพิ่ม job build-firmware</h3>
<ol>
<li>ใน Git Bash สร้าง branch ใหม่ แล้วเปิด <code class="il">.github/workflows/ci.yml</code> แทนที่เนื้อหาทั้งหมดด้วยไฟล์ข้างล่าง (ส่วน <code class="il">env:</code> และ job <code class="il">build-firmware</code> เป็นของใหม่) ถ้า FQBN ที่ได้จากขั้นที่ 1 ต่างจากในไฟล์ ให้แก้ให้ตรง</li>
<li>commit, push, เปิด PR แล้วรอ job ทั้งสองเป็นสีเขียว job ที่สองใช้เวลานานกว่าเพราะต้องดาวน์โหลด core</li>
<li>เปิดหน้า run ในแท็บ <b>Actions</b> เลื่อนลงไปที่ส่วน <b>Artifacts</b> ดาวน์โหลด <i>firmware</i> แล้วดูว่ามีไฟล์ .hex และ .zip</li>
<li>merge PR</li>
</ol>''', '''
<h3>Step 2: Add the build-firmware job</h3>
<ol>
<li>In Git Bash, create a new branch, open <code class="il">.github/workflows/ci.yml</code> and replace its content with the file below (the <code class="il">env:</code> section and the <code class="il">build-firmware</code> job are new). If the FQBN from step 1 differs from the one in the file, change it to match.</li>
<li>Commit, push, open a PR and wait for both jobs to turn green. The second job takes longer because it downloads the core.</li>
<li>Open the run in the <b>Actions</b> tab, scroll to the <b>Artifacts</b> section, download <i>firmware</i> and check that it contains a .hex and a .zip.</li>
<li>Merge the PR.</li>
</ol>''') + code(CI_ON + CI_ENV + CI_HOST + CI_BUILD, '.github/workflows/ci.yml', en=CI_EN) + code('''git switch -c ci/build-firmware
# แก้ ci.yml แล้วบันทึก จากนั้น:
git add .github/
git commit -m "ci: compile firmware after host tests"
git push -u origin ci/build-firmware
gh pr create --fill
gh pr checks --watch''', 'Git Bash', en={'# แก้ ci.yml แล้วบันทึก จากนั้น:': '# edit ci.yml and save, then:'}) + T('''
<h3>ขั้นที่ 3: บังคับให้ PR ต้องผ่าน CI</h3>
<ol>
<li>บน GitHub ไปที่ <b>Settings → Branches</b> แล้วแก้กฎของ <code class="il">main</code> ที่สร้างไว้ในบท 18</li>
<li>เปิด <b>Require status checks to pass before merging</b> แล้วค้นหาและเพิ่ม <code class="il">host-tests</code> กับ <code class="il">build-firmware</code> แล้วบันทึก</li>
<li>ใส่ badge แสดงสถานะ CI ไว้บนสุดของ README (เปลี่ยน <code class="il">&lt;user&gt;</code> เป็นชื่อบัญชี GitHub ของคุณ) แล้ว commit ผ่าน PR</li>
</ol>''', '''
<h3>Step 3: Require PRs to pass CI</h3>
<ol>
<li>On GitHub, go to <b>Settings → Branches</b> and edit the <code class="il">main</code> rule you created in lesson 18.</li>
<li>Turn on <b>Require status checks to pass before merging</b>, search for and add <code class="il">host-tests</code> and <code class="il">build-firmware</code>, and save.</li>
<li>Add a CI status badge at the top of the README (replace <code class="il">&lt;user&gt;</code> with your GitHub account name) and commit it through a PR.</li>
</ol>''') + code('![CI](https://github.com/<user>/xiao-embedded-cpp/actions/workflows/ci.yml/badge.svg)', 'README.md') + T('''
<p class="note">ถ้า compile ใน CI ล้มที่ขั้น packaging ให้ดูว่าติดตั้ง adafruit-nrfutil แล้ว และ FQBN ตรงกับที่ <code class="il">arduino-cli board listall xiao</code> แสดง เวอร์ชัน core ควร pin ด้วย <code class="il">Seeeduino:nrf52@x.y.z</code> เพื่อให้ build ซ้ำได้เหมือนเดิม</p>
''', '''
<p class="note">If the CI compile fails at the packaging step, check that adafruit-nrfutil is installed and that the FQBN matches what <code class="il">arduino-cli board listall xiao</code> shows. Pin the core version with <code class="il">Seeeduino:nrf52@x.y.z</code> so builds are reproducible.</p>
''') + qa([(T('needs: host-tests มีไว้ทำไม?', 'What is needs: host-tests for?'),
           T('ให้ build-firmware รันหลัง test ผ่านเท่านั้น ประหยัดเวลาและสื่อลำดับความสำคัญ ถ้าไม่ใส่ 2 job จะรันขนานกัน', 'build-firmware runs only after the tests pass, which saves time and makes the order of priority clear. Without it, the two jobs run in parallel.')),
          (T('ทำไมต้อง pin เวอร์ชัน core / action?', 'Why pin the core and action versions?'),
           T('ให้ build reproducible ถ้า core อัปเดตเอง firmware อาจเปลี่ยนพฤติกรรมโดยไม่มีใครแก้โค้ด เป็นหลักเดียวกับ BOM lock ในฮาร์ดแวร์', 'For reproducible builds. If the core updates itself, the firmware may change behavior without anyone touching the code. It is the same idea as a locked BOM in hardware.'))])
   + iv(T('ในทีม CI กับ CD มักถูกพูดปนกัน: CI = รวมโค้ดบ่อยและตรวจอัตโนมัติทุกครั้ง, CD = ส่งมอบ artifact ที่พร้อมใช้อัตโนมัติ (บทถัดไป) แยกให้ชัดแล้วจะคุยเรื่อง pipeline กันง่ายขึ้น',
          'Teams often mix up CI and CD: CI = integrate code often and check it automatically every time; CD = deliver ready-to-use artifacts automatically (next lesson). Keeping them apart makes pipeline discussions easier.')))
