lesson('02', 'A', T('Reference, const และ constexpr แทน #define', 'Reference, const and constexpr instead of #define'), 30, BOARD, goal(T('เลิกใช้ #define กับค่าคงที่ และส่งพารามิเตอร์ด้วย reference ได้ถูกที่', 'Stop using #define for constants, and pass parameters by reference in the right places'))
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
<li><b><code class="il">constexpr</code></b> ย่อจาก constant expression อ่านว่า "คอนสต์-เอ็กซ์-เพอร์" แปลว่าค่าคงที่ที่ compiler คำนวณเสร็จตั้งแต่ตอน compile</li>
</ul>
<h3>ทำไม constexpr ดีกว่า #define</h3>
<p>ผลลัพธ์บนบอร์ดเหมือนกัน คือตัวเลขถูกฝังลงในโค้ดและไม่กิน RAM แต่ <code class="il">#define</code> เป็นแค่การแทนข้อความ ส่วน <code class="il">constexpr</code> เป็นค่าที่ compiler รู้จักจริง จึงช่วยจับผิดได้ ตัวอย่างที่เห็นชัดที่สุด:</p>
''', '''
<ul>
<li><b>compile time / runtime</b>: a value known while compiling (on the PC, before the board) versus one known only while the program runs on the board. A compile-time value needs no work on the chip and no RAM.</li>
<li><b>scope</b>: the region where a name can be used, e.g. inside a function's <code class="il">{ }</code>. <code class="il">#define</code> ignores scope: it applies to the rest of the file.</li>
<li><b>reference (<code class="il">T&amp;</code>)</b>: a second name for an existing variable. Changing it changes the original, like passing a pointer, but with no <code class="il">&amp;</code> at the call and no <code class="il">*</code> when using it.</li>
<li><b><code class="il">constexpr</code></b>: short for constant expression, usually said "const-ex-per". A constant the compiler works out while compiling.</li>
</ul>
<h3>Why constexpr beats #define</h3>
<p>On the board the result is the same: the number is built into the code and uses no RAM. But <code class="il">#define</code> only replaces text, while <code class="il">constexpr</code> is a real value the compiler knows about, so it can catch mistakes. The clearest example:</p>
''')
   + code('''#define SIZE 2 + 3
int a = SIZE * 2;             // แทนข้อความเป็น 2 + 3 * 2 = 8 (ไม่ใช่ 10!)

constexpr int kSize = 2 + 3;
int b = kSize * 2;            // = 10 ถูกต้อง

constexpr uint8_t kBad = 300; // error: 300 ใหญ่เกิน uint8_t (0-255)''', en={'// แทนข้อความเป็น 2 + 3 * 2 = 8 (ไม่ใช่ 10!)': '// text becomes 2 + 3 * 2 = 8 (not 10!)',
                                                                         '// = 10 ถูกต้อง': '// = 10, correct',
                                                                         '// error: 300 ใหญ่เกิน uint8_t (0-255)': '// error: 300 does not fit in uint8_t (0-255)'})
   + T('''
<ul>
<li><b>มี type</b> compiler ตรวจว่าค่าใส่ใน type ได้ไหม <code class="il">#define</code> ไม่มี type จึงไม่มีใครตรวจ</li>
<li><b>มี scope</b> <code class="il">#define</code> แทนคำนั้นทุกที่หลังบรรทัดที่ประกาศ รวมถึงในไฟล์ที่ include ตามมา ถ้าชื่อไปชนกับชื่อใน library จะพังแบบหาสาเหตุยาก</li>
<li><b>error อ่านรู้เรื่อง</b> error และ debugger แสดงชื่อ <code class="il">kSize</code> ส่วน <code class="il">#define</code> จะเห็นแค่ตัวเลขที่ถูกแทนไปแล้ว</li>
</ul>
<p><code class="il">#define</code> ยังใช้กับงานของ preprocessor เช่น include guard (<code class="il">#ifndef FOO_H</code>) หรือเปิด/ปิดโค้ดด้วย <code class="il">#ifdef DEBUG</code> แต่ค่าคงที่ให้ใช้ <code class="il">constexpr</code></p>
<h3>ส่งค่า (copy) กับส่ง reference</h3>
''', '''
<ul>
<li><b>It has a type</b>: the compiler checks that the value fits. <code class="il">#define</code> has no type, so nothing is checked.</li>
<li><b>It has a scope</b>: <code class="il">#define</code> replaces the word everywhere after it, including in files included later. If the name clashes with one in a library, things break in ways that are hard to trace.</li>
<li><b>Readable errors</b>: errors and the debugger show the name <code class="il">kSize</code>; with <code class="il">#define</code> you only see the number it was replaced with.</li>
</ul>
<p><code class="il">#define</code> is still the tool for preprocessor jobs such as include guards (<code class="il">#ifndef FOO_H</code>) or switching code on and off with <code class="il">#ifdef DEBUG</code>. For constants, use <code class="il">constexpr</code>.</p>
<h3>Passing a copy vs passing a reference</h3>
''')
   + code('''void addCopy(size_t n) { n = n + 1; }   // ได้สำเนา: แก้แล้วตัวจริงไม่เปลี่ยน
void addRef(size_t& n)  { n = n + 1; }   // ได้ตัวจริง: แก้แล้วตัวจริงเปลี่ยน

size_t i = 0;
addCopy(i);   // i ยังเป็น 0
addRef(i);    // i เป็น 1''', en={'// ได้สำเนา: แก้แล้วตัวจริงไม่เปลี่ยน': '// gets a copy: the original does not change',
                                  '// ได้ตัวจริง: แก้แล้วตัวจริงเปลี่ยน': '// gets the original: the original changes',
                                  '// i ยังเป็น 0': '// i is still 0', '// i เป็น 1': '// i is now 1'})
   + T('''
<p>เปรียบเหมือนเอกสาร: ส่งค่า = ถ่ายสำเนาให้ไป ใครขีดเขียนต้นฉบับก็ไม่เปลี่ยน ส่วนส่ง reference = ยื่นต้นฉบับให้เลย เลือกใช้แบบนี้:</p>
<ul>
<li><b>ต้องแก้ตัวแปรของผู้เรียก</b> → <code class="il">T&amp;</code></li>
<li><b>แค่อ่าน และเป็นชนิดเล็ก</b> (<code class="il">int</code>, <code class="il">size_t</code>, <code class="il">float</code>, <code class="il">bool</code>, pointer) → ส่งค่าตรง ๆ copy ของเล็กเร็วพอ ๆ กับ reference</li>
<li><b>แค่อ่าน แต่ข้อมูลใหญ่</b> (struct, <code class="il">String</code>, buffer) → <code class="il">const T&amp;</code> ไม่ต้อง copy ทั้งก้อน ประหยัด RAM และ <code class="il">const</code> กันไม่ให้เผลอแก้</li>
</ul>
<p>ถ้าฟังก์ชันคืนผลได้ค่าเดียว การ <code class="il">return</code> มักอ่านง่ายกว่าแก้ผ่าน reference</p>
''', '''
<p>Think of a document: passing by value hands over a photocopy, so scribbling on it leaves the original alone; passing a reference hands over the original. How to choose:</p>
<ul>
<li><b>Must change the caller's variable</b> → <code class="il">T&amp;</code></li>
<li><b>Only reads it, small type</b> (<code class="il">int</code>, <code class="il">size_t</code>, <code class="il">float</code>, <code class="il">bool</code>, pointers) → pass by value; copying something small is as fast as a reference.</li>
<li><b>Only reads it, large data</b> (struct, <code class="il">String</code>, buffer) → <code class="il">const T&amp;</code>: no full copy, less RAM, and <code class="il">const</code> stops accidental changes.</li>
</ul>
<p>If the function produces a single result, a <code class="il">return</code> value is usually easier to read than changing a reference.</p>
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
<li><code class="il">uint8_t</code>, <code class="il">uint32_t</code> ชนิดข้อมูลที่ระบุขนาดชัด (8 และ 32 bit) ใช้แทน <code class="il">int</code> ที่ขนาดเปลี่ยนตามบอร์ด (บท 01)</li>
<li><code class="il">size_t</code> เป็น <b>type</b> (ไม่ใช่ตัวแปร) จำนวนเต็มไม่ติดลบ ใช้เก็บขนาดหรือจำนวน/index บน XIAO มีขนาด 32 bit และเป็น type ของผลลัพธ์จาก <code class="il">sizeof</code></li>
<li><code class="il">sizeof(kLedPins) / sizeof(kLedPins[0])</code> = ขนาดทั้ง array หารด้วยขนาดของ 1 ช่อง = จำนวนช่อง ที่นี่ได้ 3 / 1 = 3 (<code class="il">uint8_t</code> ช่องละ 1 byte) ใช้ได้เฉพาะกับ array ตัวจริง ถ้าส่ง array เข้าฟังก์ชันจะกลายเป็น pointer และสูตรนี้ผิด</li>
<li><code class="il">(idx + 1) % kLedCount</code> <code class="il">%</code> คือหารเอาเศษ idx จึงวน 0 → 1 → 2 → 0 (เพราะ 3 % 3 = 0) ไม่เกินจำนวน LED</li>
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
<li><code class="il">uint8_t</code>, <code class="il">uint32_t</code>: types with an explicit size (8 and 32 bits). They replace <code class="il">int</code>, whose size depends on the board (lesson 01).</li>
<li><code class="il">size_t</code> is a <b>type</b> (not a variable): an unsigned integer for sizes, counts and indexes. On the XIAO it is 32 bits, and it is the type <code class="il">sizeof</code> returns.</li>
<li><code class="il">sizeof(kLedPins) / sizeof(kLedPins[0])</code> = size of the whole array divided by the size of one element = number of elements. Here 3 / 1 = 3 (a <code class="il">uint8_t</code> is 1 byte). It only works on a real array: an array passed into a function becomes a pointer and the formula is wrong.</li>
<li><code class="il">(idx + 1) % kLedCount</code>: <code class="il">%</code> is the remainder, so idx cycles 0 → 1 → 2 → 0 (since 3 % 3 = 0) and never runs past the last LED.</li>
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
