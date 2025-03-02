from flask import Flask, request, jsonify
from flask import Flask, render_template, jsonify
from extensions import db  # Import db
from config import Config
from models import User, Post, Comment

from dotenv import load_dotenv
import os

# Sozdaem Flask prilogenie
app = Flask(__name__, static_folder='static', template_folder='templates')

# Zagrużaem nastrojki iz .env
load_dotenv()

# Parametry konfiguracii
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Swiazywaem bazu s prilorzeniem
db.init_app(app)

# Sozdanie tablicy w baze dannych
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    users = User.query.order_by(User.id).all()
    user_names = [user.username for user in users]
    posts = Post.query.order_by(Post.id.desc()).all()  # Poluczaem posty iz bazy
    return render_template('index.html', users=user_names, posts=posts)

@app.route('/post/<int:post_id>/<reaction>', methods=['POST'])
def react_to_post(post_id, reaction):
    post = Post.query.get(post_id)
    if not post:
        return jsonify({"error": "Post not found"}), 404
    return jsonify({"message": f"{reaction} registered for post {post_id}"})

@app.route('/post/<int:post_id>/comments', methods=['GET'])
def get_comments(post_id):
    post = Post.query.get(post_id)
    if not post:
        return jsonify({"error": "Post not found"}), 404
    comments = Comment.query.filter_by(post_id=post_id).all()
    return jsonify([{ "id": comment.id, "content": comment.content } for comment in comments])

@app.route('/post/<int:post_id>/comment', methods=['POST'])
def add_comment(post_id):
    post = Post.query.get(post_id)
    if not post:
        return jsonify({"error": "Post not found"}), 404
    
    data = request.get_json()
    content = data.get("content")
    if not content:
        return jsonify({"error": "Comment content is required"}), 400
    
    new_comment = Comment(content=content, post_id=post_id)
    db.session.add(new_comment)
    db.session.commit()
    
    return jsonify({"message": "Comment added successfully", "comment": {"id": new_comment.id, "content": new_comment.content}}), 201

if __name__ == "__main__":
    app.run(debug=True)
