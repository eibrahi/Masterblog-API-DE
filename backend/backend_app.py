from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]


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


@app.route('/api/posts/search', methods=['GET'])
def search_posts():
    results = []
    title = request.args.get('title')
    content = request.args.get('content')

    for post in POSTS:
        if (title and title in post["title"].lower()) or (content and content in post["content"].lower()):
            results.append(post)
    return jsonify(results), 200


@app.route('/api/posts', methods=['GET'])
def get_sorted_posts():
    sort = request.args.get('sort')
    direction = request.args.get('direction')
    if sort and direction:
        if sort not in ["title", "content"]:
            return jsonify({"error": "Sort not found."}), 404

        if direction not in ["asc", "desc"]:
            return jsonify({"error": "Direction not found."}), 404

        reverse = direction == "desc"

        return jsonify(
            sorted(POSTS, key=lambda x: x[sort], reverse=reverse))

    return jsonify(POSTS)


SWAGGER_URL = "/api/docs"  # (1) swagger endpoint e.g. HTTP://localhost:5002/api/docs
API_URL = "/static/masterblog.json"  # (2) ensure you create this dir and file

swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': 'Masterblog-API-DE'  # (3) You can change this if you like
    }
)
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
