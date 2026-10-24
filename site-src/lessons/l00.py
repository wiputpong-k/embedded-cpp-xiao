SEEED_WIKI = 'https://wiki.seeedstudio.com/XIAO_BLE/'
SEEED_IMG = 'https://files.seeedstudio.com/wiki/XIAO-BLE/'
BOARD_FIGS = (photo(SEEED_IMG + 'xiaonrf52840sence.png', 829, 620, 'Seeed XIAO nRF52840 Sense',
                    T('บอร์ด Seeed XIAO nRF52840 Sense ที่ใช้ในคอร์สนี้', 'The Seeed XIAO nRF52840 Sense board used in this course'), 'Seeed Studio Wiki', SEEED_WIKI)
              + photo(SEEED_IMG + 'XIAO_nRF52840_Sense_front_pinout.png', 7680, 4320, 'XIAO nRF52840 Sense front pinout',
                      T('แผนผังขาของ XIAO nRF52840 Sense ด้านหน้า (กดที่รูปเพื่อดูขนาดเต็ม) ช่อง ARDUINO NAME แสดงเป็น "Mbed core / Non-Mbed core" คอร์สนี้ใช้ core แบบ non-mbed จึงใช้เลขหลัง',
                        'Front pinout of the XIAO nRF52840 Sense (click the image for full size). The ARDUINO NAME column reads "Mbed core / Non-Mbed core"; this course uses the non-mbed core, so use the second number.'),
                      'Seeed Studio Wiki', SEEED_WIKI))

