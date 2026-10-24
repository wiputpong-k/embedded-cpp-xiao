lesson('09', 'A', T('Inheritance, virtual และ interface', 'Inheritance, virtual and interfaces'), 25, POT, goal(T('ออกแบบ interface ISensor ให้สลับเซนเซอร์จริงกับเซนเซอร์ปลอมได้ และรู้ต้นทุนของ virtual', 'Design an ISensor interface that lets you swap a real sensor for a fake one, and know what virtual costs')) + T('''
<p>ใน C ทำ polymorphism ด้วย struct ของ function pointer เอง ใน C++ ใช้ <code class="il">virtual</code> แล้ว compiler สร้างตาราง (vtable) ให้ ประโยชน์หลักใน embedded คือสลับ implementation ได้ เช่น ใช้ FakeSensor ตอน test โดยไม่ต้องแก้โค้ดที่เรียกใช้</p>
''', '''
<p>In C you build polymorphism yourself from a struct of function pointers. In C++ you write <code class="il">virtual</code> and the compiler builds the table (vtable) for you. The main benefit in embedded is swapping implementations, for example using FakeSensor in tests without touching the calling code.</p>
''') + fig(SVG_VTABLE, T('กลไกของ virtual call', 'How a virtual call works')) + '''
<h3>Hands-on</h3>''' + code('''class ISensor {
public:
  virtual ~ISensor() = default;
  virtual const char* name() const = 0;   // pure virtual = ต้อง override
  virtual float read() = 0;
};

class PotSensor : public ISensor {
public:
  explicit PotSensor(uint8_t pin) : pin_(pin) {}
  const char* name() const override { return "pot"; }
  float read() override { return analogRead(pin_) * (100.0f / 1023.0f); }  // %
private:
  uint8_t pin_;
};

class FakeSensor : public ISensor {
public:
  const char* name() const override { return "fake"; }
  float read() override { t_ += 0.1f; return 50.0f + 40.0f * sinf(t_); }
private:
  float t_ = 0;
};

PotSensor pot(A0);
FakeSensor fake;
ISensor* sensors[] = {&pot, &fake};

void setup() { Serial.begin(115200); }

void loop() {
  for (ISensor* s : sensors) {
    Serial.print(s->name()); Serial.print(':');
    Serial.print(s->read()); Serial.print(' ');
  }
  Serial.println();
  delay(50);
}''', 'sensors.ino', en={'// pure virtual = ต้อง override': '// pure virtual = must override'})
   + T('<p>เปิด Tools → Serial Plotter จะเห็นกราฟ 2 เส้น หมุน pot เทียบกับคลื่น sine</p>', '<p>Open Tools → Serial Plotter to see two lines: the pot as you turn it, and a sine wave.</p>')
   + qa([(T('ทำไม base class ต้องมี virtual destructor?', 'Why does the base class need a virtual destructor?'),
          T('ถ้า delete object ผ่าน pointer ของ base แล้ว destructor ไม่ virtual destructor ของ derived จะไม่ถูกเรียก resource รั่ว', 'If you delete an object through a base pointer and the destructor is not virtual, the derived destructor never runs and resources leak.')),
         (T('ถ้าไม่อยากจ่ายต้นทุน virtual มีทางเลือกอะไร?', 'What can you use if you do not want to pay for virtual?'),
          T('ใช้ template (static polymorphism / CRTP) ให้ compiler รู้ชนิดตอน compile แล้ว inline ได้ แลกกับ code size ที่อาจเพิ่มขึ้น', 'Templates (static polymorphism / CRTP): the compiler knows the type at compile time and can inline, at the cost of possibly larger code.'))])
   + iv(T('เวลาทีมถกกันว่า "virtual ช้าไหม" ให้คุยด้วยตัวเลข: เพิ่ม load 2 ครั้ง + indirect branch ต่อ call บน Cortex-M4 ราวไม่กี่ cycle ต้นทุนจริงคือ inline ไม่ได้ จึงควรเลี่ยงเฉพาะใน hot loop หรือ ISR',
          'When a team debates "is virtual slow?", talk numbers: two extra loads plus an indirect branch per call, a few cycles on a Cortex-M4. The real cost is lost inlining, so avoid it only in hot loops and ISRs.')))
