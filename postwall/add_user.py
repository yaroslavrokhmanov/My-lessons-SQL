from app import db
from app import app, db
from models import User
# from models import Users

# Sozdaem nowogo polzowatelia
new_user = User(username='Ivan')

# Dobavlaem polzowatelia vnutri prilogenia
with app.app_context():
    db.session.add(new_user)
    db.session.commit()

print("User added successfully!")
