from flask import Flask, request, jsonify
import sqlite3
import time

app = Flask(__name__)
DB_PATH = 'database.db'

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/api/records', methods=['GET'])
def get_records():
    # Pagination parameters
    try:
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 10))
    except ValueError:
        return jsonify({"error": "Invalid pagination parameters. Must be integers."}), 400

    if page < 1 or limit < 1:
        return jsonify({"error": "Page and limit must be at least 1."}), 400

    offset = (page - 1) * limit

    start_time = time.time()

    conn = get_db_connection()
    # Using SQL LIMIT and OFFSET
    query = 'SELECT * FROM records ORDER BY id ASC LIMIT ? OFFSET ?'
    records = conn.execute(query, (limit, offset)).fetchall()
    
    # We can also get the total count, but with 1M rows it might add some ms (SQLite cache it), 
    # though COUNT(*) is not extremely slow, it's something to consider.
    total_count = conn.execute('SELECT COUNT(*) FROM records').fetchone()[0]

    conn.close()

    end_time = time.time()
    query_time = (end_time - start_time) * 1000 # Convert to milliseconds

    results = [dict(ix) for ix in records]
    
    return jsonify({
        "page": page,
        "limit": limit,
        "total_records": total_count,
        "query_time_ms": round(query_time, 2),
        "data": results
    })

if __name__ == '__main__':
    # Using debug=True for development. Don't use in production.
    app.run(debug=True, port=5000)
