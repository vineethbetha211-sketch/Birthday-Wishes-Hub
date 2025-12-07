from datetime import datetime, date
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from .extensions import db, login_manager
from .utils import generate_token

class TimestampMixin:
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin, TimestampMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(180), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)

    friends = db.relationship("Friend", backref="owner", lazy=True, cascade="all, delete-orphan")
    templates = db.relationship("WishTemplate", backref="owner", lazy=True, cascade="all, delete-orphan")
    wishes = db.relationship("Wish", backref="owner", lazy=True, cascade="all, delete-orphan")
    group_cards = db.relationship("GroupCard", backref="owner", lazy=True, cascade="all, delete-orphan")

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.email}>"

class Friend(TimestampMixin, db.Model):
    __tablename__ = "friends"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    full_name = db.Column(db.String(120), nullable=False)
    nickname = db.Column(db.String(80), nullable=True)
    relationship = db.Column(db.String(80), nullable=True)
    timezone = db.Column(db.String(64), nullable=True, default="Europe/Dublin")

    birth_date = db.Column(db.Date, nullable=False)
    notes = db.Column(db.Text, nullable=True)
    photo_url = db.Column(db.String(500), nullable=True)

    wishes = db.relationship("Wish", backref="friend", lazy=True, cascade="all, delete-orphan")
    cards = db.relationship("GroupCard", backref="friend", lazy=True, cascade="all, delete-orphan")

    def days_until_birthday(self):
        today = date.today()
        this_year = date(today.year, self.birth_date.month, self.birth_date.day)
        if this_year < today:
            next_bday = date(today.year + 1, self.birth_date.month, self.birth_date.day)
        else:
            next_bday = this_year
        return (next_bday - today).days

    def __repr__(self):
        return f"<Friend {self.full_name}>"

class WishTemplate(TimestampMixin, db.Model):
    __tablename__ = "wish_templates"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    title = db.Column(db.String(120), nullable=False)
    tone = db.Column(db.String(40), nullable=False, default="warm")  # warm, funny, formal, emotional
    body = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"<WishTemplate {self.title}>"

class Wish(TimestampMixin, db.Model):
    __tablename__ = "wishes"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    friend_id = db.Column(db.Integer, db.ForeignKey("friends.id"), nullable=False)

    title = db.Column(db.String(120), nullable=False)
    body = db.Column(db.Text, nullable=False)
    tone = db.Column(db.String(40), nullable=False, default="warm")

    image_url = db.Column(db.String(500), nullable=True)

    # Scheduling + Time capsule
    is_time_capsule = db.Column(db.Boolean, default=False, nullable=False)
    scheduled_for = db.Column(db.DateTime, nullable=True)
    sent_at = db.Column(db.DateTime, nullable=True)

    # Public reveal token (for surprise share)
    reveal_token = db.Column(db.String(120), unique=True, nullable=False, default=lambda: generate_token(12))

    def is_sent(self):
        return self.sent_at is not None

    def __repr__(self):
        return f"<Wish {self.title}>"

class GroupCard(TimestampMixin, db.Model):
    __tablename__ = "group_cards"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    friend_id = db.Column(db.Integer, db.ForeignKey("friends.id"), nullable=False)

    title = db.Column(db.String(140), nullable=False)
    description = db.Column(db.Text, nullable=True)
    theme = db.Column(db.String(50), default="cloud", nullable=False)

    slug = db.Column(db.String(120), unique=True, nullable=False, default=lambda: generate_token(10))
    is_locked_until_bday = db.Column(db.Boolean, default=False, nullable=False)

    contributions = db.relationship("CardContribution", backref="card", lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<GroupCard {self.title}>"

class CardContribution(TimestampMixin, db.Model):
    __tablename__ = "card_contributions"
    id = db.Column(db.Integer, primary_key=True)
    card_id = db.Column(db.Integer, db.ForeignKey("group_cards.id"), nullable=False)

    author_name = db.Column(db.String(120), nullable=False)
    message = db.Column(db.Text, nullable=False)
    reaction = db.Column(db.String(10), nullable=True)  # optional emoji

    def __repr__(self):
        return f"<CardContribution {self.author_name}>"
