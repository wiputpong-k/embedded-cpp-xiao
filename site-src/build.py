import html, os, runpy
D = os.path.dirname(os.path.abspath(__file__))
LANGS = ('th', 'en')
# Running `python build.py` re-runs this file once per language with LANG preset.
if 'LANG' not in globals():
    for l in LANGS: runpy.run_path(os.path.abspath(__file__), init_globals={'LANG': l}, run_name='__build__')
    raise SystemExit
def T(th, en=None):
    """Bilingual text: Thai is the source; English falls back to Thai until translated."""
    return en if LANG == 'en' and en is not None else th
def rd(p): return open(os.path.join(D, 'hw', p), encoding='utf-8').read().rstrip()
RING, DEB, TEST = rd('firmware/src/RingBuffer.h'), rd('firmware/src/Debouncer.h'), rd('test/test_main.cpp')

def code(txt, label=''):
    lab = f'<div class="cl">{label}</div>' if label else ''
    return f'<div class="code">{lab}<pre><code>{html.escape(txt.strip(chr(10)))}</code></pre></div>'

def fig(svg, cap):
    return f'<figure class="dg"><div class="sv">{svg}</div><figcaption>{cap}</figcaption></figure>'

def flow(steps, labels=None, w=400):
    """steps: (title, sub, cls) vertical box-arrow flow"""
    labels = labels or []
    y, out = 10, []
    for i, (t, s, c) in enumerate(steps):
        h = 50 if s else 34
        out.append(f'<rect x="40" y="{y}" width="320" height="{h}" rx="8" class="{c or "b"}"/>')
        if s:
            out.append(f'<text x="200" y="{y+21}" text-anchor="middle" class="tt">{html.escape(t)}</text>')
            out.append(f'<text x="200" y="{y+39}" text-anchor="middle" class="sub">{html.escape(s)}</text>')
        else:
            out.append(f'<text x="200" y="{y+22}" text-anchor="middle" class="tt">{html.escape(t)}</text>')
        y += h
        if i < len(steps) - 1:
            gap = 30
            out.append(f'<line x1="200" y1="{y+2}" x2="200" y2="{y+gap-4}" class="ln" marker-end="url(#ah)"/>')
            if i < len(labels) and labels[i]:
                out.append(f'<text x="212" y="{y+19}" class="sub m">{html.escape(labels[i])}</text>')
            y += gap
    return f'<svg viewBox="0 0 {w} {y+10}" role="img">{"".join(out)}</svg>'

# ---------------- hand-drawn diagrams ----------------
def pin(x, y, label, side, hl=False):
    c = 'pa' if hl else 'pn'
    tx = x - 14 if side == 'L' else x + 14
    an = 'end' if side == 'L' else 'start'
    cls = 'tt acc' if hl else 'tt'
    return f'<circle cx="{x}" cy="{y}" r="6" class="{c}"/><text x="{tx}" y="{y+4}" text-anchor="{an}" class="{cls} m">{label}</text>'

L = ['D0 / A0', 'D1', 'D2', 'D3', 'D4 / SDA', 'D5 / SCL', 'D6 / TX']
R = ['5V', 'GND', '3V3', 'D10 / MOSI', 'D9 / MISO', 'D8 / SCK', 'D7 / RX']
pins = ''.join(pin(152, 76 + i*28, l, 'L', i < 3) for i, l in enumerate(L)) + ''.join(pin(248, 76 + i*28, r, 'R', i in (1, 2)) for i, r in enumerate(R))
SVG_PINOUT = f'''<svg viewBox="0 0 400 300" role="img">
<rect x="178" y="24" width="44" height="22" rx="5" class="b"/><text x="200" y="39" text-anchor="middle" class="sub m">USB-C</text>
<rect x="140" y="44" width="120" height="226" rx="12" class="bm"/>
<circle cx="200" cy="66" r="7" class="pa"/><text x="200" y="92" text-anchor="middle" class="sub">RGB LED</text><text x="200" y="105" text-anchor="middle" class="sub">active-LOW</text>
<text x="200" y="245" text-anchor="middle" class="tt m">XIAO</text><text x="200" y="260" text-anchor="middle" class="sub m">nRF52840</text>
{pins}
<text x="8" y="292" class="sub">สีส้ม = ขาที่ใช้ในคอร์ส: D0 Pot · D1 ปุ่ม · D2 LED ภายนอก</text>
</svg>'''

SVG_REF = '''<svg viewBox="0 0 400 190" role="img">
<text x="205" y="22" text-anchor="middle" class="sub m">current @ 0x2000_0104</text>
<rect x="150" y="30" width="110" height="46" rx="8" class="ba"/><text x="205" y="59" text-anchor="middle" class="tt m">2</text>
<rect x="14" y="120" width="140" height="42" rx="8" class="b"/><text x="84" y="138" text-anchor="middle" class="tt m">size_t* p</text><text x="84" y="154" text-anchor="middle" class="sub m">= 0x2000_0104</text>
<path d="M84 118 C84 90 120 70 148 60" class="ln" marker-end="url(#ah)"/>
<rect x="252" y="120" width="140" height="42" rx="8" class="b dash"/><text x="322" y="138" text-anchor="middle" class="tt m">size_t&amp; idx</text><text x="322" y="154" text-anchor="middle" class="sub">ชื่อเล่นของ current</text>
<path d="M300 118 C300 95 270 85 262 72" class="la" marker-end="url(#aha)"/>
<text x="84" y="182" text-anchor="middle" class="sub">เป็นตัวแปรแยก · null ได้ · ชี้ใหม่ได้</text>
<text x="322" y="182" text-anchor="middle" class="sub">ไม่ใช่ตัวแปรใหม่ · ต้องผูกตอนสร้าง</text>
</svg>'''

def mrow(y, a, b, acc=False):
    c = 'ba' if acc else 'b'
    return (f'<rect x="6" y="{y}" width="190" height="34" rx="6" class="b"/><text x="14" y="{y+21}" class="tt m sm">{html.escape(a)}</text>'
            f'<line x1="198" y1="{y+17}" x2="212" y2="{y+17}" class="ln" marker-end="url(#ah)"/>'
            f'<rect x="216" y="{y}" width="178" height="34" rx="6" class="{c}"/><text x="224" y="{y+21}" class="tt m sm">{html.escape(b)}</text>')
SVG_MANGLE = f'''<svg viewBox="0 0 400 210" role="img">
<text x="10" y="18" class="sub">ซอร์ส C++ (namespace logx)</text><text x="220" y="18" class="sub">ชื่อ symbol ใน .o / .elf</text>
{mrow(28, 'info(const char*)', '_ZN4logx4infoEPKc', True)}
{mrow(70, 'info(const char*, int)', '_ZN4logx4infoEPKci', True)}
{mrow(112, 'info(const char*,float,int)', '_ZN4logx4infoEPKcfi', True)}
{mrow(164, 'extern "C" void foo()', 'foo')}
<text x="10" y="158" class="sub">ถ้าต้องเรียกจาก C หรือ ASM ใช้ extern "C" ปิด mangling</text>
</svg>'''

SVG_WIRE = '''<svg viewBox="0 0 400 160" role="img">
<rect x="8" y="50" width="78" height="50" rx="8" class="bm"/><text x="47" y="72" text-anchor="middle" class="tt m">XIAO</text><text x="47" y="89" text-anchor="middle" class="sub m">D2</text>
<line x1="86" y1="75" x2="126" y2="75" class="w"/>
<polyline points="126,75 132,63 144,87 156,63 168,87 180,63 186,75" class="w acc"/>
<text x="156" y="52" text-anchor="middle" class="tt m acc">1 kΩ</text>
<line x1="186" y1="75" x2="226" y2="75" class="w"/>
<polygon points="226,60 226,90 254,75" class="ba"/><line x1="256" y1="60" x2="256" y2="90" class="w"/>
<line x1="246" y1="56" x2="256" y2="46" class="ln" marker-end="url(#ah)"/><line x1="236" y1="54" x2="246" y2="44" class="ln" marker-end="url(#ah)"/>
<text x="240" y="112" text-anchor="middle" class="sub">LED (ขายาว = +)</text>
<line x1="256" y1="75" x2="320" y2="75" class="w"/><line x1="320" y1="75" x2="320" y2="104" class="w"/>
<line x1="304" y1="104" x2="336" y2="104" class="w"/><line x1="309" y1="111" x2="331" y2="111" class="w"/><line x1="314" y1="118" x2="326" y2="118" class="w"/>
<text x="344" y="114" class="tt m">GND</text>
<text x="8" y="148" class="sub">I ≈ (3.3 − 2.0) V / 1 kΩ ≈ 1.3 mA — พอเห็นชัด และไม่เกิน standard drive ของ GPIO</text>
</svg>'''

SVG_RAII = '''<svg viewBox="0 0 400 200" role="img">
<path d="M26 26 H16 V174 H26" class="la"/>
<text x="36" y="32" class="tt m">{</text>
<text x="52" y="62" class="tt m sm">ScopedTimer t("read");</text>
<rect x="210" y="46" width="184" height="26" rx="6" class="bm"/><text x="218" y="63" class="sub m">ctor: start_ = micros()</text>
<text x="52" y="104" class="tt m sm">// ... งานที่จับเวลา ...</text>
<text x="36" y="150" class="tt m">}  // ออกจาก scope</text>
<rect x="210" y="134" width="184" height="26" rx="6" class="ba"/><text x="218" y="151" class="sub m">dtor: print(micros()-start_)</text>
<text x="36" y="192" class="sub">compiler รับประกันว่า destructor ถูกเรียกเสมอ ไม่ว่าออกด้วย return ทางไหน</text>
</svg>'''

SVG_BOUNCE = '''<svg viewBox="0 0 400 210" role="img">
<text x="10" y="20" class="sub">ขา D1 (raw) — HIGH = ปล่อย, LOW = กด</text>
<path d="M10 40 H120 V80 H126 V40 H132 V80 H140 V48 H146 V80 H390" class="w acc"/>
<text x="133" y="98" text-anchor="middle" class="sub">bounce 1–5 ms</text>
<text x="10" y="124" class="sub">หลัง Debouncer (stableMs = 20)</text>
<path d="M10 140 H210 V176 H390" class="w"/>
<line x1="146" y1="84" x2="146" y2="186" class="ln dash"/><line x1="210" y1="84" x2="210" y2="186" class="ln dash"/>
<line x1="148" y1="194" x2="208" y2="194" class="ln" marker-end="url(#ah)"/><text x="178" y="207" text-anchor="middle" class="sub m">20 ms</text>
<text x="218" y="160" class="tt acc">Event::Pressed</text>
</svg>'''

