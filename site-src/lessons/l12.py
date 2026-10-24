lesson('12', 'A', T('Interrupt, volatile และ lambda', 'Interrupts, volatile and lambdas'), 25, BTN, goal(T('เขียน ISR ที่ถูกต้อง และแชร์ข้อมูลระหว่าง ISR กับ loop อย่างปลอดภัย', 'Write a correct ISR, and share data between the ISR and loop safely'))
   + fig(SVG_ISR, T('ISR แทรกกลาง loop ได้ทุกเมื่อ', 'An ISR can cut into loop at any moment')) + '''
<h3>Hands-on</h3>''' + code('''constexpr uint8_t kButtonPin = D1;
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
<p>กดปุ่ม 1 ครั้ง ตัวเลขมักเพิ่มมากกว่า 1 นั่นคือ bounce ที่เห็นในบท 07 ข้อสรุป: ISR บนปุ่มกลไกต้อง debounce ด้วยเวลา (เช่นเช็ก <code class="il">millis()</code> ใน ISR หรือส่ง event ให้ loop จัดการ)</p>
''', '''
<p>Press the button once and the number often goes up by more than 1. That is the bounce from lesson 07. Conclusion: an ISR on a mechanical button still needs time-based debounce (e.g. check <code class="il">millis()</code> in the ISR, or send an event for loop to handle).</p>
''') + qa([(T('volatile ทำให้ pressCount++ เป็น atomic ไหม?', 'Does volatile make pressCount++ atomic?'),
           T('ไม่ volatile แค่บังคับให้อ่าน/เขียน memory จริงทุกครั้ง แต่ ++ คือ load-add-store 3 คำสั่ง ถูกแทรกกลางได้ ต้องใช้ critical section หรือ std::atomic', 'No. volatile only forces a real memory read/write every time, but ++ is load-add-store, three instructions that can be interrupted. Use a critical section or std::atomic.')),
          (T('อะไรห้ามทำใน ISR?', 'What must you never do in an ISR?'),
           T('delay(), Serial.print(), malloc/new, ทำงานนาน และเรียกฟังก์ชันที่ไม่ reentrant ให้ ISR ตั้ง flag หรือ push ลง buffer แล้วกลับเร็วที่สุด', 'delay(), Serial.print(), malloc/new, long work, or calling non-reentrant functions. Let the ISR set a flag or push into a buffer, and return as fast as possible.'))])
   + iv(T('การลืม volatile เป็นสาเหตุอันดับต้น ๆ ของอาการ "build debug ทำงาน แต่ build release พัง" จำ 3 กรณีที่ต้องใช้: ตัวแปรที่ ISR แก้, memory-mapped register, ตัวแปรที่แชร์ระหว่าง thread และจำไว้ว่ามันไม่ใช่ synchronization',
          'A missing volatile is a top cause of "works in debug, breaks in release". Remember the three cases that need it: variables changed by an ISR, memory-mapped registers and variables shared between threads, and remember that it is not synchronization.')))
