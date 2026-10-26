lesson('16', 'B', T('Branch, merge และแก้ conflict', 'Branch, merge and resolve conflicts'), 25, PC, goal(T('แยกงานเป็น branch และแก้ merge conflict ได้โดยไม่ตื่นตระหนก', 'Split work into branches, and resolve merge conflicts without panic')) + T('''
<ul>
<li><b>branch</b> เส้นทางงานแยกออกมาจาก <code class="il">main</code> commit บน branch ไม่กระทบ main จนกว่าจะรวมกลับ</li>
<li><b>merge</b> การรวมงานจาก branch หนึ่งเข้าอีก branch ถ้าแก้คนละบรรทัด Git รวมให้เองอัตโนมัติ</li>
<li><b>conflict</b> เมื่อทั้งสอง branch แก้บรรทัดเดียวกัน Git ไม่รู้ว่าจะเอาแบบไหน จึงหยุดให้คุณเลือก</li>
<li><b>HEAD</b> ตำแหน่งที่คุณอยู่ตอนนี้ คือ branch ที่ <code class="il">git switch</code> มาล่าสุด</li>
</ul>
''', '''
<ul>
<li><b>branch</b>: a separate line of work split off <code class="il">main</code>. Commits on a branch do not touch main until you merge them back.</li>
<li><b>merge</b>: combining the work of one branch into another. If the two changed different lines, Git combines them automatically.</li>
<li><b>conflict</b>: both branches changed the same line, so Git cannot know which to keep and stops for you to choose.</li>
<li><b>HEAD</b>: where you are right now, i.e. the branch you last <code class="il">git switch</code>ed to.</li>
</ul>
''')
   + fig(SVG_BRANCH, T('feature branch แตกจาก main แล้ว merge กลับ', 'A feature branch splits off main, then merges back')) + T('''
<h3>Hands-on: สร้าง conflict เองแล้วแก้</h3>
<p>บทนี้พิสูจน์ว่าแต่ละ branch เก็บไฟล์คนละฉบับ และเมื่อสอง branch แก้บรรทัดเดียวกัน Git จะไม่เดาให้ แต่หยุดให้คุณตัดสินใจ ทำใน Git Bash ที่โฟลเดอร์ <code class="il">~/xiao-embedded-cpp</code></p>
<ol>
<li>สร้าง branch ใหม่แล้วสลับไปอยู่ (<code class="il">switch -c</code>) เปิด <code class="il">firmware/firmware.ino</code> ด้วย <code class="il">notepad</code> แก้ <code class="il">{500, 0, blinkTask}</code> เป็น <code class="il">{250, 0, blinkTask}</code> บันทึก ปิด แล้ว commit (<code class="il">-a</code> = add ทุกไฟล์ที่แก้, <code class="il">-m</code> = ข้อความ)</li>
<li>กลับไปที่ <code class="il">main</code> แล้วเปิดไฟล์อีกครั้ง จะเห็นว่ายังเป็น <code class="il">500</code> เพราะการแก้อยู่บน branch อื่น แก้บรรทัดเดียวกันเป็น <code class="il">{1000, 0, blinkTask}</code> แล้ว commit</li>
<li>รัน <code class="il">git merge</code> จะได้ข้อความ <code class="il">CONFLICT (content): Merge conflict in firmware/firmware.ino</code></li>
</ol>
''', '''
<h3>Hands-on: create a conflict, then resolve it</h3>
<p>This lesson proves that each branch keeps its own version of a file, and that when two branches change the same line Git does not guess but stops for you to decide. Work in Git Bash in the <code class="il">~/xiao-embedded-cpp</code> folder.</p>
<ol>
<li>Create a new branch and switch to it (<code class="il">switch -c</code>). Open <code class="il">firmware/firmware.ino</code> with <code class="il">notepad</code>, change <code class="il">{500, 0, blinkTask}</code> to <code class="il">{250, 0, blinkTask}</code>, save, close, and commit (<code class="il">-a</code> = add every changed file, <code class="il">-m</code> = message).</li>
<li>Switch back to <code class="il">main</code> and open the file again: it still says <code class="il">500</code>, because the change lives on the other branch. Change the same line to <code class="il">{1000, 0, blinkTask}</code> and commit.</li>
<li>Run <code class="il">git merge</code>. You get <code class="il">CONFLICT (content): Merge conflict in firmware/firmware.ino</code>.</li>
</ol>
''') + code('''cd ~/xiao-embedded-cpp
git switch -c feature/fast-blink
notepad firmware/firmware.ino      # แก้ 500 เป็น 250 บันทึก ปิด
git commit -am "feat: faster default blink"

git switch main
notepad firmware/firmware.ino      # ยังเป็น 500: แก้เป็น 1000 บันทึก ปิด
git commit -am "chore: slower default blink"

git merge feature/fast-blink       # → CONFLICT''', 'Git Bash', en={'# แก้ 500 เป็น 250 บันทึก ปิด': '# change 500 to 250, save, close',
                                                       '# ยังเป็น 500: แก้เป็น 1000 บันทึก ปิด': '# still 500: change to 1000, save, close'}) + T('''
<ol start="4">
<li>เปิด <code class="il">firmware/firmware.ino</code> อีกครั้ง Git ใส่เครื่องหมายไว้ตรงบรรทัดที่ชนกัน ส่วนระหว่าง <code class="il">&lt;&lt;&lt;&lt;&lt;&lt;&lt; HEAD</code> กับ <code class="il">=======</code> คือของ branch ที่คุณอยู่ (main) ส่วนระหว่าง <code class="il">=======</code> กับ <code class="il">&gt;&gt;&gt;&gt;&gt;&gt;&gt;</code> คือของ branch ที่กำลัง merge เข้ามา</li>
<li>เลือกเก็บบรรทัดเดียวที่ต้องการ เช่น <code class="il">{250, 0, blinkTask},</code> ลบอีกบรรทัดและเครื่องหมาย 3 บรรทัดออกให้หมด แล้วบันทึก</li>
</ol>
''', '''
<ol start="4">
<li>Open <code class="il">firmware/firmware.ino</code> again. Git has marked the clashing lines: between <code class="il">&lt;&lt;&lt;&lt;&lt;&lt;&lt; HEAD</code> and <code class="il">=======</code> is your current branch's version (main); between <code class="il">=======</code> and <code class="il">&gt;&gt;&gt;&gt;&gt;&gt;&gt;</code> is the version from the branch being merged.</li>
<li>Keep the one line you want, e.g. <code class="il">{250, 0, blinkTask},</code>, delete the other line and all three marker lines, and save.</li>
</ol>
''') + code('''<<<<<<< HEAD
  {1000, 0, blinkTask},
=======
  {250, 0, blinkTask},
>>>>>>> feature/fast-blink''', T('firmware.ino ตอน conflict', 'firmware.ino during the conflict')) + T('''
<ol start="6">
<li>รัน <code class="il">git add</code> และ <code class="il">git commit</code> โดยไม่ใส่ <code class="il">-m</code> Git จะเปิด editor ที่เลือกไว้ในบท 15 พร้อมข้อความ <code class="il">Merge branch 'feature/fast-blink'</code> ให้แล้ว แค่บันทึกแล้วปิดหน้าต่าง editor commit จะเสร็จเมื่อปิด editor</li>
<li>รัน <code class="il">git log --oneline --graph --all</code> จะเห็นเส้นของสอง branch มาบรรจบกันเหมือนในรูป แล้วลบ branch ที่ใช้เสร็จแล้ว</li>
</ol>
''', '''
<ol start="6">
<li>Run <code class="il">git add</code> and <code class="il">git commit</code> without <code class="il">-m</code>. Git opens the editor you chose in lesson 15 with the message <code class="il">Merge branch 'feature/fast-blink'</code> already filled in. Just save and close the editor window; the commit finishes when the editor closes.</li>
<li>Run <code class="il">git log --oneline --graph --all</code>: the lines of the two branches join, as in the figure. Then delete the finished branch.</li>
</ol>
''') + code('''git add firmware/firmware.ino
git commit                         # ปิด merge: บันทึกแล้วปิด editor
git log --oneline --graph --all
git branch -d feature/fast-blink''', 'Git Bash', en={'# ปิด merge: บันทึกแล้วปิด editor': '# completes the merge: save and close the editor'}) + T('''
<p>ผลนี้บอกอะไร: ขั้นที่ 2 เห็นว่า main ยังเป็น 500 คือแต่ละ branch แยกกันจริง ส่วนขั้นที่ 3 Git ไม่เลือกค่าให้เอง เพราะการตัดสินว่าค่าไหนถูกเป็นหน้าที่ของคน conflict จึงไม่ใช่ error แต่เป็นคำถามจาก Git ตอบด้วยการแก้ไฟล์แล้ว commit</p>
<p class="note">merge เก็บประวัติตามจริง (มี merge commit) ส่วน <code class="il">git rebase main</code> ย้าย commit ของ branch ไปต่อท้าย main ทำให้ประวัติเป็นเส้นตรง กฎ: ห้าม rebase branch ที่คนอื่นดึงไปแล้ว</p>
''', '''
<p>What this tells you: in step 2 main still said 500, so the branches really are separate. In step 3 Git did not pick a value, because deciding which is right is a person's job. A conflict is not an error but a question from Git, answered by editing the file and committing.</p>
<p class="note">merge keeps the real history (with a merge commit), while <code class="il">git rebase main</code> replays the branch's commits on top of main for a straight-line history. Rule: never rebase a branch someone else has already pulled.</p>
''') + qa([(T('ถ้าแก้ conflict ผิดแล้วอยากเริ่มใหม่ทำอย่างไร?', 'You resolved a conflict wrongly and want to start over. What do you do?'),
           T('git merge --abort ก่อน commit จะกลับไปสถานะก่อน merge', 'git merge --abort before you commit takes you back to the state before the merge.')),
          (T('ทำไมทีมไม่ commit ตรงเข้า main?', 'Why do teams not commit straight to main?'),
           T('main ควร build ได้และ test ผ่านเสมอ การผ่าน branch + PR ให้ CI และคนอื่นตรวจก่อน และย้อนกลับง่าย', 'main should always build and pass its tests. Going through a branch + PR lets CI and teammates check first, and makes changes easy to revert.'))]))