SVG_STATE = '''<svg viewBox="0 0 400 130" role="img">
<rect x="14" y="40" width="88" height="40" rx="20" class="b"/><text x="58" y="65" text-anchor="middle" class="tt m">Off</text>
<rect x="156" y="40" width="88" height="40" rx="20" class="bm"/><text x="200" y="65" text-anchor="middle" class="tt m">Slow</text>
<rect x="298" y="40" width="88" height="40" rx="20" class="ba"/><text x="342" y="65" text-anchor="middle" class="tt m">Fast</text>
<line x1="104" y1="60" x2="152" y2="60" class="ln" marker-end="url(#ah)"/><line x1="246" y1="60" x2="294" y2="60" class="ln" marker-end="url(#ah)"/>
<path d="M342 82 C342 122 58 122 58 84" class="ln" marker-end="url(#ah)"/>
<text x="128" y="32" text-anchor="middle" class="sub">กด</text><text x="270" y="32" text-anchor="middle" class="sub">กด</text><text x="200" y="124" text-anchor="middle" class="sub">กด</text>
<text x="200" y="98" text-anchor="middle" class="sub m">500 ms   ·   100 ms</text>
</svg>'''

SVG_VTABLE = '''<svg viewBox="0 0 400 200" role="img">
<text x="10" y="18" class="sub">object: pot</text>
<rect x="10" y="26" width="118" height="34" rx="6" class="ba"/><text x="20" y="48" class="tt m sm">vptr (4 B)</text>
<rect x="10" y="60" width="118" height="34" rx="6" class="b"/><text x="20" y="82" class="tt m sm">pin_ = A0</text>
<text x="150" y="18" class="sub">vtable ของ PotSensor (flash)</text>
<rect x="150" y="26" width="110" height="30" rx="0" class="bm"/><text x="160" y="46" class="tt m sm">[0] ~dtor</text>
<rect x="150" y="56" width="110" height="30" rx="0" class="bm"/><text x="160" y="76" class="tt m sm">[1] name</text>
<rect x="150" y="86" width="110" height="30" rx="0" class="bm"/><text x="160" y="106" class="tt m sm">[2] read</text>
<line x1="128" y1="43" x2="146" y2="43" class="la" marker-end="url(#aha)"/>
<line x1="260" y1="71" x2="280" y2="71" class="ln" marker-end="url(#ah)"/><text x="284" y="75" class="tt m sm">Pot::name()</text>
<line x1="260" y1="101" x2="280" y2="101" class="ln" marker-end="url(#ah)"/><text x="284" y="105" class="tt m sm">Pot::read()</text>
<text x="10" y="146" class="sub">s-&gt;read() = อ่าน vptr → อ่าน entry [2] → กระโดดไปเรียก</text>
<text x="10" y="166" class="sub">ต้นทุน: RAM +4 B ต่อ object, flash 1 ตารางต่อ class, call ทางอ้อม 1 ครั้ง</text>
<text x="10" y="186" class="sub">FakeSensor มี vtable ของตัวเอง ชี้ไปฟังก์ชันของมัน</text>
</svg>'''

slots = ''
vals = {2: '611', 3: '608', 4: '615', 5: '603'}
for i in range(8):
    x = 18 + i*46
    c = 'ba' if i in vals else 'b'
    slots += f'<rect x="{x}" y="58" width="40" height="40" rx="6" class="{c}"/><text x="{x+20}" y="83" text-anchor="middle" class="tt m sm">{vals.get(i, "")}</text><text x="{x+20}" y="112" text-anchor="middle" class="sub m">{i}</text>'
SVG_RING = f'''<svg viewBox="0 0 400 170" role="img">
{slots}
<text x="130" y="22" text-anchor="middle" class="tt acc">tail → pop()</text><line x1="130" y1="28" x2="130" y2="54" class="la" marker-end="url(#aha)"/>
<text x="314" y="22" text-anchor="middle" class="tt">head → push()</text><line x1="314" y1="28" x2="314" y2="54" class="ln" marker-end="url(#ah)"/>
<path d="M360 118 C360 156 38 156 38 120" class="ln dash" marker-end="url(#ah)"/>
<text x="200" y="166" text-anchor="middle" class="sub">index = (index + 1) % N → วนกลับต้น buffer ไม่ต้องเลื่อนข้อมูล</text>
</svg>'''

def seg(x, y, h, t, c, sub=''):
    s = f'<rect x="{x}" y="{y}" width="160" height="{h}" class="{c}"/><text x="{x+80}" y="{y+h/2+(0 if sub else 4)}" text-anchor="middle" class="tt sm">{t}</text>'
    if sub: s += f'<text x="{x+80}" y="{y+h/2+15}" text-anchor="middle" class="sub m">{sub}</text>'
    return s
SVG_MEM = f'''<svg viewBox="0 0 400 350" role="img">
<text x="100" y="20" text-anchor="middle" class="tt">Flash 1 MB</text><text x="100" y="35" text-anchor="middle" class="sub">ไม่หายเมื่อไฟดับ</text>
<text x="300" y="20" text-anchor="middle" class="tt">RAM 256 KB</text><text x="300" y="35" text-anchor="middle" class="sub">หายเมื่อไฟดับ</text>
{seg(20, 44, 34, 'Bootloader (UF2)', 'b')}
{seg(20, 78, 52, 'ว่าง', 'b dash')}
{seg(20, 130, 24, '.data ค่าเริ่มต้น', 'bm')}
{seg(20, 154, 80, '.text โค้ด', 'ba', '+ .rodata (const)')}
{seg(20, 234, 66, 'SoftDevice + MBR', 'b', '~150 KB (BLE stack)')}
{seg(220, 44, 52, '↓ stack', 'ba', 'ตัวแปร local, ISR')}
{seg(220, 96, 52, 'ว่าง', 'b dash')}
{seg(220, 148, 34, '↑ heap (new/malloc)', 'b')}
{seg(220, 182, 34, '.bss (static = 0)', 'bm')}
{seg(220, 216, 34, '.data (static มีค่า)', 'bm')}
{seg(220, 250, 50, 'SoftDevice RAM', 'b')}
<path d="M180 142 C200 142 200 233 216 233" class="la" marker-end="url(#aha)"/>
<text x="20" y="316" class="sub m">0x0000_0000 (ล่าง)</text><text x="220" y="316" class="sub m">0x2000_0000 (ล่าง)</text>
<text x="20" y="336" class="sub">ลูกศรส้ม: startup code copy .data จาก flash ไป RAM ก่อน setup()</text>
</svg>'''

SVG_ISR = '''<svg viewBox="0 0 400 190" role="img">
<text x="10" y="30" class="sub m">loop()</text><text x="10" y="112" class="sub m">ISR</text>
<rect x="60" y="16" width="120" height="26" rx="5" class="bm"/><text x="120" y="33" text-anchor="middle" class="sub m">อ่าน pressCount</text>
<rect x="222" y="16" width="160" height="26" rx="5" class="bm"/><text x="302" y="33" text-anchor="middle" class="sub m">ทำงานต่อจากเดิม</text>
<line x1="180" y1="42" x2="186" y2="92" class="la" marker-end="url(#aha)"/>
<rect x="186" y="96" width="44" height="26" rx="5" class="ba"/><text x="208" y="113" text-anchor="middle" class="sub m">+1</text>
<line x1="230" y1="96" x2="234" y2="46" class="ln" marker-end="url(#ah)"/>
<path d="M10 160 H180 V140 H190 V160 H390" class="w acc"/>
<text x="120" y="180" text-anchor="middle" class="sub">ขอบ FALLING ที่ D1 → CPU กระโดดเข้า ISR ทันที</text>
<text x="300" y="134" text-anchor="middle" class="sub">ISR: สั้น · ไม่ delay · ไม่ Serial</text>
</svg>'''

SVG_GITAREA = flow([
    ('Working directory', 'ไฟล์ที่คุณแก้อยู่จริงในเครื่อง', 'b'),
    ('Staging area (index)', 'รายการที่จะเข้า commit ถัดไป', 'bm'),
    ('Local repository (.git)', 'ประวัติ commit ทั้งหมดในเครื่อง', 'ba'),
    ('Remote (GitHub)', 'สำเนาบนเซิร์ฟเวอร์ แชร์กับทีม / CI', 'b'),
], ['git add', 'git commit', 'git push'])

SVG_BRANCH = '''<svg viewBox="0 0 400 170" role="img">
<line x1="30" y1="50" x2="370" y2="50" class="w"/>
<path d="M150 50 C170 50 170 112 196 112 H270 C296 112 296 50 314 50" class="w acc"/>
<circle cx="40" cy="50" r="9" class="pn"/><circle cx="95" cy="50" r="9" class="pn"/><circle cx="150" cy="50" r="9" class="pn"/>
<circle cx="230" cy="50" r="9" class="pn"/><circle cx="318" cy="50" r="11" class="pm"/>
<circle cx="206" cy="112" r="9" class="pa"/><circle cx="262" cy="112" r="9" class="pa"/>
<text x="374" y="54" class="tt m sm">main</text>
<text x="230" y="148" text-anchor="middle" class="tt m sm acc">feature/fast-blink</text>
<text x="230" y="28" text-anchor="middle" class="sub">แก้บรรทัดเดียวกัน</text><text x="318" y="28" text-anchor="middle" class="sub">merge</text>
<text x="10" y="166" class="sub">ถ้า 2 branch แก้บรรทัดเดียวกัน git จะหยุดให้คุณเลือก = merge conflict</text>
</svg>'''

SVG_LAYERS = '''<svg viewBox="0 0 400 270" role="img">
<rect x="10" y="14" width="270" height="48" rx="8" class="b"/><text x="22" y="34" class="tt m sm">firmware.ino</text><text x="22" y="52" class="sub">ประกอบชิ้นส่วน · scheduler · wiring</text>
<rect x="10" y="72" width="270" height="56" rx="8" class="ba"/><text x="22" y="94" class="tt m sm">Pure logic</text><text x="22" y="114" class="sub">Debouncer, RingBuffer, filter — ไม่รู้จัก Arduino</text>
<rect x="10" y="138" width="270" height="48" rx="8" class="bm"/><text x="22" y="158" class="tt m sm">HAL / Arduino API</text><text x="22" y="176" class="sub">digitalRead, millis, analogRead, Serial</text>
<rect x="10" y="196" width="270" height="48" rx="8" class="b"/><text x="22" y="216" class="tt m sm">Hardware</text><text x="22" y="234" class="sub">nRF52840 GPIO, SAADC, USB</text>
<path d="M290 76 H300 V124 H290" class="la"/><text x="306" y="96" class="tt sm acc">test บน PC</text><text x="306" y="112" class="sub">g++ · วินาที · ใน CI</text>
<path d="M290 18 H300 V240 H290" class="ln"/><text x="306" y="200" class="tt sm">test บนบอร์ด</text><text x="306" y="216" class="sub">ช้ากว่า · ต้องมือ</text>
<text x="10" y="264" class="sub">กฎ: logic ที่ซับซ้อนควรอยู่ชั้นส้ม เพราะ test อัตโนมัติได้</text>
</svg>'''

SVG_BUILD = flow([
    ('firmware.ino', 'ที่คุณเขียน', 'b'),
    ('Arduino preprocessor', '#include <Arduino.h> + สร้าง prototype ให้', 'b'),
    ('firmware.ino.cpp', 'กลายเป็นไฟล์ C++ ปกติ', 'bm'),
    ('arm-none-eabi-g++', 'compile → .o (Cortex-M4F)', 'ba'),
    ('linker + linker script', 'รวม core.a + libs → .elf', 'b'),
    ('objcopy / packager', '.hex · .zip (DFU) · .uf2', 'bm'),
], ['', '', '', '', ''])

