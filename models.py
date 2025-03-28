from app import db

class Waitlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True)
    phone = db.Column(db.String(50), nullable=True)

    def __repr__(self):
        return f"<Waitlist {self.name}>"
