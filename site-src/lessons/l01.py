lesson('01', 'A', T('.ino คือ C++ และเส้นทางจากโค้ดถึงบอร์ด', '.ino is C++, and the path from code to board'), 25, BOARD, goal(T('เข้าใจว่า Arduino ซ่อนอะไรไว้ และเห็น toolchain จริง', 'See what Arduino hides from you, and the real toolchain')) + T('''
<p>ถ้าเคยเขียน C บน <b>microcontroller</b> (MCU: ชิปตัวเดียวที่มี CPU, หน่วยความจำ และขา I/O อยู่ในตัว เช่น nRF52840 บน XIAO) คุณเขียน <code class="il">main()</code> เองใน <code class="il">src/main.c</code> แล้วใครเรียก <code class="il">main()</code>? บน PC คือ OS แต่ MCU ไม่มี OS: เมื่อจ่ายไฟหรือกด reset CPU จะรัน <b>startup code</b> (โค้ดสั้น ๆ ที่มากับชิป เช่นไฟล์ <code class="il">startup_xxx.s</code>) ซึ่งเตรียม stack และตัวแปร global แล้วกระโดดไป <code class="il">main()</code></p>
<p>Arduino ใช้กลไกเดียวกัน ต่างแค่ <code class="il">main()</code> ย้ายไปอยู่ใน core และ <code class="il">main()</code> ตัวนั้นเรียก <code class="il">setup()</code> กับ <code class="il">loop()</code> ที่คุณเขียนใน .ino แทน sketch จึงไม่มี <code class="il">main()</code></p>
''' + fig(SVG_ENTRY, T('จาก reset ถึงโค้ดของคุณ: ใน C คุณเขียน main() เอง ใน Arduino คุณเขียนแค่ setup() กับ loop()', 'From reset to your code: in C you write main(); in Arduino you write only setup() and loop()')) + '''
<p><b>".ino คือ C++"</b> หมายความว่า .ino ไม่ใช่ภาษาพิเศษ IDE แค่เติม <code class="il">#include &lt;Arduino.h&gt;</code> และสร้าง function prototype ให้ แล้วส่งให้ <b>arm-none-eabi-g++</b> คอมไพล์เป็น C++ ปกติ ผลคือทุกอย่างของ C++ (class, namespace, template ฯลฯ) ใช้ใน sketch ได้ ซึ่งคือสิ่งที่คอร์สนี้สอนต่อไป และแยกโค้ดเป็นไฟล์ .h/.cpp ได้เหมือนโปรเจกต์ C++ ทั่วไป คำศัพท์ในย่อหน้านี้:</p>
<ul>
<li><b>toolchain</b> ชุดโปรแกรมที่แปลงโค้ดเป็นไฟล์ที่ลงชิปได้ (compiler, linker, เครื่องมือแปลงไฟล์) IDE เรียกให้เองเมื่อกด Verify</li>
<li><b>arm-none-eabi-g++</b> g++ แบบ <b>cross-compiler</b> คือรันบน PC แต่สร้างโค้ดให้ CPU อื่น: <i>arm</i> = CPU ตระกูล ARM (nRF52840 ใช้ Cortex-M4F), <i>none</i> = ไม่มี OS, <i>eabi</i> = มาตรฐานการเรียกฟังก์ชันและจัดข้อมูลของ ARM สำหรับ embedded</li>
<li><b>core</b> โค้ดที่ผู้ผลิตเตรียมไว้ให้ชิปรุ่นนั้น มี <code class="il">main()</code>, <code class="il">digitalWrite()</code>, <code class="il">Serial</code> ฯลฯ คือสิ่งที่ติดตั้งจาก Boards Manager ในบท 00</li>
<li><b>function prototype</b> บรรทัดประกาศฟังก์ชันล่วงหน้า เช่น <code class="il">void blink(int ms);</code> C++ บังคับให้ประกาศก่อนเรียก ใน .ino เขียนฟังก์ชันไว้ท้ายไฟล์ได้เพราะ IDE สร้างบรรทัดนี้ให้</li>
</ul>
<p><code class="il">main()</code> ตัวจริงอยู่ใน core:</p>
''', '''
<p>If you have written C for a <b>microcontroller</b> (MCU: a single chip with CPU, memory and I/O pins built in, like the nRF52840 on the XIAO), you wrote <code class="il">main()</code> yourself in <code class="il">src/main.c</code>. But who calls <code class="il">main()</code>? On a PC it is the OS. An MCU has no OS: on power-up or reset, the CPU runs the <b>startup code</b> (a short piece of code that comes with the chip, e.g. <code class="il">startup_xxx.s</code>), which sets up the stack and global variables and then jumps to <code class="il">main()</code>.</p>
<p>Arduino uses the same mechanism. The only difference is that <code class="il">main()</code> moved into the core, and that <code class="il">main()</code> calls the <code class="il">setup()</code> and <code class="il">loop()</code> you write in the .ino. That is why a sketch has no <code class="il">main()</code>.</p>
''' + fig(SVG_ENTRY, T('จาก reset ถึงโค้ดของคุณ: ใน C คุณเขียน main() เอง ใน Arduino คุณเขียนแค่ setup() กับ loop()', 'From reset to your code: in C you write main(); in Arduino you write only setup() and loop()')) + '''
<p><b>".ino is C++"</b> means a .ino file is not a special language. The IDE only adds <code class="il">#include &lt;Arduino.h&gt;</code> and function prototypes, then hands the file to <b>arm-none-eabi-g++</b> to compile as ordinary C++. So everything in C++ (classes, namespaces, templates and so on) works in a sketch, which is what the rest of this course teaches, and you can split code into .h/.cpp files like any C++ project. The terms in that paragraph:</p>
<ul>
<li><b>toolchain</b>: the set of programs that turns code into a file the chip can run (compiler, linker, file converters). The IDE runs them when you press Verify.</li>
<li><b>arm-none-eabi-g++</b>: a <b>cross-compiler</b> version of g++. It runs on your PC but produces code for another CPU: <i>arm</i> = the ARM CPU family (the nRF52840 is a Cortex-M4F), <i>none</i> = no OS, <i>eabi</i> = ARM's embedded standard for calling functions and laying out data.</li>
<li><b>core</b>: code the vendor provides for that chip, with <code class="il">main()</code>, <code class="il">digitalWrite()</code>, <code class="il">Serial</code> and so on. It is what you installed from Boards Manager in lesson 00.</li>
<li><b>function prototype</b>: a line that declares a function ahead of time, e.g. <code class="il">void blink(int ms);</code>. C++ requires a declaration before a call. In a .ino you can put functions at the end of the file because the IDE writes these lines for you.</li>
</ul>
<p>The real <code class="il">main()</code> lives in the core:</p>
''') + code('''int main() {
  init();          // clock, timer, USB CDC
  setup();
  for (;;) {
    loop();
  }
}''', T('core/main.cpp (ย่อ)', 'core/main.cpp (trimmed)')) + T('''
<p><code class="il">main()</code> ของ core เรียก <code class="il">init()</code> เตรียมฮาร์ดแวร์ เรียก <code class="il">setup()</code> ครั้งเดียว แล้ววนเรียก <code class="il">loop()</code> ไม่รู้จบ เพราะ firmware ไม่มี OS ให้ "จบแล้วกลับไป" สิ่งที่ <code class="il">init()</code> เตรียม:</p>
<ul>
<li><b>clock</b> สัญญาณจังหวะที่ขับ CPU และวงจรอื่น (nRF52840 = 64 MHz) ต้องตั้งก่อนทุกอย่าง</li>
<li><b>timer</b> วงจรนับเวลาในชิป เป็นที่มาของ <code class="il">millis()</code> และ <code class="il">delay()</code></li>
<li><b>USB CDC</b> ทำให้บอร์ดแสดงตัวเป็น serial port เสมือนผ่านสาย USB (พอร์ต COM ที่เห็นใน Windows) Serial Monitor คุยกับบอร์ดผ่านช่องนี้</li>
</ul>
<p class="note">core nRF52 ตัวจริงรัน <code class="il">setup()</code>/<code class="il">loop()</code> ใน task ของ FreeRTOS (OS ขนาดเล็กสำหรับ MCU) และมีขั้นตอนมากกว่านี้ แต่ลำดับ init → setup → loop เหมือนเดิม</p>
''', '''
<p>The core's <code class="il">main()</code> calls <code class="il">init()</code> to prepare the hardware, calls <code class="il">setup()</code> once, then calls <code class="il">loop()</code> forever, because firmware has no OS to "return to". What <code class="il">init()</code> prepares:</p>
<ul>
<li><b>clock</b>: the timing signal that drives the CPU and other circuits (64 MHz on the nRF52840). It must be set up first.</li>
<li><b>timer</b>: a counting circuit in the chip. <code class="il">millis()</code> and <code class="il">delay()</code> are built on it.</li>
<li><b>USB CDC</b>: makes the board appear as a virtual serial port over USB (the COM port you see in Windows). Serial Monitor talks to the board through it.</li>
</ul>
<p class="note">The real nRF52 core runs <code class="il">setup()</code>/<code class="il">loop()</code> inside a FreeRTOS task (a small OS for MCUs) and does more steps, but the order init → setup → loop is the same.</p>
''') + fig(SVG_BUILD, T('pipeline การ build ที่เกิดขึ้นทุกครั้งที่กด Verify', 'The build pipeline that runs every time you press Verify')) + T('''
<p>ไฟล์และเครื่องมือในรูป:</p>
<ul>
<li><b>.o</b> (object file) ผลการ compile ทีละไฟล์ เป็นคำสั่งเครื่องของ ARM แล้ว แต่ยังไม่มี address จริง และยังเรียกฟังก์ชันในไฟล์อื่นไม่ได้</li>
<li><b>linker</b> รวม .o ทุกไฟล์กับ core.a (core ที่ compile ไว้แล้ว) และ library แล้วต่อการเรียกข้ามไฟล์ให้ครบ</li>
<li><b>linker script</b> ไฟล์บอก linker ว่า flash และ RAM เริ่มที่ address ไหน มีขนาดเท่าไร และโค้ดกับตัวแปรวางตรงไหน</li>
<li><b>.elf</b> ผลของ linker มีทั้งโค้ดและ debug symbol (ชื่อฟังก์ชัน ตัวแปร เลขบรรทัด)</li>
<li><b>objcopy</b> ตัดเหลือเฉพาะ byte ที่จะเขียนลงชิป (.hex, .uf2) จากนั้นขั้น upload หรือ <b>flash</b> ส่งไฟล์ให้ <b>bootloader</b> (โปรแกรมเล็ก ๆ ในชิปที่รับ firmware ใหม่) เขียนลงหน่วยความจำ</li>
</ul>
''', '''
<p>The files and tools in the figure:</p>
<ul>
<li><b>.o</b> (object file): one source file after compiling. It is ARM machine code, but it has no final addresses yet and cannot call functions in other files.</li>
<li><b>linker</b>: combines all .o files with core.a (the precompiled core) and libraries, and connects calls between files.</li>
<li><b>linker script</b>: tells the linker where flash and RAM start, how big they are, and where code and variables go.</li>
<li><b>.elf</b>: the linker's output, holding the code plus debug symbols (function and variable names, line numbers).</li>
<li><b>objcopy</b>: keeps only the bytes to be written to the chip (.hex, .uf2). Then the upload, or <b>flash</b>, step hands the file to the <b>bootloader</b> (a small program on the chip that receives new firmware), which writes it into memory.</li>
</ul>
''') + '''
<h3>Hands-on</h3>''' + T('''
<p>การทดลองนี้พิสูจน์ 4 เรื่องจากด้านบน: .ino ถูก compile เป็น C++, IDE สร้าง prototype ให้, โค้ดถูกสร้างให้ CPU ของบอร์ด (ไม่ใช่ PC) และ <code class="il">init()</code> ของ core เตรียม USB ไว้ให้ก่อน <code class="il">setup()</code></p>
<ol>
<li>เปิด Arduino IDE เลือกบอร์ดและพอร์ตเหมือนบท 00 แล้วสร้าง sketch ใหม่ (<b>File → New Sketch</b>) วางโค้ดด้านล่างแทนของเดิม บันทึกชื่อ <code class="il">whoami</code></li>
<li>กด <b>Upload</b> รอจนแถบ Output ขึ้น <i>Device programmed</i> หรือ upload เสร็จ</li>
<li>เปิด <b>Tools → Serial Monitor</b> แล้วตั้งความเร็วมุมขวาเป็น <b>115200 baud</b> ถ้าไม่มีข้อความขึ้น ให้กด reset บนบอร์ด 1 ครั้ง</li>
</ol>
''', '''
<p>This exercise proves four points from above: the .ino is compiled as C++, the IDE generates prototypes, the code is built for the board's CPU (not your PC), and the core's <code class="il">init()</code> prepares USB before <code class="il">setup()</code>.</p>
<ol>
<li>Open Arduino IDE, select the board and port as in lesson 00, and create a new sketch (<b>File → New Sketch</b>). Replace its contents with the code below and save it as <code class="il">whoami</code>.</li>
<li>Press <b>Upload</b> and wait until the Output panel shows <i>Device programmed</i> or the upload finishes.</li>
<li>Open <b>Tools → Serial Monitor</b> and set the speed at the right to <b>115200 baud</b>. If nothing appears, press reset on the board once.</li>
</ol>
''') + code('''void setup() {
  Serial.begin(115200);
  while (!Serial) {}             // รอ USB CDC พร้อม
  printInfo();                   // ฟังก์ชันอยู่ท้ายไฟล์ แต่เรียกได้
}

void loop() {}

void printInfo() {
  Serial.print("__cplusplus = ");  Serial.println(__cplusplus);
  Serial.print("sizeof(int) = ");  Serial.println(sizeof(int));
  Serial.print("sizeof(void*) = ");Serial.println(sizeof(void*));
  Serial.print("sizeof(bool) = "); Serial.println(sizeof(bool));
}''', 'whoami.ino', en={'// รอ USB CDC พร้อม': '// wait for USB CDC', '// ฟังก์ชันอยู่ท้ายไฟล์ แต่เรียกได้': '// defined at the end, still callable'}) + T('''
<ul>
<li><code class="il">Serial.begin(115200)</code> เปิด serial ที่ 115200 baud (bit ต่อวินาที) สำหรับ USB CDC ตัวเลขนี้ไม่มีผลจริง แต่ให้ตั้งตรงกับ Serial Monitor จนเป็นนิสัย เพราะ serial แบบสายจริง (UART) ต้องตรงกันทั้งสองฝั่ง</li>
<li><code class="il">while (!Serial) {}</code> รอจนคอมพิวเตอร์เปิดพอร์ต ไม่อย่างนั้นข้อความจะถูกส่งออกไปก่อนเปิด Serial Monitor และหายไป</li>
<li><code class="il">sizeof(x)</code> ขนาดของชนิดข้อมูลเป็น byte</li>
</ul>
<p>ผลที่ควรเห็น:</p>
''', '''
<ul>
<li><code class="il">Serial.begin(115200)</code> opens serial at 115200 baud (bits per second). Over USB CDC the number has no real effect, but make a habit of matching it in Serial Monitor, because a wired serial port (UART) needs both sides to agree.</li>
<li><code class="il">while (!Serial) {}</code> waits until the computer opens the port. Otherwise the text is sent before Serial Monitor opens and is lost.</li>
<li><code class="il">sizeof(x)</code> gives the size of a type in bytes.</li>
</ul>
<p>Expected output:</p>
''') + code('''__cplusplus = 201103
sizeof(int) = 4
sizeof(void*) = 4
sizeof(bool) = 1''', 'Serial Monitor') + T('''
<p>ผลนี้บอกอะไร เทียบกับเนื้อหาด้านบน:</p>
<ul>
<li><b>.ino คือ C++</b> <code class="il">__cplusplus</code> มีค่า แปลว่าไฟล์ถูก compile เป็น C++ (macro นี้มีเฉพาะใน C++ ถ้า compile เป็นภาษา C บรรทัดนี้จะ error) ค่า 201103 = C++11 (201703 = C++17) จดไว้ เพราะ feature ที่ใช้ได้ขึ้นกับค่านี้</li>
<li><b>prototype</b> compile ผ่านทั้งที่ <code class="il">setup()</code> เรียก <code class="il">printInfo()</code> ก่อนบรรทัดที่ประกาศ ถ้าเป็นไฟล์ .cpp ปกติจะได้ error <code class="il">'printInfo' was not declared in this scope</code> ที่ผ่านได้เพราะ IDE เติม prototype ไว้ต้นไฟล์ให้</li>
<li><b>cross-compiler</b> <code class="il">int</code> และ pointer ได้ 4 byte เพราะ Cortex-M4F เป็น CPU 32-bit ถ้า compile โค้ดเดียวกันบน PC 64-bit จะได้ <code class="il">sizeof(void*) = 8</code> และบน Arduino Uno (8-bit) <code class="il">int</code> มีแค่ 2 byte โค้ด embedded จึงไม่ควรเดาขนาด <code class="il">int</code></li>
<li><b><code class="il">main()</code> ของ core</b> ข้อความขึ้นได้เพราะ <code class="il">init()</code> เปิด USB CDC ไว้ก่อน <code class="il">setup()</code> จะถูกเรียก</li>
</ul>
<p>อยากเห็นไฟล์ C++ ที่ IDE สร้างจริง: เปิด <b>File → Preferences</b> ติ๊ก <i>Show verbose output during compile</i> แล้วกด Verify ในแถบ Output หาคำสั่งที่ลงท้ายด้วย <code class="il">sketch\\whoami.ino.cpp</code> แล้วเปิดไฟล์ตาม path นั้นด้วย Notepad จะเห็นประมาณนี้:</p>
''', '''
<p>What the output tells you, point by point:</p>
<ul>
<li><b>.ino is C++</b>: <code class="il">__cplusplus</code> has a value, so the file was compiled as C++ (the macro exists only in C++; compiled as C, this line would fail). 201103 = C++11 (201703 = C++17). Note it down, because the features you can use depend on it.</li>
<li><b>prototype</b>: it compiles even though <code class="il">setup()</code> calls <code class="il">printInfo()</code> before the line that defines it. In a plain .cpp file you would get <code class="il">'printInfo' was not declared in this scope</code>. It works because the IDE adds prototypes at the top of the file.</li>
<li><b>cross-compiler</b>: <code class="il">int</code> and pointers are 4 bytes because the Cortex-M4F is a 32-bit CPU. Compile the same code on a 64-bit PC and <code class="il">sizeof(void*)</code> is 8; on an Arduino Uno (8-bit) <code class="il">int</code> is only 2 bytes. So embedded code should not assume the size of <code class="il">int</code>.</li>
<li><b>The core's <code class="il">main()</code></b>: the text appears because <code class="il">init()</code> set up USB CDC before <code class="il">setup()</code> was called.</li>
</ul>
<p>To see the C++ file the IDE generates: open <b>File → Preferences</b>, tick <i>Show verbose output during compile</i> and press Verify. In the Output panel, find the command ending in <code class="il">sketch\\whoami.ino.cpp</code> and open that file in Notepad. It looks roughly like this:</p>
''') + code('''#include <Arduino.h>            // IDE เติมให้
#include <Adafruit_TinyUSB.h>
void setup();                   // prototype ที่ IDE สร้างให้
void loop();
void printInfo();
void setup() {
  Serial.begin(115200);
  ...''', T('whoami.ino.cpp (ตัดบรรทัด #line ออก)', 'whoami.ino.cpp (#line lines removed)'),
         en={'// IDE เติมให้': '// added by the IDE', '// prototype ที่ IDE สร้างให้': '// prototypes generated by the IDE'}) + T('''
<p class="note">บรรทัด <code class="il">#line</code> ที่ IDE แทรกไว้ทำให้ error ชี้กลับไปที่เลขบรรทัดใน .ino ไม่ใช่ใน .ino.cpp</p>
<p>สุดท้ายดูบรรทัดท้ายของแถบ Output หลัง Verify หรือ Upload ตัวเลขนี้มาจากขั้น link ในรูป pipeline:</p>
<ul>
<li><i>Sketch uses … bytes</i> = ขนาดโปรแกรมใน <b>flash</b> หน่วยความจำถาวรที่เก็บโปรแกรม ไฟดับไม่หาย (nRF52840 มี 1 MB แต่ส่วนหนึ่งถูกจองให้ bootloader และ stack BLE จึงเห็น Maximum น้อยกว่านั้น)</li>
<li><i>Global variables use …</i> = <b>RAM</b> แบบ static หน่วยความจำทำงาน (256 KB) ที่ไฟดับแล้วหาย "static" คือส่วนที่รู้ขนาดตั้งแต่ตอน build ได้แก่ตัวแปร global ส่วน RAM ที่เหลือใช้เป็น <b>stack</b> (ตัวแปร local) และ heap</li>
</ul>
''', '''
<p class="note">The <code class="il">#line</code> lines the IDE inserts make errors point to line numbers in the .ino, not in the .ino.cpp.</p>
<p>Finally, read the last lines of the Output panel after Verify or Upload. These numbers come from the link stage in the pipeline figure:</p>
<ul>
<li><i>Sketch uses … bytes</i> = program size in <b>flash</b>, the permanent memory that holds the program and survives power-off (the nRF52840 has 1 MB, but part is reserved for the bootloader and the BLE stack, so the Maximum shown is smaller).</li>
<li><i>Global variables use …</i> = static <b>RAM</b>, the working memory (256 KB) that is lost at power-off. "Static" means its size is known at build time: the global variables. The rest of RAM is used for the <b>stack</b> (local variables) and the heap.</li>
</ul>
''') + qa([(T('ถ้า __cplusplus ได้ 201103 จะใช้ if constexpr ได้ไหม?', 'If __cplusplus is 201103, can you use if constexpr?'),
           T('ไม่ได้ if constexpr เป็นของ C++17 ต้องเพิ่ม flag -std=gnu++17 หรือเลี่ยงไปใช้ template overload', 'No. if constexpr is C++17. Add -std=gnu++17 or fall back to template overloads.')),
          (T('"Global variables use" นับ stack ด้วยไหม?', 'Does "Global variables use" include the stack?'),
           T('ไม่นับ นับเฉพาะ .data (global ที่มีค่าเริ่มต้น) + .bss (global ที่เริ่มเป็น 0) ซึ่งรู้ขนาดตอน link ตัวแปร local บน stack ไม่อยู่ในตัวเลขนี้', 'No. It counts only .data (globals with an initial value) + .bss (globals that start at 0), whose sizes are known at link time. Local variables on the stack are not in that number.'))])
   + iv(T('ในงานจริงเมื่อ build มีปัญหา ให้ไล่ตามลำดับ preprocess → compile → link (linker script กำหนด address) → objcopy → flash จะรู้ว่าพังที่ขั้นไหน และเก็บ .elf ไว้เสมอ เพราะมี debug symbol ที่ debugger ต้องใช้ ส่วน .hex/.bin คือ image ที่ลงชิป',
          'When a build breaks, walk the stages in order: preprocess → compile → link (the linker script sets the addresses) → objcopy → flash, and you will see where it failed. Always keep the .elf: it carries the debug symbols the debugger needs, while the .hex/.bin is the image that goes onto the chip.')))
