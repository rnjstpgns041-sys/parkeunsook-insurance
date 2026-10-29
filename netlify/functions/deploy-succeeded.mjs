import { connectLambda, getStore } from '@netlify/blobs';
import { submitNew } from '../lib/indexnow.mjs';

// Netlify runs this after every successful deploy.
export const handler = async (event) => {
  connectLambda(event);
  try {
    const r = await submitNew(getStore({ name: 'stats', consistency: 'strong' }));
    console.log('indexnow', JSON.stringify(r));
  } catch (e) {
    console.log('indexnow failed', e.message);
  }
  return { statusCode: 200 };
};
