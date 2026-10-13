/* Visit counter for the owner's stats page. Sends the page path, the referring
   site and button clicks. No cookies; skipped on devices that opened /stats/. */
(function () {
  try { if (localStorage.getItem('ps_owner')) return; } catch (e) {}
  function send(e) {
    var d = JSON.stringify({ e: e, p: location.pathname, r: document.referrer || '' });
    try {
      if (navigator.sendBeacon && navigator.sendBeacon('/api/hit', new Blob([d], { type: 'application/json' }))) return;
    } catch (x) {}
    try { fetch('/api/hit', { method: 'POST', body: d, keepalive: true, headers: { 'content-type': 'application/json' } }); } catch (x) {}
  }
  send('view');
  document.addEventListener('click', function (ev) {
    var t = ev.target;
    if (!t || !t.closest) return;
    if (t.closest('a[href^="tel:"]')) send('call');
    else if (t.closest('button.copy[data-copy="phone"]')) send('copy');
  }, true);
})();
