from flask import Flask, jsonify, request
from flask_swagger_ui import get_swaggerui_blueprint
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent))


app = Flask(__name__)

SWAGGER_URL = '/api/docs'
API_URL = '/swagger.yaml'

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={'app_name': "API Quản lý Sách"}
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

books = [
    {"id": 1, "title": "Nhà Giả Kim", "author": "Paulo Coelho"},
    {"id": 2, "title": "Tư duy nhanh và chậm", "author": "Daniel Kahneman"}
]

@app.route('/books', methods=['GET'])
def get_books():
    return jsonify(books), 200

@app.route('/books', methods=['POST'])
def add_book():
    data = request.get_json()
    new_book = {
        "id": len(books) + 1,
        "title": data.get("title"),
        "author": data.get("author")
    }
    books.append(new_book)
    return jsonify(new_book), 201

@app.route('/books/<int:id>', methods=['GET'])
def get_book(id):
    book = next((b for b in books if b["id"] == id), None)
    if book:
        return jsonify(book), 200
    return jsonify({"error": "Không tìm thấy sách"}), 404

@app.route('/books/<int:id>', methods=['PUT'])
def update_book(id):
    book = next((b for b in books if b["id"] == id), None)
    if book:
        data = request.get_json()
        book.update({"title": data.get("title"), "author": data.get("author")})
        return jsonify(book), 200
    return jsonify({"error": "Không tìm thấy sách"}), 404

@app.route('/books/<int:id>', methods=['DELETE'])
def delete_book(id):
    global books
    books = [b for b in books if b["id"] != id]
    return jsonify({"message": "Đã xóa thành công"}), 200

if __name__ == "__main__":
    app.run(debug=True, port=5000)