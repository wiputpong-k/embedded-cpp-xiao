lesson('07', 'A', T('ปุ่มกดและ debounce', 'Buttons and debounce'), 30, BTN, goal(T('ต่อปุ่มกด และเขียน debounce แบบ non-blocking เป็น class ที่ไม่พึ่ง Arduino (จะ test บน PC ในบท 19)', 'Wire a button, and write non-blocking debounce as a class that does not depend on Arduino (you will test it on a PC in lesson 19)')) + T('''
<h3>ต่อวงจร</h3>
<p>ปุ่มกด tactile มี 4 ขา ขาที่อยู่ฝั่งเดียวกันเป็นคู่ที่ต่อกันอยู่แล้วข้างใน ถ้าวางผิดทิศ ปุ่มจะดูเหมือนกดค้างตลอดเวลา วิธีที่ปลอดภัยที่สุดคือใช้ขาที่อยู่ <b>ทแยงมุม</b> กัน เพราะจะเป็นคนละคู่เสมอ</p>
<ol>
<li>ถอดสาย USB ออกก่อน</li>
<li>เสียบปุ่มคร่อมร่องกลางของ breadboard</li>
<li>ต่อสายจากขาหนึ่งของปุ่มไปที่ขา D1</li>
<li>ต่อขาที่อยู่ทแยงมุมกับขานั้นไปที่ GND</li>
</ol>
<p>วงจรนี้ไม่ต้องใช้ R ภายนอก เพราะโค้ดจะเปิด <code class="il">INPUT_PULLUP</code> คือ R ภายในชิปที่ดึงขา D1 ขึ้นไปที่ 3.3 V ตอนปล่อยปุ่มขาจึงเป็น HIGH และตอนกดปุ่ม ขาถูกต่อลง GND จึงเป็น LOW</p>
<h3>ทำไมต้อง debounce</h3>
<p>หน้าสัมผัสโลหะในปุ่มจะเด้งกระทบกันหลายครั้งในช่วง 1–5 ms แรกของการกด ถ้าโค้ดอ่านขาตรง ๆ กดครั้งเดียวอาจนับได้หลายครั้ง Debouncer แก้ปัญหานี้โดยยืนยันสถานะใหม่ก็ต่อเมื่อสัญญาณนิ่งต่อเนื่องครบเวลาที่กำหนด (ค่าเริ่มต้น 20 ms)</p>
''', '''
<h3>Wire it up</h3>
<p>A tactile button has 4 legs. The legs on the same side are pairs that are already connected inside. If you place it the wrong way round, the button looks permanently pressed. The safe trick is to use two legs that are <b>diagonally opposite</b>, because they always belong to different pairs.</p>
<ol>
<li>Unplug the USB cable first.</li>
<li>Press the button into the breadboard across the center gap.</li>
<li>Run a wire from one button leg to pin D1.</li>
<li>Connect the diagonally opposite leg to GND.</li>
</ol>
<p>No external resistor is needed, because the code turns on <code class="il">INPUT_PULLUP</code>: a resistor inside the chip that pulls D1 up to 3.3 V. So when the button is released the pin reads HIGH, and when it is pressed the pin is connected to GND and reads LOW.</p>
<h3>Why debounce</h3>
<p>The metal contacts inside a button bounce against each other several times in the first 1–5 ms of a press. If the code reads the pin directly, one press can count as several. The Debouncer fixes this by accepting a new state only after the signal has stayed stable for a set time (20 ms by default).</p>
''') + fig(SVG_BOUNCE, T('Debouncer รอให้สัญญาณนิ่งครบ 20 ms ก่อนยืนยัน', 'The Debouncer waits until the signal has been stable for 20 ms before confirming')) + T('''
<h3>Hands-on</h3>
<ol>
<li>สร้าง sketch ใหม่ (<b>File → New Sketch</b>) แล้วบันทึกชื่อ <code class="il">button_count</code></li>
<li>สร้างไฟล์ <code class="il">src/Debouncer.h</code> แบบเดียวกับบท 05 (<b>Sketch → Show Sketch Folder</b> → สร้างโฟลเดอร์ <code class="il">src</code> → สร้างไฟล์ <code class="il">Debouncer.h</code>) แล้ววางโค้ดชุดแรกข้างล่าง</li>
<li>วางโค้ดชุดที่สองลงใน <code class="il">button_count.ino</code> แล้วกด <b>Upload</b></li>
<li>เปิด <b>Tools → Serial Monitor</b> แล้วตั้งค่าความเร็วที่มุมขวาของหน้าต่าง Serial Monitor เป็น <b>115200 baud</b> ให้ตรงกับ <code class="il">Serial.begin(115200)</code> ในโค้ด</li>
<li>กดปุ่มทีละครั้ง ตัวเลข <code class="il">presses</code> ต้องเพิ่มทีละ 1</li>
</ol>''', '''
<h3>Hands-on</h3>
<ol>
<li>Create a new sketch (<b>File → New Sketch</b>) and save it as <code class="il">button_count</code>.</li>
<li>Create <code class="il">src/Debouncer.h</code> the same way as in lesson 05 (<b>Sketch → Show Sketch Folder</b> → create a <code class="il">src</code> folder → create <code class="il">Debouncer.h</code>) and paste the first code block below.</li>
<li>Paste the second code block into <code class="il">button_count.ino</code> and click <b>Upload</b>.</li>
<li>Open <b>Tools → Serial Monitor</b> and set the speed at the right of the Serial Monitor panel to <b>115200 baud</b>, to match <code class="il">Serial.begin(115200)</code> in the code.</li>
<li>Press the button a few times. <code class="il">presses</code> should go up by exactly 1 each time.</li>
</ol>''') + code(DEB, 'src/Debouncer.h') + code('''#include "src/Debouncer.h"

constexpr uint8_t kButtonPin = D1;

Debouncer button;        // stableMs = 20 (ค่าเริ่มต้น)
uint32_t presses = 0;

void setup() {
  Serial.begin(115200);
  pinMode(kButtonPin, INPUT_PULLUP);
}

void loop() {
  bool pressed = (digitalRead(kButtonPin) == LOW);   // active-LOW → true = กด
  if (button.update(pressed, millis()) == Debouncer::Event::Pressed) {
    presses++;
    Serial.print("presses = ");
    Serial.println(presses);
  }
}''', 'button_count.ino', en={'// stableMs = 20 (ค่าเริ่มต้น)': '// stableMs = 20 (default)', '// active-LOW → true = กด': '// active-LOW → true = pressed'}) + T('''
<h3>Debouncer ทำงานอย่างไร</h3>
<ul>
<li><code class="il">update()</code> ถูกเรียกทุกรอบ loop พร้อมค่าที่อ่านได้ (<code class="il">raw</code>) และเวลาปัจจุบัน (<code class="il">nowMs</code>) ไม่มี <code class="il">delay()</code> เลย loop จึงทำงานอื่นต่อได้</li>
<li>ถ้า <code class="il">raw</code> ต่างจากรอบที่แล้ว แปลว่ายังเด้งอยู่ จึงจำเวลาไว้ใน <code class="il">changedAt_</code> แล้วเริ่มนับใหม่</li>
<li>ถ้า <code class="il">raw</code> นิ่งมานานครบ <code class="il">stableMs_</code> และต่างจากสถานะที่ยืนยันแล้ว (<code class="il">stable_</code>) จึงเปลี่ยนสถานะ แล้วคืน <code class="il">Event::Pressed</code> หรือ <code class="il">Event::Released</code> ครั้งเดียว</li>
<li>class นี้ไม่เรียก <code class="il">millis()</code> หรือ <code class="il">digitalRead()</code> เอง ผู้เรียกเป็นคนส่งค่าเข้ามา จึงนำไป test บน PC ได้ในบท 19</li>
</ul>
<p>ลองเปลี่ยนบรรทัด <code class="il">Debouncer button;</code> เป็น <code class="il">Debouncer button(0);</code> (ไม่รอให้นิ่งเลย) แล้ว Upload ใหม่ กดปุ่มดูว่าบางครั้งตัวเลขกระโดดเพิ่มทีละหลายค่า นั่นคือ bounce ที่ Debouncer กรองออก จากนั้นเปลี่ยนกลับ</p>
''', '''
<h3>How the Debouncer works</h3>
<ul>
<li><code class="il">update()</code> is called on every pass of loop with the value just read (<code class="il">raw</code>) and the current time (<code class="il">nowMs</code>). There is no <code class="il">delay()</code>, so loop stays free for other work.</li>
<li>If <code class="il">raw</code> differs from the previous call, the contacts are still bouncing, so it stores the time in <code class="il">changedAt_</code> and starts counting again.</li>
<li>Once <code class="il">raw</code> has been stable for <code class="il">stableMs_</code> and differs from the confirmed state (<code class="il">stable_</code>), it switches state and returns <code class="il">Event::Pressed</code> or <code class="il">Event::Released</code> exactly once.</li>
<li>The class never calls <code class="il">millis()</code> or <code class="il">digitalRead()</code> itself; the caller passes the values in. That is what lets you test it on a PC in lesson 19.</li>
</ul>
<p>Try changing <code class="il">Debouncer button;</code> to <code class="il">Debouncer button(0);</code> (no waiting at all) and upload again. Press the button and watch the count sometimes jump by several at once. That is the bounce the Debouncer filters out. Then change it back.</p>
''') + qa([(T('ทำไม nowMs - changedAt_ ยังถูกต้องแม้ millis() overflow (ราว 49.7 วัน)?', 'Why is nowMs - changedAt_ still correct when millis() overflows (after about 49.7 days)?'),
           T('การลบ unsigned 32-bit เป็น modulo 2³² ผลต่างจึงถูกเสมอตราบใดที่ช่วงเวลาไม่เกิน 49.7 วัน ห้ามเขียนแบบ now > changedAt_ + stableMs_ เพราะพังตอน overflow', 'Unsigned 32-bit subtraction is modulo 2³², so the difference is always right as long as the interval is under 49.7 days. Never write now > changedAt_ + stableMs_; that breaks on overflow.')),
          (T('ทำไมไม่ใช้ delay(20) หลังอ่านปุ่มแทน?', 'Why not just call delay(20) after reading the button?'),
           T('delay() หยุดทั้งโปรแกรม ระหว่างนั้นอ่านเซนเซอร์หรือกระพริบ LED ไม่ได้ และยังพลาดการกดสั้น ๆ ได้ Debouncer แบบนี้ใช้เวลาแค่ไม่กี่ไมโครวินาทีต่อรอบ', 'delay() stops the whole program, so nothing else can run (no sensor reads, no LED blinking), and short presses can still be missed. This Debouncer costs only a few microseconds per call.'))]))
