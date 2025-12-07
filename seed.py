"""Optional local seed script.

Usage:
    python seed.py

It will create a demo user, a couple of friends, templates, and sample wishes.
"""

from datetime import date, datetime, timedelta
from app import create_app
from app.extensions import db
from app.models import User, Friend, WishTemplate, Wish, GroupCard, CardContribution

app = create_app()

with app.app_context():
    db.create_all()

    if User.query.filter_by(email="demo@bwh.local").first():
        print("Demo data already exists.")
        raise SystemExit(0)

    user = User(name="Demo User", email="demo@bwh.local")
    user.set_password("password123")
    db.session.add(user)
    db.session.commit()

    friend1 = Friend(
        user_id=user.id, full_name="Aarav Sharma", nickname="Aaru",
        relationship="Best Friend", timezone="Europe/Dublin",
        birth_date=date(1999, 12, 10),
        notes="That 2022 trip still cracks me up."
    )
    friend2 = Friend(
        user_id=user.id, full_name="Meera Nair",
        relationship="Colleague", timezone="Europe/Dublin",
        birth_date=date(1998, 1, 3)
    )
    db.session.add_all([friend1, friend2])
    db.session.commit()

    t1 = WishTemplate(user_id=user.id, title="Warm Classic", tone="warm", body="Wishing you a day full of laughter and love!")
    t2 = WishTemplate(user_id=user.id, title="Office Friendly", tone="formal", body="Wishing you continued success and happiness. Happy Birthday!")
    db.session.add_all([t1, t2])
    db.session.commit()

    w1 = Wish(user_id=user.id, friend_id=friend1.id, title="Aaru's Big Day", tone="funny",
              body="Happy birthday! May your cake be bigger than your problems 😂")
    w2 = Wish(user_id=user.id, friend_id=friend1.id, title="Time Capsule Note", tone="emotional",
              body="You’ve always been my constant. Proud of you.",
              is_time_capsule=True)
    w3 = Wish(user_id=user.id, friend_id=friend2.id, title="Scheduled Office Wish", tone="formal",
              body="Happy Birthday! Hope you have a wonderful year ahead.",
              scheduled_for=datetime.utcnow() + timedelta(minutes=2))
    db.session.add_all([w1, w2, w3])
    db.session.commit()

    card = GroupCard(user_id=user.id, friend_id=friend1.id, title="Aarav's Group Surprise", theme="party")
    db.session.add(card)
    db.session.commit()

    c1 = CardContribution(card_id=card.id, author_name="Team Alpha", message="Have an amazing year ahead! 🎉", reaction="🎉")
    db.session.add(c1)
    db.session.commit()

    print("Seed complete.")
