import hashlib, html, json, os, re, runpy, shutil
D = os.path.dirname(os.path.abspath(__file__))
LANGS = ('th', 'en')
# Running `python build.py` re-runs this file once per language with LANG preset.
if 'LANG' not in globals():
    shutil.rmtree(os.path.join(D, 'pages'), ignore_errors=True)
    for l in LANGS: runpy.run_path(os.path.abspath(__file__), init_globals={'LANG': l}, run_name='__build__')
    raise SystemExit
def T(th, en=None):
    """Bilingual text: Thai is the source; English falls back to Thai until translated."""
    return en if LANG == 'en' and en is not None else th
def tr(s, en):
    """English page: swap Thai fragments in shared code/SVG. Fails if a fragment no longer exists."""
    if LANG != 'en' or not en: return s
    for a, b in en.items():
        assert a in s, f'tr(): Thai text not found: {a}'
        s = s.replace(a, b)
    return s
def rd(p): return open(os.path.join(D, 'hw', p), encoding='utf-8').read().rstrip()
RING, DEB, TEST = rd('firmware/src/RingBuffer.h'), rd('firmware/src/Debouncer.h'), rd('test/test_main.cpp')
# English page: comments only; the tested code itself is untouched
DEB = tr(DEB, {'ไม่เรียก Arduino API เลย จึง test บน PC ได้': 'never calls the Arduino API, so it can be tested on a PC',
               'true = กดอยู่ (แปลง active-LOW มาแล้ว), nowMs: เวลาปัจจุบัน': 'true = pressed (already converted from active-LOW), nowMs: current time',
               'ยังเด้งอยู่ → เริ่มจับเวลาใหม่': 'still bouncing → restart the timer'})
RING = tr(RING, {'core ของ Seeed nRF52 มี class RingBuffer อยู่แล้ว จึงต้องอยู่ใน namespace ไม่ให้ชื่อชนกัน': 'The Seeed nRF52 core already has a class RingBuffer, so this one lives in a namespace to avoid the clash',
                 'FIFO ขนาดคงที่ ไม่ใช้ heap — ขนาด N ถูกกำหนดตอน compile': 'Fixed-size FIFO, no heap: N is set at compile time',
                 '// เต็มแล้วให้ทิ้งตัวเก่าสุด (เหมาะกับ moving average)': '// when full, drop the oldest (good for a moving average)',
                 '// เต็ม': '// full', '// ว่าง': '// empty', '// 0 = เก่าสุด': '// 0 = oldest'})
TEST = tr(TEST, {'// เต็มแล้ว': '// already full', '// FIFO: ออกตัวแรกก่อน': '// FIFO: first in, first out', '// เต็ม → ทิ้ง 2': '// full → drops 2',
                 '// เริ่มกด': '// press starts', '// เด้ง': '// bounce', '// นิ่งมาแค่ 12 ms': '// stable for only 12 ms',
                 '// กดค้าง ไม่ยิงซ้ำ': '// held down, no repeat event'})

def code(txt, label='', en=None):
    txt = tr(txt, en)
    if label.endswith('.ino'):
        # The Seeed nRF52 core links USB (TinyUSB) only when the sketch includes it; without it there is no
        # USB port or Serial output. Every sketch therefore starts with this line (explained in lesson 00).
        txt = T('#include <Adafruit_TinyUSB.h>   // เปิด USB และ Serial (core นี้ต้องมี)',
                '#include <Adafruit_TinyUSB.h>   // enables USB and Serial (required by this core)') + '\n' + txt.lstrip('\n')
    lab = f'<div class="cl">{label}</div>' if label else ''
    return f'<div class="code">{lab}<pre><code>{html.escape(txt.strip(chr(10)))}</code></pre></div>'

def fig(svg, cap):
    return f'<figure class="dg"><div class="sv">{svg}</div><figcaption>{cap}</figcaption></figure>'

def video(name, w, h, cap, max_w=320):
    """Course video from site-src/media/ (copied to the site's media/). @ROOT@ becomes the path to the site root."""
    return (f'<figure class="dg ph"><video src="@ROOT@media/{name}" width="{w}" height="{h}" style="max-width:min(100%,{max_w}px);height:auto" '
            f'autoplay muted loop playsinline controls preload="metadata"></video><figcaption>{cap}</figcaption></figure>')

