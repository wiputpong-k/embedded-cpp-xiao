lesson('02', 'A', T('Reference, const และ constexpr แทน #define', 'Reference, const and constexpr instead of #define'), 25, BOARD, goal(T('เลิกใช้ #define กับค่าคงที่ และส่งพารามิเตอร์ด้วย reference ได้ถูกที่', 'Stop using #define for constants, and pass parameters by reference in the right places'))
   + T('''
<p>ใน C ค่าคงที่มักเขียนเป็น <code class="il">#define LED_COUNT 3</code> ซึ่ง preprocessor (ขั้นแรกของ build ในบท 01) แค่แทนข้อความ <code class="il">LED_COUNT</code> ด้วย <code class="il">3</code> ก่อน compile ตัวเลขนั้นจึงไม่มี type และไม่มี scope C++ มีทางที่ดีกว่า และมี reference ที่ใช้แทน pointer ได้ในหลายกรณี</p>
''', '''
<p>In C, constants are often <code class="il">#define LED_COUNT 3</code>. The preprocessor (the first build stage from lesson 01) simply replaces the text <code class="il">LED_COUNT</code> with <code class="il">3</code> before compiling, so the value has no type and no scope. C++ has a better way, plus references, which replace pointers in many cases.</p>
''')
   + vs(T('ค่าคงที่ใช้ <code class="il">#define</code> ไม่มี type ไม่มี scope แก้ตัวแปรของผู้เรียกต้องส่ง pointer', 'Constants use <code class="il">#define</code>: no type, no scope. To change the caller\'s variable you pass a pointer.'),
        T('<code class="il">constexpr</code> มี type และคำนวณตอน compile ไม่กิน RAM ส่วน <code class="il">T&amp;</code> คือชื่อเล่นของตัวแปรเดิม ไม่มี null ไม่ต้องเขียน <code class="il">*</code>', '<code class="il">constexpr</code> has a type and is computed at compile time, using no RAM. <code class="il">T&amp;</code> is an alias for an existing variable: never null, no <code class="il">*</code> needed.'))
   + T('''
<ul>
<li><b>compile time / runtime</b> ค่าที่รู้ตอน compile (บน PC ก่อนลงบอร์ด) เทียบกับค่าที่รู้ตอนโปรแกรมทำงานบนบอร์ด ค่าที่รู้ตอน compile ไม่ต้องคำนวณบนชิปและไม่ต้องเก็บใน RAM</li>
<li><b>scope</b> ขอบเขตที่ชื่อหนึ่งใช้ได้ เช่น ภายใน <code class="il">{ }</code> ของฟังก์ชัน <code class="il">#define</code> ไม่สน scope ใช้ได้ทั้งไฟล์หลังบรรทัดที่ประกาศ</li>
<li><b>reference (<code class="il">T&amp;</code>)</b> ชื่อที่สองของตัวแปรเดิม แก้ผ่าน reference = แก้ตัวแปรเดิม เหมือนส่ง pointer แต่ไม่ต้องเขียน <code class="il">&amp;</code> ตอนเรียกและ <code class="il">*</code> ตอนใช้</li>
</ul>
''', '''
<ul>
<li><b>compile time / runtime</b>: a value known while compiling (on the PC, before the board) versus one known only while the program runs on the board. A compile-time value needs no work on the chip and no RAM.</li>
<li><b>scope</b>: the region where a name can be used, e.g. inside a function's <code class="il">{ }</code>. <code class="il">#define</code> ignores scope: it applies to the rest of the file.</li>
<li><b>reference (<code class="il">T&amp;</code>)</b>: a second name for an existing variable. Changing it changes the original, like passing a pointer, but with no <code class="il">&amp;</code> at the call and no <code class="il">*</code> when using it.</li>
</ul>
''')
   + fig(SVG_REF, T('pointer เก็บ address แยก ส่วน reference ผูกกับตัวแปรเดิมตลอดชีวิต', 'A pointer stores an address of its own; a reference stays bound to the original variable for life')) + '''
<h3>Hands-on</h3>''' + T('''
<p>sketch นี้พิสูจน์ 3 เรื่อง: <code class="il">constexpr</code> ใช้เป็นขนาด array และคำนวณตอน compile ได้, reference แก้ตัวแปรของผู้เรียกได้โดยไม่ใช้ pointer และ <code class="il">const</code> ให้ compiler จับบั๊กให้</p>
<ol>
<li>สร้าง sketch ใหม่ (<b>File → New Sketch</b>) วางโค้ดข้างล่าง แล้วบันทึกชื่อ <code class="il">rgb_cycle</code></li>
<li>กด <b>Upload</b> ผลที่ควรเห็น: LED บนบอร์ดเปลี่ยนสีวน แดง → เขียว → น้ำเงิน ทุก 0.15 วินาที</li>
</ol>
''', '''
<p>This sketch proves three things: <code class="il">constexpr</code> can size an array and is computed at compile time, a reference changes the caller's variable without a pointer, and <code class="il">const</code> lets the compiler catch bugs for you.</p>
<ol>
<li>Create a new sketch (<b>File → New Sketch</b>), paste the code below, and save it as <code class="il">rgb_cycle</code>.</li>
<li>Press <b>Upload</b>. Expected result: the on-board LED cycles red → green → blue every 0.15 s.</li>
</ol>
''') + code('''constexpr uint8_t kLedPins[] = {LED_RED, LED_GREEN, LED_BLUE};
constexpr size_t  kLedCount  = sizeof(kLedPins) / sizeof(kLedPins[0]);
constexpr uint32_t kStepMs   = 150;

void allOff() {
  for (uint8_t pin : kLedPins) {   // range-based for (C++11)
    digitalWrite(pin, HIGH);
  }
}

void nextIndex(size_t& idx) {      // reference: แก้ตัวแปรของผู้เรียกได้เลย
  idx = (idx + 1) % kLedCount;
}

size_t current = 0;

void setup() {
  for (uint8_t pin : kLedPins) pinMode(pin, OUTPUT);
  allOff();
}

void loop() {
  allOff();
  digitalWrite(kLedPins[current], LOW);
  delay(kStepMs);
  nextIndex(current);
}''', 'rgb_cycle.ino', en={'// reference: แก้ตัวแปรของผู้เรียกได้เลย': "// reference: changes the caller's variable directly"}) + T('''
<ul>
<li><code class="il">uint8_t</code>, <code class="il">uint32_t</code> ชนิดข้อมูลที่ระบุขนาดชัด (8 และ 32 bit) ส่วน <code class="il">size_t</code> ใช้นับจำนวนหรือขนาด ใช้แทน <code class="il">int</code> ที่ขนาดเปลี่ยนตามบอร์ด (บท 01)</li>
<li><code class="il">for (uint8_t pin : kLedPins)</code> คือ <b>range-based for</b> ของ C++11 วนทุกตัวใน array โดยไม่ต้องเขียน index เอง</li>
<li>เขียน <code class="il">HIGH</code> = ดับ และ <code class="il">LOW</code> = ติด เพราะ LED บนบอร์ดเป็น active-LOW (บท 00)</li>
</ul>
<p>ผลนี้บอกอะไร:</p>
<ul>
<li><b>reference</b> สีเปลี่ยนได้เพราะ <code class="il">nextIndex(current)</code> แก้ <code class="il">current</code> ตัวจริง ถ้าเป็น C ต้องเขียน <code class="il">nextIndex(&amp;current)</code> และ <code class="il">*idx = ...</code></li>
<li><b>constexpr</b> <code class="il">kLedCount</code> = 3 ถูกคำนวณตอน compile จาก <code class="il">sizeof</code> ถ้าเพิ่มขาใน <code class="il">kLedPins</code> ค่านี้จะตามเองโดยไม่ต้องแก้ตัวเลข</li>
</ul>
<p>ลอง <code class="il">const</code>: เพิ่มฟังก์ชันนี้ไว้เหนือ <code class="il">setup()</code> แล้วกด Verify</p>
''', '''
<ul>
<li><code class="il">uint8_t</code>, <code class="il">uint32_t</code>: types with an explicit size (8 and 32 bits); <code class="il">size_t</code> is for counts and sizes. They replace <code class="il">int</code>, whose size depends on the board (lesson 01).</li>
<li><code class="il">for (uint8_t pin : kLedPins)</code> is C++11's <b>range-based for</b>: it visits every element of the array without an index.</li>
<li><code class="il">HIGH</code> = off and <code class="il">LOW</code> = on, because the on-board LED is active-LOW (lesson 00).</li>
</ul>
<p>What the result tells you:</p>
<ul>
<li><b>reference</b>: the colour changes because <code class="il">nextIndex(current)</code> modifies the real <code class="il">current</code>. In C you would write <code class="il">nextIndex(&amp;current)</code> and <code class="il">*idx = ...</code>.</li>
<li><b>constexpr</b>: <code class="il">kLedCount</code> = 3 is computed at compile time from <code class="il">sizeof</code>. Add a pin to <code class="il">kLedPins</code> and it follows without editing a number.</li>
</ul>
<p>Try <code class="il">const</code>: add this function above <code class="il">setup()</code> and press Verify.</p>
''') + code('''void printPin(const uint8_t& p) {
  p = 0;
}''', T('เพิ่มใน rgb_cycle.ino', 'add to rgb_cycle.ino')) + T('''
<p>compiler จะไม่ยอม compile และแจ้ง <code class="il">error: assignment of read-only reference 'p'</code> นี่คือประโยชน์ของ const: บั๊กถูกจับตอน compile ไม่ใช่ตอนบอร์ดทำงาน (ใช้ <code class="il">const uint8_t&amp;</code> ที่นี่เพื่อการทดลองเท่านั้น ชนิดเล็กแบบนี้ปกติส่งค่าตรง ๆ ดูคำถามข้อแรกด้านล่าง) ลองแล้วลบฟังก์ชันนี้ออก</p>
''', '''
<p>The compiler refuses with <code class="il">error: assignment of read-only reference 'p'</code>. That is what const buys you: the bug is caught at compile time, not while the board runs. (<code class="il">const uint8_t&amp;</code> is only for this experiment; small types like this are normally passed by value, see the first question below.) Delete the function afterwards.</p>
''')
   + qa([(T('เมื่อไหร่ควรส่ง const T& แทนส่งค่า?', 'When should you pass const T& instead of by value?'),
           T('เมื่อ T ใหญ่กว่า register (ช่องเก็บข้อมูลใน CPU ขนาด 32 bit) เช่น struct หรือ buffer เพื่อเลี่ยงการ copy ส่วน int, float, pointer ส่งค่าตรง ๆ เร็วกว่าและอ่านง่ายกว่า', 'When T is bigger than a register (a 32-bit storage slot inside the CPU), such as a struct or buffer, to avoid a copy. Pass int, float and pointers by value: faster and easier to read.')),
          (T('constexpr ต่างจาก const อย่างไร?', 'How does constexpr differ from const?'),
           T('const = ห้ามแก้ แต่อาจรู้ค่าตอน runtime ส่วน constexpr = ต้องรู้ค่าตอน compile จึงใช้เป็นขนาด array ได้ (และใช้กับ template ในบท 10)', 'const means read-only, but the value may only be known at runtime. constexpr must be known at compile time, so it can size an array (and feed templates, lesson 10).'))])
   + iv(T('ใน code review ของทีม firmware ค่าคงที่แบบ #define มักถูกขอให้เปลี่ยนเป็น constexpr เพราะ #define ไม่มี type checking, ไม่เคารพ namespace/scope, debugger มองไม่เห็นชื่อ และอาจเกิด side effect จาก macro expansion',
          'In firmware code reviews, #define constants are often sent back to become constexpr: #define has no type checking, ignores namespaces and scope, is invisible to the debugger, and macro expansion can cause side effects.')))
