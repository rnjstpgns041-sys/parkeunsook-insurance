import { getStore } from '@netlify/blobs';
import { createHash, randomBytes } from 'node:crypto';
import { kstDay, b64e } from '../lib/common.mjs';

// Records one visit or button event. Each hit is one blob whose key carries the
// data, so the stats page can read a whole day with a single list call.
const EVENTS = new Set(['view', 'call', 'copy']);
const BOT = /bot|crawl|spider|slurp|yeti|daum|bingpreview|headless|lighthouse|python|curl|wget/i;

function refKind(ref, host) {
  if (!ref) return 'direct';
  let u;
  try { u = new URL(ref); } catch { return 'direct'; }
  if (u.host === host) return 'internal';
  const h = u.hostname;
  if (/naver\.com$/.test(h)) return 'naver';
  if (/google\./.test(h)) return 'google';
  if (/daum\.net$|kakao\.com$/.test(h)) return 'daum';
  if (/instagram\.com$|facebook\.com$|threads\.net$/.test(h)) return 'sns';
  return 'other:' + h.slice(0, 60);
}

function decodeSafe(s) {
  try { return decodeURI(s); } catch { return s; }
}

export default async (req, context) => {
  if (req.method !== 'POST') return new Response(null, { status: 405 });
  const ua = req.headers.get('user-agent') || '';
  if (BOT.test(ua)) return new Response(null, { status: 204 });
  let body;
  try { body = JSON.parse(await req.text()); } catch { return new Response(null, { status: 400 }); }
  const e = EVENTS.has(body.e) ? body.e : null;
  if (!e) return new Response(null, { status: 400 });
  const host = new URL(req.url).host;
  const now = Date.now();
  const day = kstDay(now);
  const ip = context.ip || req.headers.get('x-nf-client-connection-ip') || '';
  // Daily visitor id: not reversible, changes every day, raw IP is never stored.
  const v = createHash('sha256').update(day + '|' + ip + '|' + ua).digest('base64url').slice(0, 10);
  const rec = {
    e,
    p: encodeURI(decodeSafe(String(body.p || '/'))).slice(0, 100),
    r: refKind(String(body.r || ''), host),
    d: /Mobi|Android|iPhone/i.test(ua) ? 'm' : 'd',
    v,
  };
  const key = `h/${day}/${now.toString(36)}${randomBytes(3).toString('hex')}~${b64e(rec)}`;
  if (Buffer.byteLength(key) > 600) return new Response(null, { status: 400 });
  await getStore('stats').set(key, '');
  return new Response(null, { status: 204 });
};

export const config = { path: '/api/hit' };
