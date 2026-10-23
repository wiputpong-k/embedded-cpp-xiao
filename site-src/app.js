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
  render();
  if (location.hash) {
    var t = document.getElementById(location.hash.slice(1));
    if (t) setTimeout(function () { t.scrollIntoView(); }, 50);
  }
})();
