from flask import Blueprint, render_template, redirect, url_for, flash, abort, request
from flask_login import login_required, current_user
from datetime import datetime, date

from ..extensions import db
from ..models import Wish, Friend, WishTemplate
from ..forms import WishForm

wishes_bp = Blueprint("wishes", __name__)

@wishes_bp.route("/")
@login_required
def list_wishes():
    wishes = Wish.query.filter_by(user_id=current_user.id).order_by(Wish.created_at.desc()).all()
    return render_template("wishes/list.html", wishes=wishes)

def _get_friend_choices():
    friends = Friend.query.filter_by(user_id=current_user.id).order_by(Friend.full_name.asc()).all()
    return friends

@wishes_bp.route("/create", methods=["GET", "POST"])
@login_required
def create_wish():
    friends = _get_friend_choices()
    if not friends:
        flash("Add a friend first to create wishes.", "warning")
        return redirect(url_for("friends.create_friend"))

    form = WishForm()

    template_id = request.args.get("template")
    prefill = None
    if template_id:
        prefill = WishTemplate.query.filter_by(id=int(template_id), user_id=current_user.id).first()

    if request.method == "GET" and prefill:
        form.title.data = prefill.title
        form.tone.data = prefill.tone
        form.body.data = prefill.body

    if form.validate_on_submit():
        friend_id = int(request.form.get("friend_id"))
        friend = Friend.query.filter_by(id=friend_id, user_id=current_user.id).first()
        if not friend:
            flash("Invalid friend selected.", "danger")
            return redirect(url_for("wishes.create_wish"))

        scheduled_for = form.scheduled_for.data
        wish = Wish(
            user_id=current_user.id,
            friend_id=friend.id,
            title=form.title.data.strip(),
            tone=form.tone.data,
            body=form.body.data.strip(),
            image_url=form.image_url.data.strip() if form.image_url.data else None,
            is_time_capsule=bool(form.is_time_capsule.data),
            scheduled_for=scheduled_for if scheduled_for else None,
        )

        db.session.add(wish)
        db.session.commit()
        flash("Wish created!", "success")
        return redirect(url_for("wishes.list_wishes"))

    return render_template("wishes/form.html", form=form, friends=friends, mode="create")

def _get_wish_or_404(wish_id):
    wish = Wish.query.get_or_404(wish_id)
    if wish.user_id != current_user.id:
        abort(403)
    return wish

@wishes_bp.route("/<int:wish_id>")
@login_required
def view_wish(wish_id):
    wish = _get_wish_or_404(wish_id)
    friend = wish.friend

    today = date.today()
    is_bday_today = (friend.birth_date.month == today.month and friend.birth_date.day == today.day)

    # Time capsule rule: hide body if enabled and not birthday yet
    hide_body = wish.is_time_capsule and not is_bday_today

    return render_template("wishes/view.html", wish=wish, hide_body=hide_body, is_bday_today=is_bday_today)

@wishes_bp.route("/<int:wish_id>/edit", methods=["GET", "POST"])
@login_required
def edit_wish(wish_id):
    wish = _get_wish_or_404(wish_id)
    friends = _get_friend_choices()
    form = WishForm(obj=wish)

    if form.validate_on_submit():
        friend_id = int(request.form.get("friend_id"))
        friend = Friend.query.filter_by(id=friend_id, user_id=current_user.id).first()
        if not friend:
            flash("Invalid friend selected.", "danger")
            return redirect(url_for("wishes.edit_wish", wish_id=wish.id))

        wish.friend_id = friend.id
        wish.title = form.title.data.strip()
        wish.tone = form.tone.data
        wish.body = form.body.data.strip()
        wish.image_url = form.image_url.data.strip() if form.image_url.data else None
        wish.is_time_capsule = bool(form.is_time_capsule.data)
        wish.scheduled_for = form.scheduled_for.data if form.scheduled_for.data else None

        db.session.commit()
        flash("Wish updated.", "success")
        return redirect(url_for("wishes.view_wish", wish_id=wish.id))

    return render_template("wishes/form.html", form=form, friends=friends, mode="edit", wish=wish)

@wishes_bp.route("/<int:wish_id>/mark_sent", methods=["POST"])
@login_required
def mark_sent(wish_id):
    wish = _get_wish_or_404(wish_id)
    if wish.sent_at:
        flash("Already marked as sent.", "info")
        return redirect(url_for("wishes.view_wish", wish_id=wish.id))

    wish.sent_at = datetime.utcnow()
    db.session.commit()
    flash("Wish marked as sent.", "success")
    return redirect(url_for("wishes.view_wish", wish_id=wish.id))

@wishes_bp.route("/<int:wish_id>/delete", methods=["POST"])
@login_required
def delete_wish(wish_id):
    wish = _get_wish_or_404(wish_id)
    db.session.delete(wish)
    db.session.commit()
    flash("Wish deleted.", "info")
    return redirect(url_for("wishes.list_wishes"))

# Public surprise reveal page
@wishes_bp.route("/reveal/<token>")
def public_reveal(token):
    wish = Wish.query.filter_by(reveal_token=token).first_or_404()
    friend = wish.friend
    today = date.today()
    is_bday_today = (friend.birth_date.month == today.month and friend.birth_date.day == today.day)
    hide_body = wish.is_time_capsule and not is_bday_today
    return render_template("wishes/reveal_public.html", wish=wish, hide_body=hide_body, is_bday_today=is_bday_today)
