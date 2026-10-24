lesson('03', 'A', 'namespace, overloading, enum class', 20, BOARD, goal(T('จัดระเบียบชื่อและเข้าใจว่าทำไม C++ ต้องมี name mangling', 'Organize names, and understand why C++ needs name mangling'))
   + vs(T('ชื่อฟังก์ชันซ้ำไม่ได้ ต้องตั้ง <code class="il">log_int</code>, <code class="il">log_float</code> และ <code class="il">enum</code> ปนกับ int ได้ทุกที่', 'Function names must be unique, so you write <code class="il">log_int</code>, <code class="il">log_float</code>, and an <code class="il">enum</code> mixes with int anywhere.'),
        T('overload ชื่อเดียวหลายพารามิเตอร์ได้ <code class="il">namespace</code> กันชื่อชน <code class="il">enum class</code> ไม่แปลงเป็น int เอง กำหนดขนาด <code class="il">: uint8_t</code> ได้', 'One name can be overloaded for different parameters, <code class="il">namespace</code> prevents name clashes, and <code class="il">enum class</code> never converts to int by itself and can set its size with <code class="il">: uint8_t</code>.'))
   + fig(SVG_MANGLE, T('compiler ฝังชนิดพารามิเตอร์ลงในชื่อ symbol จึง overload ได้', 'The compiler encodes parameter types into the symbol name, which makes overloading possible')) + '''
<h3>Hands-on</h3>''' + code('''namespace logx {
void info(const char* msg) {
  Serial.print("[I] "); Serial.println(msg);
}
void info(const char* key, int value) {
  Serial.print("[I] "); Serial.print(key); Serial.print('='); Serial.println(value);
}
void info(const char* key, float value, int digits = 2) {   // default argument
  Serial.print("[I] "); Serial.print(key); Serial.print('='); Serial.println(value, digits);
}
}  // namespace logx

enum class Mode : uint8_t { Off, Slow, Fast };

void setup() {
  Serial.begin(115200);
  while (!Serial) {}
  logx::info("boot");
  logx::info("uptime_ms", (int)millis());
  logx::info("vbat", 3.71f);
  logx::info("pi", 3.14159f, 4);
  Mode m = Mode::Slow;
  logx::info("mode", static_cast<int>(m));   // ต้อง cast เอง
  // int bad = m;   // ลองเปิดบรรทัดนี้: compile error
}

void loop() {}''', 'logx.ino', en={'// ต้อง cast เอง': '// explicit cast required', '// ลองเปิดบรรทัดนี้: compile error': '// uncomment this line: compile error'})
   + qa([(T('ถ้า library เขียนด้วย C ต้อง include อย่างไร?', 'How do you include a library written in C?'),
          T('ครอบ header ด้วย extern "C" { … } เพื่อให้ linker หา symbol ชื่อแบบ C เจอ ถ้าไม่ครอบจะ error undefined reference', 'Wrap the header in extern "C" { … } so the linker finds the C-style symbol names. Without it you get undefined reference errors.')),
         (T('ทำไม enum class ปลอดภัยกว่า enum?', 'Why is enum class safer than enum?'),
          T('ไม่แปลงเป็น int เอง ชื่อ enumerator ไม่หลุดออกมาใน scope ภายนอก และกำหนด underlying type ได้ จึงคุมขนาดในหน่วยความจำได้', 'It never converts to int implicitly, its enumerator names do not leak into the outer scope, and you can set the underlying type to control its size in memory.'))]))
