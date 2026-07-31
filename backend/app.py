from functools import wraps

from flask import Flask, jsonify, request, session
from werkzeug.security import check_password_hash
from werkzeug.middleware.proxy_fix import Proxyfix
from flask_cors import CORS

import db

app = Flask(__name__)
CORS(app)
app.secret_key = "change-me-in-production"


app.config.update(
    SESSION_COOKIE_SAMESITE="None",
    SESSION_COOKIE_SECURE=True,
)

db.init_db()


def to_user(row):
    return {"id": row["id"], "username": row["username"]}


def to_todo(row):
    return {"id": row["id"], "title": row["title"], "done": bool(row["done"])}


def current_user():
    user_id = session.get("user_id")
    if user_id is None:
        return None
    return db.get_user_by_id(user_id)


def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        user = current_user()
        if user is None:
            return jsonify({"error": "not logged in"}), 401
        return f(user, *args, **kwargs)

    return wrapper


@app.post("/api/auth/register")
def register():
    data = request.get_json(silent=True) or {}
    username = (data.get("username") or "").strip()
    password = data.get("password") or ""

    if not username or not password:
        return jsonify({"error": "username and password are required"}), 400
    if db.get_user_by_username(username) is not None:
        return jsonify({"error": "username already taken"}), 409

    user_id = db.create_user(username, password)
    session["user_id"] = user_id
    return jsonify({"user": to_user(db.get_user_by_id(user_id))}), 201


@app.post("/api/auth/login")
def login():
    data = request.get_json(silent=True) or {}
    username = (data.get("username") or "").strip()
    password = data.get("password") or ""

    user = db.get_user_by_username(username)
    if user is None or not check_password_hash(user["password_hash"], password):
        return jsonify({"error": "invalid credentials"}), 401

    session["user_id"] = user["id"]
    return jsonify({"user": to_user(user)})


@app.post("/api/auth/logout")
def logout():
    session.clear()
    return jsonify({"ok": True})


@app.get("/api/auth/me")
def me():
    user = current_user()
    if user is None:
        return jsonify({"error": "not logged in"}), 401
    return jsonify({"user": to_user(user)})


@app.get("/api/todos")
@login_required
def get_todos(user):
    todos = [to_todo(row) for row in db.list_todos(user["id"])]
    return jsonify({"todos": todos})


@app.post("/api/todos")
@login_required
def create_todo(user):
    data = request.get_json(silent=True) or {}
    title = (data.get("title") or "").strip()
    if not title:
        return jsonify({"error": "title is required"}), 400

    todo_id = db.add_todo(user["id"], title)
    return jsonify({"todo": to_todo(db.get_todo(todo_id))}), 201


@app.patch("/api/todos/<int:todo_id>")
@login_required
def update_todo(user, todo_id):
    data = request.get_json(silent=True) or {}
    if "done" not in data:
        return jsonify({"error": "done is required"}), 400

    db.update_todo(todo_id, bool(data["done"]))
    return jsonify({"ok": True})


@app.delete("/api/todos/<int:todo_id>")
@login_required
def remove_todo(user, todo_id):
    db.delete_todo(todo_id)
    return jsonify({"ok": True})
app.wsgi_app = Proxyfix(app.wsgi_app,x_for=1,x_proto=1,x_host=1,x_prefix=1)
app.config.update(
    SESSION_COKKIE_SECURE=False,
    SESSION_COKKIE_HTTPONLY=True,
    SESSION_COKKIE_SAMESITE='Lax',
)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
