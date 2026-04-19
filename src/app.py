from flask import Flask, jsonify, request

app = Flask(__name__)

# In-memory storage (simple list acting as a database)
tasks = []


@app.route("/health", methods=["GET"])
def health_check():
    """Returns healthy status. Used by pipeline smoke tests after every deployment.."""
    return jsonify({"status": "healthy"}), 200


@app.route("/api/version", methods=["GET"])
def get_version():
    """Returns the current API version."""
    return jsonify({"version": "1.0.0"}), 200


@app.route("/api/tasks", methods=["GET"])
def get_tasks():
    """Return all tasks."""
    return jsonify({"tasks": tasks}), 200


@app.route("/api/tasks", methods=["POST"])
def create_task():
    """Create a new task. Expects JSON: {"title": "something"}"""
    data = request.get_json()

    if not data or "title" not in data:
        return jsonify({"error": "title is required"}), 400

    task = {
        "id": len(tasks) + 1,
        "title": data["title"],
        "done": False,
    }
    tasks.append(task)
    return jsonify(task), 201


@app.route("/api/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    """Mark a task as done."""
    for task in tasks:
        if task["id"] == task_id:
            task["done"] = True
            return jsonify(task), 200
    return jsonify({"error": "task not found"}), 404


if __name__ == "__main__":
    import os
    debug_mode = os.environ.get("FLASK_DEBUG", "false").lower() == "true"
    app.run(debug=debug_mode, host="0.0.0.0", port=5000)  # nosec B104
