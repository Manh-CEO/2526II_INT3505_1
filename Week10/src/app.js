const express = require('express');
const winston = require('winston');
const client = require('prom-client');
const rateLimit = require('express-rate-limit');
const helmet = require('helmet');

const app = express();
const port = process.env.PORT || 3000;

// 1. THIẾT LẬP LOGGING (Winston)
const logger = winston.createLogger({
  level: 'info',
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.json()
  ),
  transports: [
    new winston.transports.Console(),
    new winston.transports.File({ filename: 'logs/error.log', level: 'error' }),
    new winston.transports.File({ filename: 'logs/combined.log' }),
  ],
});

// 2. THIẾT LẬP MONITORING (Prometheus)
const collectDefaultMetrics = client.collectDefaultMetrics;
collectDefaultMetrics({ register: client.register });

const httpRequestDurationMicroseconds = new client.Histogram({
  name: 'http_request_duration_seconds',
  help: 'Duration of HTTP requests in microseconds',
  labelNames: ['method', 'route', 'code'],
  buckets: [0.1, 0.3, 0.5, 0.7, 1, 3, 5, 7, 10]
});

// 3. THIẾT LẬP SECURITY & RATE LIMITING
app.use(helmet()); // Bảo mật headers

const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 phút
  max: 100, // Giới hạn 100 request mỗi IP
  message: {
    status: 429,
    message: 'Quá nhiều request từ IP này, vui lòng thử lại sau 15 phút.'
  },
  standardHeaders: true,
  legacyHeaders: false,
});
app.use('/api/', limiter); // Áp dụng rate limit cho các route /api/

// Middleware để log request và tính thời gian xử lý
app.use((req, res, next) => {
  const start = Date.now();
  res.on('finish', () => {
    const duration = Date.now() - start;
    httpRequestDurationMicroseconds
      .labels(req.method, req.path, res.statusCode)
      .observe(duration / 1000);
    
    logger.info({
      method: req.method,
      url: req.url,
      status: res.statusCode,
      duration: `${duration}ms`,
    });
  });
  next();
});

// ROUTES
app.get('/', (req, res) => {
  res.send('<h1>Week 10: Production API Demo</h1><p>Check <a href="/metrics">/metrics</a> for Prometheus data.</p>');
});

app.get('/api/data', (req, res) => {
  res.json({ message: 'Đây là dữ liệu từ API đã được bảo mật và giám sát!', timestamp: new Date() });
});

// Endpoint cho Prometheus scraper
app.get('/metrics', async (req, res) => {
  res.set('Content-Type', client.register.contentType);
  res.end(await client.register.metrics());
});

// Error handling log
app.get('/api/error', (req, res) => {
  logger.error('Cố tình tạo lỗi để kiểm tra log file');
  res.status(500).json({ error: 'Đã có lỗi xảy ra!' });
});

app.listen(port, () => {
  console.log(`Server đang chạy tại http://localhost:${port}`);
  logger.info(`Server started on port ${port}`);
});
