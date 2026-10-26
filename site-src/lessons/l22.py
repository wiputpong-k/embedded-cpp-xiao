lesson('22', 'C', T('CI 2: compile firmware ใน CI', 'CI 2: compile the firmware in CI'), 30, PC, goal(T('เพิ่ม job ที่ compile firmware ทุกครั้งหลัง test ผ่าน และบังคับให้ PR ต้องผ่าน CI ก่อน merge', 'Add a job that compiles the firmware after the tests pass, and require PRs to pass CI before merging')) + T('''
<p>บทที่แล้ว CI รัน test ของ logic แต่ยังไม่รู้ว่า firmware ทั้งก้อน compile ผ่านหรือเปล่า บทนี้พิสูจน์ว่า firmware build ได้บนเครื่องเปล่าที่ไม่ใช่เครื่องเรา (ไม่ใช่แค่ "ในเครื่องผมได้") และ PR ที่ทำให้ build พังจะ merge ไม่ได้</p>
<h3>ขั้นที่ 1: หาค่า FQBN ด้วย arduino-cli</h3>
<p>CI ไม่มี Arduino IDE ให้กด จึงใช้ <b>arduino-cli</b> คือ Arduino แบบสั่งงานด้วยคำสั่งพิมพ์ (Arduino IDE 2 เองก็เรียก arduino-cli อยู่เบื้องหลัง) ต้องบอกชื่อเต็มของบอร์ดที่เรียกว่า <b>FQBN</b> (Fully Qualified Board Name) ในรูป <code class="il">ผู้ผลิต:สถาปัตยกรรม:บอร์ด</code> บรรทัดแรกของ verbose output ในบท 01 ก็แสดงค่านี้</p>
<ol>
<li>Arduino IDE 2 มี arduino-cli มาให้แล้ว และใช้ core ที่ติดตั้งไว้ในบท 00 ตัวเดียวกัน เปิด PowerShell แล้วรันคำสั่งข้างล่าง (ถ้าติดตั้ง IDE ไว้ที่อื่น ให้แก้ path ให้ตรง)</li>
<li>มองหาบรรทัด <i>Seeed XIAO nRF52840 Sense</i> ค่า FQBN คือ <code class="il">Seeeduino:nrf52:xiaonRF52840Sense</code> ถ้าบอร์ดของคุณไม่ใช่รุ่น Sense ให้ใช้ค่าของรุ่นนั้นแทน</li>
</ol>
<p class="note">macOS / Linux หรือไม่ได้ใช้ Arduino IDE 2: ดาวน์โหลด arduino-cli จาก <a href="https://github.com/arduino/arduino-cli/releases">github.com/arduino/arduino-cli/releases</a> แล้วรัน <code class="il">core install Seeeduino:nrf52 --additional-urls …</code> ก่อน <code class="il">board listall</code> แบบเดียวกับขั้น <i>Install board core</i> ใน ci.yml ข้างล่าง</p>
''', '''
<p>The last lesson's CI tests the logic, but nobody checks yet that the whole firmware compiles. This lesson proves that the firmware builds on a clean machine that is not yours (not just "works on my PC"), and that a PR that breaks the build cannot be merged.</p>
<h3>Step 1: Find the FQBN with arduino-cli</h3>
<p>CI has no Arduino IDE to click, so it uses <b>arduino-cli</b>, Arduino driven by typed commands (Arduino IDE 2 itself runs arduino-cli behind the scenes). It needs the board's full name, the <b>FQBN</b> (Fully Qualified Board Name), in the form <code class="il">vendor:architecture:board</code>. The first line of the verbose output in lesson 01 shows it too.</p>
<ol>
<li>Arduino IDE 2 ships with arduino-cli and shares the core you installed in lesson 00. Open PowerShell and run the command below (if the IDE is installed elsewhere, adjust the path).</li>
<li>Find the <i>Seeed XIAO nRF52840 Sense</i> line. Its FQBN is <code class="il">Seeeduino:nrf52:xiaonRF52840Sense</code>. If your board is not the Sense model, use that model's value instead.</li>
</ol>
<p class="note">macOS / Linux, or not using Arduino IDE 2: download arduino-cli from <a href="https://github.com/arduino/arduino-cli/releases">github.com/arduino/arduino-cli/releases</a> and run <code class="il">core install Seeeduino:nrf52 --additional-urls …</code> before <code class="il">board listall</code>, as in the <i>Install board core</i> step of ci.yml below.</p>
''') + code('''& "C:\\Program Files\\Arduino IDE\\resources\\app\\lib\\backend\\resources\\arduino-cli.exe" board listall xiao''', 'PowerShell') + code('''Board Name                     FQBN
Seeed XIAO nRF52840            Seeeduino:nrf52:xiaonRF52840
Seeed XIAO nRF52840 Plus       Seeeduino:nrf52:xiaonRF52840Plus
Seeed XIAO nRF52840 Sense      Seeeduino:nrf52:xiaonRF52840Sense
Seeed XIAO nRF52840 Sense Plus Seeeduino:nrf52:xiaonRF52840SensePlus''', T('ผลที่ควรเห็น', 'Expected output')) + T('''
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
</ol>''') + code(CI_ON + CI_ENV + CI_HOST + CI_BUILD, '.github/workflows/ci.yml', en=CI_EN) + T('''
<p>ส่วนที่เพิ่มจากบท 21:</p>
<ul>
<li><code class="il">env:</code> ตัวแปรที่ทุก job ใช้ร่วมกัน เรียกในคำสั่งด้วย <code class="il">"$BOARD_URL"</code> และ <code class="il">"$FQBN"</code> แก้ที่เดียวพอ</li>
<li><code class="il">needs: host-tests</code> ให้ job นี้รอจน <code class="il">host-tests</code> ผ่านก่อนค่อยเริ่ม</li>
<li><code class="il">setup-python</code> + <code class="il">pip install adafruit-nrfutil</code> เครื่องมือที่ core ใช้แพ็กไฟล์ .zip สำหรับ bootloader (บท 23) บน Linux ต้องติดตั้งเอง</li>
<li><code class="il">setup-arduino-cli</code> และขั้น <i>Install board core</i> ติดตั้ง arduino-cli และ core ของ Seeed ทุกครั้ง เพราะ runner เป็นเครื่องเปล่า เทียบได้กับ Boards Manager ในบท 00</li>
<li><i>Compile</i> คือปุ่ม Verify ของ IDE ในรูปคำสั่ง <code class="il">--output-dir out</code> ให้เก็บผลลัพธ์ (.hex, .zip) ไว้ในโฟลเดอร์ <code class="il">out</code></li>
<li><code class="il">upload-artifact</code> เก็บโฟลเดอร์ <code class="il">out</code> ไว้กับ run นั้นในชื่อ <i>firmware</i> ไฟล์ที่ได้จากการ build แบบนี้เรียกว่า <b>artifact</b></li>
</ul>
''', '''
<p>What is new since lesson 21:</p>
<ul>
<li><code class="il">env:</code>: variables shared by every job, used in commands as <code class="il">"$BOARD_URL"</code> and <code class="il">"$FQBN"</code>, so you change them in one place.</li>
<li><code class="il">needs: host-tests</code>: this job waits until <code class="il">host-tests</code> has passed.</li>
<li><code class="il">setup-python</code> + <code class="il">pip install adafruit-nrfutil</code>: the tool the core uses to package the .zip for the bootloader (lesson 23); on Linux you install it yourself.</li>
<li><code class="il">setup-arduino-cli</code> and the <i>Install board core</i> step install arduino-cli and the Seeed core every time, because the runner is a clean machine. It is the same as Boards Manager in lesson 00.</li>
<li><i>Compile</i> is the IDE's Verify button as a command. <code class="il">--output-dir out</code> puts the results (.hex, .zip) in an <code class="il">out</code> folder.</li>
<li><code class="il">upload-artifact</code> stores the <code class="il">out</code> folder with that run under the name <i>firmware</i>. Files produced by a build like this are called <b>artifacts</b>.</li>
</ul>
''') + code('''git switch -c ci/build-firmware
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
           T('ให้ build ซ้ำเมื่อไรก็ได้ firmware เหมือนเดิม ถ้า core อัปเดตเอง firmware อาจทำงานต่างไปโดยไม่มีใครแก้โค้ด เป็นหลักเดียวกับการล็อกรุ่นชิ้นส่วนใน BOM (รายการชิ้นส่วน) ของฮาร์ดแวร์', 'So that building again at any time gives the same firmware. If the core updates itself, the firmware may behave differently without anyone touching the code. It is the same idea as locking part numbers in a hardware BOM (bill of materials).'))])
   + iv(T('ในทีม CI กับ CD มักถูกพูดปนกัน: CI = รวมโค้ดบ่อยและตรวจอัตโนมัติทุกครั้ง, CD = ส่งมอบ artifact ที่พร้อมใช้อัตโนมัติ (บทถัดไป) แยกให้ชัดแล้วจะคุยเรื่อง pipeline กันง่ายขึ้น',
          'Teams often mix up CI and CD: CI = integrate code often and check it automatically every time; CD = deliver ready-to-use artifacts automatically (next lesson). Keeping them apart makes pipeline discussions easier.')))
