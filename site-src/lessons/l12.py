lesson('12', 'A', T('Interrupt, volatile และ lambda', 'Interrupts, volatile and lambdas'), 30, BTN, goal(T('เขียน ISR ที่ถูกต้อง และแชร์ข้อมูลระหว่าง ISR กับ loop อย่างปลอดภัย', 'Write a correct ISR, and share data between the ISR and loop safely')) + T('''
<p>บท 07 อ่านปุ่มด้วยการเช็กใน <code class="il">loop()</code> ทุกรอบ (เรียกว่า polling) ถ้า loop ติด <code class="il">delay()</code> อยู่ อาจพลาดการกดสั้น ๆ อีกวิธีคือให้ฮาร์ดแวร์เรียกโค้ดเราเองทันทีที่ขาเปลี่ยน คำศัพท์ในบทนี้:</p>
<ul>
<li><b>ISR</b> (Interrupt Service Routine) ฟังก์ชันที่ CPU กระโดดไปทำทันทีเมื่อเกิด interrupt (บท 06) ทำเสร็จแล้วกลับมาทำงานเดิมต่อตรงจุดที่ค้างไว้ ตามรูป</li>
<li><b>FALLING</b> จังหวะที่ขาเปลี่ยนจาก HIGH เป็น LOW คือตอนเริ่มกดปุ่ม เพราะต่อแบบ INPUT_PULLUP (บท 07)</li>
<li><b>volatile</b> ปกติ compiler อาจเก็บค่าตัวแปรไว้ใน register ของ CPU แล้วไม่อ่านจาก RAM ซ้ำ ถ้า ISR แก้ค่าใน RAM loop อาจไม่เห็น <code class="il">volatile</code> บังคับให้อ่านและเขียน RAM จริงทุกครั้ง</li>
<li><b>atomic</b> การทำงานที่ไม่มีทางถูกแทรกกลาง <code class="il">noInterrupts()</code> / <code class="il">interrupts()</code> ปิดและเปิด interrupt เพื่อให้โค้ดช่วงนั้นเป็น atomic (เหมือน <code class="il">CriticalSection</code> บท 06)</li>
<li><b>lambda</b> ฟังก์ชันไม่มีชื่อที่เขียนไว้ตรงที่ใช้ รูปแบบ <code class="il">[] { … }</code> โดย <code class="il">[]</code> ว่างหมายถึงไม่ดึงตัวแปร local ข้างนอกเข้าไปใช้ lambda แบบนี้ส่งเป็น function pointer ให้ <code class="il">attachInterrupt</code> ได้</li>
</ul>
''', '''
<p>Lesson 07 read the button by checking it in every <code class="il">loop()</code> pass (polling). If loop is stuck in <code class="il">delay()</code>, a short press can be missed. The alternative is to let the hardware call your code the moment the pin changes. Terms in this lesson:</p>
<ul>
<li><b>ISR</b> (Interrupt Service Routine): the function the CPU jumps to as soon as an interrupt (lesson 06) happens. When it finishes, the CPU resumes exactly where it left off, as in the figure.</li>
<li><b>FALLING</b>: the moment a pin goes from HIGH to LOW, i.e. when the button starts being pressed, because it is wired with INPUT_PULLUP (lesson 07).</li>
<li><b>volatile</b>: normally the compiler may keep a variable in a CPU register and not re-read RAM. If an ISR changes the value in RAM, loop may never see it. <code class="il">volatile</code> forces a real RAM read and write every time.</li>
<li><b>atomic</b>: an operation that cannot be cut in the middle. <code class="il">noInterrupts()</code> / <code class="il">interrupts()</code> turn interrupts off and on so the code between them is atomic (like <code class="il">CriticalSection</code>, lesson 06).</li>
<li><b>lambda</b>: an unnamed function written right where it is used, in the form <code class="il">[] { … }</code>. The empty <code class="il">[]</code> means it uses no local variables from outside, so it can be passed to <code class="il">attachInterrupt</code> as a function pointer.</li>
</ul>
''')
   + fig(SVG_ISR, T('ISR แทรกกลาง loop ได้ทุกเมื่อ', 'An ISR can cut into loop at any moment')) + '''
<h3>Hands-on</h3>''' + T('''
<p>sketch นี้พิสูจน์ว่า ISR ทำงานแทรกเข้ามาเองแม้ <code class="il">loop()</code> กำลังหยุดรอใน <code class="il">delay(500)</code> และแสดงว่าทำไม ISR บนปุ่มยังต้อง debounce ใช้วงจรปุ่มที่ D1 จากบท 07</p>
<ol>
<li>สร้าง sketch ใหม่ วางโค้ดข้างล่าง บันทึกชื่อ <code class="il">isr_count</code> แล้วกด <b>Upload</b></li>
<li>เปิด <b>Tools → Serial Monitor</b> ที่ 115200 baud จะเห็นตัวเลขขึ้นทุกครึ่งวินาที</li>
<li>กดปุ่มทีละครั้ง แล้วลองกดรัว ๆ 3 ครั้งภายในครึ่งวินาที</li>
</ol>
''', '''
<p>This sketch proves that the ISR cuts in by itself even while <code class="il">loop()</code> is waiting in <code class="il">delay(500)</code>, and shows why an ISR on a button still needs debouncing. It uses the button on D1 from lesson 07.</p>
<ol>
<li>Create a new sketch, paste the code below, save it as <code class="il">isr_count</code>, and press <b>Upload</b>.</li>
<li>Open <b>Tools → Serial Monitor</b> at 115200 baud. A number appears every half second.</li>
<li>Press the button once at a time, then try 3 quick presses within half a second.</li>
</ol>
''') + code('''constexpr uint8_t kButtonPin = D1;
volatile uint32_t pressCount = 0;   // volatile: ค่าเปลี่ยนนอก flow ปกติ ห้าม cache

void setup() {
  Serial.begin(115200);
  pinMode(kButtonPin, INPUT_PULLUP);
  // lambda ที่ไม่ capture อะไร แปลงเป็น function pointer ได้
  attachInterrupt(digitalPinToInterrupt(kButtonPin), [] {
    pressCount = pressCount + 1;
  }, FALLING);
}

void loop() {
  uint32_t count;
  noInterrupts();          // copy ออกมาแบบ atomic
  count = pressCount;
  interrupts();
  Serial.println(count);
  delay(500);
}''', 'isr_count.ino', en={'// volatile: ค่าเปลี่ยนนอก flow ปกติ ห้าม cache': '// volatile: changes outside normal flow, never cache',
                          '// lambda ที่ไม่ capture อะไร แปลงเป็น function pointer ได้': '// a capture-less lambda converts to a function pointer',
                          '// copy ออกมาแบบ atomic': '// copy it out atomically'}) + T('''
<p><code class="il">attachInterrupt(ขา, ฟังก์ชัน, จังหวะ)</code> สั่งให้เรียกฟังก์ชันนั้นเมื่อขาเปลี่ยนตามจังหวะที่กำหนด ส่วน <code class="il">digitalPinToInterrupt()</code> แปลงเลขขาเป็นเลข interrupt ที่ core ใช้</p>
<p>ผลนี้บอกอะไร:</p>
<ul>
<li><b>ISR แทรกได้ทุกเมื่อ</b> กดรัว 3 ครั้งในครึ่งวินาที ตัวเลขเพิ่มอย่างน้อย 3 ทั้งที่ช่วงนั้น <code class="il">loop()</code> หยุดอยู่ใน <code class="il">delay()</code> ตลอด ถ้าใช้ polling แบบบท 07 คู่กับ <code class="il">delay(500)</code> จะพลาดการกดส่วนใหญ่</li>
<li><b>ยังต้อง debounce</b> กด 1 ครั้งตัวเลขมักเพิ่มมากกว่า 1 นั่นคือ bounce ที่เห็นในบท 07 เพราะหน้าสัมผัสเด้งทำให้เกิด FALLING หลายครั้ง ISR บนปุ่มกลไกจึงต้อง debounce ด้วยเวลา เช่นเช็ก <code class="il">millis()</code> ใน ISR หรือให้ ISR แค่บอก loop แล้วให้ <code class="il">Debouncer</code> จัดการ</li>
</ul>
<p class="note">บน Cortex-M การอ่านตัวแปร 32 bit ครั้งเดียวไม่ถูกแทรกกลางอยู่แล้ว แต่ถ้าต้องอ่านหลายตัวแปรพร้อมกัน หรือแก้ค่าแบบ <code class="il">++</code> ต้องครอบด้วย <code class="il">noInterrupts()</code> เสมอ ตัวอย่างนี้ครอบไว้ให้เป็นนิสัย</p>
''', '''
<p><code class="il">attachInterrupt(pin, function, mode)</code> calls the function whenever the pin changes in the given way. <code class="il">digitalPinToInterrupt()</code> turns a pin number into the interrupt number the core uses.</p>
<p>What the result tells you:</p>
<ul>
<li><b>The ISR cuts in at any moment</b>: press 3 times within half a second and the number rises by at least 3, even though <code class="il">loop()</code> sat in <code class="il">delay()</code> the whole time. Polling as in lesson 07 combined with <code class="il">delay(500)</code> would miss most of those presses.</li>
<li><b>Debouncing is still needed</b>: one press often adds more than 1. That is the bounce from lesson 07: the bouncing contacts produce several FALLING edges. An ISR on a mechanical button therefore needs time-based debouncing, e.g. checking <code class="il">millis()</code> in the ISR, or letting the ISR only notify loop and leaving the rest to <code class="il">Debouncer</code>.</li>
</ul>
<p class="note">On a Cortex-M, a single read of a 32-bit variable cannot be cut in the middle anyway. But when you read several variables together, or modify a value with <code class="il">++</code>, always wrap it in <code class="il">noInterrupts()</code>. The example wraps it to build the habit.</p>
''') + qa([(T('volatile ทำให้ pressCount++ ปลอดภัยจากการถูกแทรกไหม?', 'Does volatile make pressCount++ safe from being interrupted?'),
           T('ไม่ volatile แค่บังคับให้อ่าน/เขียน RAM จริงทุกครั้ง แต่ ++ คือ 3 คำสั่ง (อ่าน, บวก, เขียนกลับ) ISR อาจแทรกระหว่างนั้นได้ ต้องครอบด้วย noInterrupts() หรือ CriticalSection หรือใช้ std::atomic', 'No. volatile only forces a real RAM read/write every time, but ++ is three instructions (read, add, write back), and an ISR can cut in between them. Wrap it with noInterrupts() or a CriticalSection, or use std::atomic.')),
          (T('อะไรห้ามทำใน ISR?', 'What must you never do in an ISR?'),
           T('delay(), Serial.print(), malloc/new และงานที่ใช้เวลานาน รวมถึงฟังก์ชันที่จะพังถ้าถูกเรียกซ้อนกัน (เช่น ฟังก์ชันที่ loop กำลังเรียกอยู่ตอน ISR แทรกเข้ามา) ให้ ISR แค่ตั้ง flag หรือ push ลง buffer แล้วกลับเร็วที่สุด', 'delay(), Serial.print(), malloc/new, long work, or functions that break when called while already running (e.g. one that loop was in the middle of when the ISR cut in). Let the ISR set a flag or push into a buffer, and return as fast as possible.'))])
   + iv(T('ลืม volatile มักทำให้โปรแกรมทำงานได้ตอนที่ compiler แทบไม่ optimize แต่พังเมื่อ optimize มากขึ้น (core นี้ใช้ -Ofast ดูได้ใน verbose output บท 01) จำ 3 กรณีที่ต้องใช้: ตัวแปรที่ ISR แก้, register ของฮาร์ดแวร์ที่อ่านผ่าน address และตัวแปรที่แชร์ระหว่าง task และจำไว้ว่า volatile ไม่ได้กันการถูกแทรกกลาง',
          'A missing volatile often works while the compiler barely optimizes, then breaks as optimization increases (this core uses -Ofast; see the verbose output, lesson 01). Remember the three cases that need it: variables changed by an ISR, hardware registers read through an address, and variables shared between tasks. And remember that volatile does not stop code being cut in the middle.')))
