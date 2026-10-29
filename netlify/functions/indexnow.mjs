import { getStore } from '@netlify/blobs';
import { authed, json } from '../lib/common.mjs';
import { submitNew } from '../lib/indexnow.mjs';

// GET: last automatic submission. POST: submit anything not sent yet.
export default async (req) => {
  if (!authed(req)) return json({ error: 'password' }, 401);
  const store = getStore({ name: 'stats', consistency: 'strong' });
  if (req.method === 'POST') return json(await submitNew(store));
  return json((await store.get('indexnow/last', { type: 'json' })) || {});
};

export const config = { path: '/api/indexnow' };
