from flask import Blueprint, render_template, redirect, url_for, flash, abort
from flask_login import login_required, current_user

from ..extensions import db
from ..models import WishTemplate
from ..forms import TemplateForm

templates_bp = Blueprint("templates", __name__)

@templates_bp.route("/")
@login_required
def list_templates():
    items = WishTemplate.query.filter_by(user_id=current_user.id).order_by(WishTemplate.created_at.desc()).all()
    return render_template("templates/list.html", items=items)

@templates_bp.route("/create", methods=["GET", "POST"])
@login_required
def create_template():
    form = TemplateForm()
    if form.validate_on_submit():
        t = WishTemplate(
            user_id=current_user.id,
            title=form.title.data.strip(),
            tone=form.tone.data,
            body=form.body.data.strip(),
        )
        db.session.add(t)
        db.session.commit()
        flash("Template saved!", "success")
        return redirect(url_for("templates.list_templates"))
    return render_template("templates/form.html", form=form, mode="create")

def _get_template_or_404(template_id):
    t = WishTemplate.query.get_or_404(template_id)
    if t.user_id != current_user.id:
        abort(403)
    return t

@templates_bp.route("/<int:template_id>/edit", methods=["GET", "POST"])
@login_required
def edit_template(template_id):
    t = _get_template_or_404(template_id)
    form = TemplateForm(obj=t)
    if form.validate_on_submit():
        t.title = form.title.data.strip()
        t.tone = form.tone.data
        t.body = form.body.data.strip()
        db.session.commit()
        flash("Template updated.", "success")
        return redirect(url_for("templates.list_templates"))
    return render_template("templates/form.html", form=form, mode="edit", item=t)

@templates_bp.route("/<int:template_id>/delete", methods=["POST"])
@login_required
def delete_template(template_id):
    t = _get_template_or_404(template_id)
    db.session.delete(t)
    db.session.commit()
    flash("Template deleted.", "info")
    return redirect(url_for("templates.list_templates"))
