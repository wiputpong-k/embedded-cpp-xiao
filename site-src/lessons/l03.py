lesson('03', 'A', 'namespace, overloading, enum class', 25, BOARD, goal(T('จัดระเบียบชื่อและเข้าใจว่าทำไม C++ ต้องมี name mangling', 'Organize names, and understand why C++ needs name mangling'))
   + vs(T('ชื่อฟังก์ชันซ้ำไม่ได้ ต้องตั้ง <code class="il">log_int</code>, <code class="il">log_float</code> และ <code class="il">enum</code> ปนกับ int ได้ทุกที่', 'Function names must be unique, so you write <code class="il">log_int</code>, <code class="il">log_float</code>, and an <code class="il">enum</code> mixes with int anywhere.'),
        T('overload ชื่อเดียวหลายพารามิเตอร์ได้ <code class="il">namespace</code> กันชื่อชน <code class="il">enum class</code> ไม่แปลงเป็น int เอง กำหนดขนาด <code class="il">: uint8_t</code> ได้', 'One name can be overloaded for different parameters, <code class="il">namespace</code> prevents name clashes, and <code class="il">enum class</code> never converts to int by itself and can set its size with <code class="il">: uint8_t</code>.'))
   + T('''
<ul>
<li><b>overloading</b> ฟังก์ชันชื่อเดียวกันหลายตัวที่รับพารามิเตอร์ต่างกัน compiler เลือกตัวที่ตรงกับค่าที่ส่งเข้าไปให้เอง</li>
<li><b>namespace</b> กล่องใส่ชื่อ เรียกด้วย <code class="il">กล่อง::ชื่อ</code> เช่น <code class="il">logx::info</code> ชื่อในกล่องต่างกันจึงไม่ชนกัน แม้ library อื่นมี <code class="il">info</code> เหมือนกัน</li>
<li><b>enum class</b> enum ที่ต้องเรียกเต็ม เช่น <code class="il">Mode::Slow</code> และไม่กลายเป็นตัวเลขเอง ส่วน <code class="il">: uint8_t</code> กำหนดว่าใช้ที่ 1 byte</li>
</ul>
<p>ใน C ฟังก์ชันชื่อ <code class="il">info</code> ใน <code class="il">.o</code> ก็ชื่อ <code class="il">info</code> แต่ใน C++ มี <code class="il">info</code> ได้หลายตัว ชื่อนี้จึงไม่พอให้ linker (บท 01) แยกได้ compiler จึงต่อชนิดพารามิเตอร์ลงไปในชื่อ เรียกว่า <b>name mangling</b> ชื่อที่ได้เรียกว่า <b>symbol</b> คือชื่อที่ linker ใช้จับคู่ "คนเรียก" กับ "ตัวฟังก์ชัน" ถ้าหา symbol ไม่เจอ จะได้ error <code class="il">undefined reference</code> เช่น ถ้า sketch ไม่มี <code class="il">setup()</code> linker จะแจ้ง <code class="il">undefined reference to `setup'</code> เพราะ <code class="il">main()</code> ของ core เรียกหาแต่ไม่เจอ</p>
''', '''
<ul>
<li><b>overloading</b>: several functions share one name but take different parameters. The compiler picks the one that matches the arguments.</li>
<li><b>namespace</b>: a box for names, used as <code class="il">box::name</code>, e.g. <code class="il">logx::info</code>. Names in different boxes never clash, even if another library also has an <code class="il">info</code>.</li>
<li><b>enum class</b>: an enum you must spell out in full, e.g. <code class="il">Mode::Slow</code>, and that never turns into a number by itself. <code class="il">: uint8_t</code> makes it take 1 byte.</li>
</ul>
<p>In C, a function called <code class="il">info</code> is also called <code class="il">info</code> in the <code class="il">.o</code> file. C++ allows several <code class="il">info</code> functions, so that name is not enough for the linker (lesson 01) to tell them apart. The compiler therefore appends the parameter types to the name, which is called <b>name mangling</b>. The resulting name is the <b>symbol</b>: the name the linker uses to match a call with the function body. If a symbol cannot be found you get an <code class="il">undefined reference</code> error. For example, if a sketch has no <code class="il">setup()</code>, the linker reports <code class="il">undefined reference to `setup'</code>, because the core's <code class="il">main()</code> calls it and finds nothing.</p>
''')
   + fig(SVG_MANGLE, T('compiler ฝังชนิดพารามิเตอร์ลงในชื่อ symbol จึง overload ได้', 'The compiler encodes parameter types into the symbol name, which makes overloading possible')) + '''
<h3>Hands-on</h3>''' + T('''
<p>sketch นี้พิสูจน์ว่า <code class="il">info</code> 3 ตัวอยู่ร่วมกันได้ (compiler เลือกตัวตามพารามิเตอร์) และ <code class="il">enum class</code> ไม่ยอมกลายเป็นตัวเลขเอง</p>
<ol>
<li>สร้าง sketch ใหม่ วางโค้ดข้างล่าง บันทึกชื่อ <code class="il">logx</code> แล้วกด <b>Upload</b></li>
<li>เปิด <b>Tools → Serial Monitor</b> ที่ 115200 baud ถ้าไม่มีข้อความ กด reset บนบอร์ด 1 ครั้ง</li>
</ol>
''', '''
<p>This sketch proves that three <code class="il">info</code> functions can live side by side (the compiler picks one by its parameters), and that an <code class="il">enum class</code> refuses to become a number by itself.</p>
<ol>
<li>Create a new sketch, paste the code below, save it as <code class="il">logx</code>, and press <b>Upload</b>.</li>
<li>Open <b>Tools → Serial Monitor</b> at 115200 baud. If nothing appears, press reset on the board once.</li>
</ol>
''') + code('''namespace logx {
void info(const char* msg) {
  Serial.print("[I] "); Serial.println(msg);
}
void info(const char* key, int value) {
  Serial.print("[I] "); Serial.print(key); Serial.print('='); Serial.println(value);
}
void info(const char* key, float value, int digits = 2) {   // default argument
  Serial.print("[I] "); Serial.print(key); Serial.print('='); Serial.println(value, digits);
}
}  // namespace logx

enum class Mode : uint8_t { Off, Slow, Fast };

void setup() {
  Serial.begin(115200);
  while (!Serial) {}
  logx::info("boot");
  logx::info("uptime_ms", (int)millis());
  logx::info("vbat", 3.71f);
  logx::info("pi", 3.14159f, 4);
  Mode m = Mode::Slow;
  logx::info("mode", static_cast<int>(m));   // ต้อง cast เอง
  // int bad = m;   // ลองเปิดบรรทัดนี้: compile error
}

void loop() {}''', 'logx.ino', en={'// ต้อง cast เอง': '// explicit cast required', '// ลองเปิดบรรทัดนี้: compile error': '// uncomment this line: compile error'}) + T('''
<ul>
<li><b>default argument</b> <code class="il">int digits = 2</code> ถ้าผู้เรียกไม่ส่งค่านี้มา จะใช้ 2</li>
<li><code class="il">static_cast&lt;int&gt;(m)</code> การแปลงชนิดแบบ C++ ทำหน้าที่เหมือน <code class="il">(int)m</code> ของ C แต่ชัดเจนกว่าว่าตั้งใจแปลง</li>
</ul>
<p>ผลที่ควรเห็น (ตัวเลข <code class="il">uptime_ms</code> ขึ้นกับว่าเปิด Serial Monitor เมื่อไร):</p>
''', '''
<ul>
<li><b>default argument</b>: <code class="il">int digits = 2</code> means 2 is used when the caller leaves it out.</li>
<li><code class="il">static_cast&lt;int&gt;(m)</code>: the C++ cast. It does what C's <code class="il">(int)m</code> does, but makes the intent obvious.</li>
</ul>
<p>Expected output (the <code class="il">uptime_ms</code> number depends on when you open Serial Monitor):</p>
''') + code('''[I] boot
[I] uptime_ms=1234
[I] vbat=3.71
[I] pi=3.1416
[I] mode=1''', 'Serial Monitor') + T('''
<p>ผลนี้บอกอะไร:</p>
<ul>
<li><b>overloading</b> ทุกบรรทัดเรียก <code class="il">logx::info</code> ชื่อเดียวกัน แต่รูปแบบที่พิมพ์ต่างกันตามพารามิเตอร์ <code class="il">vbat</code> ได้ทศนิยม 2 ตำแหน่งจาก default argument ส่วน <code class="il">pi</code> ได้ 4 ตำแหน่งตามที่ส่งไป</li>
<li><b>enum class</b> <code class="il">mode=1</code> เพราะ <code class="il">Slow</code> เป็นตัวที่สอง (นับจาก 0) แต่ต้องแปลงเองด้วย <code class="il">static_cast</code> ลองลบ <code class="il">//</code> หน้าบรรทัด <code class="il">int bad = m;</code> แล้วกด Verify จะได้ <code class="il">error: cannot convert 'Mode' to 'int' in initialization</code> แล้วใส่ <code class="il">//</code> กลับ</li>
</ul>
''', '''
<p>What the output tells you:</p>
<ul>
<li><b>overloading</b>: every line calls the same <code class="il">logx::info</code>, yet the format differs by parameters. <code class="il">vbat</code> gets 2 decimals from the default argument; <code class="il">pi</code> gets the 4 you passed.</li>
<li><b>enum class</b>: <code class="il">mode=1</code> because <code class="il">Slow</code> is the second value (counting from 0), but you had to convert it with <code class="il">static_cast</code>. Remove the <code class="il">//</code> in front of <code class="il">int bad = m;</code> and press Verify: you get <code class="il">error: cannot convert 'Mode' to 'int' in initialization</code>. Then put the <code class="il">//</code> back.</li>
</ul>
''')
   + qa([(T('ถ้า library เขียนด้วย C ต้อง include อย่างไร?', 'How do you include a library written in C?'),
          T('ครอบ header ด้วย extern "C" { … } เพื่อปิด name mangling ให้ฟังก์ชันเหล่านั้น linker จึงหา symbol ชื่อแบบ C เจอ ถ้าไม่ครอบจะ error undefined reference', 'Wrap the header in extern "C" { … } to turn off name mangling for those functions, so the linker finds the C-style symbol names. Without it you get undefined reference errors.')),
         (T('ทำไม enum class ปลอดภัยกว่า enum?', 'Why is enum class safer than enum?'),
          T('ไม่แปลงเป็น int เอง ชื่อในนั้น (เช่น Off) ไม่หลุดออกมาชนกับชื่ออื่นข้างนอก และกำหนดชนิดที่ใช้เก็บได้ (: uint8_t) จึงคุมขนาดในหน่วยความจำได้', 'It never converts to int implicitly, its value names (like Off) do not leak out and clash with other names, and you can choose the storage type (: uint8_t) to control its size in memory.'))]))
