/* Shared helpers for the owner pages: password gate and API calls. */
var PS = (function () {
  var KEY = 'ps_stats_key';
  function getKey() { try { return localStorage.getItem(KEY) || ''; } catch (e) { return ''; } }
  function setKey(k) {
    try {
      localStorage.setItem(KEY, k);
      localStorage.setItem('ps_owner', '1'); // this device stops counting as a visitor
    } catch (e) {}
  }
  function clearKey() { try { localStorage.removeItem(KEY); } catch (e) {} }
  async function api(path, opts) {
    opts = opts || {};
    var res = await fetch(path, {
      method: opts.method || 'GET',
      headers: Object.assign({ 'x-stats-key': opts.key || getKey(), 'content-type': 'application/json' }),
      body: opts.body ? JSON.stringify(opts.body) : undefined,
    });
    if (res.status === 401) { var e = new Error('password'); e.code = 401; throw e; }
    var data = await res.json().catch(function () { return {}; });
    if (!res.ok) throw new Error(data.error || '서버 응답 오류 (' + res.status + ')');
    return data;
  }
  // Show the login form until a key works, then call onReady.
  function gate(onReady) {
    var login = document.getElementById('login'), app = document.getElementById('app');
    var form = document.getElementById('login-form'), err = document.getElementById('login-err');
    function show(ok) { login.hidden = ok; app.hidden = !ok; }
    async function tryKey(k, fromForm) {
      try {
        await onReady(k);
        if (fromForm) setKey(k);
        show(true);
      } catch (e) {
        show(false);
        if (e.code === 401) { clearKey(); if (fromForm) err.textContent = '비밀번호가 맞지 않아요.'; }
        else err.textContent = '불러오지 못했어요. ' + e.message;
      }
    }
    form.addEventListener('submit', function (ev) {
      ev.preventDefault(); err.textContent = '';
      var k = document.getElementById('pw').value.trim();
      if (k) tryKey(k, true);
    });
    var saved = getKey();
    if (saved) tryKey(saved, false); else show(false);
  }
  function won(n) { return Math.round(n).toLocaleString('ko-KR') + '원'; }
  function num(n) { return (n || 0).toLocaleString('ko-KR'); }
  return { api: api, gate: gate, getKey: getKey, won: won, num: num };
})();
