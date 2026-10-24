lesson('18', 'B', 'Pull Request', 25, PC, goal(T('ทำงานผ่าน Pull Request แบบทีมจริง และตั้งกฎให้ main เปลี่ยนได้ผ่าน PR เท่านั้น', 'Work through Pull Requests like a real team, and set a rule so main only changes through PRs'))
   + T('''
<p>Pull Request (PR) คือคำขอให้รวม branch หนึ่งเข้า <code class="il">main</code> บน GitHub มีหน้าแสดง diff ให้คนอื่นอ่านและ comment ได้ และเป็นจุดที่ CI จะตรวจโค้ดให้อัตโนมัติก่อนรวม แม้ทำงานคนเดียว การผ่าน PR ก็ช่วยให้มีบันทึกว่าแต่ละการเปลี่ยนแปลงทำไปเพื่ออะไร</p>
''', '''
<p>A Pull Request (PR) is a request to merge one branch into <code class="il">main</code> on GitHub. It has a page that shows the diff for others to read and comment on, and it is where CI checks the code automatically before the merge. Even when you work alone, going through PRs leaves a record of why each change was made.</p>
''') + fig(SVG_PR, T('GitHub flow ที่บริษัทส่วนใหญ่ใช้', 'The GitHub flow most companies use')) + T('''
<h3>Hands-on: PR แรก</h3>
<ol>
<li>สร้าง branch ใหม่ แล้วสร้างไฟล์ <code class="il">README.md</code> ในโฟลเดอร์ repo (เปิดด้วย VS Code หรือ Notepad) เขียนสั้น ๆ ว่าโปรเจกต์นี้คืออะไร ต่อขาไหนบ้าง และ build อย่างไร</li>
<li>commit แล้ว push branch ขึ้น GitHub จากนั้นสร้าง PR ด้วย <code class="il">gh pr create --fill</code> (ใช้ข้อความ commit เป็นชื่อและคำอธิบาย PR)</li>
<li>รัน <code class="il">gh pr view --web</code> เพื่อเปิด PR บนเว็บ ดูแท็บ <b>Files changed</b> แล้วลอง comment บรรทัดใดบรรทัดหนึ่ง 1 จุด</li>
<li>รวม PR ด้วย squash merge แล้วกลับมาที่ <code class="il">main</code> ในเครื่องพร้อมดึงของใหม่ลงมา</li>
</ol>''', '''
<h3>Hands-on: your first PR</h3>
<ol>
<li>Create a new branch, then create <code class="il">README.md</code> in the repo folder (open it with VS Code or Notepad). Write briefly what the project is, which pins it uses and how to build it.</li>
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
<h3>ตั้งกฎให้ main</h3>
<ol>
<li>เปิดหน้า repo บน GitHub ไปที่ <b>Settings → Branches</b></li>
<li>เพิ่มกฎสำหรับ branch <code class="il">main</code> (ปุ่ม <i>Add branch ruleset</i> หรือ <i>Add classic branch protection rule</i> ชื่อปุ่มอาจต่างกันเล็กน้อยตามช่วงเวลาที่ GitHub ปรับหน้าเว็บ)</li>
<li>เปิดตัวเลือก <b>Require a pull request before merging</b> แล้วบันทึก</li>
</ol>
<p class="note">ตอนนี้ยังไม่ต้องเปิด required status checks เพราะยังไม่มี CI จะกลับมาเปิดในบท 22 กฎนี้ใช้ได้ฟรีกับ repo แบบ public</p>
''', '''
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
