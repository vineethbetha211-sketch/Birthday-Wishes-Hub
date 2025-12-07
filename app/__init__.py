from flask import Flask
from .config import Config
from .extensions import db, login_manager, migrate, csrf
from .scheduler import init_scheduler

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Extensions
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)

    # Blueprints
    from .routes.auth import auth_bp
    from .routes.dashboard import dashboard_bp
    from .routes.friends import friends_bp
    from .routes.templates import templates_bp
    from .routes.wishes import wishes_bp
    from .routes.group_cards import group_cards_bp
    from .routes.errors import errors_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(friends_bp, url_prefix="/friends")
    app.register_blueprint(templates_bp, url_prefix="/templates")
    app.register_blueprint(wishes_bp, url_prefix="/wishes")
    app.register_blueprint(group_cards_bp, url_prefix="/cards")
    app.register_blueprint(errors_bp)

    # Scheduler (optional)
    init_scheduler(app)

    @app.shell_context_processor
    def make_shell_context():
        from . import models
        return {"db": db, "models": models}

    return app
