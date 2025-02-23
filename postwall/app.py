from flask import Flask, render_template
from extensions import db  # Import db
from config import Config
from models import User, Post, Comment

from dotenv import load_dotenv
import os

# Sozdaen Flask prilogenie
app = Flask(__name__, static_folder='static', template_folder='templates')



# Zagruzka nastroek iz .env
load_dotenv()

# Ustanawliwaem parametry konfiguracii
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Sviazywaem db s prilogeniem
db.init_app(app)

# СSozdanie tablicy w baze dannych
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    users = User.query.order_by(User.id).all()  # Sortirowka po id
    user_names = [user.username for user in users]
    return render_template('index.html', users=user_names)

if __name__ == "__main__":
    app.run(debug=True)

