import { pbkdf2Sync, timingSafeEqual, createHash } from 'node:crypto';

// Owner password for /stats/. Only a slow hash lives in this public repo.
// To change the password, set STATS_PASSWORD in Netlify environment variables.
const SALT = '3e5da2d1fcd72a62e2d7ca55d1b4d83e';
const HASH = '25d15473287fab8dccf7d3e8da198459eca6cd2a6de05b4d5f8af44d0935c97a';

export function checkPassword(pw) {
  if (typeof pw !== 'string' || !pw || pw.length > 200) return false;
  const envPw = process.env.STATS_PASSWORD;
  if (envPw) {
    const a = createHash('sha256').update(pw).digest();
    const b = createHash('sha256').update(envPw).digest();
    return timingSafeEqual(a, b);
  }
  const got = pbkdf2Sync(pw, SALT, 210000, 32, 'sha256');
  return timingSafeEqual(got, Buffer.from(HASH, 'hex'));
}

export function authed(req) {
  return checkPassword(req.headers.get('x-stats-key') || '');
}

// Dates are counted in Korea time.
export function kstDay(ms = Date.now()) {
  return new Date(ms + 9 * 3600e3).toISOString().slice(0, 10);
}

export function json(data, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { 'content-type': 'application/json; charset=utf-8', 'cache-control': 'no-store' },
  });
}

export function b64e(obj) {
  return Buffer.from(JSON.stringify(obj)).toString('base64url');
}
export function b64d(s) {
  try { return JSON.parse(Buffer.from(s, 'base64url').toString()); } catch { return null; }
}