def photo(src, w, h, alt, cap, credit, credit_url, max_w=None):
    """Third-party image: linked from its source (not copied into the repo), with a visible credit.
    Sizing is inline so a stale cached stylesheet can never let a large image stretch the page."""
    style = f'max-width:min(100%,{max_w}px)' if max_w else 'max-width:100%'
    return (f'<figure class="dg ph"><a href="{src}"><img src="{src}" width="{w}" height="{h}" style="{style};height:auto" loading="lazy" alt="{html.escape(alt)}"></a>'
            f'<figcaption>{cap} <span class="credit">({T("ที่มา", "Source")}: <a href="{credit_url}">{credit}</a>)</span></figcaption></figure>')

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

SVG_ENTRY = '''<svg viewBox="0 0 400 346" role="img">
<rect x="110" y="10" width="180" height="34" rx="8" class="b"/><text x="200" y="32" text-anchor="middle" class="tt">Reset / จ่ายไฟ</text>
<line x1="200" y1="46" x2="200" y2="70" class="ln" marker-end="url(#ah)"/>
<rect x="30" y="74" width="340" height="50" rx="8" class="b"/><text x="200" y="95" text-anchor="middle" class="tt m">startup code (Reset_Handler)</text>
<text x="200" y="113" text-anchor="middle" class="sub">เตรียม stack และตัวแปร global แล้วเรียก main()</text>
<line x1="200" y1="126" x2="110" y2="154" class="ln" marker-end="url(#ah)"/><line x1="200" y1="126" x2="290" y2="154" class="ln" marker-end="url(#ah)"/>
<text x="105" y="174" text-anchor="middle" class="sub">C แบบ bare-metal</text><text x="295" y="174" text-anchor="middle" class="sub">Arduino (.ino)</text>
<rect x="12" y="184" width="186" height="50" rx="8" class="ba"/><text x="105" y="205" text-anchor="middle" class="tt m">main()</text>
<text x="105" y="223" text-anchor="middle" class="sub m">src/main.c · คุณเขียน</text>
<rect x="202" y="184" width="186" height="50" rx="8" class="bm"/><text x="295" y="205" text-anchor="middle" class="tt m">main()</text>
<text x="295" y="223" text-anchor="middle" class="sub m">core/main.cpp · มีให้แล้ว</text>
<line x1="105" y1="236" x2="105" y2="258" class="ln" marker-end="url(#ah)"/><line x1="295" y1="236" x2="295" y2="258" class="ln" marker-end="url(#ah)"/>
<rect x="12" y="262" width="186" height="50" rx="8" class="ba"/><text x="105" y="283" text-anchor="middle" class="tt m">init + while (1)</text>
<text x="105" y="301" text-anchor="middle" class="sub">คุณเขียนเองทั้งหมด</text>
<rect x="202" y="262" width="186" height="50" rx="8" class="ba"/><text x="295" y="283" text-anchor="middle" class="tt m">setup() · loop()</text>
<text x="295" y="301" text-anchor="middle" class="sub">ใน .ino · คุณเขียนแค่นี้</text>
<text x="200" y="336" text-anchor="middle" class="sub">กรอบเน้นสี = โค้ดที่คุณเขียน · ส่วนอื่นมากับชิปหรือ core</text>
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
    ('Working directory', T('ไฟล์ที่คุณแก้อยู่จริงในเครื่อง', 'the files you are actually editing'), 'b'),
    ('Staging area (index)', T('รายการที่จะเข้า commit ถัดไป', 'what goes into the next commit'), 'bm'),
    ('Local repository (.git)', T('ประวัติ commit ทั้งหมดในเครื่อง', 'full commit history on your machine'), 'ba'),
    ('Remote (GitHub)', T('สำเนาบนเซิร์ฟเวอร์ แชร์กับทีม / CI', 'server copy, shared with the team / CI'), 'b'),
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
    ('firmware.ino', T('ที่คุณเขียน', 'what you write'), 'b'),
    ('Arduino preprocessor', T('#include <Arduino.h> + สร้าง prototype ให้', '#include <Arduino.h> + generated prototypes'), 'b'),
    ('firmware.ino.cpp', T('กลายเป็นไฟล์ C++ ปกติ', 'now a plain C++ file'), 'bm'),
    ('arm-none-eabi-g++', 'compile → .o (Cortex-M4F)', 'ba'),
    ('linker + linker script', T('รวม core.a + libs → .elf', 'core.a + libs → .elf'), 'b'),
    ('objcopy / packager', '.hex · .zip (DFU) · .uf2', 'bm'),
], ['', '', '', '', ''])

SVG_SCHED = flow([
    ('loop()', T('วนเร็วที่สุด ไม่มี delay()', 'spins as fast as it can, no delay()'), 'b'),
    ('now = millis()', '', 'b'),
    (T('ทุก task: now − lastRun ≥ period ?', 'each task: now − lastRun ≥ period ?'), T('ใช่ → lastRun = now; run()', 'yes → lastRun = now; run()'), 'ba'),
    ('handleSerial()', T('อ่านคำสั่งทีละตัวอักษร ไม่ block', 'reads input one char at a time, never blocks'), 'bm'),
], ['', '', T('แล้ววนกลับ', 'and repeat')])

SVG_PR = flow([
    ('git switch -c feature/x', T('แตก branch จาก main', 'branch off main'), 'b'),
    ('commit + git push', '', 'b'),
    ('Pull Request', T('คำอธิบาย + diff ให้คน review', 'description + diff for review'), 'ba'),
    (T('CI ตรวจอัตโนมัติ', 'automatic CI checks'), T('test + build ต้องผ่าน', 'test + build must pass'), 'bm'),
    ('Review → Squash merge', T('ลบ branch · main สะอาด', 'branch deleted · clean main'), 'b'),
])

SVG_CI = flow([
    ('push / pull_request', T('event ที่ trigger workflow', 'events that trigger the workflow'), 'b'),
    ('job: host-tests', 'g++ → ./test_runner → cppcheck', 'ba'),
    ('job: build-firmware', 'arduino-cli compile (needs: host-tests)', 'bm'),
    ('artifact: firmware', T('.hex / .zip ดาวน์โหลดได้จากหน้า Actions', '.hex / .zip, downloadable from Actions'), 'b'),
], ['ubuntu runner', T('ผ่านแล้วค่อยรัน', 'runs only if tests pass'), ''])

SVG_REL = flow([
    ('git tag -a v0.1.0', T('ติดเวอร์ชันแบบ SemVer', 'SemVer version tag'), 'b'),
    ('git push origin v0.1.0', '', 'b'),
    ('release.yml', T('สร้าง version.h → compile', 'write version.h → compile'), 'ba'),
    ('GitHub Release', T('แนบ .hex / .zip + release notes', 'attach .hex / .zip + release notes'), 'bm'),
    (T('ทีม / QA ดาวน์โหลดไปแฟลช', 'team / QA download and flash'), T('ทุกเวอร์ชันย้อนกลับได้', 'any version can be restored'), 'b'),
])

SVG_ROAD = flow([
    (T('คอร์สนี้', 'This course'), 'C++ · RAII · ISR · test · CI/CD', 'ba'),
    (T('I²C + IMU บนบอร์ด (Sense)', 'I²C + on-board IMU (Sense)'), T('driver class ของ LSM6DS3', 'LSM6DS3 driver class'), 'b'),
    ('BLE peripheral', T('ส่งค่าเซนเซอร์เข้ามือถือ', 'stream sensor data to a phone'), 'b'),
    ('Zephyr / nRF Connect SDK', T('RTOS · devicetree · ใช้จริงในอุตสาหกรรม', 'RTOS · devicetree · used across industry'), 'bm'),
    ('Custom board + production test', T('สิ่งที่คุณทำงานอยู่แล้ว ต่อยอดได้', 'builds on the work you already do'), 'b'),
])

# English labels for hand-drawn diagrams (keep each line inside its viewBox)
SVG_PINOUT = tr(SVG_PINOUT, {'สีส้ม = ขาที่ใช้ในคอร์ส: D0 Pot · D1 ปุ่ม · D2 LED ภายนอก': 'Orange = course pins: D0 pot · D1 button · D2 external LED'})
SVG_REF = tr(SVG_REF, {'ชื่อเล่นของ current': 'alias of current', 'เป็นตัวแปรแยก · null ได้ · ชี้ใหม่ได้': 'nullable · can re-point',
                       'ไม่ใช่ตัวแปรใหม่ · ต้องผูกตอนสร้าง': 'never null · bound at init'})
SVG_ENTRY = tr(SVG_ENTRY, {'จ่ายไฟ': 'power-up', 'เตรียม stack และตัวแปร global แล้วเรียก main()': 'sets up stack and globals, then calls main()',
                           'C แบบ bare-metal': 'Bare-metal C', '· คุณเขียน<': '· yours<', '· มีให้แล้ว': '· provided',
                           'คุณเขียนเองทั้งหมด': 'all written by you', 'ใน .ino · คุณเขียนแค่นี้': 'in .ino · all you write',
                           'กรอบเน้นสี = โค้ดที่คุณเขียน · ส่วนอื่นมากับชิปหรือ core': 'Highlighted = code you write · the rest comes with the chip or core'})
SVG_MANGLE = tr(SVG_MANGLE, {'ซอร์ส C++ (namespace logx)': 'C++ source (namespace logx)', 'ชื่อ symbol ใน .o / .elf': 'symbol name in .o / .elf',
                             'ถ้าต้องเรียกจาก C หรือ ASM ใช้ extern "C" ปิด mangling': 'Called from C or ASM? extern "C" turns mangling off'})
SVG_WIRE = tr(SVG_WIRE, {'LED (ขายาว = +)': 'LED (long leg = +)', '— พอเห็นชัด และไม่เกิน standard drive ของ GPIO': ': bright enough, safe for GPIO'})
SVG_RAII = tr(SVG_RAII, {'// ... งานที่จับเวลา ...': '// ... timed work ...', '// ออกจาก scope': '// leave scope',
                         'compiler รับประกันว่า destructor ถูกเรียกเสมอ ไม่ว่าออกด้วย return ทางไหน': 'The destructor always runs, whichever way you leave the scope'})
SVG_BOUNCE = tr(SVG_BOUNCE, {'ขา D1 (raw) — HIGH = ปล่อย, LOW = กด': 'Pin D1 (raw): HIGH = released, LOW = pressed', 'หลัง Debouncer': 'After Debouncer'})
SVG_STATE = tr(SVG_STATE, {'>กด<': '>press<'})
SVG_VTABLE = tr(SVG_VTABLE, {'vtable ของ PotSensor (flash)': 'PotSensor vtable (flash)', 'อ่าน vptr → อ่าน entry [2] → กระโดดไปเรียก': 'load vptr → load entry [2] → jump',
                             'ต้นทุน: RAM +4 B ต่อ object, flash 1 ตารางต่อ class, call ทางอ้อม 1 ครั้ง': 'Cost: +4 B RAM/object, 1 flash table/class, 1 indirect call',
                             'FakeSensor มี vtable ของตัวเอง ชี้ไปฟังก์ชันของมัน': 'FakeSensor has its own vtable pointing to its own functions'})
SVG_RING = tr(SVG_RING, {'วนกลับต้น buffer ไม่ต้องเลื่อนข้อมูล': 'wraps to the start, no data moves'})
SVG_MEM = tr(SVG_MEM, {'>ไม่หายเมื่อไฟดับ<': '>kept without power<', '>หายเมื่อไฟดับ<': '>lost without power<', '>ว่าง<': '>free<',
                       '.data ค่าเริ่มต้น': '.data initial values', '.text โค้ด': '.text code', 'ตัวแปร local, ISR': 'locals, ISR frames',
                       '.data (static มีค่า)': '.data (initialized)', '(ล่าง)': '(bottom)',
                       'ลูกศรส้ม: startup code copy .data จาก flash ไป RAM ก่อน setup()': 'Orange arrow: startup copies .data flash → RAM before setup()'})
SVG_BRANCH = tr(SVG_BRANCH, {'ถ้า 2 branch แก้บรรทัดเดียวกัน git จะหยุดให้คุณเลือก = merge conflict': 'Same line changed on both branches → git stops = merge conflict',
                             '>แก้บรรทัดเดียวกัน<': '>same line edited<'})
SVG_LAYERS = tr(SVG_LAYERS, {'ประกอบชิ้นส่วน · scheduler · wiring': 'glue code · scheduler · wiring', '— ไม่รู้จัก Arduino': ': no Arduino',
                             'test บน PC': 'test on PC', 'g++ · วินาที · ใน CI': 'g++ · secs · CI', 'test บนบอร์ด': 'test on board',
                             'ช้ากว่า · ต้องมือ': 'slower · manual',
                             'กฎ: logic ที่ซับซ้อนควรอยู่ชั้นส้ม เพราะ test อัตโนมัติได้': 'Rule: complex logic goes in the orange layer, which CI can test'})
SVG_ISR = tr(SVG_ISR, {'อ่าน pressCount': 'read pressCount', 'ทำงานต่อจากเดิม': 'resume where it was',
                       'ขอบ FALLING ที่ D1 → CPU กระโดดเข้า ISR ทันที': 'FALLING edge on D1 → CPU jumps to the ISR',
                       'ISR: สั้น · ไม่ delay · ไม่ Serial': 'ISR: short · no delay · no Serial'})

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
def iv(t): return f'<aside class="iv"><b>{T("มุมงานจริง", "In practice")}</b><p>{t}</p></aside>'
def goal(t): return f'<p class="goal"><b>{T("เป้าหมาย", "Goal")}</b> {t}</p>'
def vs(c, cpp): return f'<div class="vs"><div><span class="tag">C</span><p>{c}</p></div><div><span class="tag t2">C++</span><p>{cpp}</p></div></div>'

BOARD = T('บอร์ดอย่างเดียว', 'Board only')
POT = T('Pot ที่ A0', 'Pot on A0')
BTN = T('ปุ่มกดที่ D1', 'Button on D1')
PC = T('คอมพิวเตอร์', 'Computer')

SEEED_URL = 'https://files.seeedstudio.com/arduino/package_seeeduino_boards_index.json'

# Lesson content lives in lessons/lNN.py, one file per lesson, run in file order.
for _f in sorted(os.listdir(os.path.join(D, 'lessons'))):
    if re.fullmatch(r'l\d\d\.py', _f):
        exec(compile(open(os.path.join(D, 'lessons', _f), encoding='utf-8').read(), _f, 'exec'))

# ---------------- pages ----------------
# Site layout (th at the root, en under en/):
#   index.html, lesson/NN/index.html, assets/style.css, assets/app.js (assets shared by both languages)
N = len(LESSONS)
OUT = os.path.join(D, 'pages')
LROOT = '' if LANG == 'th' else '../'          # from this language's home to the site root
TITLE = T('Embedded C++ บน XIAO', 'Embedded C++ on XIAO')
MINS = T('นาที', 'min')
# Version tag on asset URLs, so browsers fetch the new CSS/JS as soon as it changes
ASSET_V = hashlib.sha1(b''.join(open(os.path.join(D, f), 'rb').read() for f in ('style.css', 'app.js'))).hexdigest()[:8]

def strip(s): return html.unescape(re.sub(r'<[^>]+>', '', s)).strip()

def add_toc(body):
    """Give every h3 an id (s1, s2, ...) and return (body, toc links)."""
    heads = []
    def rep(m):
        heads.append(strip(m.group(1)))
        return f'<h3 id="s{len(heads)}">{m.group(1)}</h3>'
    body = re.sub(r'<h3>(.*?)</h3>', rep, body)
    links = ''.join(f'<li><a href="#s{i}">{html.escape(h)}</a></li>' for i, h in enumerate(heads, 1))
    return body, heads, links

SITE = 'https://wiputpong-k.github.io/embedded-cpp-xiao/'
def url(lang, path): return SITE + ('' if lang == 'th' else 'en/') + path

def doc(title, depth, other_href, body, page_class, path, desc):
    """depth = folders below this language's home (0 for home, 2 for lesson/NN/).
    path = page path below the language root ('' or 'lesson/NN/'); desc = search-result snippet."""
    up = '../' * depth
    root = up + LROOT
    lang_label, lang_aria, lang_code = (('EN', 'Read in English', 'en') if LANG == 'th' else ('ไทย', 'อ่านภาษาไทย', 'th'))
    opts = ''.join(f'<option value="{up}lesson/{l["num"]}/">{l["num"]} · {html.escape(l["title"])}</option>' for l in LESSONS)
    return f'''<!doctype html>
