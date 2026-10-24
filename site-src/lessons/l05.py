lesson('05', 'A', T('แยกโค้ดเป็นหลายไฟล์: header และ src/', 'Split code into files: headers and src/'), 25, 'LED + R 1 kΩ', goal(T('ย้าย class Led ไปไว้ในไฟล์ <code class="il">src/Led.h</code> เพื่อใช้ซ้ำในบทหลัง ๆ', 'Move the Led class into <code class="il">src/Led.h</code> so later lessons can reuse it'))
   + vs(T('แยก <code class="il">.h</code> (ประกาศ) กับ <code class="il">.c</code> (ตัวฟังก์ชัน) และกัน include ซ้ำด้วย <code class="il">#ifndef</code> guard', 'Split into <code class="il">.h</code> (declarations) and <code class="il">.c</code> (function bodies), and guard against double includes with <code class="il">#ifndef</code>.'),
        T('class ที่เขียนตัวฟังก์ชันไว้ในตัว class อยู่ใน <code class="il">.h</code> ไฟล์เดียวได้ เพราะฟังก์ชันแบบนี้เป็น inline โดยอัตโนมัติ กัน include ซ้ำด้วย <code class="il">#pragma once</code> บรรทัดเดียว', 'A class whose member functions are written inside the class body can live in a single <code class="il">.h</code>, because those functions are implicitly inline. One line of <code class="il">#pragma once</code> guards against double includes.'))
   + T('''
<ul>
<li><b>header (.h)</b> ไฟล์ที่ <code class="il">#include</code> เข้าไปในไฟล์อื่น preprocessor แปะเนื้อหาทั้งไฟล์ลงตรงบรรทัด <code class="il">#include</code> จริง ๆ ไม่ได้ compile แยกเป็น <code class="il">.o</code> ของตัวเอง (บท 01)</li>
<li><b>include guard / <code class="il">#pragma once</code></b> กันไม่ให้ header เดียวถูกแปะซ้ำ 2 ครั้งในไฟล์เดียวกัน ซึ่งจะทำให้ class ถูกประกาศซ้ำแล้ว compile ไม่ผ่าน</li>
<li><b>inline</b> ในบทนี้หมายถึง "ยอมให้ฟังก์ชันนี้มีตัวเต็มอยู่ในหลาย <code class="il">.o</code> ได้" linker จะเก็บไว้ตัวเดียว ฟังก์ชันที่เขียนไว้ใน <code class="il">{ }</code> ของ class เป็นแบบนี้โดยอัตโนมัติ</li>
</ul>
<p>เมื่อโปรเจกต์ใหญ่ขึ้น การเก็บทุกอย่างไว้ในไฟล์ <code class="il">.ino</code> เดียวจะอ่านยาก และนำไปใช้ซ้ำไม่ได้ Arduino จะ compile ทุกไฟล์ในโฟลเดอร์ <code class="il">src/</code> ที่อยู่ในโฟลเดอร์ sketch ให้อัตโนมัติ คอร์สนี้จึงเก็บ class ที่ใช้ซ้ำไว้ใน <code class="il">src/</code> ตั้งแต่บทนี้ไปจนถึงบท 13</p>
<p class="note">Arduino IDE 2 แสดงเป็นแท็บเฉพาะไฟล์ที่อยู่ชั้นบนสุดของโฟลเดอร์ sketch ไฟล์ใน <code class="il">src/</code> จะไม่ขึ้นเป็นแท็บ ต้องแก้ด้วยโปรแกรมอื่น เช่น VS Code หรือ Notepad แต่ IDE ยัง compile ไฟล์เหล่านี้ตามปกติ</p>
<h3>Hands-on</h3>
<p>บทนี้พิสูจน์ว่าการแยกไฟล์เปลี่ยนแค่การจัดระเบียบโค้ด ไม่เปลี่ยนโปรแกรมที่ได้</p>
<ol>
<li>เปิด sketch <code class="il">led_class</code> จากบทที่แล้ว (<b>File → Open…</b> หรือ <b>File → Sketchbook</b>)</li>
<li>กด <b>Sketch → Show Sketch Folder</b> จะเปิดโฟลเดอร์ของ sketch ใน File Explorer</li>
<li>ถ้ายังมองไม่เห็นนามสกุลไฟล์ ให้เปิดใน File Explorer: <b>View → Show → File name extensions</b></li>
<li>สร้างโฟลเดอร์ใหม่ชื่อ <code class="il">src</code> แล้วเข้าไปในโฟลเดอร์นั้น คลิกขวา <b>New → Text Document</b> เปลี่ยนชื่อเป็น <code class="il">Led.h</code> (ต้องลบ <code class="il">.txt</code> ออกด้วย) ถ้า Windows ถามเรื่องเปลี่ยนนามสกุล ให้กด Yes</li>
<li>คลิกขวาที่ <code class="il">Led.h</code> แล้วเปิดด้วย VS Code หรือ Notepad คัดลอกโค้ด <code class="il">src/Led.h</code> ข้างล่างไปวาง แล้วบันทึก</li>
<li>กลับมาที่ Arduino IDE แทนที่โค้ดใน <code class="il">led_class.ino</code> ทั้งหมดด้วยโค้ดชุดที่สองข้างล่าง แล้วกด <b>Upload</b> ผลต้องเหมือนบทที่แล้วทุกอย่าง</li>
</ol>''', '''
<ul>
<li><b>header (.h)</b>: a file that is <code class="il">#include</code>d into other files. The preprocessor literally pastes its whole content at the <code class="il">#include</code> line; it is not compiled into a <code class="il">.o</code> of its own (lesson 01).</li>
<li><b>include guard / <code class="il">#pragma once</code></b>: stops one header from being pasted twice into the same file, which would declare the class twice and fail to compile.</li>
<li><b>inline</b>: here it means "this function's full body may appear in several <code class="il">.o</code> files"; the linker keeps one. Functions written inside a class's <code class="il">{ }</code> are inline automatically.</li>
</ul>
<p>As a project grows, keeping everything in one <code class="il">.ino</code> file gets hard to read and impossible to reuse. Arduino automatically compiles every file in a <code class="il">src/</code> folder inside the sketch folder, so from this lesson through lesson 13 the course keeps reusable classes in <code class="il">src/</code>.</p>
<p class="note">Arduino IDE 2 only shows tabs for files at the top level of the sketch folder. Files in <code class="il">src/</code> do not appear as tabs, so edit them with another program such as VS Code or Notepad. The IDE still compiles them as usual.</p>
<h3>Hands-on</h3>
<p>This lesson proves that splitting files only changes how the code is organized, not the program you get.</p>
<ol>
<li>Open the <code class="il">led_class</code> sketch from the previous lesson (<b>File → Open…</b> or <b>File → Sketchbook</b>).</li>
<li>Click <b>Sketch → Show Sketch Folder</b>. The sketch folder opens in File Explorer.</li>
<li>If you cannot see file extensions, turn them on in File Explorer: <b>View → Show → File name extensions</b>.</li>
<li>Create a new folder named <code class="il">src</code> and open it. Right-click, choose <b>New → Text Document</b>, and rename it to <code class="il">Led.h</code> (remove the <code class="il">.txt</code> too). If Windows asks about changing the extension, click Yes.</li>
<li>Right-click <code class="il">Led.h</code>, open it with VS Code or Notepad, paste the <code class="il">src/Led.h</code> code below and save.</li>
<li>Back in Arduino IDE, replace everything in <code class="il">led_class.ino</code> with the second code block below and click <b>Upload</b>. It should behave exactly like the previous lesson.</li>
</ol>''') + code('#pragma once\n#include <Arduino.h>\n\n' + LED_CLASS, 'src/Led.h', en=LED_CLASS_EN)
   + code('#include "src/Led.h"\n\n' + LED_MAIN, 'led_class.ino', en=LED_MAIN_EN) + T('''
<p><code class="il">#include "src/Led.h"</code> ใช้เครื่องหมายคำพูด แปลว่าให้หาไฟล์จากโฟลเดอร์ของ sketch ก่อน ส่วน <code class="il">#include &lt;Arduino.h&gt;</code> ใช้วงเล็บมุม แปลว่าหาจาก library และ core ที่ติดตั้งไว้ ไฟล์ <code class="il">Led.h</code> ต้อง include <code class="il">Arduino.h</code> เอง เพราะ IDE เติมให้เฉพาะไฟล์ <code class="il">.ino</code></p>
<p>ผลนี้บอกอะไร: LED กระพริบเหมือนเดิม และถ้าดูบรรทัด <i>Sketch uses … bytes</i> กับ <i>Global variables use …</i> ในแถบ Output จะได้ตัวเลข<b>เท่ากับบท 04 ทุก byte</b> เพราะ <code class="il">#include</code> แปะโค้ด class เดิมกลับเข้าไปใน <code class="il">led_class.ino.cpp</code> compiler จึงได้โค้ดชุดเดียวกัน</p>
''', '''
<p><code class="il">#include "src/Led.h"</code> uses quotes, which means "look in the sketch folder first". <code class="il">#include &lt;Arduino.h&gt;</code> uses angle brackets, which means "look in the installed libraries and core". <code class="il">Led.h</code> has to include <code class="il">Arduino.h</code> itself, because the IDE only adds it to <code class="il">.ino</code> files.</p>
<p>What the result tells you: the LED blinks as before, and the <i>Sketch uses … bytes</i> and <i>Global variables use …</i> lines in the Output panel match lesson 04 <b>to the byte</b>, because <code class="il">#include</code> pastes the same class code back into <code class="il">led_class.ino.cpp</code>, so the compiler sees identical code.</p>
''') + qa([(T('ถ้าลบ #pragma once ออก แล้ว include Led.h จาก 2 ไฟล์ที่ include ต่อกัน จะเกิดอะไรขึ้น?', 'What happens if you remove #pragma once and Led.h ends up included twice through other headers?'),
           T('compiler เห็น class Led ถูกประกาศ 2 ครั้งใน translation unit เดียว (ไฟล์ .cpp หนึ่งไฟล์รวมกับ header ทั้งหมดที่ include เข้ามา = สิ่งที่ compile เป็น .o หนึ่งไฟล์) แล้ว error ว่า redefinition #pragma once (หรือ #ifndef guard) ทำให้ไฟล์ถูกอ่านแค่ครั้งเดียว', 'The compiler sees class Led defined twice in one translation unit (one .cpp file plus every header it includes, i.e. what becomes one .o) and reports a redefinition error. #pragma once (or an #ifndef guard) makes the file be read only once.')),
          (T('ทำไมเขียนตัวฟังก์ชันไว้ใน Led.h แล้ว include จากหลายไฟล์ .cpp ได้โดยไม่ error multiple definition?', 'Why can Led.h contain function bodies and be included from several .cpp files without a multiple-definition error?'),
           T('ฟังก์ชันที่เขียนไว้ใน class body เป็น inline โดยอัตโนมัติ linker จึงยอมให้มีหลายสำเนาและเลือกใช้ตัวเดียว ถ้าเขียนฟังก์ชันธรรมดานอก class ไว้ใน .h ต้องใส่ inline เอง', 'Member functions defined inside the class body are implicitly inline, so the linker accepts the copies and keeps one. A plain function written outside a class in a .h needs inline added by hand.'))])
   + iv(T('เมื่อโปรเจกต์มีหลายไฟล์ ลำดับที่ object global ของแต่ละไฟล์ถูกสร้างไม่แน่นอน ถ้า constructor ของ object หนึ่งไปใช้ object ในอีกไฟล์ อาจเจอตัวที่ยังไม่ถูกสร้าง (เรียกกันว่า static initialization order fiasco) ทางแก้ที่คอร์สนี้ใช้คือให้ constructor แค่เก็บค่า แล้วทำงานจริงใน begin() ที่เรียกจาก setup()',
          'In a multi-file project, the order in which the global objects of each file are constructed is not defined. If the constructor of one object uses an object from another file, that object may not exist yet (the "static initialization order fiasco"). The fix used in this course: constructors only store values, and the real work happens in begin(), called from setup().')))