SVG_SCHED = flow([
    ('loop()', 'วนเร็วที่สุด ไม่มี delay()', 'b'),
    ('now = millis()', '', 'b'),
    ('ทุก task: now − lastRun ≥ period ?', 'ใช่ → lastRun = now; run()', 'ba'),
    ('handleSerial()', 'อ่านคำสั่งทีละตัวอักษร ไม่ block', 'bm'),
], ['', '', 'แล้ววนกลับ'])

SVG_PR = flow([
    ('git switch -c feature/x', 'แตก branch จาก main', 'b'),
    ('commit + git push', '', 'b'),
    ('Pull Request', 'คำอธิบาย + diff ให้คน review', 'ba'),
    ('CI ตรวจอัตโนมัติ', 'test + build ต้องผ่าน', 'bm'),
    ('Review → Squash merge', 'ลบ branch · main สะอาด', 'b'),
])

SVG_CI = flow([
    ('push / pull_request', 'event ที่ trigger workflow', 'b'),
    ('job: host-tests', 'g++ → ./test_runner → cppcheck', 'ba'),
    ('job: build-firmware', 'arduino-cli compile (needs: host-tests)', 'bm'),
    ('artifact: firmware', '.hex / .zip ดาวน์โหลดได้จากหน้า Actions', 'b'),
], ['ubuntu runner', 'ผ่านแล้วค่อยรัน', ''])

SVG_REL = flow([
    ('git tag -a v0.1.0', 'ติดเวอร์ชันแบบ SemVer', 'b'),
    ('git push origin v0.1.0', '', 'b'),
    ('release.yml', 'สร้าง version.h → compile', 'ba'),
    ('GitHub Release', 'แนบ .hex / .zip + release notes', 'bm'),
    ('ทีม / QA ดาวน์โหลดไปแฟลช', 'ทุกเวอร์ชันย้อนกลับได้', 'b'),
])

SVG_ROAD = flow([
    ('คอร์สนี้', 'C++ · RAII · ISR · test · CI/CD', 'ba'),
    ('I²C + IMU บนบอร์ด (Sense)', 'driver class ของ LSM6DS3', 'b'),
    ('BLE peripheral', 'ส่งค่าเซนเซอร์เข้ามือถือ', 'b'),
    ('Zephyr / nRF Connect SDK', 'RTOS · devicetree · ใช้จริงในอุตสาหกรรม', 'bm'),
    ('Custom board + production test', 'สิ่งที่คุณทำงานอยู่แล้ว ต่อยอดได้', 'b'),
])

# ---------------- lessons ----------------
MODS = {
 'S': T('โมดูล 0 · เตรียมเครื่อง', 'Module 0 · Setup'),
 'A': T('โมดูล A · C++ สำหรับคนเขียน C', 'Module A · C++ for C programmers'),
 'B': T('โมดูล B · Git และ GitHub', 'Module B · Git and GitHub'),
 'C': T('โมดูล C · Testable code และ CI/CD', 'Module C · Testable code and CI/CD'),
}
LESSONS = []
def lesson(num, mod, title, mins, hw, body):
    LESSONS.append(dict(num=num, mod=mod, title=title, mins=mins, hw=hw, body=body))

def qa(pairs):
    return f'<h3>{T("เช็กความเข้าใจ", "Check your understanding")}</h3>' + ''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in pairs)
def iv(t): return f'<aside class="iv"><b>{T("มุมสัมภาษณ์", "Interview angle")}</b><p>{t}</p></aside>'
def goal(t): return f'<p class="goal"><b>{T("เป้าหมาย", "Goal")}</b> {t}</p>'
def vs(c, cpp): return f'<div class="vs"><div><span class="tag">C</span><p>{c}</p></div><div><span class="tag t2">C++</span><p>{cpp}</p></div></div>'

lesson('00', 'S', 'ติดตั้งเครื่องมือ + Blink แรก', 30, 'บอร์ดอย่างเดียว', goal('IDE คอมไพล์และแฟลชบอร์ดได้ รู้ว่า LED บนบอร์ดเป็น active-LOW') + '''
<h3>ติดตั้ง</h3>
<ol>
<li>ติดตั้ง <b>Arduino IDE 2</b> และ <b>Git</b> (Windows: Git for Windows, เลือก editor เป็น VS Code)</li>
<li>File → Preferences → Additional boards manager URLs ใส่<br><code class="il">https://files.seeedstudio.com/arduino/package_seeeduino_boards_index.json</code></li>
<li>Boards Manager ค้น <b>Seeed nRF52 Boards</b> (ตัวที่ไม่มีคำว่า mbed) แล้วติดตั้ง → เลือกบอร์ด <b>Seeed XIAO nRF52840 Sense</b></li>
<li>ติดตั้ง <b>arduino-cli</b> ไว้ด้วย จะใช้ในบท CI แล้วรัน <code class="il">arduino-cli board listall xiao</code> จดค่า FQBN ที่ได้</li>
</ol>
<p class="note">เลือก core แบบ non-mbed เพราะ build เร็วกว่าและใช้ BLE library ของ Adafruit ได้ ถ้าอัปโหลดไม่ขึ้น ให้กดปุ่ม reset 2 ครั้งเร็ว ๆ เพื่อเข้า bootloader แล้วเลือกพอร์ตใหม่</p>
''' + fig(SVG_PINOUT, 'XIAO nRF52840 Sense: GPIO เป็น 3.3 V ห้ามป้อน 5 V เข้าขา D') + '''
<h3>Hands-on</h3>''' + code('''// LED บนบอร์ดต่อขั้วบวกไว้ที่ 3V3 จึงติดเมื่อเขียน LOW
void setup() {
  pinMode(LED_RED, OUTPUT);
  digitalWrite(LED_RED, HIGH);   // ดับ
}

void loop() {
  digitalWrite(LED_RED, LOW);    // ติด
  delay(200);
  digitalWrite(LED_RED, HIGH);   // ดับ
  delay(800);
}''', 'blink.ino') + '''
<p>ลองเปลี่ยนเป็น <code class="il">LED_GREEN</code> / <code class="il">LED_BLUE</code> แล้วเปิด Preferences → Show verbose output during compile เพื่อดูคำสั่ง compiler ที่ IDE เรียกจริง</p>
''' + qa([('ทำไม LED_RED ติดตอนเขียน LOW?', 'LED ต่อแบบ active-LOW: ขั้วบวกอยู่ที่ 3V3 ขา GPIO ทำหน้าที่ sink กระแส เมื่อขาเป็น LOW จึงมีกระแสไหล'),
          ('ทำไมต้องใช้ core non-mbed ในคอร์สนี้?', 'build เร็วกว่า ใช้ Bluefruit BLE ได้ และ compile ใน CI ได้ง่าย ทั้งสอง core เขียน C++ ได้เหมือนกัน')]))

lesson('01', 'A', '.ino คือ C++ และเส้นทางจากโค้ดถึงบอร์ด', 20, 'บอร์ดอย่างเดียว', goal('เข้าใจว่า Arduino ซ่อนอะไรไว้ และเห็น toolchain จริง') + '''
<p>ไฟล์ .ino ไม่ใช่ภาษาพิเศษ IDE แค่เติม <code class="il">#include &lt;Arduino.h&gt;</code> และสร้าง function prototype ให้ แล้วส่งให้ <b>arm-none-eabi-g++</b> คอมไพล์เป็น C++ ปกติ ส่วน <code class="il">main()</code> อยู่ใน core:</p>
''' + code('''int main() {
  init();          // clock, timer, USB CDC
  setup();
  for (;;) {
    loop();
  }
}''', 'core/main.cpp (ย่อ)') + fig(SVG_BUILD, 'pipeline การ build ที่เกิดขึ้นทุกครั้งที่กด Verify') + '''
<h3>Hands-on</h3>''' + code('''void setup() {
  Serial.begin(115200);
  while (!Serial) {}             // รอ USB CDC พร้อม
  Serial.print("__cplusplus = ");  Serial.println(__cplusplus);
  Serial.print("sizeof(int) = ");  Serial.println(sizeof(int));
  Serial.print("sizeof(void*) = ");Serial.println(sizeof(void*));
  Serial.print("sizeof(bool) = "); Serial.println(sizeof(bool));
}

void loop() {}''', 'whoami.ino') + '''
<p>ค่า <code class="il">__cplusplus</code> บอกมาตรฐานภาษาที่ compiler ใช้ (เช่น 201103 = C++11, 201703 = C++17) จดไว้ เพราะ feature ที่ใช้ได้ขึ้นกับค่านี้ จากนั้นดูบรรทัดท้ายของ output: <i>Sketch uses … bytes</i> = flash, <i>Global variables use …</i> = RAM แบบ static</p>
''' + qa([('ถ้า __cplusplus ได้ 201103 จะใช้ if constexpr ได้ไหม?', 'ไม่ได้ if constexpr เป็นของ C++17 ต้องเพิ่ม flag -std=gnu++17 หรือเลี่ยงไปใช้ template overload'),
          ('"Global variables use" นับ stack ด้วยไหม?', 'ไม่นับ นับเฉพาะ .data + .bss ที่รู้ขนาดตอน link ตัวแปร local บน stack ไม่อยู่ในตัวเลขนี้')]) + iv('ถูกถามบ่อยว่า "อธิบายขั้นตอน build firmware" ให้ตอบเป็นลำดับ preprocess → compile → link (linker script กำหนด address) → objcopy → flash และบอกว่า .elf มี debug symbol ส่วน .hex/.bin คือ image ที่ลงชิป'))

