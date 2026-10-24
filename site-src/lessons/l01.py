lesson('01', 'A', T('.ino คือ C++ และเส้นทางจากโค้ดถึงบอร์ด', '.ino is C++, and the path from code to board'), 20, BOARD, goal(T('เข้าใจว่า Arduino ซ่อนอะไรไว้ และเห็น toolchain จริง', 'See what Arduino hides from you, and the real toolchain')) + T('''
<p>ไฟล์ .ino ไม่ใช่ภาษาพิเศษ IDE แค่เติม <code class="il">#include &lt;Arduino.h&gt;</code> และสร้าง function prototype ให้ แล้วส่งให้ <b>arm-none-eabi-g++</b> คอมไพล์เป็น C++ ปกติ ส่วน <code class="il">main()</code> อยู่ใน core:</p>
''', '''
<p>A .ino file is not a special language. The IDE only adds <code class="il">#include &lt;Arduino.h&gt;</code> and function prototypes, then hands the file to <b>arm-none-eabi-g++</b> to compile as ordinary C++. <code class="il">main()</code> lives in the core:</p>
''') + code('''int main() {
  init();          // clock, timer, USB CDC
  setup();
  for (;;) {
    loop();
  }
}''', T('core/main.cpp (ย่อ)', 'core/main.cpp (trimmed)')) + fig(SVG_BUILD, T('pipeline การ build ที่เกิดขึ้นทุกครั้งที่กด Verify', 'The build pipeline that runs every time you press Verify')) + '''
<h3>Hands-on</h3>''' + code('''void setup() {
  Serial.begin(115200);
  while (!Serial) {}             // รอ USB CDC พร้อม
  Serial.print("__cplusplus = ");  Serial.println(__cplusplus);
  Serial.print("sizeof(int) = ");  Serial.println(sizeof(int));
  Serial.print("sizeof(void*) = ");Serial.println(sizeof(void*));
  Serial.print("sizeof(bool) = "); Serial.println(sizeof(bool));
}

void loop() {}''', 'whoami.ino', en={'// รอ USB CDC พร้อม': '// wait for USB CDC'}) + T('''
<p>ค่า <code class="il">__cplusplus</code> บอกมาตรฐานภาษาที่ compiler ใช้ (เช่น 201103 = C++11, 201703 = C++17) จดไว้ เพราะ feature ที่ใช้ได้ขึ้นกับค่านี้ จากนั้นดูบรรทัดท้ายของ output: <i>Sketch uses … bytes</i> = flash, <i>Global variables use …</i> = RAM แบบ static</p>
''', '''
<p><code class="il">__cplusplus</code> tells you the language standard the compiler uses (e.g. 201103 = C++11, 201703 = C++17). Note it down, because the features you can use depend on it. Then read the last lines of the output: <i>Sketch uses … bytes</i> = flash, <i>Global variables use …</i> = static RAM.</p>
''') + qa([(T('ถ้า __cplusplus ได้ 201103 จะใช้ if constexpr ได้ไหม?', 'If __cplusplus is 201103, can you use if constexpr?'),
           T('ไม่ได้ if constexpr เป็นของ C++17 ต้องเพิ่ม flag -std=gnu++17 หรือเลี่ยงไปใช้ template overload', 'No. if constexpr is C++17. Add -std=gnu++17 or fall back to template overloads.')),
          (T('"Global variables use" นับ stack ด้วยไหม?', 'Does "Global variables use" include the stack?'),
           T('ไม่นับ นับเฉพาะ .data + .bss ที่รู้ขนาดตอน link ตัวแปร local บน stack ไม่อยู่ในตัวเลขนี้', 'No. It counts only .data + .bss, whose sizes are known at link time. Local variables on the stack are not in that number.'))])
   + iv(T('ในงานจริงเมื่อ build มีปัญหา ให้ไล่ตามลำดับ preprocess → compile → link (linker script กำหนด address) → objcopy → flash จะรู้ว่าพังที่ขั้นไหน และเก็บ .elf ไว้เสมอ เพราะมี debug symbol ที่ debugger ต้องใช้ ส่วน .hex/.bin คือ image ที่ลงชิป',
          'When a build breaks, walk the stages in order: preprocess → compile → link (the linker script sets the addresses) → objcopy → flash, and you will see where it failed. Always keep the .elf: it carries the debug symbols the debugger needs, while the .hex/.bin is the image that goes onto the chip.')))
