(function () {
  // Progress is shared by both languages. v2: lessons were renumbered when the course grew to 25.
  var KEY = 'xiao-cpp-done-v2', LAST = 'xiao-cpp-last';
  function load(k, fallback) { try { return JSON.parse(localStorage.getItem(k)) || fallback; } catch (e) { return fallback; } }
  function save(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) {} }
  var done = load(KEY, {});
  var pc = document.getElementById('pc');
  var total = pc ? +pc.dataset.total : 0;

  function count(ids) { return ids.filter(function (id) { return done[id]; }).length; }
  function renderBar() {
    var n = Object.keys(done).filter(function (k) { return done[k]; }).length;
    document.getElementById('pf').style.width = (total ? n / total * 100 : 0) + '%';
    pc.textContent = n + '/' + total;
  }

  // Lesson page: "finished" checkbox, and remember this lesson as the last one opened.
  var box = document.querySelector('.done input');
  if (box) {
    var id = box.dataset.l;
    box.checked = !!done[id];
    box.addEventListener('change', function () {
      done[id] = box.checked;
      save(KEY, done);
      renderBar();
    });
    save(LAST, id);
  }

  // Home page: dots, per-module progress, continue button, search.
  document.querySelectorAll('.modblock').forEach(function (mod) {
    var dots = Array.prototype.slice.call(mod.querySelectorAll('.dot'));
    var ids = dots.map(function (d) { return d.dataset.for; });
    dots.forEach(function (d) { d.classList.toggle('on', !!done[d.dataset.for]); });
    var n = count(ids);
    mod.querySelector('.mc').textContent = n + '/' + ids.length;
    mod.querySelector('.mpf').style.width = (ids.length ? n / ids.length * 100 : 0) + '%';
  });
  var idxEl = document.getElementById('lessons-index');
  var lessons = [];
  try { lessons = idxEl ? JSON.parse(idxEl.textContent) : []; } catch (e) { lessons = []; }
  var cta = document.getElementById('continue');
  if (cta && lessons.length) {
    var last = load(LAST, null);
    var pick = null, label = cta.dataset.start;
    for (var i = 0; i < lessons.length; i++) if ('l' + lessons[i].n === last) pick = i;
    if (pick !== null && done['l' + lessons[pick].n]) {
      // last one is finished: go to the next unfinished lesson after it
      for (var j = pick + 1; j < lessons.length; j++) if (!done['l' + lessons[j].n]) { pick = j; break; }
    }
    if (pick !== null) {
      var L = lessons[pick];
      label = (done['l' + L.n] ? cta.dataset.done : cta.dataset.resume) + ' ' + L.n + ' · ' + L.t;
      cta.href = L.u;
    }
    cta.textContent = label;
  }
  var q = document.getElementById('q');
  if (q) {
    var results = document.getElementById('results'), none = document.getElementById('noresults');
    q.addEventListener('input', function () {
      var terms = q.value.toLowerCase().split(/\s+/).filter(Boolean);
      results.innerHTML = '';
      if (!terms.length) { results.hidden = true; none.hidden = true; return; }
      var hits = lessons.filter(function (L) {
        var hay = (L.n + ' ' + L.t + ' ' + L.g + ' ' + L.h.join(' ') + ' ' + L.m).toLowerCase();
        return terms.every(function (t) { return hay.indexOf(t) !== -1; });
      });
      hits.slice(0, 8).forEach(function (L) {
        var li = document.createElement('li'), a = document.createElement('a');
        a.href = L.u;
        var num = document.createElement('span'); num.className = 'pn2 m'; num.textContent = L.n;
        var t = document.createElement('span'); t.className = 'pt'; t.textContent = L.t;
        var g = document.createElement('small'); g.textContent = L.g;
        t.appendChild(g);
        a.appendChild(num); a.appendChild(t); li.appendChild(a); results.appendChild(li);
      });
      results.hidden = !hits.length;
      none.hidden = !!hits.length;
    });
  }
  if (pc) renderBar();

  // Jump menu in the top bar.
  var jump = document.getElementById('jump');
  if (jump) jump.addEventListener('change', function () { location.href = jump.value; });

  // Copy button on every code block; label follows the page language.
  var th = document.documentElement.lang === 'th';
  var C = th ? { copy: 'คัดลอก', done: 'คัดลอกแล้ว', fail: 'คัดลอกไม่ได้' } : { copy: 'Copy', done: 'Copied', fail: 'Copy failed' };
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
  document.querySelectorAll('.code').forEach(function (codeBox) {
    var code = codeBox.querySelector('pre code');
    if (!code) return;
    var btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'copy';
    btn.textContent = C.copy;
    btn.addEventListener('click', function () {
      copyText(code.textContent).then(function () { btn.textContent = C.done; }, function () { btn.textContent = C.fail; });
      setTimeout(function () { btn.textContent = C.copy; }, 1800);
    });
    codeBox.appendChild(btn);
  });

  // Language switch: keep the section currently on screen (both languages share the s1, s2, ... ids).
  var lang = document.getElementById('lang');
  if (lang) lang.addEventListener('click', function () {
    var cur = '';
    document.querySelectorAll('.lesson h3[id]').forEach(function (h) {
      if (h.getBoundingClientRect().top < window.innerHeight / 3) cur = '#' + h.id;
    });
    if (cur) lang.href = lang.href.split('#')[0] + cur;
  });
})();
