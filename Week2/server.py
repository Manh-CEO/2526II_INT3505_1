from flask import Flask
from dataclasses import dataclass

app = Flask(__name__)

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




@app.route('/')
def hello():
    return 'Hello World!'

@app.route('/books')
def get_books():
    return [book.__dict__ for book in books]



if __name__ == '__main__':
    app.run(debug=True, )