lesson('11', 'A', T('หน่วยความจำใน embedded', 'Memory in embedded systems'), 30, BOARD, goal(T('รู้ว่าตัวแปรแต่ละแบบไปอยู่ส่วนไหน และกฎที่ทีม firmware ใช้จริง', 'Know where each kind of variable lives, and the rules real firmware teams follow')) + T('''
<p>บท 01 เห็นตัวเลข flash กับ RAM ตอน build แล้ว บทนี้ดูว่าข้างในแบ่งเป็นส่วนอะไรบ้าง linker วางแต่ละส่วนไว้ที่ address ตาม linker script ภาพรวมนี้เรียกว่า <b>memory map</b>:</p>
<ul>
<li><b>.text</b> โค้ดของโปรแกรม และ <b>.rodata</b> ค่าคงที่ (<code class="il">const</code>) อยู่ใน flash</li>
<li><b>.data</b> ตัวแปร global ที่มีค่าเริ่มต้น อยู่ใน RAM แต่ค่าเริ่มต้นเก็บใน flash แล้ว startup code copy มาให้ก่อน <code class="il">setup()</code> (ลูกศรส้มในรูป)</li>
<li><b>.bss</b> ตัวแปร global ที่เริ่มเป็น 0 อยู่ใน RAM startup code เคลียร์เป็น 0 ให้</li>
<li><b>heap</b> RAM ที่จองตอนรันด้วย <code class="il">new</code> / <code class="il">malloc</code> (บท 10)</li>
<li><b>stack</b> RAM ของตัวแปร local พารามิเตอร์ และ address ที่ต้องกลับเมื่อฟังก์ชันจบ ใช้แล้วคืนทันทีที่ฟังก์ชันจบ</li>
</ul>
''', '''
<p>Lesson 01 showed the flash and RAM numbers at build time. This lesson looks at the sections inside them. The linker places each section at an address from the linker script; that layout is the <b>memory map</b>:</p>
<ul>
<li><b>.text</b> (program code) and <b>.rodata</b> (<code class="il">const</code> data) live in flash.</li>
<li><b>.data</b>: globals with an initial value. They live in RAM, but the initial values are stored in flash and the startup code copies them over before <code class="il">setup()</code> (the orange arrow in the figure).</li>
<li><b>.bss</b>: globals that start at 0, in RAM. The startup code clears them.</li>
<li><b>heap</b>: RAM reserved at runtime with <code class="il">new</code> / <code class="il">malloc</code> (lesson 10).</li>
<li><b>stack</b>: RAM for local variables, parameters and return addresses, given back as soon as a function returns.</li>
</ul>
''')
   + fig(SVG_MEM, T('memory map แบบย่อของ nRF52840 (ตัวเลขประมาณ ขึ้นกับ SoftDevice และ bootloader)', 'Simplified nRF52840 memory map (approximate; depends on the SoftDevice and bootloader)')) + '''
<h3>Hands-on</h3>''' + T('''
<p>sketch นี้พิสูจน์ว่าตัวแปรแต่ละแบบไปอยู่คนละส่วนตามรูปจริง โดยพิมพ์ address ของมันออกมา</p>
<ol>
<li>สร้าง sketch ใหม่ วางโค้ดข้างล่าง บันทึกชื่อ <code class="il">memmap</code> กด <b>Upload</b> แล้วจดตัวเลข <i>Global variables use</i> ไว้</li>
<li>เปิด <b>Tools → Serial Monitor</b> ที่ 115200 baud ถ้าไม่มีข้อความ กด reset บนบอร์ด 1 ครั้ง</li>
</ol>
''', '''
<p>This sketch proves that each kind of variable lands in a different section, as in the figure, by printing their addresses.</p>
<ol>
<li>Create a new sketch, paste the code below, save it as <code class="il">memmap</code>, press <b>Upload</b>, and note the <i>Global variables use</i> number.</li>
<li>Open <b>Tools → Serial Monitor</b> at 115200 baud. If nothing appears, press reset on the board once.</li>
</ol>
''') + code('''uint8_t bigStatic[8192];        // .bss  → นับใน "Global variables use"
const char kMsg[] = "hello";    // .rodata → อยู่ใน flash

void setup() {
  Serial.begin(115200);
  while (!Serial) {}
  uint8_t onStack[256];         // stack → ไม่อยู่ในตัวเลขตอน compile
  onStack[0] = 1;
  bigStatic[0] = onStack[0];
  Serial.print("flash  : 0x"); Serial.println((uintptr_t)kMsg, HEX);
  Serial.print("static : 0x"); Serial.println((uintptr_t)bigStatic, HEX);
  Serial.print("stack  : 0x"); Serial.println((uintptr_t)onStack, HEX);
}

void loop() {}''', 'memmap.ino', en={'// .bss  → นับใน "Global variables use"': '// .bss  → counted in "Global variables use"',
                                     '// .rodata → อยู่ใน flash': '// .rodata → lives in flash',
                                     '// stack → ไม่อยู่ในตัวเลขตอน compile': '// stack → not in the compile-time numbers'}) + T('''
<p><code class="il">(uintptr_t)</code> แปลง pointer เป็นตัวเลขขนาดเท่า address เพื่อพิมพ์เป็นเลขฐาน 16 (<code class="il">HEX</code>) ผลที่ควรเห็นประมาณนี้ (ตัวเลขอาจต่างไปเล็กน้อยตามเวอร์ชันของ core):</p>
''', '''
<p><code class="il">(uintptr_t)</code> turns a pointer into an address-sized number so it can be printed in hex (<code class="il">HEX</code>). Expected output, roughly (the numbers may differ slightly with the core version):</p>
''') + code('''flash  : 0x30BCC
static : 0x2000630C
stack  : 0x2000…''', 'Serial Monitor') + T('''
<p>ผลนี้บอกอะไร:</p>
<ul>
<li><b>flash กับ RAM แยกกันด้วย address</b> <code class="il">kMsg</code> = 0x30BCC (เต็ม ๆ คือ 0x0003_0BCC เพราะ <code class="il">HEX</code> ไม่พิมพ์เลข 0 นำหน้า) อยู่ในช่วงของ flash ที่เริ่มจาก 0x0000_0000 ตามรูป ส่วน <code class="il">bigStatic</code> และ <code class="il">onStack</code> ขึ้นต้นด้วย 0x2000… คืออยู่ใน RAM</li>
<li><b>global นับตอน build, local ไม่นับ</b> เปลี่ยน <code class="il">8192</code> เป็น <code class="il">32768</code> แล้วกด Verify <i>Global variables use</i> จะเพิ่ม 24576 byte พอดี ถ้าเพิ่มขนาด <code class="il">onStack</code> แทน ตัวเลขนี้จะไม่เปลี่ยน (ตรงกับคำถามเรื่อง stack ในบท 01)</li>
<li><b>stack ของ <code class="il">loop()</code> บนบอร์ดนี้</b> address ของ <code class="il">onStack</code> อยู่สูงกว่า <code class="il">bigStatic</code> แต่ไม่ได้อยู่ปลาย RAM เพราะ core nRF52 รัน <code class="il">setup()</code>/<code class="il">loop()</code> ใน task ของ FreeRTOS (บท 01) ซึ่ง stack ของ task ถูกจองจาก heap ขนาดเพียง 4 KB (<code class="il">LOOP_STACK_SZ</code> ใน <code class="il">main.cpp</code> ของ core) แม้ build จะบอกว่าเหลือ RAM กว่า 200 KB ก็ห้ามประกาศ array local ขนาดหลาย KB ใน <code class="il">loop()</code></li>
</ul>
''', '''
<p>What the output tells you:</p>
<ul>
<li><b>Flash and RAM are told apart by address</b>: <code class="il">kMsg</code> = 0x30BCC (0x0003_0BCC in full; <code class="il">HEX</code> drops leading zeros), inside flash, which starts at 0x0000_0000 as in the figure. <code class="il">bigStatic</code> and <code class="il">onStack</code> start with 0x2000…, so they are in RAM.</li>
<li><b>Globals are counted at build time, locals are not</b>: change <code class="il">8192</code> to <code class="il">32768</code> and press Verify. <i>Global variables use</i> grows by exactly 24576 bytes. Make <code class="il">onStack</code> bigger instead and the number does not change (the stack question from lesson 01).</li>
<li><b>The stack of <code class="il">loop()</code> on this board</b>: <code class="il">onStack</code> sits above <code class="il">bigStatic</code> but not at the top of RAM, because the nRF52 core runs <code class="il">setup()</code>/<code class="il">loop()</code> in a FreeRTOS task (lesson 01), and a task's stack is taken from the heap, only 4 KB here (<code class="il">LOOP_STACK_SZ</code> in the core's <code class="il">main.cpp</code>). Even though the build says over 200 KB of RAM is left, never declare local arrays of several KB in <code class="il">loop()</code>.</li>
</ul>
''') + T('''
<h3>กฎที่ใช้ในทีมจริง</h3>
<ul>
<li>จอง memory ตอนเริ่มต้นเท่านั้น หลังจากนั้นห้าม <code class="il">new</code>/<code class="il">malloc</code> ใน loop เพราะ heap จะเป็นรูพรุน (fragmentation: ที่ว่างรวมยังพอ แต่แตกเป็นชิ้นเล็กจนจองก้อนใหญ่ไม่ได้) แล้วพังหลังรันไปหลายวัน</li>
<li>เลี่ยง <code class="il">String</code> ของ Arduino ซึ่งจอง heap ทุกครั้งที่ต่อข้อความ ใช้ <code class="il">char buf[32]</code> + <code class="il">snprintf</code> แทน</li>
<li>ใช้ <code class="il">std::array</code> หรือ buffer ขนาดคงที่ หลีกเลี่ยง <code class="il">std::vector</code>, <code class="il">std::function</code> ที่อาจจอง heap เอง</li>
<li>embedded มักปิด exceptions (<code class="il">try</code>/<code class="il">catch</code>) และ RTTI (ข้อมูลชนิดตอนรัน) เพื่อประหยัด flash จึงจัดการ error ด้วยค่าที่ return ดูได้จาก flag <code class="il">-fno-exceptions -fno-rtti</code> ในคำสั่ง compile แบบ verbose (บท 01)</li>
</ul>
''', '''
<h3>Rules real teams use</h3>
<ul>
<li>Allocate memory at startup only. Never <code class="il">new</code>/<code class="il">malloc</code> in the loop afterwards: the heap fragments (enough free space in total, but in pieces too small for a large request) and the device fails after days of running.</li>
<li>Avoid Arduino's <code class="il">String</code>, which allocates on the heap every time you append; use <code class="il">char buf[32]</code> + <code class="il">snprintf</code> instead.</li>
<li>Use <code class="il">std::array</code> or fixed-size buffers, and avoid <code class="il">std::vector</code> and <code class="il">std::function</code>, which may allocate on the heap.</li>
<li>Embedded builds often disable exceptions (<code class="il">try</code>/<code class="il">catch</code>) and RTTI (type information at runtime) to save flash, so errors are handled with return values. You can see the <code class="il">-fno-exceptions -fno-rtti</code> flags in the verbose compile command (lesson 01).</li>
</ul>
''') + qa([(T('ตัวแปร static ภายในฟังก์ชันอยู่ส่วนไหน?', 'Where does a static variable inside a function live?'),
           T('.data หรือ .bss เหมือน global แต่ใช้ชื่อได้แค่ในฟังก์ชันนั้น จึงคงค่าไว้ระหว่างการเรียกแต่ละครั้ง', 'In .data or .bss like a global, but its name is only usable inside that function, so it keeps its value between calls.')),
          (T('stack overflow บน MCU ที่ไม่มี OS แสดงอาการอย่างไร?', 'What does a stack overflow look like on an MCU without an OS?'),
           T('stack โตจนทับข้อมูลส่วนอื่น ค่าตัวแปรเพี้ยนแบบสุ่ม หรือ CPU หยุดด้วย HardFault (error ร้ายแรงของ Cortex-M ที่ทำให้บอร์ดค้างหรือ reset) วิธีตรวจคือเติมค่าที่รู้จักลงใน stack ตอนเริ่ม แล้วดูภายหลังว่าถูกเขียนทับลึกแค่ไหน', 'The stack grows over other data: variables change at random, or the CPU stops with a HardFault (a fatal Cortex-M error that hangs or resets the board). To detect it, fill the stack with a known value at startup and later check how deep it has been overwritten.'))])
   + iv(T('ใช้ memory map นี้ทุกครั้งที่เจอ HardFault หรือ RAM ไม่พอ: ดูว่า address ที่พังอยู่ใน .text / .data / .bss / heap / stack ส่วนไหน และเปิดไฟล์ .map ที่ linker สร้าง (อยู่ในโฟลเดอร์ build เดียวกับ .elf) ดูว่าอะไรกินที่มากที่สุด',
          'Reach for this memory map whenever you hit a HardFault or run out of RAM: find which of .text / .data / .bss / heap / stack the faulting address falls in, and open the .map file the linker writes (in the same build folder as the .elf) to see what uses the most space.')))
