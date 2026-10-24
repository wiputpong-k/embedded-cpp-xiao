lesson('17', 'B', T('GitHub: สร้าง repo และ push', 'GitHub: create a repo and push'), 30, PC, goal(T('ตั้งค่า GitHub CLI แล้วส่ง repo ในเครื่องขึ้น GitHub เป็นครั้งแรก', 'Set up the GitHub CLI and push your local repo to GitHub for the first time'))
   + T('''
<p>GitHub คือเว็บที่เก็บ repo Git ไว้บนเซิร์ฟเวอร์ ใช้แชร์โค้ดกับทีม และเป็นที่ที่ CI (บท 21) จะรัน ส่วน GitHub CLI (<code class="il">gh</code>) คือโปรแกรมที่ให้สั่งงาน GitHub จาก terminal ได้ เช่น สร้าง repo หรือเปิด Pull Request โดยไม่ต้องคลิกบนเว็บ</p>
<h3>ขั้นที่ 1: สมัครบัญชี GitHub</h3>
<p>ถ้ายังไม่มีบัญชี ให้สมัครที่ <a href="https://github.com/signup">github.com/signup</a> แล้วยืนยันอีเมลให้เรียบร้อย ถ้ามีแล้วข้ามขั้นนี้ได้</p>
<h3>ขั้นที่ 2: ติดตั้ง GitHub CLI</h3>
<ol>
<li>เปิด PowerShell แล้วรันคำสั่งแรกข้างล่าง (ใช้ winget ที่มากับ Windows 10/11) หรือดาวน์โหลดตัวติดตั้งจาก <a href="https://cli.github.com/">cli.github.com</a></li>
<li>ปิด PowerShell แล้วเปิดใหม่ จากนั้นรัน <code class="il">gh --version</code> ต้องเห็นเลขเวอร์ชัน</li>
</ol>''', '''
<p>GitHub is a website that hosts Git repos on a server. You use it to share code with a team, and it is where CI (lesson 21) runs. The GitHub CLI (<code class="il">gh</code>) lets you drive GitHub from the terminal, for example creating a repo or opening a Pull Request without clicking around the website.</p>
<h3>Step 1: Create a GitHub account</h3>
<p>If you do not have an account yet, sign up at <a href="https://github.com/signup">github.com/signup</a> and confirm your email. If you already have one, skip this step.</p>
<h3>Step 2: Install the GitHub CLI</h3>
<ol>
<li>Open PowerShell and run the first command below (winget comes with Windows 10/11), or download the installer from <a href="https://cli.github.com/">cli.github.com</a>.</li>
<li>Close PowerShell, open it again, and run <code class="il">gh --version</code>. You should see a version number.</li>
</ol>''') + code('''winget install --id GitHub.cli
gh --version''', 'PowerShell') + T('''
<h3>ขั้นที่ 3: login ครั้งเดียว</h3>
<p>รัน <code class="il">gh auth login</code> แล้วตอบคำถามตามนี้ (ใช้ลูกศรขึ้นลงเลือก แล้วกด Enter)</p>
<ol>
<li><i>Where do you use GitHub?</i> → <b>GitHub.com</b></li>
<li><i>What is your preferred protocol for Git operations?</i> → <b>HTTPS</b></li>
<li><i>Authenticate Git with your GitHub credentials?</i> → <b>Yes</b></li>
<li><i>How would you like to authenticate GitHub CLI?</i> → <b>Login with a web browser</b></li>
<li>terminal จะแสดงรหัส 8 ตัว (one-time code) จดไว้ แล้วกด Enter เบราว์เซอร์จะเปิดหน้า GitHub ให้ใส่รหัสนั้น แล้วกด <b>Authorize</b></li>
</ol>
<p class="note">เช็ก: รัน <code class="il">gh auth status</code> ต้องเห็นข้อความว่า Logged in to github.com พร้อมชื่อบัญชีของคุณ</p>
''', '''
<h3>Step 3: Log in once</h3>
<p>Run <code class="il">gh auth login</code> and answer the prompts like this (use the arrow keys, then Enter):</p>
<ol>
<li><i>Where do you use GitHub?</i> → <b>GitHub.com</b></li>
<li><i>What is your preferred protocol for Git operations?</i> → <b>HTTPS</b></li>
<li><i>Authenticate Git with your GitHub credentials?</i> → <b>Yes</b></li>
<li><i>How would you like to authenticate GitHub CLI?</i> → <b>Login with a web browser</b></li>
<li>The terminal shows an 8-character one-time code. Note it and press Enter. Your browser opens a GitHub page; enter the code there and click <b>Authorize</b>.</li>
</ol>
<p class="note">Check: run <code class="il">gh auth status</code>. It should say you are logged in to github.com with your account name.</p>
''') + code('gh auth login\ngh auth status', 'PowerShell') + T('''
<h3>ขั้นที่ 4: สร้าง repo บน GitHub แล้ว push</h3>
<p>เข้าไปในโฟลเดอร์ repo จากบท 15 แล้วรันคำสั่งข้างล่าง คำสั่ง <code class="il">gh repo create</code> จะสร้าง repo ชื่อเดียวกันบน GitHub ตั้งชื่อ remote ว่า <code class="il">origin</code> แล้ว push commit ทั้งหมดขึ้นไปในขั้นตอนเดียว</p>''', '''
<h3>Step 4: Create the repo on GitHub and push</h3>
<p>Go into the repo folder from lesson 15 and run the commands below. <code class="il">gh repo create</code> creates a repo of the same name on GitHub, names the remote <code class="il">origin</code>, and pushes all your commits in one go.</p>''') + code('''cd ~/xiao-embedded-cpp
gh repo create xiao-embedded-cpp --public --source=. --remote=origin --push
gh repo view --web          # เปิดหน้า repo ในเบราว์เซอร์''', 'terminal', en={'# เปิดหน้า repo ในเบราว์เซอร์': '# open the repo page in your browser'}) + T('''
<p class="note">เช็ก: หน้า repo บน GitHub ต้องเห็นโฟลเดอร์ <code class="il">firmware/</code> และไฟล์ <code class="il">.gitignore</code> ส่วนแท็บ Commits ต้องเห็น commit จากบท 15–16 ตั้งแต่นี้ไป ทุกครั้งที่ commit ในเครื่องแล้ว ให้รัน <code class="il">git push</code> เพื่อส่งขึ้น GitHub</p>
''', '''
<p class="note">Check: the repo page on GitHub shows the <code class="il">firmware/</code> folder and <code class="il">.gitignore</code>, and the Commits view lists your commits from lessons 15–16. From now on, after you commit locally, run <code class="il">git push</code> to send it to GitHub.</p>
''') + qa([(T('fetch กับ pull ต่างกันอย่างไร?', 'How do fetch and pull differ?'),
           T('fetch ดึงข้อมูล remote มาเก็บไว้ (origin/main) แต่ยังไม่แตะ branch ของเรา pull = fetch + merge (หรือ rebase) เข้ามา', 'fetch downloads the remote state (origin/main) without touching your branch. pull = fetch + merge (or rebase) into your branch.')),
          (T('origin คืออะไร?', 'What is origin?'),
           T('ชื่อเล่นของ URL ของ repo บนเซิร์ฟเวอร์ ตั้งชื่ออื่นได้ แต่ origin เป็นธรรมเนียมสำหรับ remote หลัก ดูได้ด้วย git remote -v', 'A short name for the URL of the repo on the server. Any name works, but origin is the convention for the main remote. See it with git remote -v.'))]))
