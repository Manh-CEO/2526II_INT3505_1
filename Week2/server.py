import jwt
import datetime
from flask import Flask, request, jsonify
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

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization') # Client phải gửi kèm token

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        except:
            return jsonify({'message': 'Token is invalid or expired!'}), 401

        return f(*args, **kwargs)
    return decorated

@app.route('/books', methods=['GET'])
@token_required
def get_books():
    return jsonify([book.__dict__ for book in books])

if __name__ == '__main__':
    app.run(debug=True)