<html lang="{LANG}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{url(LANG, path)}">
<link rel="alternate" hreflang="th" href="{url('th', path)}"><link rel="alternate" hreflang="en" href="{url('en', path)}"><link rel="alternate" hreflang="x-default" href="{url('th', path)}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Chakra+Petch:wght@500;600;700&family=IBM+Plex+Sans+Thai:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap">
<link rel="stylesheet" href="{root}assets/style.css?v={ASSET_V}">
</head>
<body class="{page_class}">
<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>
<marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" class="mk"/></marker>
<marker id="aha" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" class="mka"/></marker>
</defs></svg>
<div class="bar"><div class="barin">
<a href="{up or './'}" class="brand m">XIAO·C++</a>
<select id="jump" aria-label="{T('ไปที่บทเรียน', 'Go to lesson')}"><option value="{up or './'}">{T('สารบัญ', 'Contents')}</option>{opts}</select>
<div class="prog" aria-label="{T('ความคืบหน้า', 'Progress')}"><div class="pf" id="pf"></div></div><span class="pc m" id="pc" data-total="{N}">0/{N}</span>
<a href="{other_href}" class="lang" id="lang" hreflang="{lang_code}" aria-label="{lang_aria}">{lang_label}</a>
</div></div>
{body}
<script src="{root}assets/app.js?v={ASSET_V}"></script>
</body>
</html>
'''

def write(rel, text):
    path = os.path.join(OUT, '' if LANG == 'th' else 'en', rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, 'w', encoding='utf-8').write(text)

# ---- lesson pages ----
search = []
for i, l in enumerate(LESSONS):
    n = l['num']
    body, heads, toc = add_toc(l['body'].replace('@ROOT@', '../../' + LROOT))
    m = re.search(r'<p class="goal"><b>.*?</b> (.*?)</p>', body)
    goal_text = strip(m.group(1)) if m else ''
    search.append(dict(n=n, t=strip(l['title']), g=goal_text, h=heads, u=f'lesson/{n}/', m=MODS[l['mod']]))
    prev = LESSONS[i - 1] if i else None
    nxt = LESSONS[i + 1] if i + 1 < N else None
    def pager_link(x, cls, label):
        if not x:
            return f'<span class="{cls} none"></span>'
        return f'<a class="{cls}" href="../{x["num"]}/"><small>{label}</small><span>{x["num"]} · {html.escape(x["title"])}</span></a>'
    other = (f'../../en/lesson/{n}/' if LANG == 'th' else f'../../../lesson/{n}/')
    page_body = f'''<main class="wrap">
