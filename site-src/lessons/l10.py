lesson('10', 'A', 'Template: RingBuffer<T, N>', 30, POT, goal(T('เขียน container ขนาดคงที่ใช้ซ้ำได้ทุกชนิด โดยไม่ใช้ heap', 'Write a reusable fixed-size container for any type, without the heap'))
   + vs(T('ทำ buffer สำหรับ int, float แยกกัน หรือใช้ <code class="il">void*</code> + macro ซึ่งไม่มี type safety', 'Write separate buffers for int and float, or use <code class="il">void*</code> + macros with no type safety.'),
        T('template ให้ compiler สร้างโค้ดเฉพาะชนิดให้ ขนาด N เป็นค่าตอน compile ตรวจได้ด้วย <code class="il">static_assert</code>', 'A template lets the compiler generate code for each type. N is a compile-time value you can check with <code class="il">static_assert</code>.'))
   + fig(SVG_RING, T('ring buffer: head เขียน tail อ่าน วนรอบด้วย modulo', 'Ring buffer: head writes, tail reads, both wrap around with modulo')) + '''
<h3>Hands-on</h3>''' + T('<p>สร้าง <code class="il">src/RingBuffer.h</code></p>', '<p>Create <code class="il">src/RingBuffer.h</code>.</p>') + code(RING, 'src/RingBuffer.h') + code('''#include "src/RingBuffer.h"

xiao::RingBuffer<uint16_t, 16> samples;   // 16 ค่าล่าสุด

void setup() { Serial.begin(115200); }

void loop() {
  uint16_t raw = analogRead(A0);
  samples.pushOverwrite(raw);
  Serial.print("raw:"); Serial.print(raw);
  Serial.print(" avg:"); Serial.println(average(samples));
  delay(20);
}''', 'moving_average.ino', en={'// 16 ค่าล่าสุด': '// last 16 values'})
   + T('<p class="note">ทำไมต้องเขียน <code class="il">xiao::RingBuffer</code>? core ของ Seeed nRF52 มี class ชื่อ <code class="il">RingBuffer</code> อยู่แล้ว (ใช้ภายในตัวจัดการ UART) ถ้าประกาศชื่อเดียวกันไว้นอก namespace จะ compile ไม่ผ่านเพราะชื่อชนกัน ไฟล์ <code class="il">RingBuffer.h</code> ของคอร์สจึงอยู่ใน <code class="il">namespace xiao</code> นี่คือเหตุผลจริงที่ต้องมี namespace ตามบท 03 ส่วน <code class="il">average(samples)</code> เรียกได้โดยไม่ต้องเติม <code class="il">xiao::</code> เพราะ compiler หาฟังก์ชันใน namespace ของชนิดพารามิเตอร์ให้เอง (argument-dependent lookup)</p>'
       '<p>เปิด Serial Plotter เทียบเส้น raw กับ avg ลองเปลี่ยน N เป็น 4 และ 64 สังเกตความหน่วงและความเรียบ (moving average N จุด = delay ราว N/2 sample)</p>',
       '<p class="note">Why <code class="il">xiao::RingBuffer</code>? The Seeed nRF52 core already has a class named <code class="il">RingBuffer</code> (used inside its UART driver). Declaring the same name outside a namespace fails to compile because the names clash, so the course\'s <code class="il">RingBuffer.h</code> lives in <code class="il">namespace xiao</code>. That is exactly the kind of clash namespaces from lesson 03 exist for. <code class="il">average(samples)</code> works without <code class="il">xiao::</code> because the compiler also searches the namespace of the argument\'s type (argument-dependent lookup).</p>'
       '<p>Open Serial Plotter and compare the raw and avg lines. Try N = 4 and N = 64 and watch the lag and smoothness (an N-point moving average delays the signal by about N/2 samples).</p>')
   + qa([(T('ถ้าใช้ RingBuffer&lt;uint16_t,16&gt; และ RingBuffer&lt;float,16&gt; flash จะเป็นอย่างไร?', 'What happens to flash if you use RingBuffer&lt;uint16_t,16&gt; and RingBuffer&lt;float,16&gt;?'),
          T('compiler สร้างโค้ด 2 ชุด (template instantiation) flash เพิ่มขึ้น ถ้ามีหลายชนิดเกินไปเรียกว่า code bloat', 'The compiler generates two copies of the code (template instantiation), so flash grows. Too many types leads to code bloat.')),
         (T('ถ้า ISR เป็นคน push และ loop เป็นคน pop ปลอดภัยไหม?', 'Is it safe if an ISR pushes and loop pops?'),
          T('ยังไม่ปลอดภัย เพราะ count_ ถูกแก้จากทั้งสองฝั่ง ต้องครอบด้วย CriticalSection หรือออกแบบ SPSC ที่ฝั่ง producer แก้แค่ head ฝั่ง consumer แก้แค่ tail', 'Not yet, because count_ is changed from both sides. Wrap it in a CriticalSection, or design an SPSC buffer where the producer only touches head and the consumer only touches tail.'))]))
