import { getStore } from '@netlify/blobs';
import { authed, json, kstDay, b64d } from '../lib/common.mjs';

function emptyDay() {
  return { views: 0, visitors: 0, calls: 0, copies: 0, pages: {}, refs: {}, devices: {} };
}

function aggregate(keys) {
  const a = emptyDay();
  const seen = new Set();
  for (const k of keys) {
    const rec = b64d(k.slice(k.indexOf('~') + 1));
    if (!rec) continue;
    if (rec.e === 'call') { a.calls++; continue; }
    if (rec.e === 'copy') { a.copies++; continue; }
    a.views++;
    a.pages[rec.p] = (a.pages[rec.p] || 0) + 1;
    if (!seen.has(rec.v)) {
      seen.add(rec.v);
      // Count where a visitor came from and their device once per day, on first view.
      const r = rec.r === 'internal' ? 'direct' : rec.r;
      a.refs[r] = (a.refs[r] || 0) + 1;
      a.devices[rec.d] = (a.devices[rec.d] || 0) + 1;
    }
  }
  a.visitors = seen.size;
  return a;
}

async function dayStats(store, day, today) {
  // Finished days are summarised once and cached.
  if (day < today) {
    const cached = await store.get(`agg/${day}`, { type: 'json' });
    if (cached) return cached;
  }
  const { blobs } = await store.list({ prefix: `h/${day}/` });
  const a = aggregate(blobs.map((b) => b.key));
  if (day < today) await store.setJSON(`agg/${day}`, a);
  return a;
}

export default async (req) => {
  if (!authed(req)) return json({ error: 'password' }, 401);
  const url = new URL(req.url);
  const n = Math.min(Math.max(parseInt(url.searchParams.get('days') || '30', 10) || 30, 1), 92);
  const store = getStore({ name: 'stats', consistency: 'strong' });
  const today = kstDay();
  const days = [];
  for (let i = n - 1; i >= 0; i--) days.push(kstDay(Date.now() - i * 86400e3));
  const out = [];
  for (let i = 0; i < days.length; i += 8) {
    const chunk = days.slice(i, i + 8);
    out.push(...(await Promise.all(chunk.map((d) => dayStats(store, d, today)))));
  }
  return json({ today, days: days.map((d, i) => ({ day: d, ...out[i] })) });
};

export const config = { path: '/api/stats' };