<nav class="crumb"><a href="../../">← {T('สารบัญ', 'Contents')}</a><span class="m">{n} / {N - 1:02d}</span></nav>
<article class="lesson" id="l{n}">
<header class="lh"><span class="big m">{n}</span><div class="lhm"><p class="mod">{MODS[l["mod"]]}</p><h1>{html.escape(l["title"])}</h1><p class="meta">{l["mins"]} {T("นาที · ฮาร์ดแวร์", "min · Hardware")}: {l["hw"]}</p></div></header>
<nav class="toc" aria-label="{T('ในบทนี้', 'In this lesson')}"><b>{T('ในบทนี้', 'In this lesson')}</b><ol>{toc}</ol></nav>
{body}
<label class="done"><input type="checkbox" id="done-l{n}" data-l="l{n}"> {T("เรียนบทนี้จบแล้ว", "I finished this lesson")}</label>
</article>
<nav class="pager">{pager_link(prev, 'prev', T('← บทก่อนหน้า', '← Previous'))}{pager_link(nxt, 'next', T('บทถัดไป →', 'Next →'))}</nav>
</main>'''
    write(f'lesson/{n}/index.html', doc(f'{n} · {strip(l["title"])} · {TITLE}', 2, other, page_body, 'lesson-page', f'lesson/{n}/',
                                            f'{T("บท", "Lesson")} {n}: {goal_text} · {TITLE}'))

# ---- home ----
total_h = sum(l['mins'] for l in LESSONS) / 60
mods = ''
for key, name in MODS.items():
    ls = [l for l in LESSONS if l['mod'] == key]
    rows = ''.join(f'<li><a href="lesson/{l["num"]}/"><span class="pn2 m">{l["num"]}</span><span class="pt">{html.escape(l["title"])}</span><span class="pm2">{l["mins"]}′</span></a><span class="dot" data-for="l{l["num"]}"></span></li>' for l in ls)
    mods += f'''<section class="modblock">
