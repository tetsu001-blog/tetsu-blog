export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    // pages.dev ドメインからのアクセスを判定
    if (url.hostname === 'tetsu-blog.pages.dev') {
      url.hostname = 'tetsu-blog.net';
      return Response.redirect(url.toString(), 301);
    }

    // それ以外（すでにて.netの場合など）は通常通りコンテンツを返す
    const response = await env.ASSETS.fetch(request);

    if (!shouldNoindex(url.pathname)) {
      return response;
    }

    const headers = new Headers(response.headers);
    headers.set('X-Robots-Tag', 'noindex, follow');
    return new Response(response.body, {
      status: response.status,
      statusText: response.statusText,
      headers,
    });
  },
};

function shouldNoindex(pathname) {
  const normalizedPath = pathname.endsWith('/') ? pathname : `${pathname}/`;
  const noindexPaths = new Set([
    '/about/',
    '/contact/',
    '/thanks/',
    '/privacy/',
    '/swap/',
    '/trade/',
    '/posts/',
  ]);

  return (
    pathname === '/index.json' ||
    pathname === '/index.xml' ||
    pathname.endsWith('/index.xml') ||
    normalizedPath.startsWith('/page/') ||
    normalizedPath.startsWith('/tags/') ||
    normalizedPath.startsWith('/categories/') ||
    noindexPaths.has(normalizedPath)
  );
}