lesson('02', 'A', 'Reference, const และ constexpr แทน #define', 25, 'บอร์ดอย่างเดียว', goal('เลิกใช้ #define กับค่าคงที่ และส่งพารามิเตอร์ด้วย reference ได้ถูกที่') + vs('ค่าคงที่ใช้ <code class="il">#define</code> ไม่มี type ไม่มี scope แก้ตัวแปรของผู้เรียกต้องส่ง pointer', '<code class="il">constexpr</code> มี type และคำนวณตอน compile ไม่กิน RAM ส่วน <code class="il">T&amp;</code> คือชื่อเล่นของตัวแปรเดิม ไม่มี null ไม่ต้องเขียน <code class="il">*</code>') + fig(SVG_REF, 'pointer เก็บ address แยก ส่วน reference ผูกกับตัวแปรเดิมตลอดชีวิต') + '''
<h3>Hands-on</h3>''' + code('''constexpr uint8_t kLedPins[] = {LED_RED, LED_GREEN, LED_BLUE};
constexpr size_t  kLedCount  = sizeof(kLedPins) / sizeof(kLedPins[0]);
constexpr uint32_t kStepMs   = 150;

void allOff() {
  for (uint8_t pin : kLedPins) {   // range-based for (C++11)
    digitalWrite(pin, HIGH);
  }
}

void nextIndex(size_t& idx) {      // reference: แก้ตัวแปรของผู้เรียกได้เลย
  idx = (idx + 1) % kLedCount;
}

size_t current = 0;

void setup() {
  for (uint8_t pin : kLedPins) pinMode(pin, OUTPUT);
  allOff();
}

void loop() {
  allOff();
  digitalWrite(kLedPins[current], LOW);
  delay(kStepMs);
  nextIndex(current);
}''', 'rgb_cycle.ino') + '''
<p>ลองเพิ่มฟังก์ชัน <code class="il">void printPin(const uint8_t&amp; p)</code> แล้วพยายามเขียน <code class="il">p = 0;</code> ข้างใน ดู error ที่ compiler ฟ้อง นี่คือประโยชน์ของ const: จับบั๊กตอน compile</p>
''' + qa([('เมื่อไหร่ควรส่ง const T& แทนส่งค่า?', 'เมื่อ T ใหญ่กว่า register (struct, buffer) เพื่อเลี่ยงการ copy ส่วน int, float, pointer ส่งค่าตรง ๆ เร็วกว่าและอ่านง่ายกว่า'),
          ('constexpr ต่างจาก const อย่างไร?', 'const = ห้ามแก้ แต่อาจรู้ค่าตอน runtime ส่วน constexpr = ต้องรู้ค่าตอน compile จึงใช้เป็นขนาด array หรือ template argument ได้')]) + iv('"ทำไมไม่ใช้ #define?" ตอบ: ไม่มี type checking, ไม่เคารพ namespace/scope, debugger มองไม่เห็นชื่อ และอาจเกิด side effect จาก macro expansion'))

lesson('03', 'A', 'namespace, overloading, enum class', 20, 'บอร์ดอย่างเดียว', goal('จัดระเบียบชื่อและเข้าใจว่าทำไม C++ ต้องมี name mangling') + vs('ชื่อฟังก์ชันซ้ำไม่ได้ ต้องตั้ง <code class="il">log_int</code>, <code class="il">log_float</code> และ <code class="il">enum</code> ปนกับ int ได้ทุกที่', 'overload ชื่อเดียวหลายพารามิเตอร์ได้ <code class="il">namespace</code> กันชื่อชน <code class="il">enum class</code> ไม่แปลงเป็น int เอง กำหนดขนาด <code class="il">: uint8_t</code> ได้') + fig(SVG_MANGLE, 'compiler ฝังชนิดพารามิเตอร์ลงในชื่อ symbol จึง overload ได้') + '''
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

void loop() {}''', 'logx.ino') + qa([('ถ้า library เขียนด้วย C ต้อง include อย่างไร?', 'ครอบ header ด้วย extern "C" { … } เพื่อให้ linker หา symbol ชื่อแบบ C เจอ ถ้าไม่ครอบจะ error undefined reference'),
          ('ทำไม enum class ปลอดภัยกว่า enum?', 'ไม่แปลงเป็น int เอง ชื่อ enumerator ไม่หลุดออกมาใน scope ภายนอก และกำหนด underlying type ได้ จึงคุมขนาดในหน่วยความจำได้')]))

lesson('04', 'A', 'class: encapsulation และ constructor', 30, 'LED + R 1 kΩ', goal('เขียน class Led ที่ซ่อนเรื่อง active-LOW ไว้ข้างใน') + vs('struct เก็บข้อมูล + ฟังก์ชัน <code class="il">led_on(&amp;led)</code> แยกกัน ใครก็แก้ field ได้', 'ข้อมูล (private) และพฤติกรรม (public) อยู่ด้วยกัน คอมไพล์แล้วได้โค้ดขนาดใกล้เคียงกัน เพราะ <code class="il">this</code> ก็คือ pointer ที่ส่งเข้าไปแบบซ่อน') + fig(SVG_WIRE, 'ต่อ LED ภายนอกที่ D2 ผ่าน R 1 kΩ ลง GND (active-HIGH)') + '''
<h3>Hands-on</h3>''' + code('''class Led {
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
};

Led red(LED_RED, true);   // บนบอร์ด: active-LOW
Led ext(D2, false);       // ภายนอก: active-HIGH

void setup() {
  red.begin();
  ext.begin();
}

void loop() {
  red.toggle();
  ext.toggle();
  delay(300);
}''', 'led_class.ino') + '''
<p class="note">ทำไมมี <code class="il">begin()</code> แยก ไม่เรียก <code class="il">pinMode</code> ใน constructor? เพราะ object global ถูกสร้างก่อน <code class="il">main()</code> และก่อน <code class="il">init()</code> ฮาร์ดแวร์อาจยังไม่พร้อม เป็น pattern มาตรฐานของ embedded C++</p>
<p>ทดลอง: ย้ายโค้ดไปไว้ที่ <code class="il">src/Led.h</code> (สร้างโฟลเดอร์ src ในโฟลเดอร์ sketch, บรรทัดแรกใส่ <code class="il">#pragma once</code> และ <code class="il">#include &lt;Arduino.h&gt;</code>) แล้ว <code class="il">#include "src/Led.h"</code> จะใช้ต่อในบท 11</p>
''' + qa([('member initializer list (: pin_(pin)) ดีกว่ากำหนดค่าใน body อย่างไร?', 'สร้าง member ด้วยค่าที่ถูกต้องตั้งแต่แรก ไม่ต้อง default-construct แล้วค่อย assign และจำเป็นสำหรับ member ที่เป็น const หรือ reference'),
          ('object Led ใช้ RAM กี่ byte โดยประมาณ?', 'ราว 3–4 byte (pin_, activeLow_, isOn_ + padding) ฟังก์ชันไม่กิน RAM ต่อ object เพราะอยู่ใน flash ใช้ร่วมกัน')]) + iv('"Static initialization order fiasco" คือคำถามระดับกลาง: ลำดับการสร้าง global object ข้ามไฟล์ไม่ถูกกำหนด ทางแก้คือ begin() หรือ function-local static'))

lesson('05', 'A', 'RAII และ destructor', 25, 'Pot 10 kΩ ที่ A0', goal('ใช้ scope ควบคุม resource อัตโนมัติ: จับเวลา, ปิด/เปิด interrupt') + '''
<p>RAII (Resource Acquisition Is Initialization): ขอ resource ใน constructor คืนใน destructor แล้ว compiler จะเรียก destructor ให้เมื่อออกจาก scope เสมอ จึงไม่มีทางลืม <code class="il">unlock</code> หรือ <code class="il">enable_irq</code> แม้จะ <code class="il">return</code> กลางทาง C ไม่มีกลไกนี้</p>
''' + fig(SVG_RAII, 'อายุของ object ผูกกับวงเล็บปีกกา') + '''
<h3>Hands-on</h3><p>ต่อ potentiometer: ขาข้าง 3V3 กับ GND, ขากลางเข้า A0</p>''' + code('''class ScopedTimer {
public:
  explicit ScopedTimer(const char* label) : label_(label), start_(micros()) {}
  ~ScopedTimer() {
    uint32_t us = micros() - start_;
    Serial.print(label_); Serial.print(": "); Serial.print(us); Serial.println(" us");
  }
  ScopedTimer(const ScopedTimer&) = delete;             // ห้าม copy
  ScopedTimer& operator=(const ScopedTimer&) = delete;
private:
  const char* label_;
  uint32_t start_;
};

// ปิด interrupt แบบซ้อนได้: เก็บสถานะเดิมแล้วคืนค่าเดิม
class CriticalSection {
public:
  CriticalSection() : primask_(__get_PRIMASK()) { __disable_irq(); }
  ~CriticalSection() { __set_PRIMASK(primask_); }
private:
  uint32_t primask_;
};

void setup() { Serial.begin(115200); }

void loop() {
  long sum = 0;
  {
    ScopedTimer t("analogRead x100");
    for (int i = 0; i < 100; ++i) sum += analogRead(A0);
  }                                   // destructor ทำงานตรงนี้
  Serial.print("avg = "); Serial.println(sum / 100);
  delay(1000);
}''', 'raii.ino') + qa([('ทำไมต้อง = delete copy constructor?', 'ถ้า copy ได้ จะมี 2 object ที่ destructor ทำงานซ้ำ เช่น เปิด interrupt 2 ครั้ง หรือพิมพ์เวลาซ้ำ resource ที่มีเจ้าของคนเดียวควรห้าม copy'),
          ('CriticalSection ใช้กับ BLE (SoftDevice) ได้ไหม?', 'ใช้ได้แค่ช่วงสั้นมาก ไม่กี่ไมโครวินาที ถ้าปิดนาน SoftDevice จะพลาด timing ของวิทยุ ในงานจริงใช้ sd_nvic_critical_region_enter แทน')]) + iv('ถ้าถูกถาม "ข้อดีที่สุดของ C++ เหนือ C ใน embedded" RAII คือคำตอบที่ดี เพราะไม่มี runtime overhead และกำจัดบั๊ก resource leak ทั้งกลุ่ม'))

lesson('06', 'A', 'ปุ่มกด, debounce และ state machine', 30, 'ปุ่มกดที่ D1', goal('เขียน debounce แบบ non-blocking เป็น class ที่ไม่พึ่ง Arduino (จะ test ได้ในบท 15)') + '''
<p>ต่อปุ่มระหว่าง D1 กับ GND แล้วใช้ <code class="il">INPUT_PULLUP</code> ปล่อย = HIGH, กด = LOW หน้าสัมผัสจะเด้งหลายครั้งในไม่กี่มิลลิวินาที ถ้าไม่ debounce กดครั้งเดียวจะนับได้หลายครั้ง</p>
''' + fig(SVG_BOUNCE, 'Debouncer รอให้สัญญาณนิ่งครบ 20 ms ก่อนยืนยัน') + '''
<h3>Hands-on</h3><p>สร้างไฟล์ <code class="il">src/Debouncer.h</code> ในโฟลเดอร์ sketch</p>''' + code(DEB, 'src/Debouncer.h') + code('''#include "src/Debouncer.h"

constexpr uint8_t kButtonPin = D1;
enum class Mode : uint8_t { Off, Slow, Fast };

Debouncer button;
Mode mode = Mode::Off;
uint32_t lastToggle = 0;
bool ledOn = false;

Mode next(Mode m) {
  switch (m) {
    case Mode::Off:  return Mode::Slow;
    case Mode::Slow: return Mode::Fast;
    case Mode::Fast: return Mode::Off;
  }
  return Mode::Off;
}

uint32_t periodMs(Mode m) { return m == Mode::Slow ? 500 : 100; }

void setup() {
  pinMode(kButtonPin, INPUT_PULLUP);
  pinMode(LED_GREEN, OUTPUT);
  digitalWrite(LED_GREEN, HIGH);
}

void loop() {
  uint32_t now = millis();
  bool pressed = (digitalRead(kButtonPin) == LOW);
  if (button.update(pressed, now) == Debouncer::Event::Pressed) {
    mode = next(mode);
  }
  if (mode == Mode::Off) {
    digitalWrite(LED_GREEN, HIGH);
  } else if (now - lastToggle >= periodMs(mode)) {
    lastToggle = now;
    ledOn = !ledOn;
    digitalWrite(LED_GREEN, ledOn ? LOW : HIGH);
  }
}''', 'button_modes.ino') + fig(SVG_STATE, 'state machine 3 สถานะ เปลี่ยนเมื่อได้ Event::Pressed') + qa([('ทำไม now - lastToggle ยังถูกต้องแม้ millis() overflow (ราว 49.7 วัน)?', 'การลบ unsigned 32-bit เป็น modulo 2³² ผลต่างจึงถูกเสมอตราบใดที่ช่วงเวลาไม่เกิน 49.7 วัน ห้ามเขียนแบบ now > lastToggle + period เพราะพังตอน overflow'),
          ('ทำไม switch มี return Mode::Off ท้ายฟังก์ชันอีก?', 'บาง compiler เตือนว่า control reaches end of non-void function แม้จะครอบทุก case แล้ว ใส่ไว้เพื่อความปลอดภัยและ warning-free')]))

