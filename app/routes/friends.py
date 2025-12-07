from flask import Blueprint, render_template, redirect, url_for, flash, abort
from flask_login import login_required, current_user

from ..extensions import db
from ..models import Friend, Wish, GroupCard
from ..forms import FriendForm

friends_bp = Blueprint("friends", __name__)

@friends_bp.route("/")
@login_required
def list_friends():
    friends = Friend.query.filter_by(user_id=current_user.id).order_by(Friend.full_name.asc()).all()
    return render_template("friends/list.html", friends=friends)

@friends_bp.route("/create", methods=["GET", "POST"])
@login_required
def create_friend():
    form = FriendForm()
    if form.validate_on_submit():
        friend = Friend(
            user_id=current_user.id,
            full_name=form.full_name.data.strip(),
            nickname=form.nickname.data.strip() if form.nickname.data else None,
            relationship=form.relationship.data.strip() if form.relationship.data else None,
            timezone=form.timezone.data.strip() if form.timezone.data else "Europe/Dublin",
            birth_date=form.birth_date.data,
            notes=form.notes.data.strip() if form.notes.data else None,
            photo_url=form.photo_url.data.strip() if form.photo_url.data else None,
        )
        db.session.add(friend)
        db.session.commit()
        flash("Friend added!", "success")
        return redirect(url_for("friends.list_friends"))
    return render_template("friends/form.html", form=form, mode="create")

def _get_friend_or_404(friend_id: int):
    friend = Friend.query.get_or_404(friend_id)
    if friend.user_id != current_user.id:
        abort(403)
    return friend

@friends_bp.route("/<int:friend_id>/edit", methods=["GET", "POST"])
@login_required
def edit_friend(friend_id):
    friend = _get_friend_or_404(friend_id)
    form = FriendForm(obj=friend)
    if form.validate_on_submit():
        friend.full_name = form.full_name.data.strip()
        friend.nickname = form.nickname.data.strip() if form.nickname.data else None
        friend.relationship = form.relationship.data.strip() if form.relationship.data else None
        friend.timezone = form.timezone.data.strip() if form.timezone.data else friend.timezone
        friend.birth_date = form.birth_date.data
        friend.notes = form.notes.data.strip() if form.notes.data else None
        friend.photo_url = form.photo_url.data.strip() if form.photo_url.data else None

        db.session.commit()
        flash("Friend updated.", "success")
        return redirect(url_for("friends.list_friends"))
    return render_template("friends/form.html", form=form, mode="edit", friend=friend)

@friends_bp.route("/<int:friend_id>")
@login_required
def view_friend(friend_id):
    friend = _get_friend_or_404(friend_id)
    wishes = Wish.query.filter_by(friend_id=friend.id, user_id=current_user.id).order_by(Wish.created_at.desc()).all()
    cards = GroupCard.query.filter_by(friend_id=friend.id, user_id=current_user.id).order_by(GroupCard.created_at.desc()).all()
    return render_template("friends/view.html", friend=friend, wishes=wishes, cards=cards)

@friends_bp.route("/<int:friend_id>/delete", methods=["POST"])
@login_required
def delete_friend(friend_id):
    friend = _get_friend_or_404(friend_id)
    db.session.delete(friend)
    db.session.commit()
    flash("Friend deleted.", "info")
    return redirect(url_for("friends.list_friends"))
