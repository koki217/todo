"""
TODOアプリ Webサーバー

起動:
    python server.py

ブラウザで http://localhost:5000 を開く
"""

from flask import Flask, jsonify, request, send_from_directory
from pathlib import Path
import todo_app

app = Flask(__name__, static_folder=".")

todo_app.init_db()


@app.get("/")
def index():
    return send_from_directory(".", "index.html")


@app.get("/api/todos")
def api_list():
    show_all = request.args.get("all", "false").lower() == "true"
    rows = todo_app.list_todos(show_all=show_all)
    return jsonify([dict(r) for r in rows])


@app.post("/api/todos")
def api_add():
    title = (request.get_json() or {}).get("title", "").strip()
    if not title:
        return jsonify({"error": "title is required"}), 400
    todo_id = todo_app.add_todo(title)
    return jsonify({"id": todo_id, "title": title}), 201


@app.patch("/api/todos/<int:todo_id>/done")
def api_done(todo_id: int):
    if todo_app.mark_done(todo_id):
        return jsonify({"ok": True})
    return jsonify({"error": "not found"}), 404


@app.delete("/api/todos/<int:todo_id>")
def api_delete(todo_id: int):
    if todo_app.delete_todo(todo_id):
        return jsonify({"ok": True})
    return jsonify({"error": "not found"}), 404


@app.delete("/api/todos/done")
def api_clear_done():
    count = todo_app.clear_done()
    return jsonify({"deleted": count})


if __name__ == "__main__":
    app.run(debug=True, port=5001)
