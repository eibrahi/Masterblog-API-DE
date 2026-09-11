from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]


@app.route('/api/posts', methods=['GET'])
def get_posts():
    return jsonify(POSTS)


@app.route('/api/posts', methods=['POST'])
def add_post():
    data = request.get_json()

    new_id = max([post["id"] for post in POSTS]) + 1

    if data.get("title") and data.get("content"):
        new_post = {
            "id": new_id,
            "title": data["title"],
            "content": data["content"]
        }
        POSTS.append(new_post)

        return jsonify(new_post), 201

    return jsonify({"error": "Title or Content not found."}), 400


@app.route('/api/posts/<int:id>', methods=['DELETE'])
def delete_post(id):
    for post in POSTS:
        if post["id"] == id:
            POSTS.remove(post)
            return jsonify({
                "message": f"Post with id <{id}> has been deleted successfully."
            }), 200

    return jsonify({"error": "Post not found."}), 404

@app.route('/api/posts/<int:id>', methods=['PUT'])
def update_post(id):
    data = request.get_json()

    for post in POSTS:
        if post["id"] == id:
            if data.get("title"):
                post["title"] = data["title"]
            if data.get("content"):
                post["content"] = data["content"]
            return jsonify(post), 200
    return jsonify({"error": "Post not found."}), 404


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