lesson('07', 'A', 'Inheritance, virtual และ interface', 25, 'Pot ที่ A0', goal('ออกแบบ interface ISensor ให้สลับเซนเซอร์จริงกับเซนเซอร์ปลอมได้ และรู้ต้นทุนของ virtual') + '''
<p>ใน C ทำ polymorphism ด้วย struct ของ function pointer เอง ใน C++ ใช้ <code class="il">virtual</code> แล้ว compiler สร้างตาราง (vtable) ให้ ประโยชน์หลักใน embedded คือสลับ implementation ได้ เช่น ใช้ FakeSensor ตอน test โดยไม่ต้องแก้โค้ดที่เรียกใช้</p>
''' + fig(SVG_VTABLE, 'กลไกของ virtual call') + '''
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
}''', 'sensors.ino') + '<p>เปิด Tools → Serial Plotter จะเห็นกราฟ 2 เส้น หมุน pot เทียบกับคลื่น sine</p>' + qa([('ทำไม base class ต้องมี virtual destructor?', 'ถ้า delete object ผ่าน pointer ของ base แล้ว destructor ไม่ virtual destructor ของ derived จะไม่ถูกเรียก resource รั่ว'),
          ('ถ้าไม่อยากจ่ายต้นทุน virtual มีทางเลือกอะไร?', 'ใช้ template (static polymorphism / CRTP) ให้ compiler รู้ชนิดตอน compile แล้ว inline ได้ แลกกับ code size ที่อาจเพิ่มขึ้น')]) + iv('คำถามคลาสสิก: "virtual ช้าไหม?" ตอบเป็นตัวเลข: เพิ่ม load 2 ครั้ง + indirect branch ต่อ call บน Cortex-M4 ราวไม่กี่ cycle ปัญหาจริงคือ inline ไม่ได้ ไม่ใช่ความช้าโดยตรง'))

lesson('08', 'A', 'Template: RingBuffer<T, N>', 30, 'Pot ที่ A0', goal('เขียน container ขนาดคงที่ใช้ซ้ำได้ทุกชนิด โดยไม่ใช้ heap') + vs('ทำ buffer สำหรับ int, float แยกกัน หรือใช้ <code class="il">void*</code> + macro ซึ่งไม่มี type safety', 'template ให้ compiler สร้างโค้ดเฉพาะชนิดให้ ขนาด N เป็นค่าตอน compile ตรวจได้ด้วย <code class="il">static_assert</code>') + fig(SVG_RING, 'ring buffer: head เขียน tail อ่าน วนรอบด้วย modulo') + '''
<h3>Hands-on</h3><p>สร้าง <code class="il">src/RingBuffer.h</code></p>''' + code(RING, 'src/RingBuffer.h') + code('''#include "src/RingBuffer.h"

RingBuffer<uint16_t, 16> samples;   // 16 ค่าล่าสุด

void setup() { Serial.begin(115200); }

void loop() {
  uint16_t raw = analogRead(A0);
  samples.pushOverwrite(raw);
  Serial.print("raw:"); Serial.print(raw);
  Serial.print(" avg:"); Serial.println(average(samples));
  delay(20);
}''', 'moving_average.ino') + '<p>เปิด Serial Plotter เทียบเส้น raw กับ avg ลองเปลี่ยน N เป็น 4 และ 64 สังเกตความหน่วงและความเรียบ (moving average N จุด = delay ราว N/2 sample)</p>' + qa([('ถ้าใช้ RingBuffer&lt;uint16_t,16&gt; และ RingBuffer&lt;float,16&gt; flash จะเป็นอย่างไร?', 'compiler สร้างโค้ด 2 ชุด (template instantiation) flash เพิ่มขึ้น ถ้ามีหลายชนิดเกินไปเรียกว่า code bloat'),
          ('ถ้า ISR เป็นคน push และ loop เป็นคน pop ปลอดภัยไหม?', 'ยังไม่ปลอดภัย เพราะ count_ ถูกแก้จากทั้งสองฝั่ง ต้องครอบด้วย CriticalSection หรือออกแบบ SPSC ที่ฝั่ง producer แก้แค่ head ฝั่ง consumer แก้แค่ tail')]))

lesson('09', 'A', 'หน่วยความจำใน embedded', 25, 'บอร์ดอย่างเดียว', goal('รู้ว่าตัวแปรแต่ละแบบไปอยู่ส่วนไหน และกฎที่ทีม firmware ใช้จริง') + fig(SVG_MEM, 'memory map แบบย่อของ nRF52840 (ตัวเลขประมาณ ขึ้นกับ SoftDevice และ bootloader)') + '''
<h3>Hands-on</h3>''' + code('''uint8_t bigStatic[8192];        // .bss  → นับใน "Global variables use"
const char kMsg[] = "hello";    // .rodata → อยู่ใน flash

void setup() {
  Serial.begin(115200);
  while (!Serial) {}
  uint8_t onStack[256];         // stack → ไม่อยู่ในตัวเลขตอน compile
  onStack[0] = 1;
  bigStatic[0] = onStack[0];
  Serial.print("flash  : 0x"); Serial.println((uintptr_t)kMsg, HEX);
  Serial.print("static : 0x"); Serial.println((uintptr_t)bigStatic, HEX);
  Serial.print("stack  : 0x"); Serial.println((uintptr_t)onStack, HEX);
}

void loop() {}''', 'memmap.ino') + '''
<p>ดูว่า address ขึ้นต้น 0x000… (flash) หรือ 0x2000… (RAM) ตามรูปไหม จากนั้นเปลี่ยน <code class="il">bigStatic</code> เป็น 32768 แล้วดูตัวเลข RAM ตอน compile เปลี่ยน</p>
<h3>กฎที่ใช้ในทีมจริง</h3>
<ul>
<li>จอง memory ตอน init เท่านั้น หลังจากนั้นห้าม <code class="il">new</code>/<code class="il">malloc</code> ใน loop เพราะ heap fragment แล้วพังหลังรันหลายวัน</li>
<li>เลี่ยง <code class="il">String</code> ของ Arduino ใช้ <code class="il">char buf[32]</code> + <code class="il">snprintf</code> แทน</li>
<li>ใช้ <code class="il">std::array</code> / buffer ขนาดคงที่ หลีกเลี่ยง <code class="il">std::vector</code>, <code class="il">std::function</code> ที่อาจจอง heap เอง</li>
<li>embedded มักปิด exceptions และ RTTI (<code class="il">-fno-exceptions -fno-rtti</code>) จึงจัดการ error ด้วยค่าที่ return</li>
</ul>
''' + qa([('ตัวแปร static ภายในฟังก์ชันอยู่ส่วนไหน?', '.data หรือ .bss เหมือน global แต่ scope จำกัดในฟังก์ชัน จึงคงค่าระหว่างการเรียก'),
          ('stack overflow บน MCU ไม่มี OS แสดงอาการอย่างไร?', 'stack โตลงไปทับ heap หรือ .bss ทำให้ค่าตัวแปรเพี้ยนแบบสุ่มหรือ HardFault วิธีตรวจคือ stack painting (เติม pattern แล้วดูว่าถูกเขียนลึกแค่ไหน) หรือเปิด MPU guard')]) + iv('เตรียมอธิบาย .text / .data / .bss / heap / stack ด้วยรูปนี้ได้ภายใน 1 นาที เป็นคำถามที่เจอเกือบทุกที่'))

lesson('10', 'A', 'Interrupt, volatile และ lambda', 25, 'ปุ่มกดที่ D1', goal('เขียน ISR ที่ถูกต้อง และแชร์ข้อมูลระหว่าง ISR กับ loop อย่างปลอดภัย') + fig(SVG_ISR, 'ISR แทรกกลาง loop ได้ทุกเมื่อ') + '''
<h3>Hands-on</h3>''' + code('''constexpr uint8_t kButtonPin = D1;
volatile uint32_t pressCount = 0;   // volatile: ค่าเปลี่ยนนอก flow ปกติ ห้าม cache

void setup() {
  Serial.begin(115200);
  pinMode(kButtonPin, INPUT_PULLUP);
  // lambda ที่ไม่ capture อะไร แปลงเป็น function pointer ได้
  attachInterrupt(digitalPinToInterrupt(kButtonPin), [] {
    pressCount = pressCount + 1;
  }, FALLING);
}

void loop() {
  uint32_t count;
  noInterrupts();          // copy ออกมาแบบ atomic
  count = pressCount;
  interrupts();
  Serial.println(count);
  delay(500);
}''', 'isr_count.ino') + '''
<p>กดปุ่ม 1 ครั้ง ตัวเลขมักเพิ่มมากกว่า 1 นั่นคือ bounce ที่เห็นในบท 6 ข้อสรุป: ISR บนปุ่มกลไกต้อง debounce ด้วยเวลา (เช่นเช็ก <code class="il">millis()</code> ใน ISR หรือส่ง event ให้ loop จัดการ)</p>
''' + qa([('volatile ทำให้ pressCount++ เป็น atomic ไหม?', 'ไม่ volatile แค่บังคับให้อ่าน/เขียน memory จริงทุกครั้ง แต่ ++ คือ load-add-store 3 คำสั่ง ถูกแทรกกลางได้ ต้องใช้ critical section หรือ std::atomic'),
          ('อะไรห้ามทำใน ISR?', 'delay(), Serial.print(), malloc/new, ทำงานนาน และเรียกฟังก์ชันที่ไม่ reentrant ให้ ISR ตั้ง flag หรือ push ลง buffer แล้วกลับเร็วที่สุด')]) + iv('volatile คือคำถามที่ถูกถามบ่อยที่สุดในสาย embedded ตอบให้ครบ 3 กรณี: ตัวแปรที่ ISR แก้, memory-mapped register, ตัวแปรที่แชร์ระหว่าง thread (และบอกว่ามันไม่ใช่ synchronization)'))

