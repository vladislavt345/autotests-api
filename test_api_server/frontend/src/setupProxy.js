const { createProxyMiddleware } = require('http-proxy-middleware');

module.exports = function(app) {
  app.use(
    '/cats',
    createProxyMiddleware({
      target: 'http://26.206.108.15:8000',
      changeOrigin: true,
    })
  );
  // Добавь сюда остальные пути, если нужно проксировать другие эндпоинты
};
