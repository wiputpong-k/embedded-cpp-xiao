LED_CLASS = '''class Led {
public:
  Led(uint8_t pin, bool activeLow) : pin_(pin), activeLow_(activeLow) {}

  void begin() { pinMode(pin_, OUTPUT); off(); }
  void on()     { write(true); }
  void off()    { write(false); }
  void toggle() { write(!isOn_); }
  bool isOn() const { return isOn_; }   // const method: ไม่แก้ state

private:
  void write(bool on) {
    isOn_ = on;
    digitalWrite(pin_, (on != activeLow_) ? HIGH : LOW);
  }
  uint8_t pin_;
  bool activeLow_;
  bool isOn_ = false;
};'''
LED_MAIN = '''Led red(LED_RED, true);   // บนบอร์ด: active-LOW
Led ext(D2, false);       // ภายนอก: active-HIGH

void setup() {
  red.begin();
  ext.begin();
}

void loop() {
  red.toggle();
  ext.toggle();
  delay(300);
}'''
LED_CLASS_EN = {'// const method: ไม่แก้ state': '// const method: does not change state'}
LED_MAIN_EN = {'// บนบอร์ด: active-LOW': '// on-board: active-LOW', '// ภายนอก: active-HIGH': '// external: active-HIGH'}
LED_EN = {**LED_CLASS_EN, **LED_MAIN_EN}

