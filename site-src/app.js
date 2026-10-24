(function () {
  var KEY = 'xiao-cpp-done';
  var done = {};
  try { done = JSON.parse(localStorage.getItem(KEY) || '{}') || {}; } catch (e) { done = {}; }
  var boxes = document.querySelectorAll('.done input');
  var total = boxes.length;
  function render() {
    var n = 0;
    boxes.forEach(function (b) {
      var on = !!done[b.dataset.l];
      b.checked = on;
      if (on) n++;
      var d = document.querySelector('.dot[data-for="' + b.dataset.l + '"]');
      if (d) d.classList.toggle('on', on);
    });
    document.getElementById('pf').style.width = (total ? n / total * 100 : 0) + '%';
    document.getElementById('pc').textContent = n + '/' + total;
  }
  boxes.forEach(function (b) {
    b.addEventListener('change', function () {
      done[b.dataset.l] = b.checked;
      try { localStorage.setItem(KEY, JSON.stringify(done)); } catch (e) {}
      render();
    });
  });
  var jump = document.getElementById('jump');
  jump.addEventListener('change', function () {
    var el = document.getElementById(jump.value);
    if (el) el.scrollIntoView();
  });
  // Copy button on every code block; label follows the page language.
  var th = document.documentElement.lang === 'th';
  var L = th ? { copy: 'คัดลอก', done: 'คัดลอกแล้ว', fail: 'คัดลอกไม่ได้' } : { copy: 'Copy', done: 'Copied', fail: 'Copy failed' };
  function copyText(text) {
    if (navigator.clipboard && window.isSecureContext) return navigator.clipboard.writeText(text);
    return new Promise(function (ok, bad) {
      var ta = document.createElement('textarea');
      ta.value = text;
      ta.setAttribute('readonly', '');
      ta.style.position = 'fixed';
      ta.style.opacity = '0';
      document.body.appendChild(ta);
      ta.select();
      try { document.execCommand('copy') ? ok() : bad(); } catch (e) { bad(e); }
      document.body.removeChild(ta);
    });
  }
  document.querySelectorAll('.code').forEach(function (box) {
    var code = box.querySelector('pre code');
    if (!code) return;
    var btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'copy';
    btn.textContent = L.copy;
    btn.addEventListener('click', function () {
      copyText(code.textContent).then(function () { btn.textContent = L.done; }, function () { btn.textContent = L.fail; });
      setTimeout(function () { btn.textContent = L.copy; }, 1800);
    });
    box.appendChild(btn);
  });

  // Language switch: carry the lesson currently on screen over to the other page.
  var lang = document.getElementById('lang');
  if (lang) lang.addEventListener('click', function () {
    var cur = location.hash;
    document.querySelectorAll('.lesson').forEach(function (s) {
      if (s.getBoundingClientRect().top < window.innerHeight / 3) cur = '#' + s.id;
    });
    if (cur) lang.href = lang.href.split('#')[0] + cur;
  });
  render();
  if (location.hash) {
    var t = document.getElementById(location.hash.slice(1));
    if (t) setTimeout(function () { t.scrollIntoView(); }, 50);
  }
})();
