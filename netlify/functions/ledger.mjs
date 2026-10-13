import { getStore } from '@netlify/blobs';
import { randomBytes } from 'node:crypto';
import { authed, json } from '../lib/common.mjs';

// Advertising ledger: one JSON list of spend entries, owner only.
export default async (req) => {
  if (!authed(req)) return json({ error: 'password' }, 401);
  const store = getStore({ name: 'stats', consistency: 'strong' });
  const list = (await store.get('ledger', { type: 'json' })) || [];
  if (req.method === 'GET') return json({ entries: list });

  let body;
  try { body = JSON.parse(await req.text()); } catch { return json({ error: 'bad json' }, 400); }
  if (req.method === 'POST') {
    const amount = Math.round(Number(body.amount));
    if (!/^\d{4}-\d{2}-\d{2}$/.test(body.date || '') || !Number.isFinite(amount) || amount < 0 || amount > 1e10) {
      return json({ error: '날짜와 금액을 확인해 주세요.' }, 400);
    }
    list.push({
      id: randomBytes(6).toString('hex'),
      date: body.date,
      channel: String(body.channel || '기타').slice(0, 40),
      amount,
      memo: String(body.memo || '').slice(0, 200),
    });
  } else if (req.method === 'DELETE') {
    const i = list.findIndex((x) => x.id === body.id);
    if (i < 0) return json({ error: 'not found' }, 404);
    list.splice(i, 1);
  } else {
    return json({ error: 'method' }, 405);
  }
  list.sort((a, b) => (a.date < b.date ? 1 : a.date > b.date ? -1 : 0));
  await store.setJSON('ledger', list);
  return json({ entries: list });
};

export const config = { path: '/api/ledger' };