<div class="modhead"><h2>{name}</h2><span class="mc m">0/{len(ls)}</span></div>
<div class="mprog"><div class="mpf"></div></div>
<ol>{rows}</ol>
</section>'''
home_body = f'''<main class="wrap" id="top">
<header class="hero">
<p class="eyebrow m">nRF52840 · Cortex-M4F · {N} {T('บท · วันละ 20–30 นาที', 'lessons · 20–30 min a day')}</p>
<h1>{TITLE}</h1>
<p class="lede">{T('ปูพื้น C++ สำหรับคนที่เขียน C มาแล้ว ผ่านการลงมือบนบอร์ดจริง ต่อด้วย Git, GitHub และ CI/CD จนได้โปรเจกต์ firmware ที่สมบูรณ์ มีทั้ง test, CI และ release อัตโนมัติ',
 'C++ foundations for people who already write C, learned hands-on with a real board, followed by Git, GitHub and CI/CD, ending with a complete firmware project with tests, CI and automated releases.')}</p>
<div class="start">
<a class="cta" id="continue" href="lesson/00/" data-start="{T('เริ่มเรียนบท 00', 'Start with lesson 00')}" data-resume="{T('เรียนต่อ: บท', 'Continue: lesson')}" data-done="{T('ทบทวนบท', 'Review lesson')}">{T('เริ่มเรียนบท 00', 'Start with lesson 00')}</a>
<div class="search"><input type="search" id="q" placeholder="{T('ค้นหาบทเรียน เช่น volatile, Git, ปุ่ม', 'Search lessons, e.g. volatile, Git, button')}" aria-label="{T('ค้นหาบทเรียน', 'Search lessons')}" autocomplete="off">
<ol id="results" hidden></ol><p id="noresults" class="note" hidden>{T('ไม่พบบทที่ตรงกับคำค้น', 'No lessons match your search')}</p></div>
</div>
</header>
<section class="ov">
<div class="ovg">
<div><h2>{T('วิธีเรียน', 'How to study')}</h2><p>{T(f'เรียนวันละบทตามลำดับ รวม {N} บท ประมาณ {total_h:.0f} ชั่วโมง แต่ละบทมี เป้าหมาย → แนวคิด + diagram → hands-on → คำถามเช็ก ทุกบทต่อยอดจากบทก่อน โค้ดในบท 07, 10 และ 13–14 จะถูกนำไป test และ build ใน CI ช่วงท้าย',
 f'Take one lesson a day, in order: {N} lessons, about {total_h:.0f} hours in total. Each lesson goes goal → concept + diagram → hands-on → check questions, and builds on the one before. The code from lessons 07, 10 and 13–14 is tested and built in CI near the end.')}</p>
