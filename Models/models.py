from main import app
import sqlalchemy as sa
from sqlalchemy.orm import relationship
import datetime

db = app.db

class Family(db.Model):
    __tablename__ = "Families"
    
    id = sa.Column(sa.Integer, autoincrement=True, primary_key=True)
    last_name = sa.Column(sa.String(200), nullable=False)
    family_members = relationship("User", back_populates='family')

    def __init__(self, id, family_id, last_name) -> None:
        self.id = id
        self.family_id = family_id
        self.last_name = last_name

    def __repr__(self) -> str:
        return (f"{self.id}, {self.last_name}")

class User(db.Model):
    __tablename__ = "Users"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    first_name = sa.Column(sa.String(250), nullable=False)
    family_id = sa.Column(sa.Integer, sa.ForeignKey("Families.id"))
    family = relationship("Family", back_populates='family_members')
    email = sa.Column(sa.String, unique=True)
    moods = relationship("Mood", back_populates='user')

    def __repr__(self) -> str:
        return self.first_name

class Mood(db.Model):
    __tablename__= "Moods"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    user_id = sa.Column(sa.Integer, sa.ForeignKey("Users.id"))
    mood = sa.Column(sa.Integer, nullable=False)
    date = sa.Column(sa.Date, nullable=False, default=datetime.date.today())
    user = relationship("User", back_populates='moods')

    def __init__(self, id, user_id, mood, date) -> None:
        self.id = id
        self.user_id = user_id
        self.mood = mood
        self.date = date

    