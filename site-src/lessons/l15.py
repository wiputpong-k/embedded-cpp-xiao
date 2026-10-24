lesson('15', 'B', T('ติดตั้ง Git และ commit แรก', 'Install Git and make your first commit'), 30, PC, goal(T('ติดตั้ง Git แล้วเก็บงานทั้งหมดที่ทำมาลง repo พร้อม commit message ที่อ่านแล้วรู้เรื่อง', 'Install Git, then put all your work so far into a repo, with commit messages that make sense')) + T('''
<p>Git คือโปรแกรมเก็บประวัติการแก้โค้ด ทุกครั้งที่ commit คือการถ่ายภาพไฟล์ทั้งหมด ณ เวลานั้นไว้ ย้อนกลับไปดูหรือกู้คืนได้เสมอ ใช้ตั้งแต่บทนี้ไปจนจบคอร์ส</p>
<h3>ขั้นที่ 1: ติดตั้ง Git</h3>
<ol>
<li>(ไม่บังคับ) ถ้าอยากใช้ VS Code เป็นโปรแกรมแก้ข้อความ ให้ติดตั้งจาก <a href="https://code.visualstudio.com/">code.visualstudio.com</a> ก่อน เพราะตัวติดตั้ง Git จะถามหาโปรแกรมนี้</li>
<li>เปิดหน้า <a href="https://git-scm.com/downloads/win">git-scm.com/downloads/win</a> แล้วดาวน์โหลดตัวติดตั้ง Git for Windows แบบ 64-bit</li>
<li>เปิดตัวติดตั้ง แล้วกด Next ตามค่าเริ่มต้น ยกเว้น 2 หน้านี้
<ul>
<li><b>Choosing the default editor used by Git:</b> เลือก <i>Use Visual Studio Code as Git's default editor</i> ถ้าติดตั้ง VS Code แล้ว หรือเลือก <i>Use Notepad as Git's default editor</i> ถ้าไม่ได้ติดตั้ง</li>
<li><b>Adjusting the name of the initial branch:</b> เลือก <i>Override the default branch name</i> แล้วพิมพ์ <code class="il">main</code></li>
</ul></li>
<li>กด Install แล้วรอจนเสร็จ</li>
</ol>
<p class="note">ทำไมต้องเลือก editor: บางคำสั่งของ Git จะเปิดโปรแกรมแก้ข้อความให้คุณพิมพ์ เช่น <code class="il">git commit</code> ที่ไม่ใส่ <code class="il">-m</code> หรือตอน merge ในบท 16 ค่าเริ่มต้นของ Git คือ Vim ซึ่งคนที่ไม่เคยใช้มักออกจากโปรแกรมไม่เป็น VS Code หรือ Notepad ใช้ง่ายกว่า เลือกตัวไหนก็ได้ ไม่มีผลกับเนื้อหาในคอร์ส</p>
<h3>ขั้นที่ 2: เปิด Git Bash และบอก Git ว่าคุณเป็นใคร</h3>
<p>ตัวติดตั้ง Git มีโปรแกรม <b>Git Bash</b> มาด้วย เป็น terminal ที่ใช้คำสั่งแบบเดียวกับ Linux และ macOS คำสั่งทั้งหมดตั้งแต่บทนี้ไปให้พิมพ์ใน Git Bash (กดปุ่ม Windows พิมพ์ <i>Git Bash</i> แล้วกด Enter) macOS และ Linux ใช้ Terminal ปกติได้เลย</p>
<p>รัน 3 บรรทัดแรกของคำสั่งข้างล่าง โดยเปลี่ยนชื่อและอีเมลเป็นของคุณ ข้อมูลนี้จะติดไปกับทุก commit และจะเห็นได้สาธารณะเมื่อ push ขึ้น GitHub ถ้าไม่อยากเปิดเผยอีเมลจริง ใช้อีเมลแบบ noreply ที่ GitHub ให้ได้ (ดูที่ GitHub → Settings → Emails)</p>
<p class="note">เช็ก: รัน <code class="il">git --version</code> ต้องเห็นข้อความแบบ <code class="il">git version 2.xx.x.windows.1</code></p>
''', '''
<p>Git keeps the history of your code. Every commit is a snapshot of all your files at that moment, which you can always look back at or restore. You use it from this lesson to the end of the course.</p>
<h3>Step 1: Install Git</h3>
<ol>
<li>(Optional) If you want VS Code as your text editor, install it first from <a href="https://code.visualstudio.com/">code.visualstudio.com</a>, because the Git installer looks for it.</li>
<li>Open <a href="https://git-scm.com/downloads/win">git-scm.com/downloads/win</a> and download the 64-bit Git for Windows installer.</li>
<li>Run the installer and click Next through the defaults, except on these two pages:
<ul>
<li><b>Choosing the default editor used by Git:</b> pick <i>Use Visual Studio Code as Git's default editor</i> if you installed VS Code, or <i>Use Notepad as Git's default editor</i> if you did not.</li>
<li><b>Adjusting the name of the initial branch:</b> pick <i>Override the default branch name</i> and type <code class="il">main</code>.</li>
</ul></li>
<li>Click Install and wait until it finishes.</li>
</ol>
<p class="note">Why choose an editor? Some Git commands open a text editor for you to type in, such as <code class="il">git commit</code> without <code class="il">-m</code>, or a merge in lesson 16. Git's default is Vim, which newcomers often cannot figure out how to exit. VS Code or Notepad is easier. Either one works for this course.</p>
<h3>Step 2: Open Git Bash and tell Git who you are</h3>
<p>The Git installer includes <b>Git Bash</b>, a terminal that uses the same commands as Linux and macOS. Type every command from this lesson on in Git Bash (press the Windows key, type <i>Git Bash</i>, press Enter). On macOS and Linux, use the normal Terminal.</p>
<p>Run the first 3 lines of the commands below with your own name and email. They are attached to every commit and become public when you push to GitHub. If you do not want to expose your real email, use the noreply address GitHub gives you (GitHub → Settings → Emails).</p>
<p class="note">Check: <code class="il">git --version</code> prints something like <code class="il">git version 2.xx.x.windows.1</code>.</p>
''') + code('''git config --global user.name "Your Name"
git config --global user.email "you@example.com"
git config --global init.defaultBranch main
git --version''', 'Git Bash') + T('''
<h3>ขั้นที่ 3: สร้าง repo และนำงานจากบท 13–14 เข้ามา</h3>
<ol>
<li>รันคำสั่งชุดข้างล่างทีละบรรทัด จะได้โฟลเดอร์ <code class="il">xiao-embedded-cpp</code> ในโฟลเดอร์ผู้ใช้ของคุณ (<code class="il">~</code>) พร้อม repo Git เปล่า</li>
<li>บรรทัด <code class="il">cp -r</code> คัดลอก sketch <code class="il">firmware</code> จากบท 13–14 เข้ามา ถ้า sketch ไม่ได้อยู่ที่ <code class="il">Documents/Arduino</code> ให้ดูตำแหน่งจริงใน Arduino IDE ที่ <b>File → Preferences → Sketchbook location</b> (ถ้าใช้ OneDrive มักเป็น <code class="il">~/OneDrive/Documents/Arduino</code>)</li>
</ol>''', '''
<h3>Step 3: Create the repo and bring in your work from lessons 13–14</h3>
<ol>
<li>Run the commands below one line at a time. You get a <code class="il">xiao-embedded-cpp</code> folder in your home folder (<code class="il">~</code>) with an empty Git repo.</li>
<li>The <code class="il">cp -r</code> line copies the <code class="il">firmware</code> sketch from lessons 13–14 in. If your sketches are not in <code class="il">Documents/Arduino</code>, check the real location in Arduino IDE under <b>File → Preferences → Sketchbook location</b> (with OneDrive it is often <code class="il">~/OneDrive/Documents/Arduino</code>).</li>
</ol>''') + code('''cd ~
mkdir xiao-embedded-cpp
cd xiao-embedded-cpp
git init
cp -r ~/Documents/Arduino/firmware .
ls firmware firmware/src''', 'Git Bash') + T('''
<h3>ขั้นที่ 4: บอก Git ว่าไฟล์ไหนไม่ต้องเก็บ</h3>
<p>ไฟล์ที่ build สร้างขึ้นใหม่ได้ เช่น .hex หรือโปรแกรม test ไม่ควรเข้า repo รัน <code class="il">notepad .gitignore</code> (หรือ <code class="il">code .gitignore</code> ถ้าใช้ VS Code) ถ้าถามว่าจะสร้างไฟล์ใหม่ไหม ให้ตอบ Yes แล้ววางเนื้อหาข้างล่าง บันทึก แล้วปิด</p>''', '''
<h3>Step 4: Tell Git which files to ignore</h3>
<p>Files that a build can regenerate, such as .hex files or the test program, do not belong in the repo. Run <code class="il">notepad .gitignore</code> (or <code class="il">code .gitignore</code> if you use VS Code). If it asks whether to create a new file, answer Yes, paste the content below, save and close.</p>''') + code('''build/
*.hex
*.zip
*.uf2
firmware/src/version.h
test_runner
test_runner.exe
.vscode/''', '.gitignore') + T('''
<h3>ขั้นที่ 5: commit แรก</h3>
<p><code class="il">git status</code> แสดงว่าไฟล์ไหนเปลี่ยนไปบ้าง <code class="il">git add</code> เลือกไฟล์เข้า staging area แล้ว <code class="il">git commit</code> เก็บเป็นภาพถ่ายถาวร</p>''', '''
<h3>Step 5: Your first commit</h3>
<p><code class="il">git status</code> shows what changed, <code class="il">git add</code> puts files into the staging area, and <code class="il">git commit</code> stores them as a permanent snapshot.</p>''') + fig(SVG_GITAREA, T('ไฟล์เดินทางผ่าน 3 พื้นที่ในเครื่องก่อนขึ้น GitHub', 'Files pass through three local areas before reaching GitHub')) + code('''git status
git add .gitignore firmware/
git commit -m "feat: led, debouncer, ring buffer and task scheduler"
git log --oneline

# แก้ไฟล์แล้วลอง:
git diff              # สิ่งที่แก้ แต่ยังไม่ add
git add -p            # เลือก add ทีละก้อน
git restore <file>    # ทิ้งการแก้ไขที่ยังไม่ add''', 'Git Bash', en={'# แก้ไฟล์แล้วลอง:': '# edit a file, then try:', '# สิ่งที่แก้ แต่ยังไม่ add': '# changes not yet added',
                                                    '# เลือก add ทีละก้อน': '# add chunk by chunk', '# ทิ้งการแก้ไขที่ยังไม่ add': '# discard changes not yet added'}) + T('''
<p>ลองแก้ตัวเลขใน <code class="il">tasks[]</code> ของ <code class="il">firmware/firmware.ino</code> แล้วรัน <code class="il">git diff</code> ดูสิ่งที่เปลี่ยน จากนั้นรัน <code class="il">git restore firmware/firmware.ino</code> เพื่อทิ้งการแก้ไขนั้น</p>
<p>รูปแบบ commit message ที่ทีมนิยม (Conventional Commits): <code class="il">feat:</code> ฟีเจอร์ใหม่, <code class="il">fix:</code> แก้บั๊ก, <code class="il">docs:</code>, <code class="il">test:</code>, <code class="il">ci:</code>, <code class="il">refactor:</code> หนึ่ง commit = หนึ่งเรื่อง</p>
''', '''
<p>Try changing a number in <code class="il">tasks[]</code> in <code class="il">firmware/firmware.ino</code>, run <code class="il">git diff</code> to see the change, then run <code class="il">git restore firmware/firmware.ino</code> to throw it away.</p>
<p>The commit message style most teams use (Conventional Commits): <code class="il">feat:</code> new feature, <code class="il">fix:</code> bug fix, <code class="il">docs:</code>, <code class="il">test:</code>, <code class="il">ci:</code>, <code class="il">refactor:</code>. One commit = one topic.</p>
''') + qa([(T('ทำไมไม่ควร commit ไฟล์ .hex?', 'Why should you not commit .hex files?'),
           T('เป็นผลลัพธ์ที่สร้างซ้ำได้จาก source เปลี่ยนทุก build ทำให้ repo บวมและ diff อ่านไม่ได้ ไฟล์ binary ควรอยู่ใน GitHub Release (บท 23)', 'They are build output you can regenerate from source. They change on every build, bloat the repo and make diffs unreadable. Binaries belong in a GitHub Release (lesson 23).')),
          (T('git add . กับ git add -p ต่างกันอย่างไร?', 'How do git add . and git add -p differ?'),
           T('add . เอาทุกการเปลี่ยนแปลง -p ให้เลือกทีละ hunk ช่วยแยก commit ตามเรื่องได้ แม้แก้หลายเรื่องในไฟล์เดียว', 'add . takes every change; -p lets you pick hunk by hunk, so you can split commits by topic even when one file has several changes.'))]))
