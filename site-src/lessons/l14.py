lesson('14', 'A', T('Mini project 2: รับคำสั่งทาง Serial', 'Mini project 2: commands over Serial'), 25, T('LED + ปุ่ม + Pot', 'LED + button + pot'), goal(T('เพิ่มการรับคำสั่งจาก Serial Monitor แบบไม่ block ให้ firmware จากบทที่แล้ว', 'Add non-blocking command input from Serial Monitor to the firmware from the previous lesson'))
   + T('''
<p>firmware จริงมักต้องรับคำสั่งจากภายนอก เช่น ตั้งค่า หรือสั่งให้ทดสอบ ปัญหาคือข้อความมาถึงทีละตัวอักษร ถ้ารอให้ครบทั้งบรรทัดด้วยฟังก์ชันอย่าง <code class="il">Serial.readStringUntil()</code> loop จะค้างระหว่างรอ task อื่นจะหยุดทำงาน</p>
<p><code class="il">handleSerial()</code> แก้ปัญหานี้โดยอ่านเฉพาะตัวอักษรที่มาถึงแล้ว เก็บสะสมใน buffer แล้วออกจากฟังก์ชันทันที เมื่อเจอตัวขึ้นบรรทัดใหม่ (<code class="il">\\n</code> หรือ <code class="il">\\r</code>) จึงแปลงข้อความเป็นตัวเลขแล้วใช้งาน</p>
<ul>
<li><code class="il">static</code> ทำให้ <code class="il">buf</code> และ <code class="il">len</code> จำค่าข้ามการเรียกแต่ละครั้ง (บท 11) ข้อความครึ่งบรรทัดจึงไม่หาย</li>
<li><code class="il">len &lt; sizeof(buf) - 1</code> กันไม่ให้เขียนเกินขนาด buffer และเว้นที่ไว้ 1 ช่องสำหรับ <code class="il">\\0</code></li>
<li>ตรวจช่วงค่า 50–5000 ก่อนใช้เสมอ ข้อมูลจากภายนอกต้องไม่ถูกเชื่อโดยไม่ตรวจ</li>
</ul>
''', '''
<p>Real firmware often takes commands from outside, such as settings or test triggers. The catch is that text arrives one character at a time. If you wait for a whole line with something like <code class="il">Serial.readStringUntil()</code>, loop stalls while it waits and every other task stops.</p>
<p><code class="il">handleSerial()</code> avoids this by reading only the characters that have already arrived, collecting them in a buffer, and returning right away. When it sees a line ending (<code class="il">\\n</code> or <code class="il">\\r</code>), it converts the text to a number and uses it.</p>
<ul>
<li><code class="il">static</code> makes <code class="il">buf</code> and <code class="il">len</code> keep their values between calls (lesson 11), so half a line is not lost.</li>
<li><code class="il">len &lt; sizeof(buf) - 1</code> stops writes past the end of the buffer and leaves one slot for <code class="il">\\0</code>.</li>
<li>Always check the range (50–5000) before using the value. Never trust outside input unchecked.</li>
</ul>
''') + T('''
<h3>Hands-on</h3>
<ol>
<li>เปิด sketch <code class="il">firmware</code> จากบทที่แล้ว แล้วแทนที่โค้ดทั้งหมดด้วยโค้ดข้างล่าง (มีฟังก์ชัน <code class="il">handleSerial()</code> เพิ่ม และเรียกใช้ในบรรทัดสุดท้ายของ <code class="il">loop()</code>)</li>
<li>กด <b>Upload</b> แล้วเปิด <b>Tools → Serial Monitor</b> ตั้งความเร็ว <b>115200 baud</b></li>
<li>ที่มุมขวาของ Serial Monitor มีตัวเลือกการขึ้นบรรทัด ให้เลือก <b>New Line</b> ไม่อย่างนั้นบอร์ดจะไม่รู้ว่าพิมพ์จบบรรทัดแล้ว</li>
<li>พิมพ์ <code class="il">100</code> ในช่องข้อความด้านบนของ Serial Monitor แล้วกด Enter LED เขียวต้องกระพริบเร็วขึ้น ลองพิมพ์ <code class="il">2000</code> แล้วลอง <code class="il">10</code> (นอกช่วง ต้องไม่มีอะไรเปลี่ยน)</li>
</ol>''', '''
<h3>Hands-on</h3>
<ol>
<li>Open the <code class="il">firmware</code> sketch from the previous lesson and replace all of its code with the code below (it adds <code class="il">handleSerial()</code> and calls it on the last line of <code class="il">loop()</code>).</li>
<li>Click <b>Upload</b>, then open <b>Tools → Serial Monitor</b> at <b>115200 baud</b>.</li>
<li>At the right of the Serial Monitor there is a line-ending option. Pick <b>New Line</b>, otherwise the board never knows you finished typing a line.</li>
<li>Type <code class="il">100</code> in the message box at the top of the Serial Monitor and press Enter. The green LED should blink faster. Try <code class="il">2000</code>, then <code class="il">10</code> (out of range, so nothing should change).</li>
</ol>''') + code(FW_HEAD + FW_SERIAL + FW_SETUP + FW_LOOP % '\n  handleSerial();', 'firmware/firmware.ino', en=FW_EN) + T('''
<p class="note">บรรทัด <code class="il">#if __has_include("src/version.h")</code> ตรวจว่ามีไฟล์ <code class="il">version.h</code> หรือไม่ ตอนนี้ยังไม่มี โปรแกรมจึงพิมพ์ <code class="il">fw dev</code> ตอนเริ่ม ในบท 23 ระบบ CI จะสร้างไฟล์นี้พร้อมเลขเวอร์ชันจริงให้อัตโนมัติ</p>
''', '''
<p class="note">The <code class="il">#if __has_include("src/version.h")</code> line checks whether <code class="il">version.h</code> exists. It does not yet, so the program prints <code class="il">fw dev</code> at startup. In lesson 23, CI generates this file with the real version number automatically.</p>
''') + qa([(T('ถ้าพิมพ์ข้อความยาวเกิน 15 ตัวอักษรจะเกิดอะไรขึ้น?', 'What happens if you type more than 15 characters?'),
           T('ตัวที่เกินจะถูกทิ้ง เพราะ len ไม่เพิ่มเกิน sizeof(buf) - 1 โปรแกรมไม่พังและไม่เขียนทับหน่วยความจำส่วนอื่น จากนั้นตัวเลขที่ได้จะถูกตรวจช่วงค่าอีกชั้น', 'The extra characters are dropped, because len never grows past sizeof(buf) - 1. The program does not crash or overwrite other memory, and the resulting number is still range-checked.')),
          (T('ทำไมต้องเช็กทั้ง \\n และ \\r?', 'Why check for both \\n and \\r?'),
           T('แต่ละโปรแกรมส่งการขึ้นบรรทัดไม่เหมือนกัน บางตัวส่ง \\n บางตัวส่ง \\r หรือส่งทั้งคู่ การรับทั้งสองแบบ และข้ามบรรทัดว่าง (len == 0) ทำให้ใช้ได้กับทุกโปรแกรม', 'Different terminal programs send different line endings: \\n, \\r, or both. Accepting either, and skipping empty lines (len == 0), makes it work with all of them.'))]))
