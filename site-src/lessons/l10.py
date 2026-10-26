lesson('10', 'A', 'Template: RingBuffer<T, N>', 30, POT, goal(T('เขียน container ขนาดคงที่ใช้ซ้ำได้ทุกชนิด โดยไม่ใช้ heap', 'Write a reusable fixed-size container for any type, without the heap')) + T('''
<p>ค่าที่อ่านจาก pot จะแกว่งเล็กน้อยทุกครั้ง วิธีทำให้เรียบคือเก็บค่าล่าสุด N ค่าไว้แล้วเฉลี่ย (moving average) ต้องมีที่เก็บที่ใส่ค่าใหม่และทิ้งค่าเก่าได้เรื่อย ๆ และอยากใช้ซ้ำได้ทั้งกับ <code class="il">uint16_t</code>, <code class="il">float</code> หรือ struct คำศัพท์ในบทนี้:</p>
<ul>
<li><b>template</b> แม่แบบของ class หรือฟังก์ชันที่เว้นชนิด (<code class="il">T</code>) หรือค่าคงที่ (<code class="il">N</code>) ไว้ เมื่อเขียน <code class="il">RingBuffer&lt;uint16_t, 16&gt;</code> compiler จะสร้างโค้ดฉบับสำหรับ <code class="il">uint16_t</code> 16 ช่องให้ เรียกว่า template instantiation</li>
<li><b>ring buffer / FIFO</b> array ขนาดคงที่ที่ใช้วนรอบ: <code class="il">head</code> คือช่องที่จะเขียนถัดไป <code class="il">tail</code> คือช่องที่จะอ่านถัดไป ถึงท้าย array ก็วนกลับไปช่อง 0 ด้วย <code class="il">% N</code> ค่าที่เข้าก่อนออกก่อน (First In, First Out)</li>
<li><b>heap</b> หน่วยความจำที่จองตอนโปรแกรมทำงานด้วย <code class="il">new</code> หรือ <code class="il">malloc</code> buffer ในบทนี้ไม่ใช้ heap ขนาดรู้ตั้งแต่ตอน build (บท 11 อธิบายว่าทำไมสำคัญ)</li>
<li><b><code class="il">static_assert</code></b> เงื่อนไขที่ compiler ตรวจตอน compile ถ้าไม่จริงจะ build ไม่ผ่าน</li>
</ul>
''', '''
<p>Pot readings jitter a little every time. To smooth them, keep the last N values and average them (a moving average). That needs storage that keeps taking new values and dropping old ones, reusable for <code class="il">uint16_t</code>, <code class="il">float</code> or a struct. Terms in this lesson:</p>
<ul>
<li><b>template</b>: a class or function pattern with a type (<code class="il">T</code>) or a constant (<code class="il">N</code>) left open. When you write <code class="il">RingBuffer&lt;uint16_t, 16&gt;</code>, the compiler generates a version for 16 <code class="il">uint16_t</code> slots. That is template instantiation.</li>
<li><b>ring buffer / FIFO</b>: a fixed-size array used in a circle. <code class="il">head</code> is the next slot to write, <code class="il">tail</code> the next slot to read; at the end of the array they wrap to slot 0 with <code class="il">% N</code>. First in, first out.</li>
<li><b>heap</b>: memory reserved while the program runs, with <code class="il">new</code> or <code class="il">malloc</code>. This buffer avoids the heap: its size is known at build time (lesson 11 explains why that matters).</li>
<li><b><code class="il">static_assert</code></b>: a condition the compiler checks while compiling. If it is false, the build fails.</li>
</ul>
''')
   + vs(T('ทำ buffer สำหรับ int, float แยกกัน หรือใช้ <code class="il">void*</code> + macro ซึ่งไม่มี type safety', 'Write separate buffers for int and float, or use <code class="il">void*</code> + macros with no type safety.'),
        T('template ให้ compiler สร้างโค้ดเฉพาะชนิดให้ ขนาด N เป็นค่าตอน compile ตรวจได้ด้วย <code class="il">static_assert</code>', 'A template lets the compiler generate code for each type. N is a compile-time value you can check with <code class="il">static_assert</code>.'))
   + fig(SVG_RING, T('ring buffer: head เขียน tail อ่าน วนรอบด้วย modulo', 'Ring buffer: head writes, tail reads, both wrap around with modulo')) + '''
<h3>Hands-on</h3>''' + T('''
<p>sketch นี้พิสูจน์ว่า template ตัวเดียวสร้าง buffer ตามชนิดและขนาดที่สั่งได้ ขนาดถูกล็อกตั้งแต่ตอน build และไม่ใช้ heap ใช้วงจร pot จากบท 06</p>
<ol>
<li>สร้าง sketch ใหม่ บันทึกชื่อ <code class="il">moving_average</code></li>
<li>สร้างไฟล์ <code class="il">src/RingBuffer.h</code> แบบเดียวกับบท 05 (<b>Sketch → Show Sketch Folder</b> → สร้างโฟลเดอร์ <code class="il">src</code> → สร้างไฟล์ <code class="il">RingBuffer.h</code>) แล้ววางโค้ดชุดแรกข้างล่าง</li>
<li>วางโค้ดชุดที่สองลงใน <code class="il">moving_average.ino</code> กด <b>Upload</b> แล้วจดตัวเลข <i>Global variables use</i> ในแถบ Output ไว้</li>
<li>เปิด <b>Tools → Serial Plotter</b> ที่ 115200 baud แล้วหมุน pot</li>
</ol>
''', '''
<p>This sketch proves that one template builds a buffer of whatever type and size you ask for, that the size is fixed at build time, and that no heap is used. It uses the pot wiring from lesson 06.</p>
<ol>
<li>Create a new sketch and save it as <code class="il">moving_average</code>.</li>
<li>Create <code class="il">src/RingBuffer.h</code> as in lesson 05 (<b>Sketch → Show Sketch Folder</b> → create a <code class="il">src</code> folder → create <code class="il">RingBuffer.h</code>) and paste the first code block below.</li>
<li>Paste the second block into <code class="il">moving_average.ino</code>, press <b>Upload</b>, and note the <i>Global variables use</i> number in the Output panel.</li>
<li>Open <b>Tools → Serial Plotter</b> at 115200 baud and turn the pot.</li>
</ol>
''') + code(RING, 'src/RingBuffer.h') + code('''#include "src/RingBuffer.h"

xiao::RingBuffer<uint16_t, 16> samples;   // 16 ค่าล่าสุด

void setup() { Serial.begin(115200); }

void loop() {
  uint16_t raw = analogRead(A0);
  samples.pushOverwrite(raw);
  Serial.print("raw:"); Serial.print(raw);
  Serial.print(" avg:"); Serial.println(average(samples));
  delay(20);
}''', 'moving_average.ino', en={'// 16 ค่าล่าสุด': '// last 16 values'})
   + T('''
<p>ผลที่ควรเห็น: เส้น <code class="il">raw</code> ขยับตาม pot และมีหยักเล็ก ๆ ส่วนเส้น <code class="il">avg</code> เรียบกว่าและตามมาช้ากว่าเล็กน้อย</p>
<p>ผลนี้บอกอะไร ลองทีละข้อ:</p>
<ul>
<li><b>ขนาดล็อกตั้งแต่ build</b> เปลี่ยน <code class="il">16</code> เป็น <code class="il">64</code> แล้วกด Verify ตัวเลข <i>Global variables use</i> จะเพิ่ม 96 byte พอดี (เพิ่ม 48 ช่อง × 2 byte ของ <code class="il">uint16_t</code>) เพราะ buffer เป็นตัวแปร global ที่ linker จองที่ไว้ตายตัว (บท 01) ไม่ได้จองจาก heap ตอนรัน</li>
<li><b>N มากขึ้น = เรียบขึ้นแต่ช้าลง</b> Upload ค่า 64 แล้วดู Plotter เส้น <code class="il">avg</code> เรียบขึ้นแต่ตามช้าลง (moving average N จุด หน่วงสัญญาณราว N/2 ค่า)</li>
<li><b><code class="il">static_assert</code></b> เปลี่ยนเป็น <code class="il">0</code> แล้วกด Verify จะได้ <code class="il">error: static assertion failed: N must be &gt; 0</code> คือบั๊กถูกจับตั้งแต่ตอน compile จากนั้นเปลี่ยนกลับเป็น 16</li>
</ul>
<p class="note">ทำไมต้องเขียน <code class="il">xiao::RingBuffer</code>? core ของ Seeed nRF52 มี class ชื่อ <code class="il">RingBuffer</code> อยู่แล้ว ถ้าประกาศชื่อเดียวกันไว้นอก namespace จะ compile ไม่ผ่านเพราะชื่อชนกัน นี่คือเหตุผลจริงที่ต้องมี namespace ตามบท 03 ส่วน <code class="il">average(samples)</code> ไม่ต้องเติม <code class="il">xiao::</code> เพราะ compiler หาฟังก์ชันใน namespace เดียวกับชนิดของพารามิเตอร์ให้เอง</p>
''', '''
<p>Expected result: the <code class="il">raw</code> line follows the pot with small jitter; the <code class="il">avg</code> line is smoother and follows slightly behind.</p>
<p>What the result tells you, one experiment at a time:</p>
<ul>
<li><b>Size fixed at build time</b>: change <code class="il">16</code> to <code class="il">64</code> and press Verify. <i>Global variables use</i> grows by exactly 96 bytes (48 more slots × 2 bytes per <code class="il">uint16_t</code>), because the buffer is a global the linker reserves up front (lesson 01), not heap memory taken at runtime.</li>
<li><b>Bigger N = smoother but slower</b>: upload with 64 and watch the Plotter. <code class="il">avg</code> is smoother but lags more (an N-point moving average delays the signal by about N/2 samples).</li>
<li><b><code class="il">static_assert</code></b>: change it to <code class="il">0</code> and press Verify. You get <code class="il">error: static assertion failed: N must be &gt; 0</code>: the bug is caught at compile time. Then set it back to 16.</li>
</ul>
<p class="note">Why <code class="il">xiao::RingBuffer</code>? The Seeed nRF52 core already has a class named <code class="il">RingBuffer</code>. Declaring the same name outside a namespace fails to compile because the names clash: exactly what namespaces from lesson 03 are for. <code class="il">average(samples)</code> needs no <code class="il">xiao::</code> because the compiler also looks in the namespace of the argument's type.</p>
''')
   + qa([(T('ถ้าใช้ RingBuffer&lt;uint16_t,16&gt; และ RingBuffer&lt;float,16&gt; flash จะเป็นอย่างไร?', 'What happens to flash if you use RingBuffer&lt;uint16_t,16&gt; and RingBuffer&lt;float,16&gt;?'),
          T('compiler สร้างโค้ด 2 ชุด ชุดละชนิด flash จึงเพิ่มขึ้น ถ้าใช้หลายชนิดมากเกินไป flash จะบวมโดยไม่รู้ตัว เรียกว่า code bloat', 'The compiler generates two copies of the code, one per type, so flash grows. Use too many types and flash swells unnoticed; that is called code bloat.')),
         (T('ถ้า ISR (บท 12) เป็นคน push และ loop เป็นคน pop ปลอดภัยไหม?', 'Is it safe if an ISR (lesson 12) pushes and loop pops?'),
          T('ยังไม่ปลอดภัย เพราะ count_ ถูกแก้จากทั้งสองฝั่ง ISR อาจแทรกเข้ามากลางการแก้ค่า ต้องครอบด้วย CriticalSection (บท 06) หรือออกแบบใหม่ให้ฝั่ง ISR แก้แค่ head และฝั่ง loop แก้แค่ tail', 'Not yet, because count_ is changed from both sides and the ISR may cut in halfway through an update. Wrap it in a CriticalSection (lesson 06), or redesign so the ISR only touches head and loop only touches tail.'))]))
