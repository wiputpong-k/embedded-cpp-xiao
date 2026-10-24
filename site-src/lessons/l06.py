lesson('06', 'A', T('RAII และ destructor', 'RAII and destructors'), 25, T('Pot 10 kΩ ที่ A0', '10 kΩ pot on A0'), goal(T('ใช้ scope ควบคุม resource อัตโนมัติ: จับเวลา, ปิด/เปิด interrupt', 'Let scope manage resources automatically: timing, disabling/enabling interrupts')) + T('''
<p>RAII (Resource Acquisition Is Initialization): ขอ resource ใน constructor คืนใน destructor แล้ว compiler จะเรียก destructor ให้เมื่อออกจาก scope เสมอ จึงไม่มีทางลืม <code class="il">unlock</code> หรือ <code class="il">enable_irq</code> แม้จะ <code class="il">return</code> กลางทาง C ไม่มีกลไกนี้</p>
''', '''
<p>RAII (Resource Acquisition Is Initialization): acquire the resource in the constructor and release it in the destructor. The compiler always calls the destructor when the object leaves scope, so you can never forget <code class="il">unlock</code> or <code class="il">enable_irq</code>, even if you <code class="il">return</code> early. C has no such mechanism.</p>
''') + fig(SVG_RAII, T('อายุของ object ผูกกับวงเล็บปีกกา', "The object's lifetime is tied to the braces")) + '''
<h3>Hands-on</h3>''' + T('<p>ต่อ potentiometer: ขาข้าง 3V3 กับ GND, ขากลางเข้า A0</p>', '<p>Wire the potentiometer: outer legs to 3V3 and GND, middle leg to A0.</p>') + code('''class ScopedTimer {
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
  delay(1000);
}''', 'raii.ino', en={'// ห้าม copy': '// no copying', '// ปิด interrupt แบบซ้อนได้: เก็บสถานะเดิมแล้วคืนค่าเดิม': '// Nestable interrupt disable: save the previous state, then restore it',
                     '// destructor ทำงานตรงนี้': '// destructor runs here'})
   + qa([(T('ทำไมต้อง = delete copy constructor?', 'Why = delete the copy constructor?'),
          T('ถ้า copy ได้ จะมี 2 object ที่ destructor ทำงานซ้ำ เช่น เปิด interrupt 2 ครั้ง หรือพิมพ์เวลาซ้ำ resource ที่มีเจ้าของคนเดียวควรห้าม copy', 'If copying were allowed, two objects would run the destructor, e.g. re-enabling interrupts twice or printing the time twice. A resource with a single owner should not be copyable.')),
         (T('CriticalSection ใช้กับ BLE (SoftDevice) ได้ไหม?', 'Can CriticalSection be used with BLE (SoftDevice)?'),
          T('ใช้ได้แค่ช่วงสั้นมาก ไม่กี่ไมโครวินาที ถ้าปิดนาน SoftDevice จะพลาด timing ของวิทยุ ในงานจริงใช้ sd_nvic_critical_region_enter แทน', 'Only for a very short time, a few microseconds. If interrupts stay off longer, the SoftDevice misses radio timing. Real projects use sd_nvic_critical_region_enter instead.'))])
   + iv(T('RAII คือเหตุผลหลักที่หลายทีมย้ายจาก C มา C++ ในงาน embedded เพราะไม่มี runtime overhead และกำจัดบั๊ก resource leak ทั้งกลุ่ม เช่น ลืมเปิด interrupt คืนใน error path',
          'RAII is a main reason many teams move from C to C++ in embedded work: zero runtime overhead, and it removes a whole class of resource-leak bugs, such as forgetting to re-enable interrupts on an error path.')))
