lesson('19', 'C', T('แยก logic ออกจากฮาร์ดแวร์ + รัน test บน PC', 'Separate logic from hardware + run tests on a PC'), 30, PC, goal(T('ติดตั้ง g++ แล้วรัน test ของ Debouncer และ RingBuffer บน PC ได้ในไม่กี่วินาที โดยไม่ต้องเสียบบอร์ด', 'Install g++ and run the Debouncer and RingBuffer tests on a PC in seconds, with no board plugged in'))
   + fig(SVG_LAYERS, T('ยิ่ง logic อยู่ชั้นที่ไม่รู้จักฮาร์ดแวร์มาก ยิ่ง test อัตโนมัติได้มาก', 'The more logic lives in layers that know nothing about hardware, the more you can test automatically')) + T('''
<p>Debouncer และ RingBuffer ไม่เรียก Arduino API เลย Debouncer รับเวลาเป็นพารามิเตอร์ (<code class="il">nowMs</code>) แทนการเรียก <code class="il">millis()</code> เอง นี่คือเทคนิค dependency injection แบบง่ายที่สุด ทำให้ compile ด้วย g++ บน PC ได้ และ test ควบคุมเวลาได้ทุกมิลลิวินาที</p>
<h3>ขั้นที่ 1: ติดตั้ง g++</h3>
<p>Windows ไม่มี compiler C++ มาให้ วิธีที่แนะนำคือติดตั้งผ่าน MSYS2</p>
<ol>
<li>เปิดหน้า <a href="https://www.msys2.org/">msys2.org</a> ดาวน์โหลดตัวติดตั้ง (<code class="il">msys2-x86_64-….exe</code>) แล้วติดตั้งตามค่าเริ่มต้น จะได้โฟลเดอร์ <code class="il">C:\\msys64</code></li>
<li>เปิดโปรแกรม <b>MSYS2 UCRT64</b> จาก Start menu แล้วรันคำสั่งแรกข้างล่าง ถ้าถามให้ยืนยัน ให้กด Enter หรือพิมพ์ <code class="il">Y</code></li>
<li>ให้ Git Bash มองเห็น g++: กดปุ่ม Windows พิมพ์ <i>Edit environment variables for your account</i> เลือก <b>Path</b> → <b>Edit</b> → <b>New</b> ใส่ <code class="il">C:\\msys64\\ucrt64\\bin</code> แล้วกด OK ทุกหน้าต่าง</li>
<li>ปิด Git Bash แล้วเปิดใหม่ รัน <code class="il">g++ --version</code> ต้องเห็นเลขเวอร์ชัน</li>
</ol>
<p class="note">macOS: รัน <code class="il">xcode-select --install</code> จะได้ compiler ที่เรียกด้วยชื่อ g++ ได้ Linux (Ubuntu): รัน <code class="il">sudo apt install g++</code></p>
''', '''
<p>The Debouncer and RingBuffer never call the Arduino API. The Debouncer takes the time as a parameter (<code class="il">nowMs</code>) instead of calling <code class="il">millis()</code> itself. This is the simplest form of dependency injection: it lets g++ compile the code on a PC, and lets a test control time down to the millisecond.</p>
<h3>Step 1: Install g++</h3>
<p>Windows has no C++ compiler built in. The recommended way to get one is MSYS2.</p>
<ol>
<li>Open <a href="https://www.msys2.org/">msys2.org</a>, download the installer (<code class="il">msys2-x86_64-….exe</code>) and install with the defaults. You get a <code class="il">C:\\msys64</code> folder.</li>
<li>Open <b>MSYS2 UCRT64</b> from the Start menu and run the first command below. When asked to confirm, press Enter or type <code class="il">Y</code>.</li>
<li>Let Git Bash find g++: press the Windows key, type <i>Edit environment variables for your account</i>, pick <b>Path</b> → <b>Edit</b> → <b>New</b>, enter <code class="il">C:\\msys64\\ucrt64\\bin</code> and click OK on every window.</li>
<li>Close Git Bash, open it again and run <code class="il">g++ --version</code>. You should see a version number.</li>
</ol>
<p class="note">macOS: run <code class="il">xcode-select --install</code>, which gives you a compiler you can call as g++. Linux (Ubuntu): run <code class="il">sudo apt install g++</code>.</p>
''') + code('''pacman -S mingw-w64-ucrt-x86_64-gcc''', 'MSYS2 UCRT64') + T('''
<h3>ขั้นที่ 2: เพิ่มไฟล์ test แล้วรัน</h3>
<ol>
<li>ใน Git Bash เข้าไปที่ repo แล้วสร้างโฟลเดอร์ <code class="il">test</code> (คำสั่ง 2 บรรทัดแรกข้างล่าง)</li>
<li>รัน <code class="il">notepad test/test_main.cpp</code> (หรือ <code class="il">code</code>) วางโค้ด <code class="il">test/test_main.cpp</code> ข้างล่าง แล้วบันทึก</li>
<li>รันคำสั่ง g++ แล้วรัน <code class="il">./test_runner</code> ต้องเห็น <code class="il">ALL TESTS PASSED</code></li>
<li>commit ไฟล์ test เข้า repo</li>
</ol>
<p><code class="il">-Ifirmware/src</code> บอก g++ ให้หาไฟล์ header ในโฟลเดอร์นั้น test จึง include <code class="il">Debouncer.h</code> และ <code class="il">RingBuffer.h</code> ตัวเดียวกับที่บอร์ดใช้ ส่วน <code class="il">-Wall -Wextra -Werror</code> เปิด warning ทั้งหมดและนับ warning เป็น error</p>
''', '''
<h3>Step 2: Add the test file and run it</h3>
<ol>
<li>In Git Bash, go into the repo and create a <code class="il">test</code> folder (the first 2 lines below).</li>
<li>Run <code class="il">notepad test/test_main.cpp</code> (or <code class="il">code</code>), paste the <code class="il">test/test_main.cpp</code> code below and save.</li>
<li>Run the g++ command, then <code class="il">./test_runner</code>. You should see <code class="il">ALL TESTS PASSED</code>.</li>
<li>Commit the test file.</li>
</ol>
<p><code class="il">-Ifirmware/src</code> tells g++ to look for headers in that folder, so the test includes the very same <code class="il">Debouncer.h</code> and <code class="il">RingBuffer.h</code> the board uses. <code class="il">-Wall -Wextra -Werror</code> turns on all warnings and treats them as errors.</p>
''') + code('''cd ~/xiao-embedded-cpp
mkdir test
g++ -std=c++17 -Wall -Wextra -Werror -Ifirmware/src test/test_main.cpp -o test_runner
./test_runner
# ALL TESTS PASSED
git add test/
git commit -m "test: add host unit tests"''', 'Git Bash') + code(TEST, 'test/test_main.cpp')
   + qa([(T('ทำไม exit code สำคัญ?', 'Why does the exit code matter?'),
          T('CI ตัดสินผ่าน/ไม่ผ่านจาก exit code ของคำสั่ง 0 = ผ่าน อย่างอื่น = fail และหยุด pipeline test_main.cpp จึงคืน EXIT_FAILURE เมื่อมี CHECK ที่ไม่ผ่าน', 'CI decides pass/fail from each command\'s exit code: 0 = pass, anything else = fail, which stops the pipeline. That is why test_main.cpp returns EXIT_FAILURE when any CHECK fails.')),
         (T('ทำไม test บน PC ไม่ต้องใช้บอร์ด แต่ยังเชื่อถือได้?', 'Why can tests on a PC be trusted when they never touch the board?'),
          T('เพราะ test compile ไฟล์ header เดียวกับ firmware จริง ทดสอบ logic ล้วน ๆ ส่วนที่ขึ้นกับฮาร์ดแวร์ (การอ่านขา, timing จริง) ยังต้อง test บนบอร์ดแยกต่างหาก', 'The tests compile the same headers as the real firmware and exercise pure logic. The hardware-dependent parts (reading pins, real timing) still need separate tests on the board.'))]))
