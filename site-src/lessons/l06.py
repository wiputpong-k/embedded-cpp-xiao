lesson('06', 'A', T('RAII และ destructor', 'RAII and destructors'), 30, T('Pot 10 kΩ ที่ A0', '10 kΩ pot on A0'), goal(T('ใช้ scope ควบคุม resource อัตโนมัติ: จับเวลา, ปิด/เปิด interrupt', 'Let scope manage resources automatically: timing, disabling/enabling interrupts')) + T('''
<p>ใน C ถ้าปิด interrupt ไว้แล้ว <code class="il">return</code> กลางฟังก์ชันโดยลืมเปิดคืน ระบบจะค้างแบบหาสาเหตุยาก C++ แก้ปัญหานี้ด้วยการผูก "การคืน" ไว้กับการออกจาก <code class="il">{ }</code> คำศัพท์ที่ใช้ในบทนี้:</p>
<ul>
<li><b>resource</b> สิ่งที่ยืมแล้วต้องคืน เช่น สถานะ "ปิด interrupt", lock หรือ buffer ที่จองไว้</li>
<li><b>interrupt</b> สัญญาณที่ทำให้ CPU หยุดงานที่ทำอยู่ชั่วคราวไปทำงานเร่งด่วน เช่น เมื่อมีข้อมูล USB เข้ามา (บท 12 ลงรายละเอียด) บางช่วงต้องปิดไว้สั้น ๆ เพื่อไม่ให้ถูกแทรกกลาง เรียกช่วงนั้นว่า <b>critical section</b></li>
<li><b>destructor</b> ฟังก์ชัน <code class="il">~ชื่อclass()</code> ที่ทำงานอัตโนมัติเมื่อ object หมดอายุ object local หมดอายุตอนออกจาก <code class="il">{ }</code> ที่ประกาศมัน (scope ในบท 02)</li>
</ul>
<p><b>RAII</b> (Resource Acquisition Is Initialization): ขอ resource ใน constructor คืนใน destructor แล้ว compiler จะเรียก destructor ให้เมื่อออกจาก scope เสมอ จึงไม่มีทางลืม <code class="il">unlock</code> หรือเปิด interrupt คืน แม้จะ <code class="il">return</code> กลางทาง C ไม่มีกลไกนี้</p>
''', '''
<p>In C, if you disable interrupts and then <code class="il">return</code> from the middle of a function without re-enabling them, the system hangs in a way that is hard to trace. C++ solves this by tying the "give back" step to leaving a <code class="il">{ }</code> block. Terms used in this lesson:</p>
<ul>
<li><b>resource</b>: something you borrow and must give back, e.g. the "interrupts disabled" state, a lock, or a reserved buffer.</li>
<li><b>interrupt</b>: a signal that makes the CPU pause its current work to handle something urgent, e.g. USB data arriving (lesson 12 goes deeper). Sometimes they must be turned off briefly so code is not cut in the middle; that stretch is a <b>critical section</b>.</li>
<li><b>destructor</b>: the function <code class="il">~ClassName()</code> that runs automatically when an object ends its life. A local object ends when execution leaves the <code class="il">{ }</code> that declared it (scope, lesson 02).</li>
</ul>
<p><b>RAII</b> (Resource Acquisition Is Initialization): acquire the resource in the constructor and release it in the destructor. The compiler always calls the destructor when the object leaves scope, so you can never forget <code class="il">unlock</code> or re-enabling interrupts, even if you <code class="il">return</code> early. C has no such mechanism.</p>
''') + fig(SVG_RAII, T('อายุของ object ผูกกับวงเล็บปีกกา', "The object's lifetime is tied to the braces")) + T('''
<h3>ต่อวงจร</h3>
<p><b>potentiometer</b> (pot) คือตัวต้านทานปรับค่าได้ มี 3 ขา ขาสองข้างต่อกับปลายทั้งสองของตัวต้านทาน ส่วนขากลาง (wiper) เลื่อนไปตามการหมุน แรงดันที่ขากลางจึงเปลี่ยนได้ตั้งแต่ 0 ถึง 3.3 V</p>
<ol>
<li>ถอดสาย USB ออกก่อน (LED จากบท 04 ต่อทิ้งไว้ได้)</li>
<li>เสียบ pot ลง breadboard ให้ 3 ขาอยู่คนละแถว</li>
<li>ต่อขาข้างหนึ่งไปที่ขา 3V3 ของบอร์ด และขาข้างที่เหลือไปที่ GND (สลับกันได้ แค่ทิศการหมุนกลับด้าน)</li>
<li>ต่อขากลางไปที่ขา A0 (ขาเดียวกับ D0)</li>
</ol>
<p class="note">ใช้ขา 3V3 เท่านั้น ห้ามต่อ 5V เพราะขาของ nRF52840 รับแรงดันได้ไม่เกิน 3.3 V</p>
''', '''
<h3>Wire it up</h3>
<p>A <b>potentiometer</b> (pot) is an adjustable resistor with 3 legs. The outer legs connect to the two ends of the resistor; the middle leg (wiper) slides along it as you turn the knob, so the voltage on the middle leg can go from 0 to 3.3 V.</p>
<ol>
<li>Unplug the USB cable first (the LED from lesson 04 can stay).</li>
<li>Press the pot into the breadboard with its 3 legs in different rows.</li>
<li>Connect one outer leg to the board's 3V3 pin and the other outer leg to GND (either way round; it only flips the turning direction).</li>
<li>Connect the middle leg to pin A0 (the same pin as D0).</li>
</ol>
<p class="note">Use 3V3 only, never 5V: the nRF52840's pins accept at most 3.3 V.</p>
''') + fig(SVG_POT, T('ขาข้างของ pot ต่อ 3V3 และ GND ขากลางต่อ A0', 'Pot outer legs to 3V3 and GND, middle leg to A0')) + '''
<h3>Hands-on</h3>''' + T('''
<p>sketch นี้พิสูจน์ว่า destructor ทำงานเองเมื่อออกจาก <code class="il">{ }</code>: <code class="il">ScopedTimer</code> พิมพ์เวลาโดยไม่มีใครสั่งพิมพ์ และ <code class="il">CriticalSection</code> เปิด interrupt คืนให้เองโดยไม่มีบรรทัดเปิดคืน</p>
<ol>
<li>เสียบ USB กลับ สร้าง sketch ใหม่ วางโค้ดข้างล่าง บันทึกชื่อ <code class="il">raii</code> แล้วกด <b>Upload</b></li>
<li>เปิด <b>Tools → Serial Monitor</b> ที่ 115200 baud แล้วลองหมุน pot</li>
</ol>
''', '''
<p>This sketch proves that destructors run by themselves when execution leaves a <code class="il">{ }</code>: <code class="il">ScopedTimer</code> prints the time though nobody calls print, and <code class="il">CriticalSection</code> re-enables interrupts though no line does it.</p>
<ol>
<li>Plug USB back in, create a new sketch, paste the code below, save it as <code class="il">raii</code>, and press <b>Upload</b>.</li>
<li>Open <b>Tools → Serial Monitor</b> at 115200 baud and turn the pot.</li>
</ol>
''') + code('''class ScopedTimer {
public:
  explicit ScopedTimer(const char* label) : label_(label), start_(micros()) {}
  ~ScopedTimer() {
    uint32_t us = micros() - start_;
    Serial.print(label_); Serial.print(": "); Serial.print(us); Serial.println(" us");
  }
  ScopedTimer(const ScopedTimer&) = delete;             // ห้าม copy
  ScopedTimer& operator=(const ScopedTimer&) = delete;
private:
  const char* label_;
  uint32_t start_;
};

// ปิด interrupt แบบซ้อนได้: เก็บสถานะเดิมแล้วคืนค่าเดิม
class CriticalSection {
public:
  CriticalSection() : primask_(__get_PRIMASK()) { __disable_irq(); }
  ~CriticalSection() { __set_PRIMASK(primask_); }
private:
  uint32_t primask_;
};

void setup() { Serial.begin(115200); }

void loop() {
  long sum = 0;
  {
    ScopedTimer t("analogRead x100");
    for (int i = 0; i < 100; ++i) sum += analogRead(A0);
  }                                   // destructor ทำงานตรงนี้
  Serial.print("avg = "); Serial.println(sum / 100);

  uint32_t inside;
  {
    CriticalSection cs;               // ปิด interrupt
    inside = __get_PRIMASK();         // 1 = ปิดอยู่
  }                                   // destructor เปิดคืน
  Serial.print("PRIMASK inside = "); Serial.print(inside);
  Serial.print(", after = ");        Serial.println(__get_PRIMASK());
  delay(1000);
}''', 'raii.ino', en={'// ห้าม copy': '// no copying', '// ปิด interrupt แบบซ้อนได้: เก็บสถานะเดิมแล้วคืนค่าเดิม': '// Nestable interrupt disable: save the previous state, then restore it',
                     '// destructor ทำงานตรงนี้': '// destructor runs here', '// ปิด interrupt': '// interrupts off', '// 1 = ปิดอยู่': '// 1 = disabled',
                     '// destructor เปิดคืน': '// destructor turns them back on'}) + T('''
<ul>
<li><code class="il">micros()</code> เวลาตั้งแต่บอร์ดเริ่มทำงาน หน่วยไมโครวินาที</li>
<li><code class="il">explicit</code> ห้าม compiler แปลงข้อความเป็น <code class="il">ScopedTimer</code> ให้เองโดยไม่ได้ตั้งใจ ส่วน <code class="il">= delete</code> ห้ามใช้ฟังก์ชันนั้น (ที่นี่คือห้าม copy ดูคำถามข้อแรก)</li>
<li><b>PRIMASK</b> register ใน CPU Cortex-M: 1 = ปิด interrupt, 0 = เปิด <code class="il">__disable_irq()</code> ตั้งเป็น 1 ส่วน <code class="il">__get_PRIMASK()</code> / <code class="il">__set_PRIMASK()</code> อ่านและเขียนค่านี้</li>
</ul>
<p>ผลที่ควรเห็น ทุก 1 วินาที (ตัวเลข us และ avg ของคุณจะต่างออกไป):</p>
''', '''
<ul>
<li><code class="il">micros()</code>: time since the board started, in microseconds.</li>
<li><code class="il">explicit</code> stops the compiler from silently turning a string into a <code class="il">ScopedTimer</code>. <code class="il">= delete</code> forbids that function (here: no copying, see the first question).</li>
<li><b>PRIMASK</b>: a register in the Cortex-M CPU: 1 = interrupts off, 0 = on. <code class="il">__disable_irq()</code> sets it to 1; <code class="il">__get_PRIMASK()</code> / <code class="il">__set_PRIMASK()</code> read and write it.</li>
</ul>
<p>Expected output every second (your us and avg numbers will differ):</p>
''') + code('''analogRead x100: … us
avg = 512
PRIMASK inside = 1, after = 0''', 'Serial Monitor') + T('''
<p>ผลนี้บอกอะไร:</p>
<ul>
<li><b>destructor ทำงานเอง</b> บรรทัด <code class="il">analogRead x100</code> ไม่มีใครเรียก print ใน <code class="il">loop()</code> มันมาจาก <code class="il">~ScopedTimer()</code> ที่ทำงานตรง <code class="il">}</code></li>
<li><b>คืน resource เสมอ</b> <code class="il">inside = 1</code> คือ interrupt ถูกปิดภายใน <code class="il">{ }</code> และ <code class="il">after = 0</code> คือถูกเปิดคืนแล้ว ทั้งที่ไม่มีบรรทัดเปิดคืนเลย</li>
<li><b>วงจร pot</b> หมุนแล้ว <code class="il">avg</code> เปลี่ยนในช่วง 0–1023 เพราะ <code class="il">analogRead()</code> ใช้ <b>ADC</b> (วงจรในชิปที่แปลงแรงดันเป็นตัวเลข) แปลง 0–3.3 V เป็น 0–1023</li>
</ul>
<p class="note">อย่าเรียก <code class="il">Serial.print</code> ระหว่างที่ interrupt ปิดอยู่ เพราะ USB ต้องใช้ interrupt จึงเก็บค่าไว้ในตัวแปรก่อนแล้วพิมพ์หลังออกจาก <code class="il">{ }</code></p>
''', '''
<p>What the output tells you:</p>
<ul>
<li><b>Destructors run by themselves</b>: nothing in <code class="il">loop()</code> prints the <code class="il">analogRead x100</code> line. It comes from <code class="il">~ScopedTimer()</code>, running at the <code class="il">}</code>.</li>
<li><b>The resource is always returned</b>: <code class="il">inside = 1</code> means interrupts were off inside the <code class="il">{ }</code>, and <code class="il">after = 0</code> means they are back on, with no line that turns them on.</li>
<li><b>Pot wiring</b>: turning the pot moves <code class="il">avg</code> between 0 and 1023, because <code class="il">analogRead()</code> uses the <b>ADC</b> (a circuit in the chip that turns a voltage into a number) to map 0–3.3 V to 0–1023.</li>
</ul>
<p class="note">Never call <code class="il">Serial.print</code> while interrupts are off, because USB needs interrupts. That is why the value is stored first and printed after the <code class="il">{ }</code>.</p>
''')
   + qa([(T('ทำไมต้อง = delete copy constructor?', 'Why = delete the copy constructor?'),
          T('ถ้า copy ได้ จะมี 2 object ที่ destructor ทำงานซ้ำ เช่น เปิด interrupt 2 ครั้ง หรือพิมพ์เวลาซ้ำ resource ที่มีเจ้าของคนเดียวควรห้าม copy', 'If copying were allowed, two objects would run the destructor, e.g. re-enabling interrupts twice or printing the time twice. A resource with a single owner should not be copyable.')),
         (T('CriticalSection ใช้ตอนเปิด BLE ได้ไหม?', 'Can CriticalSection be used while BLE is running?'),
          T('ใช้ได้แค่ช่วงสั้นมาก ไม่กี่ไมโครวินาที เพราะ BLE ของ nRF52 ทำงานด้วย SoftDevice (ซอฟต์แวร์วิทยุของ Nordic ที่อยู่ในชิป) ถ้าปิด interrupt นาน SoftDevice จะพลาดจังหวะของวิทยุ ในงานจริงใช้ฟังก์ชันของ SoftDevice เอง (sd_nvic_critical_region_enter) แทน', 'Only for a very short time, a few microseconds. BLE on the nRF52 runs through the SoftDevice (Nordic\'s radio software inside the chip); if interrupts stay off longer, it misses radio timing. Real projects use the SoftDevice\'s own function (sd_nvic_critical_region_enter) instead.'))])
   + iv(T('RAII คือเหตุผลหลักที่หลายทีมย้ายจาก C มา C++ ในงาน embedded เพราะไม่ทำให้โปรแกรมช้าลง และกำจัดบั๊กลืมคืน resource ได้ทั้งกลุ่ม เช่น ลืมเปิด interrupt คืนในทางที่ออกจากฟังก์ชันเพราะเกิด error',
          'RAII is a main reason many teams move from C to C++ in embedded work: it costs no speed, and it removes a whole class of forgot-to-give-back bugs, such as not re-enabling interrupts on the path that exits early because of an error.')))
