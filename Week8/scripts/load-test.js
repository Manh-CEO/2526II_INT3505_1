import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '30s', target: 20 }, // Ramp-up to 20 users
    { duration: '1m', target: 20 },  // Stay at 20 users (Load test)
    { duration: '30s', target: 0 },  // Ramp-down
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'], // 95% of requests must complete below 500ms
    http_req_failed: ['rate<0.01'],   // Error rate must be less than 1%
  },
};

const BASE_URL_BOOK = 'http://127.0.0.1:5000';
const BASE_URL_JWT = 'http://127.0.0.1:5001';

export default function () {
  // 1. Get Books
  let res = http.get(`${BASE_URL_BOOK}/books`);
  check(res, { 'status is 200': (r) => r.status === 200 });

  // 2. Login
  let payload = JSON.stringify({
    username: 'admin',
    password: 'password',
  });
  let params = {
    headers: {
      'Content-Type': 'application/json',
    },
  };
  res = http.post(`${BASE_URL_JWT}/api/login`, payload, params);
  check(res, { 'login success': (r) => r.status === 200 });

  sleep(1);
}
