lesson('20', 'C', T('เขียน unit test เอง', 'Write your own unit tests'), 25, PC, goal(T('เข้าใจว่า test_main.cpp ทำงานอย่างไร ทำให้ test แดงเป็น และเพิ่ม test ใหม่เองได้', 'Understand how test_main.cpp works, make a test fail on purpose, and add a new test yourself')) + T('''
<h3>test_main.cpp ทำงานอย่างไร</h3>
<ul>
<li><code class="il">CHECK(cond)</code> เป็น macro ที่ถ้า <code class="il">cond</code> เป็นเท็จ จะพิมพ์ชื่อไฟล์ (<code class="il">__FILE__</code>) เลขบรรทัด (<code class="il">__LINE__</code>) และตัวเงื่อนไขเป็นข้อความ (<code class="il">#cond</code>) แล้วนับจำนวนที่ fail ไว้</li>
<li>ครอบด้วย <code class="il">do { … } while (0)</code> เพื่อให้ macro ใช้ได้เหมือนคำสั่งเดียว แม้วางอยู่ใน <code class="il">if</code> ที่ไม่มีวงเล็บปีกกา</li>
<li>แต่ละ test เป็นฟังก์ชันแยก (<code class="il">test_ringbuffer</code>, <code class="il">test_debouncer</code>) <code class="il">main()</code> เรียกทุกตัว แล้วคืน exit code ตามผล</li>
<li><code class="il">test_debouncer</code> ส่งเวลาปลอม 0, 5, 8, 20, 28 ms เข้าไปเอง จึงทดสอบกรณีเด้งได้แม่นยำทุกครั้ง ซึ่งทำบนบอร์ดจริงด้วยมือแทบไม่ได้</li>
</ul>
<h3>Hands-on 1: ทำให้ test แดง</h3>
<ol>
<li>เปิด <code class="il">firmware/src/Debouncer.h</code> แก้ <code class="il">&gt;= stableMs_</code> เป็น <code class="il">&gt; stableMs_</code></li>
<li>compile และรัน test ใหม่ (คำสั่งเดียวกับบท 19) จะเห็นบรรทัด <code class="il">FAIL …</code> บอกไฟล์และเลขบรรทัดที่พัง และไม่มีข้อความ ALL TESTS PASSED</li>
<li>รัน <code class="il">echo $?</code> ทันทีหลังรัน test จะเห็นเลข 1 (exit code ของการ fail)</li>
<li>แก้กลับเป็น <code class="il">&gt;=</code> แล้วรันใหม่ให้ผ่าน</li>
</ol>
<h3>Hands-on 2: เพิ่ม test ของคุณเอง</h3>
<p>เพิ่มฟังก์ชันข้างล่างไว้เหนือ <code class="il">main()</code> ใน <code class="il">test/test_main.cpp</code> แล้วเพิ่มบรรทัด <code class="il">test_average_empty();</code> และ <code class="il">test_debouncer_release();</code> ใน <code class="il">main()</code> ต่อจาก test เดิม รันให้ผ่าน แล้ว commit</p>
''', '''
<h3>How test_main.cpp works</h3>
<ul>
<li><code class="il">CHECK(cond)</code> is a macro. If <code class="il">cond</code> is false, it prints the file name (<code class="il">__FILE__</code>), the line number (<code class="il">__LINE__</code>) and the condition as text (<code class="il">#cond</code>), and counts the failure.</li>
<li>It is wrapped in <code class="il">do { … } while (0)</code> so the macro behaves like a single statement, even inside an <code class="il">if</code> without braces.</li>
<li>Each test is its own function (<code class="il">test_ringbuffer</code>, <code class="il">test_debouncer</code>). <code class="il">main()</code> calls them all and returns an exit code based on the result.</li>
<li><code class="il">test_debouncer</code> feeds in fake times of 0, 5, 8, 20 and 28 ms, so it tests bouncing precisely every time, which is almost impossible to do by hand on a real board.</li>
</ul>
<h3>Hands-on 1: make a test fail</h3>
<ol>
<li>Open <code class="il">firmware/src/Debouncer.h</code> and change <code class="il">&gt;= stableMs_</code> to <code class="il">&gt; stableMs_</code>.</li>
<li>Compile and run the tests again (same commands as lesson 19). You see a <code class="il">FAIL …</code> line with the file and line number, and no ALL TESTS PASSED.</li>
<li>Run <code class="il">echo $?</code> right after the test run. It prints 1, the failure exit code.</li>
<li>Change it back to <code class="il">&gt;=</code> and run again until it passes.</li>
</ol>
<h3>Hands-on 2: add your own tests</h3>
<p>Add the functions below above <code class="il">main()</code> in <code class="il">test/test_main.cpp</code>, then add <code class="il">test_average_empty();</code> and <code class="il">test_debouncer_release();</code> to <code class="il">main()</code> after the existing tests. Make them pass, then commit.</p>
''') + code('''static void test_average_empty() {
  RingBuffer<int, 4> rb;
  CHECK(average(rb) == 0.0f);      // ว่าง → 0 ไม่หารด้วยศูนย์
}

static void test_debouncer_release() {
  using E = Debouncer::Event;
  Debouncer d(20);
  d.update(true, 0);
  CHECK(d.update(true, 20) == E::Pressed);
  CHECK(d.update(false, 30) == E::None);      // เพิ่งปล่อย ยังไม่นิ่ง
  CHECK(d.update(false, 50) == E::Released);  // นิ่งครบ 20 ms
  CHECK(!d.isPressed());
}''', 'test/test_main.cpp', en={'// ว่าง → 0 ไม่หารด้วยศูนย์': '// empty → 0, no divide by zero',
                                '// เพิ่งปล่อย ยังไม่นิ่ง': '// just released, not stable yet', '// นิ่งครบ 20 ms': '// stable for 20 ms'}) + T('''
<p class="note">ในงานจริงใช้ framework เช่น GoogleTest, Catch2 หรือ Unity (สำหรับ C) แต่หลักการเหมือนกัน: CHECK เงื่อนไข, รายงานบรรทัดที่พัง, exit code ≠ 0 เมื่อ fail เพื่อให้ CI รู้</p>
''', '''
<p class="note">Real projects use a framework such as GoogleTest, Catch2 or Unity (for C), but the idea is the same: CHECK a condition, report the failing line, and exit with a non-zero code on failure so CI knows.</p>
''') + qa([(T('จะ test โค้ดที่เรียก digitalRead() ได้อย่างไร?', 'How do you test code that calls digitalRead()?'),
           T('ซ่อนการเข้าถึงฮาร์ดแวร์ไว้หลัง interface (เช่น ISensor บท 09) แล้วใส่ fake/mock ตอน test หรือส่งค่าที่อ่านได้เข้าฟังก์ชันแทนให้ฟังก์ชันไปอ่านเอง', 'Hide hardware access behind an interface (like ISensor in lesson 09) and plug in a fake/mock for tests, or pass the value in instead of letting the function read it.')),
          (T('test ที่ดีควรเป็นอย่างไร?', 'What makes a good test?'),
           T('เร็ว ผลเหมือนเดิมทุกครั้ง ทดสอบทีละเรื่อง และอ่านแล้วรู้ว่าคาดหวังอะไร รวมถึงกรณีขอบ เช่น buffer ว่าง buffer เต็ม และเวลา overflow', 'Fast, gives the same result every run, tests one thing, and reads clearly as an expectation. Include edge cases such as an empty buffer, a full buffer and time overflow.'))])
   + iv(T('ทีม firmware ส่วนใหญ่ test เป็นชั้น: unit test บน host สำหรับ logic, HIL test บนบอร์ดจริงสำหรับ driver, system test สำหรับฟีเจอร์ ชั้นแรกเร็วและถูกที่สุด จึงรันใน CI ทุก commit',
          'Most firmware teams test in layers: host unit tests for logic, HIL tests on real boards for drivers, and system tests for features. The first layer is the fastest and cheapest, so it runs in CI on every commit.')))
