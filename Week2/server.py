import jwt
import datetime
import hashlib
import json
from flask import Flask, request, jsonify, make_response
from dataclasses import dataclass
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_super_secret_key'

@dataclass
class Book:
    id: int
    title: str
    author: str
    price: float

books = [
    Book(id=1, title="Book 1", author="Author 1", price=10.0),
    Book(id=2, title="Book 2", author="Author 2", price=20.0),
    Book(id=3, title="Book 3", author="Author 3", price=30.0),
]

def generate_etag(data_list):
    data_str = json.dumps([b.__dict__ for b in data_list], sort_keys=True)
    return hashlib.md5(data_str.encode('utf-8')).hexdigest()

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        try:
            jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        except:
            return jsonify({'message': 'Token is invalid or expired!'}), 401
        return f(*args, **kwargs)
    return decorated

@app.route('/login', methods=['POST'])
def login():
    auth = request.json
    if auth and auth.get('username') == 'admin' and auth.get('password') == '123':
        token = jwt.encode({
            'user': auth.get('username'),
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        }, app.config['SECRET_KEY'], algorithm="HS256")
        return jsonify({'token': token})
    return jsonify({"message": "Could not verify"}), 401



@app.route('/books', methods=['GET'])
@token_required
def get_books():
    current_etag = generate_etag(books)
    
    client_etag = request.headers.get('If-None-Match')
    
    if client_etag == current_etag:
        return '', 304 

    response = make_response(jsonify([book.__dict__ for book in books]))
    response.headers['ETag'] = current_etag
    response.headers['Cache-Control'] = 'public, max-age=60'
    return response

if __name__ == '__main__':
    app.run(debug=True)