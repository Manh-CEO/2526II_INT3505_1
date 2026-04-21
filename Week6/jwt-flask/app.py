import os
import datetime
from functools import wraps
from flask import Flask, request, jsonify
import jwt
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Cấu hình Secret Keys
ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET', 'super_secret_access_key')
REFRESH_TOKEN_SECRET = os.getenv('REFRESH_TOKEN_SECRET', 'super_secret_refresh_key')

# Mock Database
users = [
    {"id": 1, "username": "admin", "password": "password", "role": "admin"},
    {"id": 2, "username": "user1", "password": "password", "role": "user"}
]
refresh_tokens = set()

# ==========================
# Helpers (Sinh Token)
# ==========================
def generate_access_token(user):
    payload = {
        'id': user['id'],
        'username': user['username'],
        'role': user['role'],
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
    }
    return jwt.encode(payload, ACCESS_TOKEN_SECRET, algorithm='HS256')

def generate_refresh_token(user):
    payload = {
        'id': user['id'],
        'username': user['username'],
        'role': user['role'],
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7)
    }
    return jwt.encode(payload, REFRESH_TOKEN_SECRET, algorithm='HS256')

# ==========================
# Middleware Authenticate & Roles
# ==========================
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({'error': 'Thiếu Access Token'}), 401

        parts = auth_header.split()
        if len(parts) != 2 or parts[0] != 'Bearer':
            return jsonify({'error': 'Sai định dạng Authorization (Dùng: Bearer <token>)'}), 401
        
        token = parts[1]
        try:
            current_user = jwt.decode(token, ACCESS_TOKEN_SECRET, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token đã hết hạn'}), 403
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Token không hợp lệ'}), 403
            
        return f(current_user, *args, **kwargs)
    return decorated

def roles_required(*roles):
    def decorator(f):
        @wraps(f)
        def decorated(current_user, *args, **kwargs):
            if current_user.get('role') not in roles:
                return jsonify({'error': 'Không đủ quyền truy cập (Insufficient Permissions)'}), 403
            return f(current_user, *args, **kwargs)
        return decorated
    return decorator

# ==========================
# API Endpoints
# ==========================
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({'error': 'Thiếu username hoặc password'}), 400

    user = next((u for u in users if u['username'] == data['username'] and u['password'] == data['password']), None)
    
    if not user:
        return jsonify({'error': 'Sai tài khoản hoặc mật khẩu'}), 401

    access_token = generate_access_token(user)
    refresh_token = generate_refresh_token(user)
    refresh_tokens.add(refresh_token)

    return jsonify({
        'accessToken': access_token,
        'refreshToken': refresh_token
    })

@app.route('/api/refresh', methods=['POST'])
def refresh():
    data = request.get_json()
    if not data or 'token' not in data:
        return jsonify({'error': 'Thiếu tham số token'}), 400

    token = data['token']
    if token not in refresh_tokens:
        return jsonify({'error': 'Refresh Token không tồn tại hoặc đã bị thu hồi'}), 403

    try:
        user_data = jwt.decode(token, REFRESH_TOKEN_SECRET, algorithms=['HS256'])
        # Cấp token mới
        new_access_token = generate_access_token({
            'id': user_data['id'],
            'username': user_data['username'],
            'role': user_data['role']
        })
        return jsonify({'accessToken': new_access_token})
        
    except jwt.ExpiredSignatureError:
        refresh_tokens.remove(token) # Thu hồi token cũ
        return jsonify({'error': 'Refresh Token hết hạn, vui lòng đăng nhập lại'}), 403
    except jwt.InvalidTokenError:
        return jsonify({'error': 'Refresh Token không hợp lệ'}), 403

@app.route('/api/protected', methods=['GET'])
@token_required
def protected(current_user):
    return jsonify({
        'message': f"Xin chào {current_user['username']}, bạn đã truy cập thành công bằng Access Token hợp lệ!",
        'user': current_user
    })

@app.route('/api/admin', methods=['GET'])
@token_required
@roles_required('admin')
def admin_only(current_user):
    return jsonify({
        'message': 'Đây là dữ liệu mật cấp Admin. (Đã kiểm tra Role thành công).'
    })

# ==========================
# SECURITY AUDIT DEMO
# ==========================
@app.route('/api/leak-demo', methods=['GET'])
def leak_demo():
    token = request.args.get('token')
    if token:
        # Lỗi bảo mật Token Leakage do gắn vào URL Parameter
        return jsonify({'message': 'CẢNH BÁO BẢO MẬT: Token của bạn đã bị expose trên URL! Không bao giờ gửi Token qua URL params.'})
    else:
        return jsonify({'error': 'Hãy truyền ?token=xxx để test lỗ hổng Token Leakage.'}), 400

if __name__ == '__main__':
    app.run(debug=False, port=5001)
