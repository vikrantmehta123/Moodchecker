from main import app
import sqlalchemy as sa
from sqlalchemy.orm import relationship
import datetime
import hashlib

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
    email = sa.Column(sa.String, unique=True)
    authorization_status = sa.Column(sa.Integer)
    email_hash = sa.Column(sa.BINARY(40))
    homecoming_time = sa.Column(sa.Time)
    holiday = sa.Column(sa.Integer)
    reminders_till = sa.Column(sa.Date, nullable=True)

    family_id = sa.Column(sa.Integer, sa.ForeignKey("Families.id"))

    def __init__(self, id, first_name, email, holiday, homecoming_time, reminders_till, authorization_status=0) -> None:
        self.id = id
        self.first_name = first_name
        self.email = email
        self.reminders_till = reminders_till
        self.authorization_status = authorization_status
        self.holiday = holiday
        self.homecoming_time = homecoming_time
        self.email_hash = hashlib.sha1(email)

    family = relationship("Family", back_populates='family_members')
    moods = relationship("Mood", back_populates='user')

    def update_authorization_status(self, new_status):
        """ Updates the authorization status of the given user """
        self.authorization_status = new_status
        db.session.commit()

    def add_mood_update(self, mood):
        """ Inserts a record in the moods table for the given user """
        self.moods.append(mood)
        db.session.commit()
        return

    def update_reminder_till_date(self, new_date):
        """ Updates the date till which the google calendar reminders are set """
        self.reminders_till = new_date
        db.session.commit()
        return 

    @staticmethod
    def get_user_by_email(email):
        """ Returns the User instance for the given email """
        email_hash = hashlib.sha1(email)
        return User.query.filter_by(email_hash=email_hash).first()

    def __repr__(self) -> str:
        return self.first_name

user_email_hash_index = sa.Index("User_Email_Hash_Index", User.email_hash)

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


    