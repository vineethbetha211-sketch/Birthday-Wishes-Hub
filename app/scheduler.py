from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from flask import current_app

from .extensions import db
from .models import Wish

scheduler = BackgroundScheduler()

def process_due_wishes():
    # Run inside app context when invoked by scheduler
    now = datetime.utcnow()

    due = Wish.query.filter(
        Wish.scheduled_for.isnot(None),
        Wish.sent_at.is_(None),
        Wish.scheduled_for <= now
    ).all()

    if not due:
        return

    for wish in due:
        # For now, we only mark as sent.
        # You can integrate real email/notification here later.
        wish.sent_at = now

    db.session.commit()

def init_scheduler(app):
    if not app.config.get("SCHEDULER_ENABLED", True):
        return

    # Avoid double start in debug reloader
    if app.debug and app.config.get("ENV") == "development":
        import os
        if os.environ.get("WERKZEUG_RUN_MAIN") != "true":
            return

    with app.app_context():
        if not scheduler.get_jobs():
            scheduler.add_job(
                func=lambda: _run_with_context(app, process_due_wishes),
                trigger="interval",
                minutes=1,
                id="due_wishes_job",
                replace_existing=True,
            )
        scheduler.start()

def _run_with_context(app, fn):
    with app.app_context():
        try:
            fn()
        except Exception as e:
            # Keep scheduler resilient; log error
            app.logger.exception("Scheduler job failed: %s", e)
