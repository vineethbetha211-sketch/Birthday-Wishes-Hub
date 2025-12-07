from flask import Blueprint, render_template, redirect, url_for, flash, abort, request
from flask_login import login_required, current_user
from datetime import date

from ..extensions import db
from ..models import GroupCard, CardContribution, Friend
from ..forms import GroupCardForm, ContributionForm

group_cards_bp = Blueprint("group_cards", __name__)

def _get_friend_choices():
    return Friend.query.filter_by(user_id=current_user.id).order_by(Friend.full_name.asc()).all()

@group_cards_bp.route("/")
@login_required
def list_cards():
    cards = GroupCard.query.filter_by(user_id=current_user.id).order_by(GroupCard.created_at.desc()).all()
    return render_template("cards/list.html", cards=cards)

@group_cards_bp.route("/create", methods=["GET", "POST"])
@login_required
def create_card():
    friends = _get_friend_choices()
    if not friends:
        flash("Add a friend first to create a group card.", "warning")
        return redirect(url_for("friends.create_friend"))

    form = GroupCardForm()
    if form.validate_on_submit():
        friend_id = int(request.form.get("friend_id"))
        friend = Friend.query.filter_by(id=friend_id, user_id=current_user.id).first()
        if not friend:
            flash("Invalid friend selected.", "danger")
            return redirect(url_for("group_cards.create_card"))

        card = GroupCard(
            user_id=current_user.id,
            friend_id=friend.id,
            title=form.title.data.strip(),
            description=form.description.data.strip() if form.description.data else None,
            theme=form.theme.data,
            is_locked_until_bday=bool(form.is_locked_until_bday.data),
        )
        db.session.add(card)
        db.session.commit()
        flash("Group card created!", "success")
        return redirect(url_for("group_cards.list_cards"))

    return render_template("cards/form.html", form=form, friends=friends, mode="create")

def _get_card_or_404(card_id):
    card = GroupCard.query.get_or_404(card_id)
    if card.user_id != current_user.id:
        abort(403)
    return card

@group_cards_bp.route("/<int:card_id>")
@login_required
def view_card(card_id):
    card = _get_card_or_404(card_id)
    share_url = url_for("group_cards.public_card", slug=card.slug, _external=True)
    return render_template("cards/view.html", card=card, share_url=share_url)

@group_cards_bp.route("/<int:card_id>/delete", methods=["POST"])
@login_required
def delete_card(card_id):
    card = _get_card_or_404(card_id)
    db.session.delete(card)
    db.session.commit()
    flash("Card deleted.", "info")
    return redirect(url_for("group_cards.list_cards"))

# Public share page (no login required)
@group_cards_bp.route("/share/<slug>", methods=["GET", "POST"])
def public_card(slug):
    card = GroupCard.query.filter_by(slug=slug).first_or_404()
    friend = card.friend

    today = date.today()
    is_bday_today = (friend.birth_date.month == today.month and friend.birth_date.day == today.day)

    locked = card.is_locked_until_bday and not is_bday_today

    form = ContributionForm()
    if form.validate_on_submit():
        if locked:
            flash("This card is locked until the birthday.", "warning")
            return redirect(url_for("group_cards.public_card", slug=slug))

        c = CardContribution(
            card_id=card.id,
            author_name=form.author_name.data.strip(),
            message=form.message.data.strip(),
            reaction=form.reaction.data if form.reaction.data else None,
        )
        db.session.add(c)
        db.session.commit()
        flash("Your wish was added! 🎉", "success")
        return redirect(url_for("group_cards.public_card", slug=slug))

    return render_template(
        "cards/public.html",
        card=card,
        friend=friend,
        form=form,
        locked=locked,
        is_bday_today=is_bday_today,
    )
