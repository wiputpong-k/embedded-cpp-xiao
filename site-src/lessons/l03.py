lesson('03', 'A', 'namespace, overloading, enum class', 30, BOARD, goal(T('จัดระเบียบชื่อและเข้าใจว่าทำไม C++ ต้องมี name mangling', 'Organize names, and understand why C++ needs name mangling'))
   + vs(T('ชื่อฟังก์ชันซ้ำไม่ได้ ต้องตั้ง <code class="il">log_int</code>, <code class="il">log_float</code> และ <code class="il">enum</code> ปนกับ int ได้ทุกที่', 'Function names must be unique, so you write <code class="il">log_int</code>, <code class="il">log_float</code>, and an <code class="il">enum</code> mixes with int anywhere.'),
        T('overload ชื่อเดียวหลายพารามิเตอร์ได้ <code class="il">namespace</code> กันชื่อชน <code class="il">enum class</code> ไม่แปลงเป็น int เอง กำหนดขนาด <code class="il">: uint8_t</code> ได้', 'One name can be overloaded for different parameters, <code class="il">namespace</code> prevents name clashes, and <code class="il">enum class</code> never converts to int by itself and can set its size with <code class="il">: uint8_t</code>.'))
   + T('''
<ul>
<li><b>overloading</b> ฟังก์ชันชื่อเดียวกันหลายตัวที่รับพารามิเตอร์ต่างกัน (จำนวนหรือชนิด) compiler เลือกตัวที่ตรงกับค่าที่ส่งเข้าไปให้เอง ถ้าต่างกันแค่ชนิดที่ <code class="il">return</code> ไม่นับเป็น overload</li>
<li><b>namespace</b> กล่องใส่ชื่อ ใส่ได้ทุกอย่างที่มีชื่อ ไม่ใช่แค่ฟังก์ชัน แต่รวมถึงตัวแปร ค่าคงที่ enum และ class เรียกใช้ด้วย <code class="il">กล่อง::ชื่อ</code> เช่น <code class="il">logx::info</code></li>
<li><b>enum class</b> enum ที่ต้องเรียกเต็ม เช่น <code class="il">Mode::Slow</code> และไม่กลายเป็นตัวเลขเอง ส่วน <code class="il">: uint8_t</code> กำหนดว่าใช้ที่ 1 byte</li>
</ul>
<h3>namespace: แก้ปัญหาชื่อชนกัน</h3>
<p>ใน C ทุกชื่ออยู่รวมในที่เดียว ถ้า library สองตัวมีฟังก์ชันชื่อ <code class="il">info</code> เหมือนกัน จะ build ไม่ผ่าน คนเขียน C จึงต้องเติม prefix เอง C++ ใช้ namespace ทำหน้าที่นี้แทน</p>
''', '''
<ul>
<li><b>overloading</b>: several functions share one name but take different parameters (a different number or different types). The compiler picks the one that matches the arguments. Differing only in the <code class="il">return</code> type does not count as an overload.</li>
<li><b>namespace</b>: a box for names. It holds anything with a name, not just functions: variables, constants, enums and classes. You use it as <code class="il">box::name</code>, e.g. <code class="il">logx::info</code>.</li>
<li><b>enum class</b>: an enum you must spell out in full, e.g. <code class="il">Mode::Slow</code>, and that never turns into a number by itself. <code class="il">: uint8_t</code> makes it take 1 byte.</li>
</ul>
<h3>namespace: no more name clashes</h3>
<p>In C every name lives in one shared space. If two libraries both have a function called <code class="il">info</code>, the build fails, so C programmers add a prefix by hand. C++ uses a namespace for this instead.</p>
''')
   + code('''// C: เติม prefix เองเพื่อไม่ให้ชื่อชนกัน
void logx_info(const char* msg);
void wifi_info(const char* msg);

// C++: ใช้ namespace แทน prefix
namespace logx {
  int level = 1;                // ใส่ตัวแปรได้ด้วย
  void info(const char* msg);
}
namespace wifi {
  void info(const char* msg);   // ชื่อ info ซ้ำได้ เพราะอยู่คนละกล่อง
}

logx::info("boot");
wifi::info("connected");''', en={'// C: เติม prefix เองเพื่อไม่ให้ชื่อชนกัน': '// C: add a prefix by hand to avoid clashes',
                                 '// C++: ใช้ namespace แทน prefix': '// C++: a namespace instead of a prefix',
                                 '// ใส่ตัวแปรได้ด้วย': '// variables work too',
                                 '// ชื่อ info ซ้ำได้ เพราะอยู่คนละกล่อง': '// info again is fine: a different box'})
   + T('''
<ul>
<li><b>ตัวอย่างจริงในคอร์สนี้</b> core ของ Seeed มี class ชื่อ <code class="il">RingBuffer</code> อยู่แล้ว บท 10 จึงเก็บ <code class="il">RingBuffer</code> ของเราไว้ใน namespace <code class="il">xiao</code> แล้วเรียกเป็น <code class="il">xiao::RingBuffer</code> เพื่อไม่ให้ชนกับของ core</li>
<li><b><code class="il">std::</code></b> ที่จะเห็นบ่อย ๆ ก็เป็น namespace คือกล่องของ C++ standard library เช่น <code class="il">std::array</code></li>
<li><b>namespace ไม่ใช่ class</b> namespace แค่จัดกลุ่มชื่อ สร้างเป็น object ไม่ได้ ส่วน class เป็นชนิดข้อมูลที่สร้าง object ได้ (บท 04)</li>
</ul>
<h3>enum class ต่างจาก enum ของ C อย่างไร</h3>
<p><code class="il">enum</code> ใช้ตั้งชื่อให้ชุดตัวเลือกที่รู้ล่วงหน้า เช่น โหมดหรือสถานะ ข้างในยังเป็นตัวเลข 0, 1, 2 … เหมือนเดิม C++ เพิ่ม <code class="il">enum class</code> ที่ตรวจเข้มกว่า เทียบกันได้แบบนี้:</p>
''', '''
<ul>
<li><b>A real example from this course</b>: the Seeed core already has a class called <code class="il">RingBuffer</code>, so lesson 10 keeps our <code class="il">RingBuffer</code> in the namespace <code class="il">xiao</code> and calls it <code class="il">xiao::RingBuffer</code>, which avoids a clash with the core's.</li>
<li><b><code class="il">std::</code></b>, which you will see often, is also a namespace: the box of the C++ standard library, e.g. <code class="il">std::array</code>.</li>
<li><b>A namespace is not a class</b>: a namespace only groups names, and you cannot create an object from it. A class is a data type you create objects from (lesson 04).</li>
</ul>
<h3>How enum class differs from C's enum</h3>
<p>An <code class="il">enum</code> gives names to a fixed set of choices, such as modes or states. Underneath they are still the numbers 0, 1, 2 … C++ adds <code class="il">enum class</code>, which is checked more strictly. Compare:</p>
''')
   + code('''// C: enum ธรรมดา
enum Mode  { OFF, SLOW, FAST };
enum Speed { SLOW, FAST };      // error: SLOW ซ้ำ เพราะชื่อหลุดออกมาข้างนอก
enum Mode m = SLOW;
int x = m;                      // ได้ 1 แปลงเป็น int เองโดยไม่บอก
if (m == 2) {}                  // เทียบกับตัวเลขได้ แต่อ่านไม่รู้ว่า 2 คือโหมดไหน

// C++: enum class
enum class Mode  : uint8_t { Off, Slow, Fast };   // : uint8_t = ใช้ 1 byte
enum class Speed : uint8_t { Slow, Fast };        // ไม่ชน ชื่ออยู่ในกล่องของตัวเอง
Mode m = Mode::Slow;                              // ต้องเรียกชื่อเต็ม
int x = m;                                        // error: ไม่แปลงเป็น int เอง
int y = static_cast<int>(m);                      // ต้องแปลงเองแบบตั้งใจ''',
          en={'// C: enum ธรรมดา': '// C: a plain enum',
              '// error: SLOW ซ้ำ เพราะชื่อหลุดออกมาข้างนอก': '// error: SLOW again, the names leak out',
              '// ได้ 1 แปลงเป็น int เองโดยไม่บอก': '// 1: silently turned into an int',
              '// เทียบกับตัวเลขได้ แต่อ่านไม่รู้ว่า 2 คือโหมดไหน': '// compares with a number, but which mode is 2?',
              '// : uint8_t = ใช้ 1 byte': '// : uint8_t = takes 1 byte',
              '// ไม่ชน ชื่ออยู่ในกล่องของตัวเอง': '// no clash: the names stay in their own box',
              '// ต้องเรียกชื่อเต็ม': '// the full name is required',
              '// error: ไม่แปลงเป็น int เอง': '// error: no automatic conversion to int',
              '// ต้องแปลงเองแบบตั้งใจ': '// convert on purpose'})
   + T('''
<ul>
<li><b>ชื่อไม่หลุดออกมาข้างนอก</b> enum ของ C ทำให้ <code class="il">SLOW</code> กลายเป็นชื่อกลางที่ใช้ได้ทั้งไฟล์ จึงต้องตั้ง prefix เอง เช่น <code class="il">MODE_SLOW</code> ส่วน <code class="il">enum class</code> เก็บชื่อไว้ในกล่องของตัวเองเหมือน namespace</li>
<li><b>ไม่แปลงเป็นตัวเลขเอง</b> compiler จับ bug ที่เผลอเอาโหมดไปปนกับตัวเลขให้ตั้งแต่ตอน compile ถ้าต้องการตัวเลขจริงให้ใช้ <code class="il">static_cast&lt;int&gt;(m)</code></li>
<li><b>กำหนดขนาดได้</b> enum ของ C มีขนาดเท่า <code class="il">int</code> (4 byte บน nRF52840) <code class="il">: uint8_t</code> ทำให้รู้ขนาดแน่นอน เหมาะกับการเก็บใน struct ส่งทาง Serial/BLE หรือบันทึกลง flash</li>
</ul>
<p>หลัง compile ทั้งสองแบบเป็นตัวเลขเหมือนกัน <code class="il">enum class</code> จึงไม่ทำให้โปรแกรมช้าลง สิ่งที่ได้คือ compiler ตรวจให้เข้มขึ้น</p>
<h3>ใช้ enum กับงานแบบไหน</h3>
<p>ใช้เมื่อค่ามี<b>ตัวเลือกจำนวนจำกัดที่รู้ล่วงหน้า</b> และแต่ละตัวมีความหมาย ไม่ได้เป็นปริมาณที่เอาไปบวกลบ งาน firmware ที่ใช้บ่อย:</p>
<ul>
<li><b>สถานะของ state machine</b> เช่น <code class="il">Idle</code>, <code class="il">Connecting</code>, <code class="il">Connected</code> (ตัวอย่างข้างล่าง)</li>
<li><b>โหมดหรือการตั้งค่า</b> เช่น <code class="il">Mode::Slow</code> ในบทนี้ หรือระดับ log (<code class="il">Debug</code>, <code class="il">Info</code>, <code class="il">Error</code>)</li>
<li><b>event</b> เช่น <code class="il">Debouncer::Event::Pressed</code> ในบท 07</li>
<li><b>ผลลัพธ์และ error code</b> เช่น <code class="il">Err::Timeout</code> อ่านง่ายกว่า <code class="il">return -3;</code></li>
<li><b>คำสั่งใน protocol</b> กำหนดเลขเองให้ตรงกับเอกสาร เช่น <code class="il">enum class Cmd : uint8_t { Ping = 0x01, ReadTemp = 0x10 };</code></li>
</ul>
''', '''
<ul>
<li><b>Names stay inside</b>: C's enum makes <code class="il">SLOW</code> a shared name for the whole file, so you add a prefix by hand, such as <code class="il">MODE_SLOW</code>. <code class="il">enum class</code> keeps its names in its own box, like a namespace.</li>
<li><b>No automatic conversion to a number</b>: the compiler catches the bug of mixing a mode up with a number at compile time. When you really need the number, use <code class="il">static_cast&lt;int&gt;(m)</code>.</li>
<li><b>You can set its size</b>: C's enum is the size of an <code class="il">int</code> (4 bytes on the nRF52840). <code class="il">: uint8_t</code> fixes the size, which helps when you store it in a struct, send it over Serial/BLE or save it to flash.</li>
</ul>
<p>After compiling, both are just numbers, so <code class="il">enum class</code> costs no speed. What you gain is stricter checking by the compiler.</p>
<h3>When to use an enum</h3>
<p>Use one when a value has <b>a small set of choices known in advance</b>, each with a meaning, and it is not a quantity you add or subtract. Common cases in firmware:</p>
<ul>
<li><b>States of a state machine</b>, e.g. <code class="il">Idle</code>, <code class="il">Connecting</code>, <code class="il">Connected</code> (example below).</li>
<li><b>Modes or settings</b>, e.g. <code class="il">Mode::Slow</code> in this lesson, or log levels (<code class="il">Debug</code>, <code class="il">Info</code>, <code class="il">Error</code>).</li>
<li><b>Events</b>, e.g. <code class="il">Debouncer::Event::Pressed</code> in lesson 07.</li>
<li><b>Results and error codes</b>: <code class="il">Err::Timeout</code> reads far better than <code class="il">return -3;</code>.</li>
<li><b>Protocol commands</b>, with numbers you set to match the spec, e.g. <code class="il">enum class Cmd : uint8_t { Ping = 0x01, ReadTemp = 0x10 };</code></li>
</ul>
''')
   + code('''enum class State : uint8_t { Idle, Connecting, Connected };
State state = State::Idle;

switch (state) {
  case State::Idle:       /* รอกดปุ่ม */     break;
  case State::Connecting: /* รอเชื่อมต่อ */  break;
  case State::Connected:  /* ส่งข้อมูล */    break;
}''', en={'/* รอกดปุ่ม */': '/* wait for button */',
          '/* รอเชื่อมต่อ */': '/* wait for link */',
          '/* ส่งข้อมูล */': '/* send data */'})
   + T('''
<p><b>ไม่ควรใช้ enum</b> กับค่าที่เป็นปริมาณ เช่น อุณหภูมิ เวลา หมายเลข pin หรือ baud rate ค่าพวกนี้ใช้ <code class="il">constexpr</code> (บท 02) วิธีจำง่าย ๆ: ถ้าต้องเขียนคอมเมนต์อธิบายตัวเลข เช่น <code class="il">if (state == 2) // 2 = connected</code> แบบนี้ควรเปลี่ยนเป็น enum</p>
<h3>name mangling: overload ทำงานได้อย่างไร</h3>
<p>ใน C ฟังก์ชันชื่อ <code class="il">info</code> ใน <code class="il">.o</code> ก็ชื่อ <code class="il">info</code> แต่ใน C++ มี <code class="il">info</code> ได้หลายตัว ชื่อนี้จึงไม่พอให้ linker (บท 01) แยกได้ compiler จึงต่อชนิดพารามิเตอร์ลงไปในชื่อ เรียกว่า <b>name mangling</b> ชื่อที่ได้เรียกว่า <b>symbol</b> คือชื่อที่ linker ใช้จับคู่ "คนเรียก" กับ "ตัวฟังก์ชัน" ถ้าหา symbol ไม่เจอ จะได้ error <code class="il">undefined reference</code> เช่น ถ้า sketch ไม่มี <code class="il">setup()</code> linker จะแจ้ง <code class="il">undefined reference to `setup'</code> เพราะ <code class="il">main()</code> ของ core เรียกหาแต่ไม่เจอ</p>
''', '''
<p><b>Do not use an enum</b> for quantities such as temperature, time, a pin number or a baud rate. Use <code class="il">constexpr</code> for those (lesson 02). A simple rule: if you have to explain a number in a comment, as in <code class="il">if (state == 2) // 2 = connected</code>, it should be an enum.</p>
<h3>Name mangling: how overloading works</h3>
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
<p>อ่านโค้ดทีละส่วน:</p>
<ul>
<li><b><code class="il">const char* msg</code></b> ข้อความ <code class="il">"boot"</code> ถูกเก็บเป็น array ของ <code class="il">char</code> ที่ปิดท้ายด้วย <code class="il">'\\0'</code> (<code class="il">'b' 'o' 'o' 't' '\\0'</code>) ตอนส่งเข้าฟังก์ชันจะไม่คัดลอกข้อความทั้งก้อน แต่ส่งแค่ address ของตัวอักษรตัวแรก <code class="il">char*</code> คือ pointer ที่เก็บ address นั้น และ <code class="il">const</code> แปลว่าฟังก์ชันอ่านได้อย่างเดียว ใช้ <code class="il">char msg</code> เฉย ๆ ไม่ได้ เพราะ <code class="il">char</code> เก็บได้แค่ตัวอักษรเดียว (<code class="il">'b'</code>) ถ้าเขียนแบบนั้น <code class="il">info("boot")</code> จะ compile error</li>
<li><b><code class="il">millis()</code></b> ฟังก์ชันของ Arduino core เหมือน <code class="il">delay()</code> ใช้ได้ทุก sketch โดยไม่ต้อง include อะไรเพิ่ม คืนค่าเป็นจำนวนมิลลิวินาทีนับตั้งแต่บอร์ดเริ่มทำงาน ชนิด <code class="il">uint32_t</code> (จำนวนเต็มไม่ติดลบ 32 บิต) จะใช้จริงในบท 07–08</li>
<li><b><code class="il">(int)millis()</code></b> <code class="il">(int)</code> คือการแปลงชนิดแบบ C ต้องใส่เพราะ <code class="il">logx::info</code> มีทั้งตัวที่รับ <code class="il">int</code> และตัวที่รับ <code class="il">float</code> ถ้าส่ง <code class="il">uint32_t</code> เข้าไปตรง ๆ compiler แปลงเป็นได้ทั้งสองแบบและเลือกไม่ได้ จะได้ <code class="il">error: call of overloaded 'info(...)' is ambiguous</code> ค่าบวกที่ <code class="il">int</code> เก็บได้สูงสุดเท่ากับราว 24.8 วัน หลังจากนั้นจะกลายเป็นค่าลบ แต่ตัวอย่างนี้ไม่ต้องห่วง</li>
<li><b>default argument</b> <code class="il">int digits = 2</code> ถ้าผู้เรียกไม่ส่งค่านี้มา จะใช้ 2</li>
<li><code class="il">static_cast&lt;int&gt;(m)</code> การแปลงชนิดแบบ C++ ทำหน้าที่เหมือน <code class="il">(int)m</code> ของ C แต่ชัดเจนกว่าว่าตั้งใจแปลง</li>
</ul>
<p>ผลที่ควรเห็น (ตัวเลข <code class="il">uptime_ms</code> ขึ้นกับว่าเปิด Serial Monitor เมื่อไร):</p>
''', '''
<p>Reading the code piece by piece:</p>
<ul>
<li><b><code class="il">const char* msg</code></b>: the text <code class="il">"boot"</code> is stored as an array of <code class="il">char</code> ending in <code class="il">'\\0'</code> (<code class="il">'b' 'o' 'o' 't' '\\0'</code>). Passing it to a function does not copy the text; only the address of the first character is passed. <code class="il">char*</code> is a pointer holding that address, and <code class="il">const</code> means the function may only read it. Plain <code class="il">char msg</code> would not work: a <code class="il">char</code> holds one character (<code class="il">'b'</code>), so <code class="il">info("boot")</code> would fail to compile.</li>
<li><b><code class="il">millis()</code></b>: an Arduino core function, like <code class="il">delay()</code>, available in every sketch without any include. It returns the milliseconds since the board started, as a <code class="il">uint32_t</code> (an unsigned 32-bit integer). You will use it for real in lessons 07–08.</li>
<li><b><code class="il">(int)millis()</code></b>: <code class="il">(int)</code> is a C-style cast. It is needed because <code class="il">logx::info</code> has one version taking <code class="il">int</code> and one taking <code class="il">float</code>. Pass a <code class="il">uint32_t</code> directly and the compiler could convert it to either, cannot choose, and reports <code class="il">error: call of overloaded 'info(...)' is ambiguous</code>. The largest positive value an <code class="il">int</code> holds is about 24.8 days of milliseconds; after that it turns negative, which does not matter here.</li>
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
<li><b>ambiguous</b> ลองลบ <code class="il">(int)</code> หน้า <code class="il">millis()</code> แล้วกด Verify จะเห็น error ว่า call of overloaded <code class="il">info</code> is ambiguous แล้วใส่ <code class="il">(int)</code> กลับ</li>
</ul>
''', '''
<p>What the output tells you:</p>
<ul>
<li><b>overloading</b>: every line calls the same <code class="il">logx::info</code>, yet the format differs by parameters. <code class="il">vbat</code> gets 2 decimals from the default argument; <code class="il">pi</code> gets the 4 you passed.</li>
<li><b>enum class</b>: <code class="il">mode=1</code> because <code class="il">Slow</code> is the second value (counting from 0), but you had to convert it with <code class="il">static_cast</code>. Remove the <code class="il">//</code> in front of <code class="il">int bad = m;</code> and press Verify: you get <code class="il">error: cannot convert 'Mode' to 'int' in initialization</code>. Then put the <code class="il">//</code> back.</li>
<li><b>ambiguous</b>: remove the <code class="il">(int)</code> in front of <code class="il">millis()</code> and press Verify. The error says the call of overloaded <code class="il">info</code> is ambiguous. Then put <code class="il">(int)</code> back.</li>
</ul>
''')
   + qa([(T('ถ้า library เขียนด้วย C ต้อง include อย่างไร?', 'How do you include a library written in C?'),
          T('ครอบ header ด้วย extern "C" { … } เพื่อปิด name mangling ให้ฟังก์ชันเหล่านั้น linker จึงหา symbol ชื่อแบบ C เจอ ถ้าไม่ครอบจะ error undefined reference', 'Wrap the header in extern "C" { … } to turn off name mangling for those functions, so the linker finds the C-style symbol names. Without it you get undefined reference errors.')),
         (T('ถ้าเพิ่ม int info(const char* msg) ที่ต่างจากตัวเดิมแค่ชนิดที่ return จะ compile ผ่านไหม?', 'If you add int info(const char* msg), which differs from the existing one only in its return type, will it compile?'),
          T('ไม่ผ่าน ตอนเรียก info("boot") compiler ดูแค่ค่าที่ส่งเข้าไป ซึ่งเหมือนกันทั้งสองตัว จึงแยกไม่ได้ overload ต้องต่างกันที่พารามิเตอร์', 'No. A call like info("boot") only shows the compiler the arguments, which are the same for both, so it cannot tell them apart. An overload must differ in its parameters.')),
         (T('หมายเลข pin ของ LED ควรเก็บเป็น enum class หรือ constexpr?', 'Should an LED pin number be an enum class or a constexpr?'),
          T('constexpr เพราะ pin เป็นตัวเลขที่ต้องส่งให้ digitalWrite() ตรง ๆ ถ้าเป็น enum class ต้อง static_cast ทุกครั้งที่ใช้ enum เหมาะกับชุดตัวเลือกที่มีความหมาย เช่น โหมดหรือสถานะ', 'constexpr. A pin is a number you pass straight to digitalWrite(); as an enum class you would need a static_cast every time. Enums suit a set of meaningful choices, such as modes or states.'))]))
