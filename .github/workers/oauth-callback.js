/**
 * CANONIC OAuth Callback Worker
 *
 * Deploy to Cloudflare Workers: https://workers.cloudflare.com
 *
 * Environment variables needed:
 * - GITHUB_CLIENT_ID
 * - GITHUB_CLIENT_SECRET
 */

export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    // Handle OAuth callback
    if (url.pathname === '/callback') {
      const code = url.searchParams.get('code');
      const state = url.searchParams.get('state'); // Contains return URL

      if (!code) {
        return new Response('Missing code', { status: 400 });
      }

      try {
        // Exchange code for token
        const tokenResponse = await fetch('https://github.com/login/oauth/access_token', {
          method: 'POST',
          headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            client_id: env.GITHUB_CLIENT_ID,
            client_secret: env.GITHUB_CLIENT_SECRET,
            code: code,
          }),
        });

        const tokenData = await tokenResponse.json();

        if (tokenData.error) {
          return new Response(`OAuth error: ${tokenData.error_description}`, { status: 400 });
        }

        // Redirect back to app with token in fragment (not exposed to server logs)
        const returnUrl = state || 'https://canonic-apps.github.io/MED-CHAT/';
        const redirectUrl = `${returnUrl}#token=${tokenData.access_token}`;

        return Response.redirect(redirectUrl, 302);
      } catch (e) {
        return new Response(`Error: ${e.message}`, { status: 500 });
      }
    }

    // Handle login initiation
    if (url.pathname === '/login') {
      const returnUrl = url.searchParams.get('return') || 'https://canonic-apps.github.io/MED-CHAT/';
      const authUrl = `https://github.com/login/oauth/authorize?client_id=${env.GITHUB_CLIENT_ID}&redirect_uri=${encodeURIComponent(url.origin + '/callback')}&scope=repo&state=${encodeURIComponent(returnUrl)}`;
      return Response.redirect(authUrl, 302);
    }

    return new Response('CANONIC OAuth Worker\n\nEndpoints:\n- /login?return=URL\n- /callback', {
      headers: { 'Content-Type': 'text/plain' },
    });
  },
};
