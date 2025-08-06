from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

@app.route('/')  # The root/Index of the server
def home():
    return '''<h1>User Database Management</h1>
              <h3>Authorized Users Only</h3>'''

@app.route('/revise')  # domain/revise route
def edit_request():
    username = request.args.get('username')  # e.g. /revise?username=George_Washington
    auth = request.args.get('auth')          # e.g. /revise?username=George_Washington&auth=5

    if not username:
        return jsonify({"error": "Please provide a username."}), 400

    user_record = access_row(username)

    if not user_record:
        return jsonify({"error": f"User '{username}' not found."}), 404

    if not auth:
        return jsonify({
            "userid": user_record[0],
            "username": user_record[1],
            "password": user_record[2],
            "auth": user_record[3]
        })

    # Update auth level
    try:
        new_auth = int(auth)
    except ValueError:
        return jsonify({"error": "Invalid auth level format. Must be an integer."}), 400

    update_auth(username, new_auth)
    updated_user = access_row(username)
    return jsonify({
        "userid": updated_user[0],
        "username": updated_user[1],
        "password": updated_user[2],
        "auth": updated_user[3]
    })

def access_row(person):
    conn = sqlite3.connect('people.db')  # Correct DB
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (person,))
    user_record = cursor.fetchone()
    conn.close()
    return user_record

def update_auth(person, auth):
    conn = sqlite3.connect('people.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET auth_level = ? WHERE username = ?", (auth, person))
    conn.commit()
    conn.close()

if __name__ == '__main__':
    app.run(debug=True)