<p>{T('บท 00–14 ใช้ Arduino IDE 2 + core Seeed nRF52 (non-mbed) เพราะเร็วที่สุดในการเห็นผล หลักภาษาเหมือนกันทุก framework เมื่อจบแล้วย้ายไป nRF Connect SDK / Zephyr ได้ทันที',
 'Lessons 00–14 use Arduino IDE 2 with the Seeed nRF52 (non-mbed) core, the fastest way to see results. The language rules are the same in every framework, so you can move to nRF Connect SDK / Zephyr right after.')}</p>
<p>{T('ความคืบหน้าและบทล่าสุดที่เปิดจะถูกจำไว้ในเบราว์เซอร์นี้ ใช้ร่วมกันทั้งภาษาไทยและอังกฤษ', 'Your progress and last opened lesson are remembered in this browser, shared between Thai and English.')}</p></div>
<div><h2>{T('อุปกรณ์', 'Parts')}</h2><ul class="kit">
<li><b>1</b> Seeed XIAO nRF52840 (Sense) + {T('สาย USB-C แบบ data', 'USB-C data cable')}</li>
<li><b>1</b> breadboard + {T('สาย jumper', 'jumper wires')}</li>
<li><b>1</b> LED 5 mm + R 1 kΩ</li>
<li><b>1</b> {T('ปุ่มกด tactile', 'tactile push button')}</li>
<li><b>1</b> potentiometer 10 kΩ</li>
<li><b>—</b> Arduino IDE 2, Git, {T('บัญชี GitHub (ติดตั้งในบทที่ใช้)', 'GitHub account (set up in the lessons that use them)')}</li></ul></div>
</div>
</section>
<section class="mods">{mods}</section>
<section class="author" id="author">
<p class="mod">{T('ผู้จัดทำ', 'Author')}</p>
<p>{T('Hardware &amp; firmware engineer ประสบการณ์กว่า 13 ปีในงานออกแบบวงจร, PCB, firmware C/C++, การทดสอบ V&amp;V และ failure analysis ของอุปกรณ์ wearable และ IoT เขียนคอร์สนี้จากการเรียนจริงบนบอร์ด XIAO nRF52840 เพื่อแบ่งปันให้คนที่อยากเริ่มสาย embedded',
 'Hardware &amp; firmware engineer with over 13 years in circuit design, PCB, C/C++ firmware, V&amp;V testing and failure analysis for wearable and IoT devices. I wrote this course while learning on the XIAO nRF52840 myself, to share it with anyone starting out in embedded.')}</p>
