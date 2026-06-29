"""
CV Manager Web Application Factory
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

def create_app(config_class=None):
    """Application factory pattern"""
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///../instance/cv_app.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), '../uploads')
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
    app.config['WTF_CSRF_ENABLED'] = False  # Disable Flask-WTF CSRF, we'll use session-based
    
    # Ensure directories exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(os.path.join(os.path.dirname(__file__), '../documents'), exist_ok=True)
    
    # Initialize extensions with app
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    
    # Configure login
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'
    
    @login_manager.user_loader
    def load_user(user_id):
        from app.models import User
        return User.query.get(int(user_id))
    
    # Context processor for CSRF token
    @app.context_processor
    def inject_csrf_token():
        from flask import session
        import secrets
        if 'csrf_token' not in session:
            session['csrf_token'] = secrets.token_urlsafe(32)
        return dict(csrf_token=lambda: session.get('csrf_token', ''))
    
    # Register blueprints
    from app.routes import main, auth, cv, job
    from app.routes import admin as admin_routes
    app.register_blueprint(main.bp)
    app.register_blueprint(auth.bp, url_prefix='/auth')
    app.register_blueprint(cv.bp, url_prefix='/cv')
    app.register_blueprint(job.bp, url_prefix='/job')
    app.register_blueprint(admin_routes.bp)
    
    # Create tables
    with app.app_context():
        db.create_all()
    
    # Register CLI commands
    register_cli(app)

    return app

# Add GA configuration to your create_app function
def configure_analytics(app):
    """Configure analytics"""
    app.config['GA_MEASUREMENT_ID'] = os.environ.get('GA_MEASUREMENT_ID')

    @app.context_processor
    def inject_analytics():
        return dict(config=app.config)


def register_cli(app):
    """Register custom Flask CLI commands."""
    import click

    @app.cli.command('create-admin')
    @click.argument('username')
    def create_admin(username):
        """Promote an existing user to admin, or create one if not found."""
        with app.app_context():
            from app.models import User, Profile
            user = User.query.filter_by(username=username).first()
            if not user:
                click.echo(f"User '{username}' not found. Creating...")
                email = click.prompt('Email')
                password = click.prompt('Password', hide_input=True, confirmation_prompt=True)
                user = User(username=username, email=email, is_admin=True)
                user.set_password(password)
                db.session.add(user)
                db.session.flush()
                profile = Profile(user_id=user.id)
                db.session.add(profile)
            else:
                user.is_admin = True
            db.session.commit()
            click.echo(f"✅ '{username}' is now an admin.")