lesson('00', 'S', T('ติดตั้งเครื่องมือ + Blink แรก', 'Install the tools + first Blink'), 30, BOARD, goal(T('IDE คอมไพล์และแฟลชบอร์ดได้ รู้ว่า LED บนบอร์ดเป็น active-LOW', 'The IDE compiles and flashes the board, and you know the on-board LED is active-LOW')) + T('''
<p>บทนี้เป็นบทติดตั้ง จึงใช้เวลานานกว่าบทอื่น ทำตามทีละขั้นจากบนลงล่าง ท้ายแต่ละขั้นมีวิธีเช็กว่าทำสำเร็จแล้ว ตัวอย่างเขียนสำหรับ Windows ถ้าใช้ macOS ให้ดูหมายเหตุในขั้นนั้น</p>
<h3>ขั้นที่ 1: ติดตั้ง Arduino IDE 2</h3>
<p>Arduino IDE คือโปรแกรมที่ใช้เขียนโค้ด compile และอัปโหลดลงบอร์ด</p>
<ol>
<li>เปิดหน้า <a href="https://www.arduino.cc/en/software">arduino.cc/en/software</a></li>
<li>ในหัวข้อ Arduino IDE 2 เลือกตัวติดตั้งของ Windows (Win 10 and newer) ถ้าหน้าเว็บขอรับบริจาค กด <b>Just Download</b> ได้เลย</li>
<li>เปิดไฟล์ที่ดาวน์โหลดมา กด Next ตามค่าเริ่มต้นจนจบ ถ้า Windows ถามว่าจะติดตั้ง driver ไหม ให้กด Install</li>
<li>เปิด Arduino IDE ครั้งแรก โปรแกรมอาจดาวน์โหลดส่วนประกอบเพิ่มสักครู่ ถ้า firewall ถามสิทธิ์ ให้กด Allow</li>
</ol>
<p class="note">เช็ก: เปิดโปรแกรมแล้วเห็นหน้าต่างที่มีโค้ด <code class="il">void setup()</code> และ <code class="il">void loop()</code> ว่าง ๆ</p>
<h3>ขั้นที่ 2: เพิ่มแหล่งดาวน์โหลดบอร์ด Seeed</h3>
<p>Arduino IDE ไม่มีบอร์ด XIAO มาให้ตั้งแต่แรก ต้องบอก IDE ก่อนว่าจะดาวน์โหลดข้อมูลบอร์ดของ Seeed จากที่ไหน</p>
<ol>
<li>ใน Arduino IDE กดเมนู <b>File → Preferences…</b> (macOS: <b>Arduino IDE → Settings…</b>) จะมีหน้าต่าง Preferences เปิดขึ้นมา</li>
<li>หาช่อง <b>Additional boards manager URLs</b> ซึ่งอยู่ใกล้ด้านล่างของหน้าต่าง</li>
<li>กดปุ่มคัดลอกที่ URL ข้างล่าง แล้ววางในช่องนั้น ถ้าในช่องมี URL อื่นอยู่แล้ว ให้กดไอคอนทางขวาของช่อง แล้ววางเป็นบรรทัดใหม่</li>
<li>กด <b>OK</b> เพื่อปิดหน้าต่าง</li>
</ol>''', '''
<p>This is the setup lesson, so it takes longer than the others. Work through the steps from top to bottom; each step ends with a way to check that it worked. The instructions are for Windows; macOS notes are given where they differ.</p>
<h3>Step 1: Install Arduino IDE 2</h3>
<p>Arduino IDE is the program you use to write code, compile it and upload it to the board.</p>
<ol>
<li>Open <a href="https://www.arduino.cc/en/software">arduino.cc/en/software</a></li>
<li>Under Arduino IDE 2, pick the Windows installer (Win 10 and newer). If the page asks for a donation, you can click <b>Just Download</b>.</li>
<li>Run the downloaded file and click Next through the defaults. If Windows asks whether to install a driver, click Install.</li>
<li>Start Arduino IDE. The first launch may download extra components; if the firewall asks for permission, click Allow.</li>
</ol>
<p class="note">Check: the program opens a window with empty <code class="il">void setup()</code> and <code class="il">void loop()</code> functions.</p>
<h3>Step 2: Add the Seeed board source</h3>
<p>Arduino IDE does not include the XIAO board out of the box. First you tell the IDE where to download Seeed's board package from.</p>
<ol>
<li>In Arduino IDE, open <b>File → Preferences…</b> (macOS: <b>Arduino IDE → Settings…</b>). The Preferences window opens.</li>
<li>Find the <b>Additional boards manager URLs</b> field near the bottom of the window.</li>
<li>Copy the URL below with its copy button and paste it into that field. If the field already has other URLs, click the icon on the right of the field and paste it on a new line.</li>
<li>Click <b>OK</b> to close the window.</li>
</ol>''') + code(SEEED_URL, 'Additional boards manager URLs') + T('''
<h3>ขั้นที่ 3: ติดตั้ง core ของบอร์ด</h3>
<p>core คือชุดไฟล์ที่ทำให้ IDE รู้จักบอร์ด รวมถึง compiler สำหรับชิป nRF52840</p>
<ol>
<li>เปิด <b>Boards Manager</b> โดยกดไอคอนรูปบอร์ดที่แถบซ้ายมือ (ไอคอนที่ 2 จากบน) หรือเมนู <b>Tools → Board → Boards Manager…</b></li>
<li>พิมพ์ <code class="il">seeed nrf52</code> ในช่องค้นหา จะเจอ 2 รายการ ให้เลือก <b>Seeed nRF52 Boards</b> ไม่ใช่ <i>Seeed nRF52 mbed-enabled Boards</i></li>
<li>กด <b>Install</b> แล้วรอ อาจใช้เวลาหลายนาทีเพราะต้องดาวน์โหลด compiler ด้วย ถ้ามีหน้าต่างถามเรื่อง driver ให้กด Install หรือ Yes</li>
</ol>
<p class="note">เลือก core แบบ non-mbed เพราะ build เร็วกว่าและใช้ BLE library ของ Adafruit ได้ เช็ก: รายการ Seeed nRF52 Boards ขึ้นคำว่า INSTALLED</p>
<h3>ขั้นที่ 4: ต่อบอร์ด แล้วเลือกบอร์ดกับพอร์ต</h3>
<ol>
<li>เสียบบอร์ดเข้าคอมด้วยสาย USB-C ที่ส่งข้อมูลได้ (สายที่มากับที่ชาร์จบางเส้นชาร์จได้อย่างเดียว)</li>
<li>กดเมนู <b>Tools → Board → Seeed nRF52 Boards → Seeed XIAO nRF52840 Sense</b></li>
<li>กดเมนู <b>Tools → Port</b> แล้วเลือกพอร์ตของบอร์ด (Windows เป็น <code class="il">COM</code> ตามด้วยตัวเลข เช่น COM5 macOS เป็น <code class="il">/dev/cu.usbmodem…</code>)</li>
</ol>
<p class="note">เช็ก: ถ้าไม่รู้ว่าพอร์ตไหนคือบอร์ด ให้ถอดสายแล้วเปิดเมนู Port ดูอีกครั้ง พอร์ตที่หายไปคือบอร์ด ถ้าไม่มีพอร์ตขึ้นเลย ให้ลองเปลี่ยนสาย USB</p>
''', '''
<h3>Step 3: Install the board core</h3>
<p>A core is the set of files that teaches the IDE about a board, including the compiler for the nRF52840 chip.</p>
<ol>
<li>Open <b>Boards Manager</b>: click the board icon in the left sidebar (second icon from the top), or use <b>Tools → Board → Boards Manager…</b></li>
<li>Type <code class="il">seeed nrf52</code> in the search box. Two entries appear; pick <b>Seeed nRF52 Boards</b>, not <i>Seeed nRF52 mbed-enabled Boards</i>.</li>
<li>Click <b>Install</b> and wait. It can take several minutes because it also downloads the compiler. If a window asks about a driver, click Install or Yes.</li>
</ol>
<p class="note">We use the non-mbed core because it builds faster and works with Adafruit's BLE library. Check: the Seeed nRF52 Boards entry shows INSTALLED.</p>
<h3>Step 4: Connect the board and pick the board and port</h3>
<ol>
<li>Plug the board into your computer with a USB-C cable that carries data (some charger cables only carry power).</li>
<li>Open <b>Tools → Board → Seeed nRF52 Boards → Seeed XIAO nRF52840 Sense</b></li>
<li>Open <b>Tools → Port</b> and pick the board's port (on Windows, <code class="il">COM</code> plus a number, e.g. COM5; on macOS, <code class="il">/dev/cu.usbmodem…</code>).</li>
</ol>
<p class="note">Check: if you are not sure which port is the board, unplug the cable and open the Port menu again; the port that disappeared is the board. If no port shows up at all, try another USB cable.</p>
''') + BOARD_FIGS + fig(SVG_PINOUT, T('แผนผังย่อ: ขาที่ใช้ในคอร์สนี้ (สีส้ม) GPIO เป็น 3.3 V ห้ามป้อน 5 V เข้าขา D', 'Simplified: the pins this course uses (orange). GPIO is 3.3 V. Never feed 5 V into a D pin.')) + T('''
<h3>Hands-on: Blink แรก</h3>
<ol>
<li>กดเมนู <b>File → New Sketch</b> จะได้หน้าต่างใหม่ที่มีโค้ดตั้งต้น</li>
<li>ลบโค้ดเดิมทั้งหมด แล้วกดปุ่ม <b>คัดลอก</b> ที่มุมขวาบนของโค้ดข้างล่าง มาวางแทน</li>
<li>กดเมนู <b>File → Save As…</b> แล้วตั้งชื่อ <code class="il">blink</code></li>
<li>กดปุ่ม <b>Verify</b> (เครื่องหมายถูกที่มุมซ้ายบน) เพื่อ compile ครั้งแรกอาจนานเป็นนาที รอจนเห็น <i>Done compiling</i> ที่ด้านล่าง</li>
<li>กดปุ่ม <b>Upload</b> (ลูกศรขวาถัดจาก Verify) แล้วรอจนเห็น <i>Done uploading</i></li>
</ol>''', '''
<h3>Hands-on: your first Blink</h3>
<ol>
<li>Open <b>File → New Sketch</b>. A new window opens with starter code.</li>
<li>Delete all of that code, click the <b>Copy</b> button at the top right of the code below, and paste it in.</li>
<li>Open <b>File → Save As…</b> and name it <code class="il">blink</code>.</li>
<li>Click <b>Verify</b> (the check mark at the top left) to compile. The first compile can take a minute; wait for <i>Done compiling</i> at the bottom.</li>
<li>Click <b>Upload</b> (the right arrow next to Verify) and wait for <i>Done uploading</i>.</li>
</ol>''') + code('''// LED บนบอร์ดต่อขั้วบวกไว้ที่ 3V3 จึงติดเมื่อเขียน LOW
void setup() {
  pinMode(LED_RED, OUTPUT);
  digitalWrite(LED_RED, HIGH);   // ดับ
}

void loop() {
  digitalWrite(LED_RED, LOW);    // ติด
  delay(200);
  digitalWrite(LED_RED, HIGH);   // ดับ
  delay(800);
}''', 'blink.ino', en={'// LED บนบอร์ดต่อขั้วบวกไว้ที่ 3V3 จึงติดเมื่อเขียน LOW': '// The on-board LED anode is tied to 3V3, so it lights when you write LOW',
                      '// ดับ': '// off', '// ติด': '// on'}) + T('''
<p>ผลที่ควรเห็น: LED สีแดงบนบอร์ดกระพริบ ติด 0.2 วินาที ดับ 0.8 วินาที วนไปเรื่อย ๆ</p>
<p class="note">ถ้าอัปโหลดไม่ผ่าน: กดปุ่ม reset บนบอร์ด (ปุ่มเล็กข้างช่อง USB) 2 ครั้งเร็ว ๆ บอร์ดจะเข้าโหมด bootloader (Windows อาจเห็นไดรฟ์ใหม่ขึ้นมา) จากนั้นเปิด <b>Tools → Port</b> เลือกพอร์ตใหม่ เพราะเลขพอร์ตอาจเปลี่ยน แล้วกด Upload อีกครั้ง</p>
<h3>ลองต่อ</h3>
<ol>
<li>เปลี่ยน <code class="il">LED_RED</code> เป็น <code class="il">LED_GREEN</code> หรือ <code class="il">LED_BLUE</code> ให้ครบทั้ง 3 จุด แล้ว Upload ใหม่ สีของ LED ต้องเปลี่ยนตาม</li>
<li>เปิด <b>File → Preferences…</b> ติ๊กช่อง <b>Show verbose output during: compile</b> กด OK แล้วกด Verify อีกครั้ง หน้าต่าง Output ด้านล่างจะแสดงคำสั่ง compiler ที่ IDE เรียกจริง บท 01 จะอธิบายว่าแต่ละคำสั่งทำอะไร</li>
</ol>
''', '''
<p>What you should see: the red LED on the board blinks, on for 0.2 s and off for 0.8 s, over and over.</p>
<p class="note">If the upload fails: double-press the reset button on the board (the tiny button next to the USB port) quickly. The board enters bootloader mode (Windows may show a new drive). Then open <b>Tools → Port</b> and pick the port again, because its number may change, and click Upload again.</p>
<h3>Try next</h3>
<ol>
<li>Change <code class="il">LED_RED</code> to <code class="il">LED_GREEN</code> or <code class="il">LED_BLUE</code> in all three places and upload again. The LED color should change.</li>
<li>Open <b>File → Preferences…</b>, tick <b>Show verbose output during: compile</b>, click OK and click Verify again. The Output panel at the bottom shows the compiler commands the IDE actually runs; lesson 01 explains what each one does.</li>
</ol>
''') + qa([(T('ทำไม LED_RED ติดตอนเขียน LOW?', 'Why does LED_RED light when you write LOW?'),
           T('LED ต่อแบบ active-LOW: ขั้วบวกอยู่ที่ 3V3 ขา GPIO ทำหน้าที่ sink กระแส เมื่อขาเป็น LOW จึงมีกระแสไหล', 'The LED is active-LOW: its anode sits at 3V3 and the GPIO pin sinks the current, so current flows when the pin is LOW.')),
          (T('ทำไมต้องใช้ core non-mbed ในคอร์สนี้?', 'Why use the non-mbed core in this course?'),
           T('build เร็วกว่า ใช้ Bluefruit BLE ได้ และ compile ใน CI ได้ง่าย ทั้งสอง core เขียน C++ ได้เหมือนกัน', 'It builds faster, supports Bluefruit BLE and is easy to compile in CI. Both cores run the same C++.'))]))