lesson('11', 'A', 'Mini project: cooperative scheduler', 30, 'LED + ปุ่ม + Pot', goal('รวมทุกอย่างเป็น firmware ที่ไม่มี delay() เลย โครงสร้างแบบนี้ใช้จริงก่อนจะขึ้น RTOS') + fig(SVG_SCHED, 'แต่ละ task มีรอบของตัวเอง loop แค่ตรวจว่าถึงเวลาหรือยัง') + '''
<h3>Hands-on</h3><p>ตั้งชื่อโฟลเดอร์ <code class="il">firmware/</code> และไฟล์ <code class="il">firmware.ino</code> (Arduino บังคับให้ชื่อตรงกัน) ใน <code class="il">src/</code> มี Led.h, Debouncer.h, RingBuffer.h จากบทก่อน</p>''' + code('''#include "src/Led.h"
#include "src/Debouncer.h"
#include "src/RingBuffer.h"

#if __has_include("src/version.h")
#include "src/version.h"          // CI สร้างไฟล์นี้ (บท 17)
#else
#define FW_VERSION "dev"
#endif

constexpr uint8_t kButtonPin = D1;
constexpr uint8_t kPotPin    = A0;

Led status(LED_GREEN, true);
Led ext(D2, false);
Debouncer button;
RingBuffer<uint16_t, 16> samples;
bool paused = false;

struct Task {
  uint32_t periodMs;
  uint32_t lastRunMs;
  void (*run)();
};

void blinkTask() { if (!paused) status.toggle(); }

void buttonTask() {
  bool pressed = digitalRead(kButtonPin) == LOW;
  if (button.update(pressed, millis()) == Debouncer::Event::Pressed) {
    paused = !paused;
    ext.toggle();
  }
}

void sensorTask() { samples.pushOverwrite(analogRead(kPotPin)); }

void reportTask() {
  Serial.print("avg:");     Serial.print(average(samples));
  Serial.print(" paused:"); Serial.println(paused ? 1 : 0);
}

Task tasks[] = {
  {500, 0, blinkTask},
  {5,   0, buttonTask},
  {20,  0, sensorTask},
  {200, 0, reportTask},
};

// พิมพ์ตัวเลข 50–5000 แล้ว Enter เพื่อเปลี่ยนรอบกระพริบ
void handleSerial() {
  static char buf[16];
  static size_t len = 0;
  while (Serial.available()) {
    char c = Serial.read();
    if (c == '\\n' || c == '\\r') {
      if (len > 0) {
        buf[len] = '\\0';
        long ms = atol(buf);
        if (ms >= 50 && ms <= 5000) tasks[0].periodMs = ms;
        len = 0;
      }
    } else if (len < sizeof(buf) - 1) {
      buf[len++] = c;
    }
  }
}

void setup() {
  Serial.begin(115200);
  pinMode(kButtonPin, INPUT_PULLUP);
  status.begin();
  ext.begin();
  Serial.print("fw "); Serial.println(FW_VERSION);
}

void loop() {
  uint32_t now = millis();
  for (Task& t : tasks) {
    if (now - t.lastRunMs >= t.periodMs) {
      t.lastRunMs = now;
      t.run();
    }
  }
  handleSerial();
}''', 'firmware/firmware.ino') + '''
<p>ทดสอบ: กดปุ่ม → LED เขียวหยุด LED ภายนอกติด, หมุน pot ดู avg ใน Plotter, พิมพ์ 100 ใน Serial Monitor → กระพริบเร็วขึ้น ทั้งหมดทำงานพร้อมกันโดยไม่มี delay()</p>
''' + qa([('ถ้า reportTask ใช้เวลา 30 ms จะเกิดอะไรกับ buttonTask?', 'buttonTask ถูกเลื่อนไปจน reportTask จบ เพราะเป็น cooperative (ไม่มี preemption) ทุก task ต้องสั้น ถ้าทำไม่ได้คือสัญญาณว่าถึงเวลาใช้ RTOS'),
          ('ทำไม Task ใช้ function pointer ไม่ใช้ std::function?', 'function pointer ขนาด 4 byte ไม่จอง heap และคาดเดาได้ std::function อาจจอง heap เมื่อ capture ข้อมูล')]))

lesson('12', 'B', 'Git พื้นฐาน: add, commit, log', 25, 'คอมพิวเตอร์', goal('เก็บงานทั้งหมดที่ทำมาลง Git พร้อม commit message ที่อ่านแล้วรู้เรื่อง') + fig(SVG_GITAREA, 'ไฟล์เดินทางผ่าน 3 พื้นที่ในเครื่องก่อนขึ้น GitHub') + '''
<h3>Hands-on</h3>''' + code('''git config --global user.name "Your Name"
git config --global user.email "you@example.com"
git config --global init.defaultBranch main

mkdir xiao-embedded-cpp && cd xiao-embedded-cpp
git init
# ย้ายโฟลเดอร์ firmware/ จากบท 11 มาไว้ที่นี่ และสร้าง .gitignore
git status
git add .gitignore firmware/
git commit -m "feat: led, debouncer, ring buffer and task scheduler"
git log --oneline

# แก้ไฟล์แล้วลอง:
git diff              # สิ่งที่แก้ แต่ยังไม่ add
git add -p            # เลือก add ทีละก้อน
git restore <file>    # ทิ้งการแก้ไขที่ยังไม่ add''', 'terminal') + code('''build/
*.hex
*.zip
*.uf2
firmware/src/version.h
.vscode/''', '.gitignore') + '''
<p>รูปแบบ commit message ที่ทีมนิยม (Conventional Commits): <code class="il">feat:</code> ฟีเจอร์ใหม่, <code class="il">fix:</code> แก้บั๊ก, <code class="il">docs:</code>, <code class="il">test:</code>, <code class="il">ci:</code>, <code class="il">refactor:</code> หนึ่ง commit = หนึ่งเรื่อง</p>
''' + qa([('ทำไมไม่ควร commit ไฟล์ .hex?', 'เป็นผลลัพธ์ที่สร้างซ้ำได้จาก source เปลี่ยนทุก build ทำให้ repo บวมและ diff อ่านไม่ได้ ไฟล์ binary ควรอยู่ใน GitHub Release (บท 17)'),
          ('git add . กับ git add -p ต่างกันอย่างไร?', 'add . เอาทุกการเปลี่ยนแปลง -p ให้เลือกทีละ hunk ช่วยแยก commit ตามเรื่องได้ แม้แก้หลายเรื่องในไฟล์เดียว')]))

lesson('13', 'B', 'Branch, merge และแก้ conflict', 25, 'คอมพิวเตอร์', goal('แยกงานเป็น branch และแก้ merge conflict ได้โดยไม่ตื่นตระหนก') + fig(SVG_BRANCH, 'feature branch แตกจาก main แล้ว merge กลับ') + '''
<h3>Hands-on: สร้าง conflict เองแล้วแก้</h3>''' + code('''git switch -c feature/fast-blink
# ใน firmware.ino แก้ {500, 0, blinkTask} เป็น {250, 0, blinkTask}
git commit -am "feat: faster default blink"

git switch main
# แก้บรรทัดเดียวกันเป็น {1000, 0, blinkTask}
git commit -am "chore: slower default blink"

git merge feature/fast-blink      # → CONFLICT''', 'terminal') + code('''<<<<<<< HEAD
  {1000, 0, blinkTask},
=======
  {250, 0, blinkTask},
>>>>>>> feature/fast-blink''', 'firmware.ino ตอน conflict') + code('''# แก้ไฟล์ให้เหลือบรรทัดที่ต้องการ ลบเครื่องหมาย <<< === >>> ออก
git add firmware/firmware.ino
git commit                         # ปิด merge
git log --oneline --graph --all
git branch -d feature/fast-blink''', 'terminal') + '''
<p class="note">merge เก็บประวัติตามจริง (มี merge commit) ส่วน <code class="il">git rebase main</code> ย้าย commit ของ branch ไปต่อท้าย main ทำให้ประวัติเป็นเส้นตรง กฎ: ห้าม rebase branch ที่คนอื่นดึงไปแล้ว</p>
''' + qa([('ถ้าแก้ conflict ผิดแล้วอยากเริ่มใหม่ทำอย่างไร?', 'git merge --abort ก่อน commit จะกลับไปสถานะก่อน merge'),
          ('ทำไมทีมไม่ commit ตรงเข้า main?', 'main ควร build ได้และ test ผ่านเสมอ การผ่าน branch + PR ให้ CI และคนอื่นตรวจก่อน และย้อนกลับง่าย')]))

lesson('14', 'B', 'GitHub: push และ Pull Request', 25, 'คอมพิวเตอร์', goal('มี repo สาธารณะเป็น portfolio และทำงานผ่าน PR แบบทีมจริง') + fig(SVG_PR, 'GitHub flow ที่บริษัทส่วนใหญ่ใช้') + '''
<h3>Hands-on</h3>''' + code('''# ติดตั้ง GitHub CLI (gh) แล้ว login ครั้งเดียว
gh auth login

# สร้าง repo บน GitHub จากโฟลเดอร์นี้ แล้ว push
gh repo create xiao-embedded-cpp --public --source=. --remote=origin --push

# งานใหม่ผ่าน PR
git switch -c docs/readme
# เขียน README.md: รูป wiring, วิธี build, ขาที่ใช้
git add README.md
git commit -m "docs: add README with wiring and build steps"
git push -u origin docs/readme
gh pr create --fill
# เปิดดู PR บนเว็บ ลอง comment โค้ดตัวเอง 1 จุด
gh pr merge --squash --delete-branch
git switch main && git pull''', 'terminal') + '''
<p>ตั้งค่าเพิ่มบนเว็บ: Settings → Branches → เพิ่ม rule ให้ <code class="il">main</code> ต้องผ่าน PR (เปิด required status checks หลังบท 16)</p>
''' + qa([('fetch กับ pull ต่างกันอย่างไร?', 'fetch ดึงข้อมูล remote มาเก็บไว้ (origin/main) แต่ยังไม่แตะ branch ของเรา pull = fetch + merge (หรือ rebase) เข้ามา'),
          ('squash merge ดีอย่างไร?', 'รวม commit ย่อยใน PR เป็น commit เดียวบน main ประวัติอ่านง่าย 1 commit = 1 ฟีเจอร์ ย้อน (revert) ง่าย')]) + iv('ผู้สัมภาษณ์มักเปิด GitHub ของผู้สมัครดูจริง README ที่มีรูป wiring, badge CI สีเขียว และประวัติ commit ที่สะอาด สร้างความน่าเชื่อถือได้มากกว่า resume'))