<p class="links"><span>GitHub: <a href="https://github.com/wiputpong-k">github.com/wiputpong-k</a></span><span>{T('ข้อเสนอแนะ', 'Feedback')}: <a href="https://github.com/wiputpong-k/embedded-cpp-xiao/issues">{T('เปิด Issue ใน repo ของคอร์ส', 'open an issue in the course repo')}</a></span></p>
</section>
<footer class="ft"><p>{T('ตรวจแล้ว: Debouncer.h, RingBuffer.h และ test_main.cpp คอมไพล์ด้วย g++ (-Wall -Wextra -Werror) และ test ผ่านทั้งหมด ส่วนโค้ดบนบอร์ดและ workflow ให้ยืนยัน FQBN กับเวอร์ชัน core ในเครื่องของคุณ',
 'Verified: Debouncer.h, RingBuffer.h and test_main.cpp compile with g++ (-Wall -Wextra -Werror) and all tests pass. For the on-board code and workflows, confirm the FQBN and core version on your own machine.')}</p></footer>
</main>
<script type="application/json" id="lessons-index">{json.dumps(search, ensure_ascii=False).replace('</', '<\\/')}</script>'''
HOME_DESC = T(f'คอร์สฟรี {N} บท เรียน C++ สำหรับงาน embedded บนบอร์ด Seeed XIAO nRF52840 สำหรับคนที่เขียน C มาแล้ว ลงมือทีละขั้นบนบอร์ดจริง ต่อด้วย Git, GitHub และ CI/CD',
              f'A free {N}-lesson course on embedded C++ for C programmers, hands-on with the Seeed XIAO nRF52840 board, followed by Git, GitHub and CI/CD.')
write('index.html', doc(TITLE, 0, 'en/' if LANG == 'th' else '../', home_body, 'home-page', '', HOME_DESC))

if LANG == 'th':  # shared assets and sitemap, written once
    paths = [''] + [f'lesson/{l["num"]}/' for l in LESSONS]
    def entry(lang, p):
        alts = ''.join(f'<xhtml:link rel="alternate" hreflang="{a}" href="{url(a, p)}"/>' for a in LANGS)
        return f'<url><loc>{url(lang, p)}</loc>{alts}</url>'
    os.makedirs(OUT, exist_ok=True)
    open(os.path.join(OUT, 'sitemap.xml'), 'w', encoding='utf-8').write(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
        + '\n'.join(entry(lang, p) for p in paths for lang in LANGS) + '\n</urlset>\n')
    os.makedirs(os.path.join(OUT, 'assets'), exist_ok=True)
    for f in ('style.css', 'app.js'):
        shutil.copyfile(os.path.join(D, f), os.path.join(OUT, 'assets', f))
    if os.path.isdir(os.path.join(D, 'media')):
        shutil.copytree(os.path.join(D, 'media'), os.path.join(OUT, 'media'))
print(LANG, N, 'lessons')
