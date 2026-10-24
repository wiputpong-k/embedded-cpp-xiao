lesson('08', 'A', 'State machine', 25, BTN, goal(T('ใช้ปุ่มที่ debounce แล้วสลับโหมดการกระพริบของ LED ด้วย state machine แบบ non-blocking', 'Use the debounced button to switch LED blink modes with a non-blocking state machine')) + T('''
<p>state machine คือการออกแบบโปรแกรมให้อยู่ใน <b>สถานะ</b> (state) ใดสถานะหนึ่งเสมอ และเปลี่ยนสถานะเมื่อเกิด <b>เหตุการณ์</b> (event) เท่านั้น บทนี้มี 3 สถานะ คือ Off, Slow (กระพริบทุก 500 ms) และ Fast (ทุก 100 ms) เหตุการณ์เดียวคือ <code class="il">Event::Pressed</code> จาก Debouncer ในบทที่แล้ว</p>
<p>ใช้ <code class="il">enum class Mode</code> (บท 03) เก็บสถานะ และแยกกฎการเปลี่ยนสถานะไว้ในฟังก์ชัน <code class="il">next()</code> ที่เดียว เวลาจะเพิ่มโหมดใหม่จึงรู้ทันทีว่าต้องแก้ตรงไหน</p>
''', '''
<p>A state machine keeps the program in exactly one <b>state</b> at a time and changes state only when an <b>event</b> happens. This lesson has 3 states: Off, Slow (blink every 500 ms) and Fast (every 100 ms). The only event is <code class="il">Event::Pressed</code> from the Debouncer in the previous lesson.</p>
<p>An <code class="il">enum class Mode</code> (lesson 03) holds the state, and the transition rules live in one function, <code class="il">next()</code>, so when you add a mode you know exactly where to change things.</p>
''') + fig(SVG_STATE, T('state machine 3 สถานะ เปลี่ยนเมื่อได้ Event::Pressed', 'A 3-state machine that advances on Event::Pressed')) + T('''
<h3>Hands-on</h3>
<ol>
<li>สร้าง sketch ใหม่ชื่อ <code class="il">button_modes</code></li>
<li>คัดลอกโฟลเดอร์ <code class="il">src</code> จาก sketch <code class="il">button_count</code> มาไว้ในโฟลเดอร์ของ sketch ใหม่ (ใช้ <b>Sketch → Show Sketch Folder</b> เปิดทั้งสองโฟลเดอร์)</li>
<li>วางโค้ดข้างล่างใน <code class="il">button_modes.ino</code> แล้วกด <b>Upload</b></li>
<li>กดปุ่ม: LED เขียวต้องเปลี่ยนจากดับ → กระพริบช้า → กระพริบเร็ว → ดับ วนไปเรื่อย ๆ</li>
</ol>''', '''
<h3>Hands-on</h3>
<ol>
<li>Create a new sketch named <code class="il">button_modes</code>.</li>
<li>Copy the <code class="il">src</code> folder from the <code class="il">button_count</code> sketch into the new sketch's folder (use <b>Sketch → Show Sketch Folder</b> to open both folders).</li>
<li>Paste the code below into <code class="il">button_modes.ino</code> and click <b>Upload</b>.</li>
<li>Press the button: the green LED should go off → slow blink → fast blink → off, and around again.</li>
</ol>''') + code('''#include "src/Debouncer.h"

constexpr uint8_t kButtonPin = D1;
enum class Mode : uint8_t { Off, Slow, Fast };

Debouncer button;
Mode mode = Mode::Off;
uint32_t lastToggle = 0;
bool ledLit = false;

Mode next(Mode m) {
  switch (m) {
    case Mode::Off:  return Mode::Slow;
    case Mode::Slow: return Mode::Fast;
    case Mode::Fast: return Mode::Off;
  }
  return Mode::Off;
}

uint32_t periodMs(Mode m) { return m == Mode::Slow ? 500 : 100; }

void setup() {
  pinMode(kButtonPin, INPUT_PULLUP);
  pinMode(LED_GREEN, OUTPUT);
  digitalWrite(LED_GREEN, HIGH);
}

void loop() {
  uint32_t now = millis();
  bool pressed = (digitalRead(kButtonPin) == LOW);
  if (button.update(pressed, now) == Debouncer::Event::Pressed) {
    mode = next(mode);
  }
  if (mode == Mode::Off) {
    digitalWrite(LED_GREEN, HIGH);
  } else if (now - lastToggle >= periodMs(mode)) {
    lastToggle = now;
    ledLit = !ledLit;
    digitalWrite(LED_GREEN, ledLit ? LOW : HIGH);
  }
}''', 'button_modes.ino') + T('''
<p>สังเกตว่าการกระพริบใช้ <code class="il">now - lastToggle &gt;= periodMs(mode)</code> แทน <code class="il">delay()</code> loop จึงวนเร็วตลอดเวลา และตอบสนองต่อปุ่มได้ทันทีแม้อยู่ในโหมด Slow</p>
''', '''
<p>Notice that the blinking uses <code class="il">now - lastToggle &gt;= periodMs(mode)</code> instead of <code class="il">delay()</code>. loop keeps spinning fast, so the button responds immediately even in Slow mode.</p>
''') + qa([(T('ทำไม switch มี return Mode::Off ท้ายฟังก์ชันอีก?', 'Why is there another return Mode::Off after the switch?'),
           T('บาง compiler เตือนว่า control reaches end of non-void function แม้จะครอบทุก case แล้ว ใส่ไว้เพื่อความปลอดภัยและ warning-free', 'Some compilers warn "control reaches end of non-void function" even when every case is covered. It is there for safety and a warning-free build.')),
          (T('ถ้าจะเพิ่มโหมด "ติดค้าง" ต้องแก้ตรงไหนบ้าง?', 'What would you change to add an "always on" mode?'),
           T('เพิ่มชื่อใน enum class Mode, เพิ่ม case ใน next() ให้เข้าและออกจากโหมดใหม่ และเพิ่มเงื่อนไขใน loop ให้เขียน LOW ค้างไว้ ส่วนอื่นไม่ต้องแก้', 'Add a name to enum class Mode, add cases in next() to enter and leave the new mode, and add a branch in loop that holds the pin LOW. Nothing else changes.'))]))
