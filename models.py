from database import db
from sqlalchemy.sql import func


class User(db.Model):
    """user model"""
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f'<User {self.username}>'

    @property
    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "created_at": self.created_at
        }


class Character(db.Model):
    """character model"""
    __tablename__ = 'character'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True, index=True)
    house = db.Column(db.String(100), index=True)
    animal = db.Column(db.String(100))
    strength = db.Column(db.String(100))
    role = db.Column(db.String(100))
    nickname = db.Column(db.String(100))
    symbol = db.Column(db.String(100))
    death = db.Column(db.Integer)
    age = db.Column(db.Integer, index=True)

    @property
    def serialize(self):
        """return object data in easily serializable format"""
        return {
            "id": self.id,
            "name": self.name,
            "age": self.age,
            "house": self.house,
            "animal": self.animal,
            "symbol": self.symbol,
            "nickname": self.nickname,
            "role": self.role,
            "death": self.death,
            "strength": self.strength
        }
