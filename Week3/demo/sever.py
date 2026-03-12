from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Giả lập Database nội bộ
articles = {
    "123": {"id": "123", "title": "Học về RESTful API", "status": "draft"},
    "456": {"id": "456", "title": "Học về RESTful API", "status": "pending"},
    "789": {"id": "789", "title": "Học về RESTful API", "status": "approved"},
}

def get_links(article_id, status):
    links = {"self": {"href": f"/articles/{article_id}", "method": "GET"}}
    
    if status == "draft":
        links["submit"] = {"href": f"/articles/{article_id}/submit", "method": "POST"}
    elif status == "pending":
        links["approve"] = {"href": f"/articles/{article_id}/approve", "method": "POST"}
        links["reject"] = {"href": f"/articles/{article_id}/reject", "method": "POST"}
    
    return links

@app.route('/articles/<id>', methods=['GET'])
def get_article(id):
    art = articles.get(id)
    if not art: return jsonify({"error": "Not found"}), 404
    
    return jsonify({
        "articleId": art["id"],
        "status": art["status"],
        "title": art["title"],
        "_links": get_links(id, art["status"])
    })

@app.route('/articles/<id>/<action>', methods=['POST'])
def update_status(id, action):
    if action == "submit": articles[id]["status"] = "pending"
    elif action == "approve": articles[id]["status"] = "approved"
    elif action == "reject": articles[id]["status"] = "draft"
    return get_article(id)


app.run(port=5000)