lesson('24', 'C', T('Capstone และทบทวน', 'Capstone and review'), 30, T('ทั้งหมด', 'Everything'), goal(T('ปิด repo ให้สมบูรณ์ และทบทวนแนวคิดหลักของทั้งคอร์ส', 'Finish the repo, and review the key ideas of the whole course')) + T('''
<h3>Checklist ของ repo</h3>
<ul class="check">
<li>README: รูป wiring, ตารางขา, วิธี build ในเครื่อง, วิธีรัน test, badge CI</li>
<li>โครงสร้าง <code class="il">firmware/</code>, <code class="il">firmware/src/</code>, <code class="il">test/</code>, <code class="il">.github/workflows/</code></li>
<li>อย่างน้อย 1 release (v0.1.0) และประวัติ commit ที่ใช้ Conventional Commits</li>
<li>เพิ่ม test ของคุณเอง 1 ชุด เช่น ทดสอบ <code class="il">pushOverwrite()</code> ตอน buffer ยังไม่เต็ม</li>
<li>ฟีเจอร์ต่อยอด 1 อย่าง: กดค้าง 1 วินาที = reset ค่า (เพิ่ม Event::LongPress ใน Debouncer พร้อม test)</li>
</ul>
<h3>คำถามทบทวนก่อนจบคอร์ส</h3>
''', '''
<h3>Repo checklist</h3>
<ul class="check">
<li>README: wiring photo, pin table, how to build locally, how to run the tests, CI badge</li>
<li>Layout: <code class="il">firmware/</code>, <code class="il">firmware/src/</code>, <code class="il">test/</code>, <code class="il">.github/workflows/</code></li>
<li>At least one release (v0.1.0) and a commit history that uses Conventional Commits</li>
<li>One test suite of your own, e.g. testing <code class="il">pushOverwrite()</code> while the buffer is not yet full</li>
<li>One extra feature: hold for 1 second = reset (add Event::LongPress to the Debouncer, with tests)</li>
</ul>
<h3>Review questions</h3>
''') + ''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in [
 (T('C++ ต่างจาก C ในงาน embedded อย่างไร มีต้นทุนอะไรบ้าง?', 'How does C++ differ from C in embedded work, and what does it cost?'),
  T('ได้ class, RAII, reference, template, constexpr, enum class, namespace ที่ส่วนใหญ่ไม่มี runtime cost ส่วนที่มีต้นทุนคือ virtual (vtable), exceptions, RTTI, heap ผ่าน STL บางตัว จึงเลือกใช้เป็น subset', 'You get classes, RAII, references, templates, constexpr, enum class and namespaces, mostly with no runtime cost. The costly parts are virtual (vtables), exceptions, RTTI and heap use through some STL types, so teams use a subset.')),
 (T('volatile ใช้เมื่อไหร่ และไม่ได้ช่วยอะไร?', 'When do you use volatile, and what does it not do?'),
  T('ตัวแปรที่ ISR แก้, register ของ peripheral, ข้อมูลที่แชร์ระหว่าง context ไม่ได้ทำให้ atomic และไม่ใช่ memory barrier', 'For variables changed by an ISR, peripheral registers and data shared between contexts. It does not make anything atomic and it is not a memory barrier.')),
 (T('ISR ที่ดีเป็นอย่างไร?', 'What makes a good ISR?'),
  T('สั้น, ไม่ block, ไม่จอง memory, ตั้ง flag หรือ push ลง ring buffer แล้วให้ main/task ประมวลผล ข้อมูลที่แชร์ต้องป้องกันด้วย critical section', 'Short, non-blocking, no allocation. It sets a flag or pushes into a ring buffer and leaves the processing to main or a task. Shared data must be protected with a critical section.')),
 (T('ทำไมเลี่ยง dynamic allocation หลัง init?', 'Why avoid dynamic allocation after init?'),
  T('fragmentation, เวลาไม่แน่นอน, และ fail ได้ตอนรันไปนาน ๆ ระบบที่ต้องทำงานต่อเนื่องจึงจองทุกอย่างแบบ static', 'Fragmentation, unpredictable timing, and failures after long run times. Systems that must run continuously allocate everything statically.')),
 (T('อธิบาย RAII พร้อมตัวอย่าง', 'Explain RAII with an example'),
  T('ผูกอายุ resource กับ object: CriticalSection ปิด interrupt ใน ctor คืนค่าใน dtor ออกจาก scope ทางไหนก็คืนเสมอ', 'Tie a resource\'s lifetime to an object: CriticalSection disables interrupts in its ctor and restores them in its dtor, however you leave the scope.')),
 (T('debounce มีกี่วิธี?', 'What are the ways to debounce?'),
  T('ฮาร์ดแวร์ (RC + Schmitt trigger) และซอฟต์แวร์ (รอให้นิ่งตามเวลา หรือ sample หลายครั้ง) เลือกตามต้นทุน BOM กับ CPU', 'Hardware (RC + Schmitt trigger) and software (wait until stable for a set time, or sample several times). Choose based on BOM cost versus CPU time.')),
 (T('merge กับ rebase เลือกอย่างไร?', 'How do you choose between merge and rebase?'),
  T('merge เก็บประวัติจริงและปลอดภัยกับ branch ที่แชร์ rebase ทำประวัติเส้นตรง ใช้กับ branch ส่วนตัวก่อนเปิด PR', 'merge keeps the real history and is safe on shared branches. rebase gives a straight-line history; use it on private branches before opening a PR.')),
 (T('pipeline CI/CD ของ firmware ควรมีอะไร?', 'What should a firmware CI/CD pipeline include?'),
  T('build ทุก target, unit test บน host, static analysis, เก็บ artifact, release ตาม tag พร้อมเวอร์ชันฝังใน binary, ขั้นต่อไปคือ HIL test บน runner ที่ต่อบอร์ดจริง', 'Builds for every target, host unit tests, static analysis, stored artifacts, and tag-based releases with the version built into the binary. The next step is HIL tests on a runner wired to real boards.')),
]) + fig(SVG_ROAD, T('เส้นทางต่อหลังจบคอร์ส', 'Where to go after this course'))
   + iv(T('ประสบการณ์ PCB, failure analysis และ V&amp;V ช่วยงาน firmware ได้มาก ใน README หรือ design note ให้เชื่อม 2 ฝั่ง เช่น อธิบายว่าเลือกค่า R ของ LED และ debounce time จากอะไร คนที่มาอ่านโค้ดทีหลังจะเข้าใจเหตุผล ไม่ใช่เห็นแค่ตัวเลข',
          'PCB, failure analysis and V&amp;V experience helps firmware work a lot. Connect both sides in the README or a design note, e.g. explain how you chose the LED resistor and the debounce time, so later readers understand the reasoning, not just the numbers.')))
