lesson('18', 'B', 'Pull Request', 25, PC, goal(T('ทำงานผ่าน Pull Request แบบทีมจริง และตั้งกฎให้ main เปลี่ยนได้ผ่าน PR เท่านั้น', 'Work through Pull Requests like a real team, and set a rule so main only changes through PRs'))
   + T('''
<p>Pull Request (PR) คือคำขอให้รวม branch หนึ่งเข้า <code class="il">main</code> บน GitHub มีหน้าแสดง diff ให้คนอื่นอ่านและ comment ได้ และเป็นจุดที่ CI จะตรวจโค้ดให้อัตโนมัติก่อนรวม แม้ทำงานคนเดียว การผ่าน PR ก็ช่วยให้มีบันทึกว่าแต่ละการเปลี่ยนแปลงทำไปเพื่ออะไร</p>
''', '''
<p>A Pull Request (PR) is a request to merge one branch into <code class="il">main</code> on GitHub. It has a page that shows the diff for others to read and comment on, and it is where CI checks the code automatically before the merge. Even when you work alone, going through PRs leaves a record of why each change was made.</p>
''') + fig(SVG_PR, T('GitHub flow ที่บริษัทส่วนใหญ่ใช้', 'The GitHub flow most companies use')) + T('''
<h3>Hands-on: PR แรก</h3>
<p>บทนี้พิสูจน์ว่างานบน branch เข้า <code class="il">main</code> ได้ผ่าน PR และเมื่อ squash merge แล้ว main ได้ commit เดียวที่สรุปงานทั้ง PR</p>
<ol>
<li>สร้าง branch ใหม่ แล้วรัน <code class="il">notepad README.md</code> (หรือ <code class="il">code README.md</code>) ตอบ Yes เมื่อถามว่าจะสร้างไฟล์ใหม่ไหม วางตัวอย่าง README ข้างล่าง แก้ให้ตรงกับของคุณ บันทึก แล้วปิด</li>
<li>commit แล้ว push branch ขึ้น GitHub จากนั้นสร้าง PR ด้วย <code class="il">gh pr create --fill</code> (ใช้ข้อความ commit เป็นชื่อและคำอธิบาย PR)</li>
<li>รัน <code class="il">gh pr view --web</code> เพื่อเปิด PR บนเว็บ ดูแท็บ <b>Files changed</b> แล้วลอง comment บรรทัดใดบรรทัดหนึ่ง 1 จุด</li>
<li>รวม PR ด้วย squash merge แล้วกลับมาที่ <code class="il">main</code> ในเครื่องพร้อมดึงของใหม่ลงมา</li>
</ol>''', '''
<h3>Hands-on: your first PR</h3>
<p>This lesson proves that work on a branch reaches <code class="il">main</code> through a PR, and that a squash merge gives main a single commit that sums up the whole PR.</p>
<ol>
<li>Create a new branch, then run <code class="il">notepad README.md</code> (or <code class="il">code README.md</code>) and answer Yes when asked to create the file. Paste the README example below, adjust it to your project, save and close.</li>
<li>Commit, push the branch to GitHub, and open a PR with <code class="il">gh pr create --fill</code> (it uses your commit message as the PR title and description).</li>
<li>Run <code class="il">gh pr view --web</code> to open the PR in your browser. Look at the <b>Files changed</b> tab and leave one comment on a line.</li>
<li>Merge the PR with a squash merge, then switch back to <code class="il">main</code> locally and pull the result.</li>
</ol>''') + code('''git switch -c docs/readme
# เขียน README.md: รูป wiring, วิธี build, ขาที่ใช้
git add README.md
git commit -m "docs: add README with wiring and build steps"
git push -u origin docs/readme
gh pr create --fill
gh pr view --web
# ลอง comment โค้ดตัวเอง 1 จุดบนเว็บ แล้วกลับมารันต่อ
gh pr merge --squash --delete-branch
git switch main
git pull''', 'terminal', en={'# เขียน README.md: รูป wiring, วิธี build, ขาที่ใช้': '# write README.md: wiring photo, build steps, pins used',
                             '# ลอง comment โค้ดตัวเอง 1 จุดบนเว็บ แล้วกลับมารันต่อ': '# leave one review comment on the web, then continue'}) + T('''
<p><b>README.md</b> คือไฟล์แรกที่ GitHub แสดงบนหน้า repo เขียนด้วย <b>Markdown</b> ซึ่งเป็นข้อความธรรมดาที่มีเครื่องหมายบอกรูปแบบ: <code class="il">#</code> = หัวข้อ, <code class="il">|</code> = ช่องตาราง, <code class="il">1.</code> = รายการลำดับ และข้อความใน <code class="il">`…`</code> = โค้ด ตัวอย่าง:</p>
''', '''
<p><b>README.md</b> is the first file GitHub shows on the repo page. It is written in <b>Markdown</b>, plain text with marks for formatting: <code class="il">#</code> = heading, <code class="il">|</code> = table cell, <code class="il">1.</code> = numbered list, and text in <code class="il">`…`</code> = code. An example:</p>
''') + code(T('''# xiao-embedded-cpp

Firmware ตัวอย่างสำหรับ Seeed XIAO nRF52840 Sense: cooperative scheduler, debounce และ moving average

## การต่อขา

| ขา | ต่อกับ |
|----|--------|
| D0 / A0 | ขากลางของ pot 10 kΩ (ขาข้างต่อ 3V3 และ GND) |
| D1 | ปุ่มกด ลง GND |
| D2 | LED ผ่าน R 1 kΩ ลง GND |

## วิธี build

1. เปิด `firmware/firmware.ino` ใน Arduino IDE 2
2. เลือกบอร์ด Seeed XIAO nRF52840 Sense แล้วกด Upload
3. Serial Monitor ที่ 115200 baud: พิมพ์ตัวเลข 50–5000 เพื่อเปลี่ยนรอบกระพริบ''', '''# xiao-embedded-cpp

Example firmware for the Seeed XIAO nRF52840 Sense: cooperative scheduler, debounce and moving average.

## Wiring

| Pin | Connected to |
|-----|--------------|
| D0 / A0 | Middle leg of a 10 kΩ pot (outer legs to 3V3 and GND) |
| D1 | Push button to GND |
| D2 | LED through 1 kΩ to GND |

## Build

1. Open `firmware/firmware.ino` in Arduino IDE 2
2. Select the Seeed XIAO nRF52840 Sense board and press Upload
3. Serial Monitor at 115200 baud: type a number from 50 to 5000 to change the blink period'''), 'README.md') + T('''
<p class="note">ถ้ามีรูปการต่อวงจร ใส่ไฟล์รูปไว้ใน repo แล้วเพิ่มบรรทัด <code class="il">![wiring](wiring.jpg)</code> ใน README รูปจะแสดงบนหน้า GitHub</p>
<p>ผลนี้บอกอะไร: หลังขั้นที่ 4 หน้า repo บน GitHub แสดง README ทันที และ <code class="il">git log --oneline -3</code> ในเครื่องจะเห็น commit ใหม่ของ PR นี้เป็น commit เดียวบน main ส่วนหน้า PR (พร้อม comment ของคุณ) ยังเปิดดูย้อนหลังได้ในแท็บ <b>Pull requests → Closed</b></p>
<h3>ตั้งกฎให้ main</h3>
<ol>
<li>เปิดหน้า repo บน GitHub ไปที่ <b>Settings → Branches</b></li>
<li>เพิ่มกฎสำหรับ branch <code class="il">main</code> (ปุ่ม <i>Add branch ruleset</i> หรือ <i>Add classic branch protection rule</i> ชื่อปุ่มอาจต่างกันเล็กน้อยตามช่วงเวลาที่ GitHub ปรับหน้าเว็บ)</li>
<li>เปิดตัวเลือก <b>Require a pull request before merging</b> แล้วบันทึก</li>
</ol>
<p class="note">ตอนนี้ยังไม่ต้องเปิด required status checks เพราะยังไม่มี CI จะกลับมาเปิดในบท 22 กฎนี้ใช้ได้ฟรีกับ repo แบบ public</p>
''', '''
<p class="note">If you have a wiring photo, add the image file to the repo and put the line <code class="il">![wiring](wiring.jpg)</code> in the README; the photo shows on the GitHub page.</p>
<p>What this tells you: after step 4, the repo page on GitHub shows the README right away, and <code class="il">git log --oneline -3</code> on your PC shows this PR as a single new commit on main. The PR page (with your comment) stays available under <b>Pull requests → Closed</b>.</p>
<h3>Protect main</h3>
<ol>
<li>On the repo page on GitHub, go to <b>Settings → Branches</b>.</li>
<li>Add a rule for the <code class="il">main</code> branch (the button is <i>Add branch ruleset</i> or <i>Add classic branch protection rule</i>; the exact label changes from time to time as GitHub updates the page).</li>
<li>Turn on <b>Require a pull request before merging</b> and save.</li>
</ol>
<p class="note">Do not turn on required status checks yet, because there is no CI. You come back to it in lesson 22. This rule is free for public repos.</p>
''') + qa([(T('squash merge ดีอย่างไร?', 'What is good about a squash merge?'),
           T('รวม commit ย่อยใน PR เป็น commit เดียวบน main ประวัติอ่านง่าย 1 commit = 1 ฟีเจอร์ ย้อน (revert) ง่าย', 'It combines the PR\'s small commits into one commit on main: readable history, 1 commit = 1 feature, easy to revert.')),
          (T('ทำงานคนเดียว ทำไมยังต้องใช้ PR?', 'Why use PRs when you work alone?'),
           T('PR เป็นจุดที่ CI ตรวจโค้ดก่อนเข้า main และเก็บคำอธิบายว่าเปลี่ยนอะไรเพราะอะไรไว้ในที่เดียว ย้อนกลับไปดูหรือ revert ได้ง่าย', 'A PR is where CI checks the code before it reaches main, and it keeps the what-and-why of each change in one place, easy to look up or revert later.'))])
   + iv(T('ในทีม README ที่มีรูป wiring, badge CI สีเขียว และประวัติ commit ที่สะอาด ช่วยให้เพื่อนร่วมทีมหรือคนที่มารับงานต่อ setup และเข้าใจโปรเจกต์ได้ในไม่กี่นาที ไม่ต้องมาถามทีละเรื่อง',
          'On a team, a README with a wiring photo, a green CI badge and a clean commit history lets teammates, or whoever takes over the project, set up and understand it in minutes instead of asking one question at a time.')))
