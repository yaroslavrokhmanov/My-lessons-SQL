from app import app, db
from models import User

with app.app_context():
    users = User.query.all()
    print(users)
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:242187@localhost/postwall_db'
