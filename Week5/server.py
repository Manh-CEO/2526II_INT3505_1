from flask import Flask, jsonify, request

app = Flask(__name__)

# --- MOCK DATA (Thay thế cho Database) ---
books = [{"id": i, "title": f"Book {i}", "isbn": f"ISBN-{i}"} for i in range(1, 101)]
members = {
    "1": {"id": "1", "name": "Alice", "email": "alice@email.com"},
    "2": {"id": "2", "name": "Bob", "email": "bob@email.com"}
}
loans = {
    "1": [{"book_id": 1, "date": "2024-03-01", "status": "borrowed"}] # Loans của member 1
}

# --- ENDPOINTS ---

# 1. Independent Resource: Books (Search & Pagination)
# GET /books?q=keyword&offset=0&limit=10
@app.route('/books', methods=['GET'])
def get_books():
    query = request.args.get('q', '').lower()
    offset = int(request.args.get('offset', 0))
    limit = int(request.args.get('limit', 10))

    # Search logic
    filtered_books = [b for b in books if query in b['title'].lower()]
    
    # Pagination logic (Offset/Limit)
    paginated_data = filtered_books[offset : offset + limit]

    # HATEOAS (Hypermedia links)
    return jsonify({
        "metadata": {
            "total": len(filtered_books),
            "offset": offset,
            "limit": limit
        },
        "data": paginated_data,
        "links": {
            "next": f"/books?q={query}&offset={offset + limit}&limit={limit}" if offset + limit < len(filtered_books) else None,
            "prev": f"/books?q={query}&offset={max(0, offset - limit)}&limit={limit}" if offset > 0 else None
        }
    })

# 2. Independent Resource: Members
@app.route('/members', methods=['GET'])
def get_members():
    return jsonify(list(members.values()))

# 3. Dependent Resource: Member Loans (Resource Tree)
# GET /members/{id}/loans -> Lấy danh sách lượt mượn của 1 thành viên
@app.route('/members/<member_id>/loans', methods=['GET'])
def get_member_loans(member_id):
    if member_id not in members:
        return jsonify({"error": "Member not found"}), 404
    
    member_loans = loans.get(member_id, [])
    return jsonify({
        "member": members[member_id],
        "loans": member_loans
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)