lesson('02', 'A', T('Reference, const และ constexpr แทน #define', 'Reference, const and constexpr instead of #define'), 25, BOARD, goal(T('เลิกใช้ #define กับค่าคงที่ และส่งพารามิเตอร์ด้วย reference ได้ถูกที่', 'Stop using #define for constants, and pass parameters by reference in the right places'))
   + vs(T('ค่าคงที่ใช้ <code class="il">#define</code> ไม่มี type ไม่มี scope แก้ตัวแปรของผู้เรียกต้องส่ง pointer', 'Constants use <code class="il">#define</code>: no type, no scope. To change the caller\'s variable you pass a pointer.'),
        T('<code class="il">constexpr</code> มี type และคำนวณตอน compile ไม่กิน RAM ส่วน <code class="il">T&amp;</code> คือชื่อเล่นของตัวแปรเดิม ไม่มี null ไม่ต้องเขียน <code class="il">*</code>', '<code class="il">constexpr</code> has a type and is computed at compile time, using no RAM. <code class="il">T&amp;</code> is an alias for an existing variable: never null, no <code class="il">*</code> needed.'))
   + fig(SVG_REF, T('pointer เก็บ address แยก ส่วน reference ผูกกับตัวแปรเดิมตลอดชีวิต', 'A pointer stores an address of its own; a reference stays bound to the original variable for life')) + '''
<h3>Hands-on</h3>''' + code('''constexpr uint8_t kLedPins[] = {LED_RED, LED_GREEN, LED_BLUE};
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
<p>ลองเพิ่มฟังก์ชัน <code class="il">void printPin(const uint8_t&amp; p)</code> แล้วพยายามเขียน <code class="il">p = 0;</code> ข้างใน ดู error ที่ compiler ฟ้อง นี่คือประโยชน์ของ const: จับบั๊กตอน compile</p>
''', '''
<p>Add a function <code class="il">void printPin(const uint8_t&amp; p)</code> and try writing <code class="il">p = 0;</code> inside it. Read the compiler error. That is what const buys you: bugs caught at compile time.</p>
''') + qa([(T('เมื่อไหร่ควรส่ง const T& แทนส่งค่า?', 'When should you pass const T& instead of by value?'),
           T('เมื่อ T ใหญ่กว่า register (struct, buffer) เพื่อเลี่ยงการ copy ส่วน int, float, pointer ส่งค่าตรง ๆ เร็วกว่าและอ่านง่ายกว่า', 'When T is bigger than a register (structs, buffers), to avoid a copy. Pass int, float and pointers by value: faster and easier to read.')),
          (T('constexpr ต่างจาก const อย่างไร?', 'How does constexpr differ from const?'),
           T('const = ห้ามแก้ แต่อาจรู้ค่าตอน runtime ส่วน constexpr = ต้องรู้ค่าตอน compile จึงใช้เป็นขนาด array หรือ template argument ได้', 'const means read-only, but the value may only be known at runtime. constexpr must be known at compile time, so it can size an array or be a template argument.'))])
   + iv(T('ใน code review ของทีม firmware ค่าคงที่แบบ #define มักถูกขอให้เปลี่ยนเป็น constexpr เพราะ #define ไม่มี type checking, ไม่เคารพ namespace/scope, debugger มองไม่เห็นชื่อ และอาจเกิด side effect จาก macro expansion',
          'In firmware code reviews, #define constants are often sent back to become constexpr: #define has no type checking, ignores namespaces and scope, is invisible to the debugger, and macro expansion can cause side effects.')))
