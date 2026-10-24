lesson('16', 'B', T('Branch, merge และแก้ conflict', 'Branch, merge and resolve conflicts'), 25, PC, goal(T('แยกงานเป็น branch และแก้ merge conflict ได้โดยไม่ตื่นตระหนก', 'Split work into branches, and resolve merge conflicts without panic'))
   + fig(SVG_BRANCH, T('feature branch แตกจาก main แล้ว merge กลับ', 'A feature branch splits off main, then merges back')) + T('''
<h3>Hands-on: สร้าง conflict เองแล้วแก้</h3>''', '''
<h3>Hands-on: create a conflict, then resolve it</h3>''') + code('''git switch -c feature/fast-blink
# ใน firmware.ino แก้ {500, 0, blinkTask} เป็น {250, 0, blinkTask}
git commit -am "feat: faster default blink"

git switch main
# แก้บรรทัดเดียวกันเป็น {1000, 0, blinkTask}
git commit -am "chore: slower default blink"

git merge feature/fast-blink      # → CONFLICT''', 'terminal', en={'# ใน firmware.ino แก้ {500, 0, blinkTask} เป็น {250, 0, blinkTask}': '# in firmware.ino change {500, 0, blinkTask} to {250, 0, blinkTask}',
                                                       '# แก้บรรทัดเดียวกันเป็น {1000, 0, blinkTask}': '# change the same line to {1000, 0, blinkTask}'}) + code('''<<<<<<< HEAD
  {1000, 0, blinkTask},
=======
  {250, 0, blinkTask},
>>>>>>> feature/fast-blink''', T('firmware.ino ตอน conflict', 'firmware.ino during the conflict')) + code('''# แก้ไฟล์ให้เหลือบรรทัดที่ต้องการ ลบเครื่องหมาย <<< === >>> ออก
git add firmware/firmware.ino
git commit                         # ปิด merge
git log --oneline --graph --all
git branch -d feature/fast-blink''', 'terminal', en={'# แก้ไฟล์ให้เหลือบรรทัดที่ต้องการ ลบเครื่องหมาย <<< === >>> ออก': '# keep the line you want and delete the <<< === >>> markers',
                                                     '# ปิด merge': '# completes the merge'}) + T('''
<p class="note">merge เก็บประวัติตามจริง (มี merge commit) ส่วน <code class="il">git rebase main</code> ย้าย commit ของ branch ไปต่อท้าย main ทำให้ประวัติเป็นเส้นตรง กฎ: ห้าม rebase branch ที่คนอื่นดึงไปแล้ว</p>
''', '''
<p class="note">merge keeps the real history (with a merge commit), while <code class="il">git rebase main</code> replays the branch's commits on top of main for a straight-line history. Rule: never rebase a branch someone else has already pulled.</p>
''') + qa([(T('ถ้าแก้ conflict ผิดแล้วอยากเริ่มใหม่ทำอย่างไร?', 'You resolved a conflict wrongly and want to start over. What do you do?'),
           T('git merge --abort ก่อน commit จะกลับไปสถานะก่อน merge', 'git merge --abort before you commit takes you back to the state before the merge.')),
          (T('ทำไมทีมไม่ commit ตรงเข้า main?', 'Why do teams not commit straight to main?'),
           T('main ควร build ได้และ test ผ่านเสมอ การผ่าน branch + PR ให้ CI และคนอื่นตรวจก่อน และย้อนกลับง่าย', 'main should always build and pass its tests. Going through a branch + PR lets CI and teammates check first, and makes changes easy to revert.'))]))
