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
    try:
        post = Post.query.get(post_id)
        if not post:
            return jsonify({"error": "Post not found"}), 404
        
        if reaction not in ['like', 'dislike']:
            return jsonify({"error": "Invalid reaction"}), 400
        
        return jsonify({"message": f"{reaction} registered for post {post_id}"})
    except Exception as e:
        print(f"Ошибка в react_to_post: {e}")  # Oszibka
        return jsonify({"error": "Internal Server Error"}), 500

@app.route('/post/<int:post_id>/comments', methods=['GET'])
def get_comments(post_id):
    try:
        post = Post.query.get(post_id)
        if not post:
            return jsonify({"error": "Post not found"}), 404
        
        comments = Comment.query.filter_by(post_id=post_id).all()
        return jsonify([{"content": comment.content} for comment in comments])
    except Exception as e:
        print(f"Oszibka в get_comments: {e}")  # Oszibka
        return jsonify({"error": "Internal Server Error"}), 500

if __name__ == "__main__":
    app.run(debug=True)

