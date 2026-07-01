"""Tests for public CV version management routes."""
import io
import pytest
from unittest.mock import patch
from app import create_app, db
from app.models import User, CVVersion

@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "WTF_CSRF_ENABLED": False,
    })
    with app.app_context():
        db.create_all()
        # create a test user
        user = User(username="testuser", email="test@example.com")
        user.set_password("password")
        db.session.add(user)
        db.session.commit()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def auth_client(client, app):
    # login the test user
    with client.session_transaction() as sess:
        user = User.query.filter_by(username="testuser").first()
        sess['_user_id'] = str(user.id)
    return client

def test_list_versions_empty(auth_client):
    response = auth_client.get("/cv/versions")
    assert response.status_code == 200
    assert b"You have no saved CV versions yet" in response.data

@patch("app.utils.storage.upload_cv", return_value="gs://smartcv-public-data/dummy.html")
@patch("app.utils.storage.make_public")
@patch("app.utils.storage.make_private")
def test_create_and_toggle_version(mock_make_private, mock_make_public, mock_upload, auth_client, app):
    # Create a new version
    response = auth_client.post("/cv/versions/create", data={"title": "Test Version"}, follow_redirects=True)
    assert response.status_code == 200
    # Verify version exists in DB
    with app.app_context():
        version = CVVersion.query.filter_by(title="Test Version").first()
        assert version is not None
        assert version.is_public is False
        # Toggle public
        toggle_resp = auth_client.post(f"/cv/versions/{version.slug}/toggle_public", follow_redirects=True)
        assert toggle_resp.status_code == 200
        db.session.refresh(version)
        assert version.is_public is True
        mock_make_public.assert_called_once_with(f"{version.slug}.html")
        # Toggle back to private
        toggle_resp2 = auth_client.post(f"/cv/versions/{version.slug}/toggle_public", follow_redirects=True)
        assert toggle_resp2.status_code == 200
        db.session.refresh(version)
        assert version.is_public is False
        mock_make_private.assert_called_once_with(f"{version.slug}.html")

@patch("app.utils.storage.delete_cv")
def test_delete_version(mock_delete, auth_client, app):
    # Setup a version directly
    with app.app_context():
        user = User.query.filter_by(username="testuser").first()
        version = CVVersion(
            user_id=user.id,
            title="To Delete",
            slug="delete-slug",
            gcs_path="gs://smartcv-public-data/delete-slug.html",
            html_snapshot="<html></html>",
        )
        db.session.add(version)
        db.session.commit()
    # Delete via route
    resp = auth_client.post("/cv/versions/delete-slug/delete", follow_redirects=True)
    assert resp.status_code == 200
    with app.app_context():
        assert CVVersion.query.filter_by(slug="delete-slug").first() is None
    mock_delete.assert_called_once_with("delete-slug.html")

def test_match_get_request_returns_template(auth_client):
    response = auth_client.get("/job/match")
    assert response.status_code == 200

def test_match_post_request_missing_description(auth_client):
    data = {'job_description': ''}
    response = auth_client.post("/job/match", data=data, follow_redirects=True)
    assert b'Please enter a job description.' in response.data

def test_match_post_request_valid_description(auth_client):
    data = {'job_description': 'Looking for a Python developer'}
    response = auth_client.post("/job/match", data=data)
    assert response.status_code == 200
    assert b'Good Match' in response.data

