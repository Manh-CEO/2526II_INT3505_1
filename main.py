db_posts = [{"id": 1, "title": "API Design", "user_ id": 101}]
db_users = {
    101: {"id": 101, "full_name": "Donald Trump", "internal_email": "[EMAIL_ADDRESS]"}
}

@app.route('/api/posts-raw', methods=['GET'])
def get_posts_bad():
    posts = db_posts
    for post in posts:
        user_id = post['user_id']
        user = db_users.get(user_id)
        if user:
            post['author'] = {
                'name': user['full_name'],
                'profile_url': f"/authors/{user['id']}"
            }
    return jsonify(db_posts)