lesson('15', 'C', 'แยก logic ออกจากฮาร์ดแวร์ + unit test บน PC', 30, 'คอมพิวเตอร์', goal('รัน test ของ Debouncer และ RingBuffer บน PC ได้ในไม่กี่วินาที โดยไม่ต้องเสียบบอร์ด') + fig(SVG_LAYERS, 'ยิ่ง logic อยู่ชั้นที่ไม่รู้จักฮาร์ดแวร์มาก ยิ่ง test อัตโนมัติได้มาก') + '''
<p>Debouncer รับเวลาเป็นพารามิเตอร์ (<code class="il">nowMs</code>) แทนการเรียก <code class="il">millis()</code> เอง นี่คือเทคนิค dependency injection แบบง่ายที่สุด ทำให้ test ควบคุมเวลาได้ทุกมิลลิวินาที</p>
<h3>Hands-on</h3>''' + code(TEST, 'test/test_main.cpp') + code('''# Linux / macOS / WSL (Windows: ติดตั้ง g++ ผ่าน MSYS2 หรือใช้ WSL)
g++ -std=c++17 -Wall -Wextra -Werror -Ifirmware/src test/test_main.cpp -o test_runner
./test_runner
# ALL TESTS PASSED''', 'terminal') + '''
<p>ทดลองทำให้ test แดง: แก้ <code class="il">&gt;= stableMs_</code> ใน Debouncer.h เป็น <code class="il">&gt;</code> แล้วรันใหม่ ดูว่าบรรทัดไหน FAIL จากนั้นแก้กลับ แล้ว commit ด้วย <code class="il">test: add host unit tests</code></p>
<p class="note">ในงานจริงใช้ framework เช่น GoogleTest, Catch2 หรือ Unity (สำหรับ C) แต่หลักการเหมือนกัน: CHECK เงื่อนไข, รายงานบรรทัดที่พัง, exit code ≠ 0 เมื่อ fail เพื่อให้ CI รู้</p>
''' + qa([('ทำไม exit code สำคัญ?', 'CI ตัดสินผ่าน/ไม่ผ่านจาก exit code ของคำสั่ง 0 = ผ่าน อย่างอื่น = fail และหยุด pipeline'),
          ('จะ test โค้ดที่เรียก digitalRead() ได้อย่างไร?', 'ซ่อนการเข้าถึงฮาร์ดแวร์ไว้หลัง interface (เช่น ISensor บท 7) แล้วใส่ fake/mock ตอน test หรือส่งค่าที่อ่านได้เข้าฟังก์ชันแทนให้ฟังก์ชันไปอ่านเอง')]) + iv('"คุณ test firmware อย่างไร" ตอบเป็นชั้น: unit test บน host สำหรับ logic, HIL test บนบอร์ดจริงสำหรับ driver, system test สำหรับฟีเจอร์ แล้วบอกว่าชั้นแรกรันใน CI ทุก commit'))

CI_YML = '''name: CI

on:
  push:
    branches: [main]
  pull_request:

env:
  BOARD_URL: https://files.seeedstudio.com/arduino/package_seeeduino_boards_index.json
  FQBN: Seeeduino:nrf52:xiaonRF52840Sense   # ใช้ค่าที่ได้จาก board listall

jobs:
  host-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Build tests
        run: g++ -std=c++17 -Wall -Wextra -Werror -Ifirmware/src test/test_main.cpp -o test_runner
      - name: Run tests
        run: ./test_runner
      - name: Static analysis
        run: |
          sudo apt-get update && sudo apt-get install -y cppcheck
          cppcheck --error-exitcode=1 --enable=warning,performance --std=c++17 -Ifirmware/src test/test_main.cpp

  build-firmware:
    needs: host-tests
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install adafruit-nrfutil   # core ใช้ตอนแพ็ก .zip บน Linux
      - uses: arduino/setup-arduino-cli@v2
      - name: Install board core
        run: |
          arduino-cli core update-index --additional-urls "$BOARD_URL"
          arduino-cli core install Seeeduino:nrf52 --additional-urls "$BOARD_URL"
      - name: Compile
        run: arduino-cli compile --fqbn "$FQBN" --additional-urls "$BOARD_URL" --output-dir out firmware
      - uses: actions/upload-artifact@v4
        with:
          name: firmware
          path: out/'''

lesson('16', 'C', 'CI ด้วย GitHub Actions', 30, 'คอมพิวเตอร์', goal('ทุก push และทุก PR ถูก test และ compile firmware อัตโนมัติ') + fig(SVG_CI, 'workflow 2 job: test ก่อน ผ่านแล้วค่อย build') + '''
<h3>Hands-on</h3><p>สร้างไฟล์ตาม path นี้ใน repo</p>''' + code(CI_YML, '.github/workflows/ci.yml') + code('''git switch -c ci/github-actions
git add .github/ test/
git commit -m "ci: run host tests and compile firmware"
git push -u origin ci/github-actions
gh pr create --fill
gh pr checks --watch        # ดูสถานะ job แบบ live''', 'terminal') + '''
<ol>
<li>เปิดแท็บ Actions บน GitHub ดู log ของแต่ละ step เมื่อเขียวแล้ว ดาวน์โหลด artifact <i>firmware</i> ดูว่ามี .hex</li>
<li>ทำ PR อีกอันที่ตั้งใจให้ test fail ดูว่า PR ขึ้นกากบาทแดงและบอกบรรทัดที่พัง</li>
<li>ไปที่ Settings → Branches เปิด required status checks ให้ <code class="il">host-tests</code> และ <code class="il">build-firmware</code></li>
<li>ใส่ badge ใน README: <code class="il">![CI](https://github.com/&lt;user&gt;/xiao-embedded-cpp/actions/workflows/ci.yml/badge.svg)</code></li>
</ol>
<p class="note">ความเสี่ยงที่ควรรู้: ถ้า compile ใน CI ล้มที่ขั้น packaging ให้ดูว่าติดตั้ง adafruit-nrfutil แล้ว และ FQBN ตรงกับที่ <code class="il">arduino-cli board listall xiao</code> แสดง เวอร์ชัน core ควร pin ด้วย <code class="il">Seeeduino:nrf52@x.y.z</code> เพื่อให้ build ซ้ำได้เหมือนเดิม</p>
''' + qa([('needs: host-tests มีไว้ทำไม?', 'ให้ build-firmware รันหลัง test ผ่านเท่านั้น ประหยัดเวลาและสื่อลำดับความสำคัญ ถ้าไม่ใส่ 2 job จะรันขนานกัน'),
          ('ทำไมต้อง pin เวอร์ชัน core / action?', 'ให้ build reproducible ถ้า core อัปเดตเอง firmware อาจเปลี่ยนพฤติกรรมโดยไม่มีใครแก้โค้ด เป็นหลักเดียวกับ BOM lock ในฮาร์ดแวร์')]) + iv('อธิบายความต่าง CI กับ CD ให้ชัด: CI = รวมโค้ดบ่อยและตรวจอัตโนมัติทุกครั้ง, CD = ส่งมอบ artifact ที่พร้อมใช้อัตโนมัติ (บทถัดไป)'))

REL_YML = '''name: Release

on:
  push:
    tags: ['v*.*.*']

permissions:
  contents: write

env:
  BOARD_URL: https://files.seeedstudio.com/arduino/package_seeeduino_boards_index.json
  FQBN: Seeeduino:nrf52:xiaonRF52840Sense

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install adafruit-nrfutil
      - uses: arduino/setup-arduino-cli@v2
      - run: |
          arduino-cli core update-index --additional-urls "$BOARD_URL"
          arduino-cli core install Seeeduino:nrf52 --additional-urls "$BOARD_URL"
      - name: Stamp version
        run: echo "#define FW_VERSION \\"${GITHUB_REF_NAME}\\"" > firmware/src/version.h
      - name: Compile
        run: arduino-cli compile --fqbn "$FQBN" --additional-urls "$BOARD_URL" --output-dir out firmware
      - uses: softprops/action-gh-release@v2
        with:
          files: |
            out/*.hex
            out/*.zip
          generate_release_notes: true'''

lesson('17', 'C', 'CD: release firmware อัตโนมัติด้วย tag', 25, 'บอร์ด + คอมพิวเตอร์', goal('push tag แล้วได้ GitHub Release ที่มีไฟล์ firmware และเลขเวอร์ชันฝังในตัว') + fig(SVG_REL, 'จาก tag ถึงไฟล์ที่ QA ดาวน์โหลดไปแฟลช') + '''
<h3>Hands-on</h3>''' + code(REL_YML, '.github/workflows/release.yml') + code('''git add .github/workflows/release.yml
git commit -m "ci: release firmware on version tag"
git push

git tag -a v0.1.0 -m "first release: scheduler, debounce, moving average"
git push origin v0.1.0''', 'terminal') + '''
<p>เปิดหน้า Releases ดาวน์โหลด .hex แฟลชลงบอร์ด เปิด Serial Monitor ต้องเห็น <code class="il">fw v0.1.0</code> (ถ้า build ในเครื่องจะเห็น <code class="il">fw dev</code>) นี่คือ traceability: รู้เสมอว่าบอร์ดตัวไหนรัน firmware commit ไหน</p>
<p class="note">SemVer: MAJOR.MINOR.PATCH — แก้บั๊ก +PATCH, ฟีเจอร์ใหม่ที่เข้ากันได้ +MINOR, เปลี่ยนแบบเข้ากันไม่ได้ (เช่น protocol) +MAJOR ถ้าต้องการไฟล์ .uf2 สำหรับลากวางตอน double-tap reset ให้แปลงจาก .hex ด้วย uf2conv.py (family 0xADA52840)</p>
''' + qa([('ทำไมสร้าง version.h ใน CI แทนเขียนเลขเวอร์ชันในโค้ด?', 'ให้ tag เป็นแหล่งความจริงแหล่งเดียว ลืมแก้เลขไม่ได้ และ build ในเครื่องจะติด "dev" ชัดเจนว่าไม่ใช่ของ release'),
          ('permissions: contents: write จำเป็นไหม?', 'จำเป็น GITHUB_TOKEN ค่าเริ่มต้นอ่านอย่างเดียวในหลาย repo ต้องให้สิทธิ์เขียนเพื่อสร้าง Release')]))

