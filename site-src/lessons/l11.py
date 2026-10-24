lesson('11', 'A', T('หน่วยความจำใน embedded', 'Memory in embedded systems'), 25, BOARD, goal(T('รู้ว่าตัวแปรแต่ละแบบไปอยู่ส่วนไหน และกฎที่ทีม firmware ใช้จริง', 'Know where each kind of variable lives, and the rules real firmware teams follow'))
   + fig(SVG_MEM, T('memory map แบบย่อของ nRF52840 (ตัวเลขประมาณ ขึ้นกับ SoftDevice และ bootloader)', 'Simplified nRF52840 memory map (approximate; depends on the SoftDevice and bootloader)')) + '''
<h3>Hands-on</h3>''' + code('''uint8_t bigStatic[8192];        // .bss  → นับใน "Global variables use"
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
<p>ดูว่า address ขึ้นต้น 0x000… (flash) หรือ 0x2000… (RAM) ตามรูปไหม จากนั้นเปลี่ยน <code class="il">bigStatic</code> เป็น 32768 แล้วดูตัวเลข RAM ตอน compile เปลี่ยน</p>
<h3>กฎที่ใช้ในทีมจริง</h3>
<ul>
<li>จอง memory ตอน init เท่านั้น หลังจากนั้นห้าม <code class="il">new</code>/<code class="il">malloc</code> ใน loop เพราะ heap fragment แล้วพังหลังรันหลายวัน</li>
<li>เลี่ยง <code class="il">String</code> ของ Arduino ใช้ <code class="il">char buf[32]</code> + <code class="il">snprintf</code> แทน</li>
<li>ใช้ <code class="il">std::array</code> / buffer ขนาดคงที่ หลีกเลี่ยง <code class="il">std::vector</code>, <code class="il">std::function</code> ที่อาจจอง heap เอง</li>
<li>embedded มักปิด exceptions และ RTTI (<code class="il">-fno-exceptions -fno-rtti</code>) จึงจัดการ error ด้วยค่าที่ return</li>
</ul>
''', '''
<p>Check that the addresses start with 0x000… (flash) or 0x2000… (RAM) as in the diagram. Then change <code class="il">bigStatic</code> to 32768 and watch the RAM figure change at compile time.</p>
<h3>Rules real teams use</h3>
<ul>
<li>Allocate memory at init only. Never <code class="il">new</code>/<code class="il">malloc</code> in the loop afterwards: the heap fragments and the device fails after days of running.</li>
<li>Avoid Arduino's <code class="il">String</code>; use <code class="il">char buf[32]</code> + <code class="il">snprintf</code> instead.</li>
<li>Use <code class="il">std::array</code> / fixed-size buffers, and avoid <code class="il">std::vector</code> and <code class="il">std::function</code>, which may allocate on the heap.</li>
<li>Embedded builds often disable exceptions and RTTI (<code class="il">-fno-exceptions -fno-rtti</code>), so errors are handled with return values.</li>
</ul>
''') + qa([(T('ตัวแปร static ภายในฟังก์ชันอยู่ส่วนไหน?', 'Where does a static variable inside a function live?'),
           T('.data หรือ .bss เหมือน global แต่ scope จำกัดในฟังก์ชัน จึงคงค่าระหว่างการเรียก', 'In .data or .bss like a global, but its scope is limited to the function, so it keeps its value between calls.')),
          (T('stack overflow บน MCU ไม่มี OS แสดงอาการอย่างไร?', 'What does a stack overflow look like on an MCU without an OS?'),
           T('stack โตลงไปทับ heap หรือ .bss ทำให้ค่าตัวแปรเพี้ยนแบบสุ่มหรือ HardFault วิธีตรวจคือ stack painting (เติม pattern แล้วดูว่าถูกเขียนลึกแค่ไหน) หรือเปิด MPU guard', 'The stack grows down into the heap or .bss, causing random variable corruption or a HardFault. Detect it with stack painting (fill a pattern and see how deep it gets overwritten) or an MPU guard region.'))])
   + iv(T('ใช้ memory map นี้ทุกครั้งที่เจอ HardFault หรือ RAM ไม่พอ: ดูว่า address ที่พังอยู่ใน .text / .data / .bss / heap / stack ส่วนไหน และเปิดไฟล์ .map จาก linker ดูว่าอะไรกินที่มากที่สุด',
          'Reach for this memory map whenever you hit a HardFault or run out of RAM: find which of .text / .data / .bss / heap / stack the faulting address falls in, and open the linker .map file to see what uses the most space.')))
