from flask import Blueprint, render_template
from flask_login import login_required, current_user
from datetime import date

from ..models import Friend, Wish, GroupCard

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/dashboard")
@login_required
def index():
    friends = Friend.query.filter_by(user_id=current_user.id).all()
    upcoming = sorted(friends, key=lambda f: f.days_until_birthday())[:5]

    wishes_count = Wish.query.filter_by(user_id=current_user.id).count()
    cards_count = GroupCard.query.filter_by(user_id=current_user.id).count()

    # Today's birthdays
    today = date.today()
    todays = [f for f in friends if f.birth_date.month == today.month and f.birth_date.day == today.day]

    return render_template(
        "dashboard/index.html",
        friends_count=len(friends),
        wishes_count=wishes_count,
        cards_count=cards_count,
        upcoming=upcoming,
        todays=todays,
    )
