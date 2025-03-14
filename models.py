from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
db = SQLAlchemy()

class ImageData(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    filename = db.Column(db.Text(), nullable=False)
    original_filename = db.Column(db.Text(), nullable=False)
    upload_date = db.Column(db.DateTime(), default=datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    user = db.relationship('User', backref=db.backref('ImageData', lazy=True))  # Relationship

    def __repr__(self):
        return f"<Image {self.filename} >"

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
  
        db.session.delete(self)
        db.session.commit()





class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), nullable=False, unique=True)
    email = db.Column(db.String(80), nullable=False)
    password = db.Column(db.Text(), nullable=False)

    def __repr__(self):
        return f"<User {self.name}>"

    def save(self):
        db.session.add(self)
        db.session.commit()


    def to_dict(self):
        return {
            "id": self.id,
            "name": self.username,
            "email": self.email,
        }