lesson('04', 'A', T('class: encapsulation และ constructor', 'class: encapsulation and constructors'), 30, 'LED + R 1 kΩ', goal(T('ต่อ LED ภายนอก และเขียน class Led ที่ซ่อนเรื่อง active-LOW ไว้ข้างใน', 'Wire an external LED, and write a Led class that hides the active-LOW detail inside'))
   + vs(T('struct เก็บข้อมูล + ฟังก์ชัน <code class="il">led_on(&amp;led)</code> แยกกัน ใครก็แก้ field ได้', 'A struct holds the data and a separate function <code class="il">led_on(&amp;led)</code> acts on it. Anyone can change the fields.'),
        T('ข้อมูล (private) และพฤติกรรม (public) อยู่ด้วยกัน คอมไพล์แล้วได้โค้ดขนาดใกล้เคียงกัน เพราะ <code class="il">this</code> ก็คือ pointer ที่ส่งเข้าไปแบบซ่อน', 'Data (private) and behavior (public) live together. The compiled code is about the same size, because <code class="il">this</code> is just a hidden pointer argument.'))
   + T('''
<ul>
<li><b>class / object</b> class คือแบบพิมพ์ (เหมือน struct ที่มีฟังก์ชันอยู่ด้วย) object คือตัวจริงที่สร้างจากแบบนั้น เช่น <code class="il">red</code> และ <code class="il">ext</code></li>
<li><b>encapsulation</b> ซ่อนข้อมูลไว้ใน <code class="il">private:</code> ให้ภายนอกใช้ได้แค่ฟังก์ชันใน <code class="il">public:</code> จึงไม่มีใครแก้ค่าข้างในผิด ๆ ได้</li>
<li><b>constructor</b> ฟังก์ชันชื่อเดียวกับ class ไม่มีชนิด return ทำงานอัตโนมัติตอนสร้าง object ใช้ตั้งค่าเริ่มต้น ส่วน <code class="il">: pin_(pin)</code> เรียกว่า member initializer list คือการกำหนดค่า member ตอนสร้าง</li>
<li><b><code class="il">this</code></b> pointer ไปยัง object ที่กำลังถูกเรียก compiler ส่งให้ทุกฟังก์ชันใน class แบบซ่อน เทียบได้กับ <code class="il">&amp;led</code> ใน <code class="il">led_on(&amp;led)</code> ของ C</li>
</ul>
''', '''
<ul>
<li><b>class / object</b>: a class is the blueprint (like a struct that also holds functions); an object is a real instance made from it, such as <code class="il">red</code> and <code class="il">ext</code>.</li>
<li><b>encapsulation</b>: data hidden under <code class="il">private:</code>, so outside code can only use the functions under <code class="il">public:</code> and cannot set internal values wrongly.</li>
<li><b>constructor</b>: a function named after the class, with no return type, that runs automatically when an object is created, to set initial values. <code class="il">: pin_(pin)</code> is the member initializer list: members get their values at construction.</li>
<li><b><code class="il">this</code></b>: a pointer to the object being called. The compiler passes it to every member function behind the scenes, like <code class="il">&amp;led</code> in C's <code class="il">led_on(&amp;led)</code>.</li>
</ul>
''')
   + T('''
<h3>ต่อวงจร</h3>
<p>breadboard คือแผงเสียบสายที่ไม่ต้องบัดกรี รู 5 รูที่เรียงอยู่ในแถวเดียวกัน (แนวตั้งฉากกับร่องกลาง) ต่อถึงกันอยู่ข้างใน ส่วนแถวยาวตามขอบที่มีเส้นสีแดงและน้ำเงิน ใช้เป็นรางไฟและราง GND</p>
<ol>
<li>ถอดสาย USB ออกก่อนต่อวงจรทุกครั้ง</li>
<li>เสียบบอร์ด XIAO คร่อมร่องกลางของ breadboard ให้ขาแต่ละข้างอยู่คนละฝั่ง (ถ้าบอร์ดยังไม่ได้บัดกรีขา header ต้องบัดกรีก่อน)</li>
<li>ดูขั้วของ LED: ขายาวคือขั้วบวก (anode) ขาสั้นคือขั้วลบ (cathode) และขอบหัว LED ด้านที่แบนคือฝั่งขั้วลบ</li>
<li>ต่อสาย jumper จากขา D2 ไปที่ขาหนึ่งของ R 1 kΩ (ตัวต้านทานไม่มีขั้ว กลับด้านได้)</li>
<li>ต่ออีกขาของ R เข้ากับขายาวของ LED</li>
<li>ต่อขาสั้นของ LED ไปที่ขา GND ของบอร์ด</li>
</ol>
<p class="note">ถ้า LED ไม่ติด ให้ลองกลับด้าน LED ก่อน เพราะเป็นสาเหตุที่เจอบ่อยที่สุด R 1 kΩ มีไว้จำกัดกระแส ห้ามต่อ LED ตรงกับขาโดยไม่มี R</p>
''', '''
<h3>Wire it up</h3>
<p>A breadboard lets you connect parts without soldering. The 5 holes in each short row (across the center gap) are connected inside. The long rows along the edges, marked red and blue, are the power and GND rails.</p>
<ol>
<li>Always unplug the USB cable before you change the wiring.</li>
<li>Press the XIAO into the breadboard across the center gap, so the two rows of pins are on opposite sides. (If the board has no header pins soldered yet, solder them first.)</li>
<li>Find the LED polarity: the long leg is positive (anode), the short leg is negative (cathode), and the flat edge on the LED rim marks the negative side.</li>
<li>Run a jumper wire from pin D2 to one leg of the 1 kΩ resistor (resistors have no polarity).</li>
<li>Connect the other resistor leg to the LED's long leg.</li>
<li>Connect the LED's short leg to the board's GND pin.</li>
</ol>
<p class="note">If the LED does not light, try flipping it first; that is the most common cause. The 1 kΩ resistor limits the current. Never connect an LED straight to a pin without it.</p>
''') + fig(SVG_WIRE, T('ต่อ LED ภายนอกที่ D2 ผ่าน R 1 kΩ ลง GND (active-HIGH)', 'External LED on D2 through 1 kΩ to GND (active-HIGH)'))
   + T('''
<h3>Hands-on</h3>
<p>sketch นี้พิสูจน์ encapsulation: LED 2 ดวงที่ต่อวงจรต่างกัน (active-LOW และ active-HIGH) ถูกสั่งด้วยคำสั่งเดียวกัน</p>
<ol>
<li>เสียบสาย USB กลับ แล้วกด <b>File → New Sketch</b></li>
<li>คัดลอกโค้ดข้างล่างไปวางแทนโค้ดเดิม แล้วกด <b>File → Save As…</b> ตั้งชื่อ <code class="il">led_class</code></li>
<li>กด <b>Upload</b> แล้วดูผล: LED แดงบนบอร์ดและ LED ภายนอกกระพริบพร้อมกันทุก 0.3 วินาที</li>
</ol>''', '''
<h3>Hands-on</h3>
<p>This sketch proves encapsulation: two LEDs wired differently (active-LOW and active-HIGH) are driven with the same calls.</p>
<ol>
<li>Plug the USB cable back in and open <b>File → New Sketch</b>.</li>
<li>Copy the code below over the starter code, then <b>File → Save As…</b> and name it <code class="il">led_class</code>.</li>
<li>Click <b>Upload</b>. Both the red on-board LED and the external LED should blink together every 0.3 s.</li>
</ol>''') + code(LED_CLASS + '\n\n' + LED_MAIN, 'led_class.ino', en=LED_EN) + T('''
<p>สังเกตว่าทั้งสองดวงติดพร้อมกัน แม้ LED บนบอร์ดเป็น active-LOW และ LED ภายนอกเป็น active-HIGH เพราะ class จัดการเรื่องนี้ไว้ใน <code class="il">write()</code> คนที่เรียกใช้แค่สั่ง <code class="il">on()</code> หรือ <code class="il">toggle()</code> ไม่ต้องรู้ว่าต่อวงจรแบบไหน</p>
<p class="note">ทำไมมี <code class="il">begin()</code> แยก ไม่เรียก <code class="il">pinMode</code> ใน constructor? เพราะ constructor ของ object global ถูกเรียกโดย startup code ก่อน <code class="il">main()</code> (ดูแผนภาพบท 01) จึงทำงานก่อน <code class="il">init()</code> ฮาร์ดแวร์อาจยังไม่พร้อม เป็น pattern มาตรฐานของ embedded C++</p>
''', '''
<p>Notice that both LEDs light at the same time, even though the on-board LED is active-LOW and the external one is active-HIGH. The class handles that inside <code class="il">write()</code>; callers just use <code class="il">on()</code> or <code class="il">toggle()</code> without knowing how the LED is wired.</p>
<p class="note">Why a separate <code class="il">begin()</code> instead of calling <code class="il">pinMode</code> in the constructor? The startup code runs the constructors of global objects before <code class="il">main()</code> (see the lesson 01 diagram), so they run before <code class="il">init()</code> and the hardware may not be ready yet. This is a standard embedded C++ pattern.</p>
''') + qa([(T('member initializer list (: pin_(pin)) ดีกว่ากำหนดค่าใน body อย่างไร?', 'Why is a member initializer list (: pin_(pin)) better than assigning in the body?'),
           T('สร้าง member ด้วยค่าที่ถูกต้องตั้งแต่แรก ไม่ต้องสร้างด้วยค่าเริ่มต้นแล้วค่อยกำหนดค่าใหม่ และจำเป็นสำหรับ member ที่เป็น const หรือ reference', 'Members are constructed with the right value from the start instead of being default-constructed and then assigned. It is required for const and reference members.')),
          (T('object Led ใช้ RAM กี่ byte โดยประมาณ?', 'Roughly how many bytes of RAM does a Led object use?'),
           T('ราว 3–4 byte (pin_, activeLow_, isOn_ และอาจมี padding คือ byte ว่างที่ compiler เติมให้ข้อมูลเรียงตรงตำแหน่ง) ฟังก์ชันไม่กิน RAM ต่อ object เพราะอยู่ใน flash ใช้ร่วมกัน', 'About 3–4 bytes (pin_, activeLow_, isOn_, plus possible padding: empty bytes the compiler adds to keep data aligned). Member functions cost no RAM per object; they live in flash and are shared.'))]))
