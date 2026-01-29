/**
 * CANONIC OAuth Callback Worker
 *
 * Environment variables:
 * - GITHUB_CLIENT_ID
 * - GITHUB_CLIENT_SECRET
 */

export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    if (url.pathname === '/callback') {
      const code = url.searchParams.get('code');
      const state = url.searchParams.get('state');

      if (!code) return new Response('Missing code', { status: 400 });

      const tokenResponse = await fetch('https://github.com/login/oauth/access_token', {
        method: 'POST',
        headers: { 'Accept': 'application/json', 'Content-Type': 'application/json' },
        body: JSON.stringify({
          client_id: env.GITHUB_CLIENT_ID,
          client_secret: env.GITHUB_CLIENT_SECRET,
          code: code,
        }),
      });

      const tokenData = await tokenResponse.json();
      if (tokenData.error) return new Response(tokenData.error_description, { status: 400 });

      const returnUrl = state || 'https://canonic-apps.github.io/MED-CHAT/';
      return Response.redirect(`${returnUrl}#token=${tokenData.access_token}`, 302);
    }

    if (url.pathname === '/login') {
      const returnUrl = url.searchParams.get('return') || 'https://canonic-apps.github.io/MED-CHAT/';
      const authUrl = `https://github.com/login/oauth/authorize?client_id=${env.GITHUB_CLIENT_ID}&redirect_uri=${encodeURIComponent(url.origin + '/callback')}&scope=repo&state=${encodeURIComponent(returnUrl)}`;
      return Response.redirect(authUrl, 302);
    }

    return new Response('CANONIC OAuth\n/login?return=URL\n/callback', { headers: { 'Content-Type': 'text/plain' } });
  },
};
