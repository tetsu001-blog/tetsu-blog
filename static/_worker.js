export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    // pages.dev ドメインからのアクセスを判定
    if (url.hostname === 'tetsu-blog.pages.dev') {
      url.hostname = 'tetsu-blog.net';
      return Response.redirect(url.toString(), 301);
    }
    // それ以外（すでにて.netの場合など）は通常通りコンテンツを返す
    return env.ASSETS.fetch(request);
  },
};
