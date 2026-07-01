"""
Unit tests for the CV Manager application factory (app/__init__.py).
Generated with assistance from local-ollama / qwen2.5-coder:1.5b-base.
"""

import pytest
from app import create_app


@pytest.fixture
def app():
    """Create app instance for testing."""
    app = create_app()
    yield app


# --- Configuration Tests ---

def test_default_secret_key(app):
    assert app.config['SECRET_KEY'] == 'dev-secret-key-change-in-production'


def test_sqlalchemy_track_modifications_is_false(app):
    assert app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] is False


def test_max_content_length(app):
    assert isinstance(app.config['MAX_CONTENT_LENGTH'], int)
    assert app.config['MAX_CONTENT_LENGTH'] == 16 * 1024 * 1024  # 16 MB


def test_wtf_csrf_enabled_is_false(app):
    assert app.config['WTF_CSRF_ENABLED'] is False


# --- Blueprint Registration Tests ---

def test_blueprints_registered(app):
    expected_blueprints = {'main', 'auth', 'cv', 'job', 'admin'}
    registered_blueprints = set(app.blueprints.keys())
    assert expected_blueprints == registered_blueprints


def test_auth_blueprint_url_prefix(app):
    # Flask stores the effective prefix in the URL map rules, not on the blueprint object
    auth_rules = [str(rule) for rule in app.url_map.iter_rules() if rule.endpoint.startswith('auth.')]
    assert any(r.startswith('/auth') for r in auth_rules)


def test_cv_blueprint_url_prefix(app):
    assert app.blueprints['cv'].url_prefix == '/cv'


def test_job_blueprint_url_prefix(app):
    assert app.blueprints['job'].url_prefix == '/job'