lesson('18', 'C', 'Capstone และเตรียมสัมภาษณ์', 30, 'ทั้งหมด', goal('ปิด repo ให้พร้อมเป็น portfolio และซ้อมตอบคำถามที่เจอบ่อย') + '''
<h3>Checklist ของ repo</h3>
<ul class="check">
<li>README: รูป wiring, ตารางขา, วิธี build ในเครื่อง, วิธีรัน test, badge CI</li>
<li>โครงสร้าง <code class="il">firmware/</code>, <code class="il">firmware/src/</code>, <code class="il">test/</code>, <code class="il">.github/workflows/</code></li>
<li>อย่างน้อย 1 release (v0.1.0) และประวัติ commit ที่ใช้ Conventional Commits</li>
<li>เพิ่ม test ของคุณเอง 1 ชุด เช่น ทดสอบ <code class="il">average()</code> ตอน buffer ว่าง</li>
<li>ฟีเจอร์ต่อยอด 1 อย่าง: กดค้าง 1 วินาที = reset ค่า (เพิ่ม Event::LongPress ใน Debouncer พร้อม test)</li>
</ul>
<h3>คำถามที่ควรตอบได้ภายใน 1 นาที</h3>
''' + ''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in [
 ('C++ ต่างจาก C ในงาน embedded อย่างไร มีต้นทุนอะไรบ้าง?', 'ได้ class, RAII, reference, template, constexpr, enum class, namespace ที่ส่วนใหญ่ไม่มี runtime cost ส่วนที่มีต้นทุนคือ virtual (vtable), exceptions, RTTI, heap ผ่าน STL บางตัว จึงเลือกใช้เป็น subset'),
 ('volatile ใช้เมื่อไหร่ และไม่ได้ช่วยอะไร?', 'ตัวแปรที่ ISR แก้, register ของ peripheral, ข้อมูลที่แชร์ระหว่าง context ไม่ได้ทำให้ atomic และไม่ใช่ memory barrier'),
 ('ISR ที่ดีเป็นอย่างไร?', 'สั้น, ไม่ block, ไม่จอง memory, ตั้ง flag หรือ push ลง ring buffer แล้วให้ main/task ประมวลผล ข้อมูลที่แชร์ต้องป้องกันด้วย critical section'),
 ('ทำไมเลี่ยง dynamic allocation หลัง init?', 'fragmentation, เวลาไม่แน่นอน, และ fail ได้ตอนรันไปนาน ๆ ระบบที่ต้องทำงานต่อเนื่องจึงจองทุกอย่างแบบ static'),
 ('อธิบาย RAII พร้อมตัวอย่าง', 'ผูกอายุ resource กับ object: CriticalSection ปิด interrupt ใน ctor คืนค่าใน dtor ออกจาก scope ทางไหนก็คืนเสมอ'),
 ('debounce มีกี่วิธี?', 'ฮาร์ดแวร์ (RC + Schmitt trigger) และซอฟต์แวร์ (รอให้นิ่งตามเวลา หรือ sample หลายครั้ง) เลือกตามต้นทุน BOM กับ CPU'),
 ('merge กับ rebase เลือกอย่างไร?', 'merge เก็บประวัติจริงและปลอดภัยกับ branch ที่แชร์ rebase ทำประวัติเส้นตรง ใช้กับ branch ส่วนตัวก่อนเปิด PR'),
 ('pipeline CI/CD ของ firmware ควรมีอะไร?', 'build ทุก target, unit test บน host, static analysis, เก็บ artifact, release ตาม tag พร้อมเวอร์ชันฝังใน binary, ขั้นต่อไปคือ HIL test บน runner ที่ต่อบอร์ดจริง'),
]) + fig(SVG_ROAD, 'เส้นทางต่อหลังจบคอร์ส') + iv('ประสบการณ์ PCB, failure analysis และ V&amp;V ที่มีอยู่คือจุดแข็งที่คนสาย firmware ล้วนไม่มี ใน portfolio ให้เชื่อม 2 ฝั่ง เช่น อธิบายว่าเลือกค่า R ของ LED และ debounce time จากอะไร'))

# ---------------- page ----------------
WK = T('สัปดาห์', 'Week')
WEEKS = [(f'{WK} 1', ['00', '01', '02', '03', '04']), (f'{WK} 2', ['05', '06', '07', '08', '09']),
         (f'{WK} 3', ['10', '11', '12', '13', '14']), (f'{WK} 4', ['15', '16', '17', '18'])]
byn = {l['num']: l for l in LESSONS}
plan = ''
for w, nums in WEEKS:
    items = ''.join(f'<li><a href="#l{n}"><span class="pn2 m">{n}</span><span class="pt">{html.escape(byn[n]["title"])}</span><span class="pm2">{byn[n]["mins"]}′</span></a><span class="dot" data-for="l{n}"></span></li>' for n in nums)
    plan += f'<div class="wk"><h3>{w}</h3><ol>{items}</ol></div>'

opts = ''.join(f'<option value="l{l["num"]}">{l["num"]} · {html.escape(l["title"])}</option>' for l in LESSONS)
secs = ''
for l in LESSONS:
    secs += f'''<section class="lesson" id="l{l["num"]}">
<header class="lh"><span class="big m">{l["num"]}</span><div class="lhm"><p class="mod">{MODS[l["mod"]]}</p><h2>{html.escape(l["title"])}</h2><p class="meta">{l["mins"]} {T("นาที · ฮาร์ดแวร์", "min · Hardware")}: {l["hw"]}</p></div></header>
{l["body"]}
<label class="done"><input type="checkbox" id="done-l{l["num"]}" data-l="l{l["num"]}"> {T("เรียนบทนี้จบแล้ว", "I finished this lesson")}</label>
</section>'''

CSS = open(os.path.join(D, 'style.css'), encoding='utf-8').read()
JS = open(os.path.join(D, 'app.js'), encoding='utf-8').read()
# th lives at the site root, en under /en/
OTHER = {'th': ('en/', 'EN', 'Read in English'), 'en': ('../', 'ไทย', 'อ่านภาษาไทย')}[LANG]
page = f'''<title>{T('Embedded C++ บน XIAO', 'Embedded C++ on XIAO')}</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Chakra+Petch:wght@500;600;700&family=IBM+Plex+Sans+Thai:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap">
<style>{CSS}</style>
<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>
<marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" class="mk"/></marker>
<marker id="aha" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" class="mka"/></marker>
</defs></svg>
<div class="bar"><div class="barin">
<a href="#top" class="brand m">XIAO·C++</a>
<select id="jump" aria-label="{T('ไปที่บทเรียน', 'Go to lesson')}"><option value="top">{T('สารบัญ', 'Contents')}</option>{opts}</select>
<div class="prog" aria-label="{T('ความคืบหน้า', 'Progress')}"><div class="pf" id="pf"></div></div><span class="pc m" id="pc">0/19</span>
<a href="{OTHER[0]}" class="lang" id="lang" hreflang="{'en' if LANG == 'th' else 'th'}" aria-label="{OTHER[2]}">{OTHER[1]}</a>
</div></div>
<main class="wrap" id="top">
<header class="hero">
<p class="eyebrow m">nRF52840 · Cortex-M4F · {T('19 บท · วันละ 20–30 นาที', '19 lessons · 20–30 min a day')}</p>
<h1>{T('Embedded C++ บน XIAO', 'Embedded C++ on XIAO')}</h1>
<p class="lede">{T('ปูพื้น C++ สำหรับคนที่เขียน C มาแล้ว ผ่านการลงมือบนบอร์ดจริง ต่อด้วย Git, GitHub และ CI/CD จนได้ repo ที่ใช้เป็น portfolio ตอนสมัครงานสาย firmware',
 'C++ foundations for people who already write C, learned hands-on with a real board, followed by Git, GitHub and CI/CD, ending with a repo you can use as a portfolio when applying for firmware jobs.')}</p>
{T('', '<p class="note">The English translation is in progress. Lessons that are not translated yet are shown in Thai.</p>')}
</header>
<section class="ov">
<div class="ovg">
<div><h2>{T('วิธีเรียน', 'How to study')}</h2><p>{T('เรียนวันละบทตามลำดับ แต่ละบทมี เป้าหมาย → แนวคิด + diagram → hands-on → คำถามเช็ก ทุกบทต่อยอดจากบทก่อน โค้ดในบท 6, 8, 11 จะถูกนำไป test และ build ใน CI ช่วงท้าย',
 'Take one lesson a day, in order. Each lesson goes goal → concept + diagram → hands-on → check questions, and builds on the one before. The code from lessons 6, 8 and 11 is tested and built in CI near the end.')}</p>
<p>{T('บท 00–11 ใช้ Arduino IDE 2 + core Seeed nRF52 (non-mbed) เพราะเร็วที่สุดในการเห็นผล หลักภาษาเหมือนกันทุก framework เมื่อจบแล้วย้ายไป nRF Connect SDK / Zephyr ได้ทันที',
 'Lessons 00–11 use Arduino IDE 2 with the Seeed nRF52 (non-mbed) core, the fastest way to see results. The language rules are the same in every framework, so you can move to nRF Connect SDK / Zephyr right after.')}</p></div>
<div><h2>{T('อุปกรณ์', 'Parts')}</h2><ul class="kit">
<li><b>1</b> Seeed XIAO nRF52840 (Sense) + {T('สาย USB-C แบบ data', 'USB-C data cable')}</li>
<li><b>1</b> breadboard + {T('สาย jumper', 'jumper wires')}</li>
<li><b>1</b> LED 5 mm + R 1 kΩ</li>
<li><b>1</b> {T('ปุ่มกด tactile', 'tactile push button')}</li>
<li><b>1</b> potentiometer 10 kΩ</li>
<li><b>—</b> Git, Arduino IDE 2, arduino-cli, {T('บัญชี GitHub', 'GitHub account')}</li></ul></div>
</div>
<div class="plan">{plan}</div>
</section>
{secs}
<section class="author" id="author">
<p class="mod">{T('ผู้จัดทำ', 'Author')}</p>
<h2>Wiputpong Klinsukon (Ake)</h2>
<p>{T('Hardware &amp; firmware engineer ประสบการณ์กว่า 13 ปีในงานออกแบบวงจร, PCB, firmware C/C++, การทดสอบ V&amp;V และ failure analysis ของอุปกรณ์ wearable และ IoT เขียนคอร์สนี้จากการเรียนจริงบนบอร์ด XIAO nRF52840 เพื่อแบ่งปันให้คนที่อยากเริ่มสาย embedded',
 'Hardware &amp; firmware engineer with over 13 years in circuit design, PCB, C/C++ firmware, V&amp;V testing and failure analysis for wearable and IoT devices. I wrote this course while learning on the XIAO nRF52840 myself, to share it with anyone starting out in embedded.')}</p>
<p class="links"><span>GitHub: <a href="https://github.com/wiputpong-k">github.com/wiputpong-k</a></span><span>{T('ข้อเสนอแนะ', 'Feedback')}: <a href="https://github.com/wiputpong-k/embedded-cpp-xiao/issues">{T('เปิด Issue ใน repo ของคอร์ส', 'open an issue in the course repo')}</a></span></p>
</section>
<footer class="ft"><p>{T('ตรวจแล้ว: Debouncer.h, RingBuffer.h และ test_main.cpp คอมไพล์ด้วย g++ 13 (-Wall -Wextra -Werror) และ test ผ่านทั้งหมด ส่วนโค้ดบนบอร์ดและ workflow ให้ยืนยัน FQBN กับเวอร์ชัน core ในเครื่องของคุณ',
 'Verified: Debouncer.h, RingBuffer.h and test_main.cpp compile with g++ 13 (-Wall -Wextra -Werror) and all tests pass. For the on-board code and workflows, confirm the FQBN and core version on your own machine.')}</p></footer>
</main>
<script>{JS}</script>'''
sfx = '' if LANG == 'th' else '-en'
open(os.path.join(D, f'course{sfx}.html'), 'w', encoding='utf-8').write(page)
print(LANG, len(page))
alt = {'th': ('./', 'en/'), 'en': ('../', './')}[LANG]
std = (f'<!doctype html>\n<html lang="{LANG}">\n<head>\n<meta charset="utf-8">\n'
       '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
       f'<link rel="alternate" hreflang="th" href="{alt[0]}"><link rel="alternate" hreflang="en" href="{alt[1]}">\n'
       '<style>:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}body{margin:0}img{max-width:100%}[hidden]{display:none!important}</style>\n'
       + page.replace('<div class="bar">', '</head>\n<body>\n<div class="bar">', 1) + '\n</body>\n</html>\n')
out = os.path.join(D, 'pages', '' if LANG == 'th' else 'en')
os.makedirs(out, exist_ok=True)
open(os.path.join(out, 'index.html'), 'w', encoding='utf-8').write(std)
