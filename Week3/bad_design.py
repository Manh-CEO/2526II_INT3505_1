from flask import Flask, request, jsonify

app = Flask(__name__)

users = []

@app.route('/getUsers', methods=['GET'])
def getUsers():
    return jsonify(users)

@app.route('/addUser', methods=['POST'])
def addUser():
    data = request.json
    users.append(data)
    return "User added"

@app.route('/user', methods=['GET'])
def getUser():
    user_id = request.args.get('id')
    for u in users:
        if u['id'] == user_id:
            return jsonify(u)
    return "User not found"

@app.route('/deleteUser/<id>', methods=['GET'])
def deleteUser(id):
    global users
    users = [u for u in users if u['id'] != id]
    return "Deleted"

@app.route('/update_user', methods=['POST'])
def updateUser():
    data = request.json
    for u in users:
        if u['id'] == data['id']:
            u.update(data)
    return "Updated"

app.run(debug=True)