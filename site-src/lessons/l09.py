lesson('09', 'A', T('Inheritance, virtual และ interface', 'Inheritance, virtual and interfaces'), 25, POT, goal(T('ออกแบบ interface ISensor ให้สลับเซนเซอร์จริงกับเซนเซอร์ปลอมได้ และรู้ต้นทุนของ virtual', 'Design an ISensor interface that lets you swap a real sensor for a fake one, and know what virtual costs')) + T('''
<p>สมมติ firmware ต้องอ่านเซนเซอร์หลายแบบ และตอน test อยากใช้เซนเซอร์ปลอมแทนของจริง โดยไม่ต้องแก้โค้ดที่เรียกใช้ ใน C ทำได้ด้วย struct ที่เก็บ function pointer ไว้เอง ใน C++ ใช้ <code class="il">virtual</code> แล้ว compiler สร้างตารางนั้นให้ คำศัพท์ในบทนี้:</p>
<ul>
<li><b>inheritance</b> class ใหม่รับทุกอย่างจาก class เดิม เขียนว่า <code class="il">class PotSensor : public ISensor</code> class เดิมเรียกว่า base ส่วน class ใหม่เรียกว่า derived</li>
<li><b>virtual / override</b> <code class="il">virtual</code> บอกว่าฟังก์ชันนี้ derived เขียนทับได้ <code class="il">override</code> บอกว่ากำลังเขียนทับ (ถ้าชื่อหรือพารามิเตอร์ไม่ตรง compiler จะแจ้ง error)</li>
<li><b>pure virtual / interface</b> <code class="il">= 0</code> คือฟังก์ชันที่ base ไม่มีตัวจริง derived ต้องเขียนเอง class ที่มีแต่ฟังก์ชันแบบนี้เรียกว่า interface ใช้เป็น "สัญญา" ว่าเซนเซอร์ทุกตัวต้องมี <code class="il">name()</code> และ <code class="il">read()</code></li>
<li><b>polymorphism</b> เรียกผ่าน pointer ชนิด base (<code class="il">ISensor*</code>) แต่ฟังก์ชันที่ทำงานเป็นของชนิดจริงของ object</li>
<li><b>vtable / vptr</b> vtable คือตาราง address ของฟังก์ชัน virtual มี 1 ตารางต่อ class เก็บใน flash ส่วน vptr คือ pointer ที่ซ่อนอยู่ในทุก object ชี้ไปที่ vtable ของ class นั้น</li>
</ul>
''', '''
<p>Say your firmware reads several kinds of sensor, and in tests you want a fake sensor instead of the real one without touching the calling code. In C you build that from a struct of function pointers. In C++ you write <code class="il">virtual</code> and the compiler builds the table for you. Terms in this lesson:</p>
<ul>
<li><b>inheritance</b>: a new class takes everything from an existing one, written <code class="il">class PotSensor : public ISensor</code>. The existing class is the base; the new one is the derived class.</li>
<li><b>virtual / override</b>: <code class="il">virtual</code> says a derived class may replace this function; <code class="il">override</code> says "I am replacing it" (if the name or parameters do not match, the compiler reports an error).</li>
<li><b>pure virtual / interface</b>: <code class="il">= 0</code> marks a function with no body in the base; every derived class must write it. A class made only of these is an interface: a "contract" that every sensor has <code class="il">name()</code> and <code class="il">read()</code>.</li>
<li><b>polymorphism</b>: you call through a base pointer (<code class="il">ISensor*</code>), but the function that runs belongs to the object's real type.</li>
<li><b>vtable / vptr</b>: the vtable is a table of addresses of the virtual functions, one per class, stored in flash. The vptr is a hidden pointer inside every object that points to its class's vtable.</li>
</ul>
''') + fig(SVG_VTABLE, T('กลไกของ virtual call', 'How a virtual call works')) + '''
<h3>Hands-on</h3>''' + T('''
<p>sketch นี้พิสูจน์ polymorphism: <code class="il">loop()</code> เรียก <code class="il">s-&gt;read()</code> บรรทัดเดียว แต่ได้ค่าจากเซนเซอร์ 2 ชนิด ใช้วงจร pot จากบท 06</p>
<ol>
<li>สร้าง sketch ใหม่ วางโค้ดข้างล่าง บันทึกชื่อ <code class="il">sensors</code> แล้วกด <b>Upload</b></li>
<li>เปิด <b>Tools → Serial Plotter</b> ตั้ง 115200 baud แล้วหมุน pot</li>
</ol>
''', '''
<p>This sketch proves polymorphism: <code class="il">loop()</code> calls <code class="il">s-&gt;read()</code> on a single line, yet gets values from two kinds of sensor. It uses the pot wiring from lesson 06.</p>
<ol>
<li>Create a new sketch, paste the code below, save it as <code class="il">sensors</code>, and press <b>Upload</b>.</li>
<li>Open <b>Tools → Serial Plotter</b> at 115200 baud and turn the pot.</li>
</ol>
''') + code('''class ISensor {
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
}''', 'sensors.ino', en={'// pure virtual = ต้อง override': '// pure virtual = must override'}) + T('''
<p>ผลที่ควรเห็น: กราฟ 2 เส้น เส้น <code class="il">pot</code> ขึ้นลง 0–100 ตามที่หมุน และเส้น <code class="il">fake</code> เป็นคลื่น sine ระหว่าง 10–90 (Serial Plotter อ่านรูปแบบ <code class="il">ชื่อ:ค่า</code> ในแต่ละบรรทัดเป็นเส้นกราฟ)</p>
<p>ผลนี้บอกอะไร:</p>
<ul>
<li><b>polymorphism</b> <code class="il">s</code> เป็น <code class="il">ISensor*</code> ทั้งสองรอบ แต่รอบแรกได้ <code class="il">PotSensor::read()</code> รอบสองได้ <code class="il">FakeSensor::read()</code> เพราะแต่ละ object ชี้ไปที่ vtable ของ class ตัวเองตามรูป</li>
<li><b>สลับได้โดยไม่แก้ผู้เรียก</b> จะเพิ่มเซนเซอร์ใหม่ แค่เขียน class ที่สืบจาก <code class="il">ISensor</code> แล้วใส่ใน <code class="il">sensors[]</code> โดย <code class="il">loop()</code> ไม่ต้องแก้เลย นี่คือเหตุผลที่เซนเซอร์ปลอมใช้แทนของจริงตอน test ได้ (บท 20)</li>
</ul>
''', '''
<p>Expected result: two lines. <code class="il">pot</code> moves between 0 and 100 as you turn it, and <code class="il">fake</code> is a sine wave between 10 and 90. (Serial Plotter turns each <code class="il">name:value</code> pair on a line into a plotted line.)</p>
<p>What the result tells you:</p>
<ul>
<li><b>polymorphism</b>: <code class="il">s</code> is an <code class="il">ISensor*</code> both times, yet the first pass runs <code class="il">PotSensor::read()</code> and the second <code class="il">FakeSensor::read()</code>, because each object points to its own class's vtable, as in the figure.</li>
<li><b>Swap without touching the caller</b>: to add a sensor, write a class derived from <code class="il">ISensor</code> and put it in <code class="il">sensors[]</code>; <code class="il">loop()</code> does not change. That is why a fake sensor can stand in for the real one in tests (lesson 20).</li>
</ul>
''')
   + qa([(T('ทำไม base class ต้องมี virtual destructor?', 'Why does the base class need a virtual destructor?'),
          T('ถ้าทำลาย object ผ่าน pointer ชนิด base (เช่น delete) แล้ว destructor ไม่ virtual destructor ของ derived จะไม่ถูกเรียก resource ที่มันถืออยู่จึงไม่ถูกคืน', 'If an object is destroyed through a base pointer (e.g. with delete) and the destructor is not virtual, the derived destructor never runs, so the resources it holds are never released.')),
         (T('ถ้าไม่อยากจ่ายต้นทุน virtual มีทางเลือกอะไร?', 'What can you use if you do not want to pay for virtual?'),
          T('ใช้ template (บท 10) ให้ compiler รู้ชนิดจริงตอน compile จึงเรียกฟังก์ชันตรง ๆ ได้ แลกกับ flash ที่อาจเพิ่มขึ้น เพราะได้โค้ด 1 ชุดต่อชนิด', 'Use templates (lesson 10): the compiler knows the real type at compile time and calls the function directly, at the cost of possibly more flash, since you get one copy of the code per type.'))])
   + iv(T('virtual call ต้องอ่าน vptr และ vtable ก่อนแล้วจึงกระโดดไปเรียก เพิ่มเวลาแค่ไม่กี่ cycle (จังหวะ clock บท 01) บน Cortex-M4 ต้นทุนที่สำคัญกว่าคือ compiler นำตัวฟังก์ชันไปแปะแทนการเรียก (inline) ไม่ได้ จึงเลี่ยง virtual เฉพาะในโค้ดที่ถูกเรียกถี่มาก ๆ หรือใน ISR (บท 12) ที่เหลือใช้ได้ตามสบาย',
          'A virtual call reads the vptr and the vtable before jumping, which adds only a few cycles (clock ticks, lesson 01) on a Cortex-M4. The bigger cost is that the compiler cannot paste the function body in place of the call (inlining). So avoid virtual only in code that runs extremely often or inside an ISR (lesson 12); elsewhere use it freely.')))
