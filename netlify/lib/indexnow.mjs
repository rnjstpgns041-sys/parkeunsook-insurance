// Tells Naver (and the other IndexNow engines) about guide pages that are new since the last run.
// The key file 29c34deb8e9735aae78566a6f626da19.txt at the site root proves we own the site.
const SITE = 'https://parkeunsook-insurance.netlify.app';
const HOST = 'parkeunsook-insurance.netlify.app';
const KEY = '29c34deb8e9735aae78566a6f626da19';
const ENDPOINT = 'https://searchadvisor.naver.com/indexnow';

function readSitemap(xml) {
  return [...xml.matchAll(/<url>\s*<loc>([^<]+)<\/loc>(?:\s*<lastmod>([^<]+)<\/lastmod>)?/g)]
    .map((m) => ({ loc: m[1].trim(), lastmod: (m[2] || '').trim() }));
}

export async function submitNew(store) {
  const res = await fetch(SITE + '/sitemap.xml', { headers: { 'cache-control': 'no-cache' } });
  if (!res.ok) throw new Error('sitemap ' + res.status);
  const entries = readSitemap(await res.text());
  const sent = await store.get('indexnow/sent', { type: 'json' });
  let todo;
  if (!sent) {
    // First run: only the newest pages. Older ones were already submitted by hand.
    const newest = entries.map((e) => e.lastmod).sort().pop();
    todo = entries.filter((e) => e.lastmod === newest).map((e) => e.loc);
  } else {
    const done = new Set(sent);
    todo = entries.map((e) => e.loc).filter((u) => !done.has(u));
  }
  const result = { at: new Date().toISOString(), total: todo.length, ok: 0, status: [] };
  const okUrls = [];
  for (let i = 0; i < todo.length; i += 100) {
    const urlList = todo.slice(i, i + 100);
    const r = await fetch(ENDPOINT, {
      method: 'POST',
      headers: { 'content-type': 'application/json; charset=utf-8' },
      body: JSON.stringify({ host: HOST, key: KEY, keyLocation: SITE + '/' + KEY + '.txt', urlList }),
    });
    result.status.push(r.status);
    if (r.status === 200 || r.status === 202) { result.ok += urlList.length; okUrls.push(...urlList); }
  }
  const base = sent || entries.map((e) => e.loc).filter((u) => !todo.includes(u));
  await store.setJSON('indexnow/sent', [...new Set([...base, ...okUrls])]);
  if (todo.length) await store.setJSON('indexnow/last', { ...result, urls: todo });
  return result;
}
