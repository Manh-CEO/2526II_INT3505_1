require('dotenv').config();
const express = require('express');
const jwt = require('jsonwebtoken');

const app = express();
app.use(express.json());

const PORT = 3000;
const ACCESS_TOKEN_SECRET = process.env.ACCESS_TOKEN_SECRET || 'secret_access_key_123';
const REFRESH_TOKEN_SECRET = process.env.REFRESH_TOKEN_SECRET || 'secret_refresh_key_456';

// Mock Database (In-Memory)
let refreshTokens = [];
const users = [
    { id: 1, username: 'admin', password: 'password', role: 'admin' },
    { id: 2, username: 'user1', password: 'password', role: 'user' }
];

// Hàm hỗ trợ tạo token
function generateAccessToken(user) {
    // Access token sống 15 phút (Giảm rủi ro Replay attack)
    return jwt.sign({ id: user.id, username: user.username, role: user.role }, ACCESS_TOKEN_SECRET, { expiresIn: '15m' });
}

function generateRefreshToken(user) {
    // Refresh token sống lâu hơn
    return jwt.sign({ id: user.id, username: user.username, role: user.role }, REFRESH_TOKEN_SECRET, { expiresIn: '7d' });
}

// ==========================
// THỰC HÀNH: API Authentication
// ==========================

// 1. Đăng nhập - Cấp token
app.post('/api/login', (req, res) => {
    const { username, password } = req.body;
    const user = users.find(u => u.username === username && u.password === password);
    
    if (!user) return res.status(401).json({ error: 'Sai tài khoản hoặc mật khẩu' });

    const accessToken = generateAccessToken(user);
    const refreshToken = generateRefreshToken(user);
    
    // Lưu vào DB ở thực tế, ở đây push vào mảng
    refreshTokens.push(refreshToken);

    res.json({ accessToken, refreshToken });
});

// 2. Refresh Token - Cấp access token mới
app.post('/api/refresh', (req, res) => {
    const { token } = req.body;
    if (!token) return res.status(401).json({ error: 'Thiếu Refresh Token' });
    if (!refreshTokens.includes(token)) return res.status(403).json({ error: 'Refresh Token không hợp lệ' });

    jwt.verify(token, REFRESH_TOKEN_SECRET, (err, user) => {
        if (err) return res.status(403).json({ error: 'Refresh Token hết hạn' });
        
        // Cấp access token mới
        const accessToken = generateAccessToken({ id: user.id, username: user.username, role: user.role });
        res.json({ accessToken });
    });
});

// ==========================
// Middleware & Scopes/Roles
// ==========================

// Middleware verify Bearer Token (Chống Token Leakage trong URL)
function authenticateToken(req, res, next) {
    const authHeader = req.headers['authorization']; // Lấy Header
    // Chuẩn: Bearer <token>
    const token = authHeader && authHeader.split(' ')[1]; 
    
    if (!token) return res.status(401).json({ error: 'Thiếu Access Token' });

    jwt.verify(token, ACCESS_TOKEN_SECRET, (err, user) => {
        if (err) return res.status(403).json({ error: 'Token không hợp lệ hoặc đã hết hạn' });
        req.user = user;
        next();
    });
}

// Middleware check Roles (RBAC)
function requireRole(role) {
    return (req, res, next) => {
        if (req.user.role !== role) {
            return res.status(403).json({ error: 'Không đủ quyền truy cập (Insufficient Permissions)' });
        }
        next();
    }
}

// 3. API Protected (Chỉ cần đăng nhập)
app.get('/api/protected', authenticateToken, (req, res) => {
    res.json({ 
        message: `Xin chào ${req.user.username}, bạn đã truy cập thành công bằng Access Token hợp lệ!`, 
        user: req.user 
    });
});

// 4. API Phân quyền (Chỉ dành cho Admin)
app.get('/api/admin', authenticateToken, requireRole('admin'), (req, res) => {
    res.json({ message: 'Đây là dữ liệu mật cấp Admin. (Đã kiểm tra Role thành công).' });
});

// ==========================
// SECURITY AUDIT DEMO
// ==========================

// 5. Minh họa lỗ hổng Token Leakage (Lấy token từ URL)
app.get('/api/leak-demo', (req, res) => {
    const token = req.query.token;
    if(token) {
        // BAD PRACTICE: Lộ token trên URL -> Bị lưu tại Browser history, server logs, proxy.
        // Hacker có thể đánh cắp token bằng cách đọc URL.
        res.json({ message: 'CẢNH BÁO BẢO MẬT: Token của bạn đã bị expose trên URL! Không bao giờ gửi Token qua URL params.' });
    } else {
        res.status(400).json({ error: 'Hãy truyền ?token=xxx để test lỗ hổng Token Leakage.' });
    }
});

app.listen(PORT, () => {
    console.log(`Server JWT chạy tại http://localhost:${PORT}`);
});
